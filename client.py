import time
import requests
import pickle
import numpy as np

BANDWIDTH = 'C'
CHUNK_TYPE = 'V'

if BANDWIDTH == 'C' and CHUNK_TYPE == 'C':
    from adapter import Adapter_CC_CB as Adapter
if BANDWIDTH == 'C' and CHUNK_TYPE == 'V':
    from adapter import Adapter_CC_VB as Adapter
if BANDWIDTH == 'V' and CHUNK_TYPE == 'C':
    from adapter import Adapter_VC_CB as Adapter
if BANDWIDTH == 'V' and CHUNK_TYPE == 'V':
    from adapter import Adapter_VC_VB as Adapter

SERVER_IP = 'localhost'
SERVER_PORT = 8080


VERBOSE = True # use this for debugging
BUFFER_THRESHOLD = 20 # Max size of buffer, if this is crossed, need to drain the buffer
DRAIN_BUFFER_SLEEP_TIME = 0.5
REBUF_PENALTY = 4.5
SMOOTH_PENALTY = 1  # penalty when resolution for next chunk is changed (depends on how much changed)

'''
client class will request manifest file for all resolutions, chunk length, chunk data size

get_video_chunks() : request video chunks from server and update environment, returns matrics useful for adapt function

self.reward : current_resolution - rebuffering penalty * (rebuffering) - smooth_penalty * (abs(current_resolution - last_resolution))


'''

class Client:
    def __init__(self, server_address, server_port):
        
        self.server_url = f'http://{server_address}:{server_port}'
        
        response = requests.get(f'{self.server_url}/manifest')
        serialized_data = response.content
        data = pickle.loads(serialized_data)
        
        self.bitrate_levels = data[0] # Eg. 8 (Number of Resolutions available)
        self.video_size = data[1] # 8x50 numpy array (Each chunk length in seconds)
        self.tot_chunks = np.shape(self.video_size)[1] # 50 chunks (Total chunks for video)
        self.bitrate_resolution = data[2] # 8 resolutions in Kbps (Resolution in Kbps for each resolution)
        self.video_data_size = data[3] # 8x50 numpy array (Size of each chunk in Kilobytes)
        
        if VERBOSE:
            print(" -- Client initialized with following parameters -- ")
            print(self.bitrate_levels, " bitrate levels")
            print(" video size : ")
            for i in range(self.bitrate_levels):
                print(self.video_size[i])
            print(self.tot_chunks, " tot chunks")
            print(self.bitrate_resolution, " bitrate resolution")
            print("video data size : ")
            for i in range(self.bitrate_levels):
                print(self.video_data_size[i])
            
        
        self.buffer_threshold = BUFFER_THRESHOLD 
        self.drain_buffer_sleep_time = DRAIN_BUFFER_SLEEP_TIME
        self.rebuf_penalty = REBUF_PENALTY
        self.smooth_penalty = SMOOTH_PENALTY
        
        self.adapter = Adapter()  
        self.adapter.initialize(self.bitrate_levels, self.video_size, self.tot_chunks,
        self.bitrate_resolution, self.buffer_threshold, self.drain_buffer_sleep_time, self.rebuf_penalty,
        self.smooth_penalty, self.video_data_size)
        
        self.reward = 0 
        self.buffer_size = 0
        self.video_chunk_counter = 0
        self.rebuf = 0
        self.end_of_video = False
    
    def get_video_chunks(self, quality):
        ## also update environment
        assert quality >= 0
        assert quality < self.bitrate_levels

        video_chunk_size = self.video_size[quality][self.video_chunk_counter]

        start_time = time.time()    

        response = requests.get(f'{self.server_url}/video/{quality}/{self.video_chunk_counter}')

        if response.status_code != 200:
            print('Error: ', response.status_code)
            return None
        else:
            received_chunk_size = len(response.content)
            if VERBOSE:
                print(f'Chunk size: {video_chunk_size}, received size: {received_chunk_size}')
            end_time = time.time()
            delay = (end_time - start_time) 
            throughput = received_chunk_size / delay

        rebuf = max(0, delay - self.buffer_size)
        self.buffer_size = max(0, self.buffer_size - delay)
        self.buffer_size += video_chunk_size

        sleep_time = 0

        if VERBOSE:
            print(f'Buffer size: {self.buffer_size}, rebuf: {rebuf}')

        if self.buffer_size > self.buffer_threshold:
            drain_buffer_time = self.buffer_size - self.buffer_threshold
            sleep_time = np.ceil(drain_buffer_time / self.drain_buffer_sleep_time) * self.drain_buffer_sleep_time
            self.buffer_size -= sleep_time
            if VERBOSE:
                print(f"sleep time : {sleep_time}")
            time.sleep(sleep_time)
        
        self.video_chunk_counter += 1
        
        end_of_video = False
        
        if self.video_chunk_counter >= self.tot_chunks:
            end_of_video = True
            self.video_chunk_counter = 0
            self.buffer_size = 0

        return delay, sleep_time, self.buffer_size, self.rebuf, end_of_video, throughput         
        
                    
    def main(self):
        
        bitrate = self.adapter.adapt(None)
        last_bitrate = -1
        
        while True:
            
            delay, sleep_time, buffer_size, rebuf, end_of_video, throughput = self.get_video_chunks(bitrate)
            
            if VERBOSE:
                print(f'Throughput : {throughput} , Delay : {delay}')
            
            if end_of_video:
                return self.reward
            
            temp = None
            
            if last_bitrate != -1: 
                temp = self.bitrate_resolution[bitrate]  - self.rebuf_penalty * rebuf - self.smooth_penalty * np.abs(self.bitrate_resolution[bitrate] - self.bitrate_resolution[last_bitrate])
            else: # initial case
                temp = self.bitrate_resolution[bitrate] - self.rebuf_penalty * rebuf
                
            max_reward = self.bitrate_resolution[-1]
            self.reward += (temp/max_reward)*100
            
            if VERBOSE:
                print(f'Bitrate: {bitrate}, Reward: {self.reward}')
            
            last_bitrate = bitrate  
            
            bitrate = self.adapter.adapt(delay, sleep_time, buffer_size, rebuf, end_of_video, self.reward, throughput)
        
            
if __name__ == '__main__':
    client = Client(SERVER_IP, SERVER_PORT)
    print(client.main())