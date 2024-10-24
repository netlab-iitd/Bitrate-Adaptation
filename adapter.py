import numpy as np

class Adapter_CC_CB:
    def __init__(self) -> None:
        '''
            You might need these fields
            You are free to add more fields as per your requirement
        '''
        self.last_bitrate = 0
        self.last_buffer_size = 0
        self.last_throughput = 0
        self.last_rebuf = 0
        self.last_sleep_time = 0
        self.last_end_of_video = False
        self.video_chunk_counter = 0
        self.video_data_size = None
        
        
        # These fields will store manifest file, fields have similar meanings like client.py
        self.bitrate_levels = None 
        self.video_size = None
        self.tot_chunks = None
        self.bitrate_resolution = None
        self.buffer_threshold = None
        self.drain_buffer_sleep_time = None
        self.rebuf_penalty = None
        self.smooth_penalty = None
    
    # store manifest file
    def initialize(self, *args) -> None:
        self.bitrate_levels, self.video_size, self.tot_chunks, self.bitrate_resolution, self.buffer_threshold, self.drain_buffer_sleep_time, self.rebuf_penalty, self.smooth_penalty, self.video_data_size = args
        
    '''
    Dont change name of this method, this one is used by client.py
    You need to implement this method   
    '''
    def adapt(self, *args) -> int:
        if args == (None,):
            return np.random.choice(self.bitrate_levels) # Comment this line
            # Write your code here
        else:
            delay, sleep_time, buffer_size, rebuf, end_of_video, reward, throughput = args
            return np.random.choice(self.bitrate_levels) # Comment this line
            # Write your code here


class Adapter_VC_CB:
    def __init__(self) -> None:
        '''
            You might need these fields
            You are free to add more fields as per your requirement
        '''
        self.last_bitrate = 0
        self.last_buffer_size = 0
        self.last_throughput = 0
        self.last_rebuf = 0
        self.last_sleep_time = 0
        self.last_end_of_video = False
        self.video_chunk_counter = 0
        self.video_data_size = None
        
        
        # These fields will store manifest file, fields have similar meanings like client.py
        self.bitrate_levels = None 
        self.video_size = None
        self.tot_chunks = None
        self.bitrate_resolution = None
        self.buffer_threshold = None
        self.drain_buffer_sleep_time = None
        self.rebuf_penalty = None
        self.smooth_penalty = None
    
    # store manifest file
    def initialize(self, *args) -> None:
        self.bitrate_levels, self.video_size, self.tot_chunks, self.bitrate_resolution, self.buffer_threshold, self.drain_buffer_sleep_time, self.rebuf_penalty, self.smooth_penalty, self.video_data_size = args
        
    '''
    Dont change name of this method, this one is used by client.py
    You need to implement this method   
    '''
    def adapt(self, *args) -> int:
        if args == (None,):
            return np.random.choice(self.bitrate_levels) # Comment this line
            # Write your code here
        else:
            delay, sleep_time, buffer_size, rebuf, end_of_video, reward, throughput = args
            return np.random.choice(self.bitrate_levels) # Comment this line
            # Write your code here

class Adapter_CC_VB:
    def __init__(self) -> None:
        '''
            You might need these fields
            You are free to add more fields as per your requirement
        '''
        self.last_bitrate = 0
        self.last_buffer_size = 0
        self.last_throughput = 0
        self.last_rebuf = 0
        self.last_sleep_time = 0
        self.last_end_of_video = False
        self.video_chunk_counter = 0
        self.video_data_size = None
        
        
        # These fields will store manifest file, fields have similar meanings like client.py
        self.bitrate_levels = None 
        self.video_size = None
        self.tot_chunks = None
        self.bitrate_resolution = None
        self.buffer_threshold = None
        self.drain_buffer_sleep_time = None
        self.rebuf_penalty = None
        self.smooth_penalty = None
    
    # store manifest file
    def initialize(self, *args) -> None:
        self.bitrate_levels, self.video_size, self.tot_chunks, self.bitrate_resolution, self.buffer_threshold, self.drain_buffer_sleep_time, self.rebuf_penalty, self.smooth_penalty, self.video_data_size = args
        
    '''
    Dont change name of this method, this one is used by client.py
    You need to implement this method   
    '''
    def adapt(self, *args) -> int:
        if args == (None,):
            return np.random.choice(self.bitrate_levels) # Comment this line
            # Write your code here
        else:
            delay, sleep_time, buffer_size, rebuf, end_of_video, reward, throughput = args
            return np.random.choice(self.bitrate_levels) # Comment this line
            # Write your code here


class Adapter_VC_VB:
    def __init__(self) -> None:
        '''
            You might need these fields
            You are free to add more fields as per your requirement
        '''
        self.last_bitrate = 0
        self.last_buffer_size = 0
        self.last_throughput = 0
        self.last_rebuf = 0
        self.last_sleep_time = 0
        self.last_end_of_video = False
        self.video_chunk_counter = 0
        self.video_data_size = None
        
        
        # These fields will store manifest file, fields have similar meanings like client.py
        self.bitrate_levels = None 
        self.video_size = None
        self.tot_chunks = None
        self.bitrate_resolution = None
        self.buffer_threshold = None
        self.drain_buffer_sleep_time = None
        self.rebuf_penalty = None
        self.smooth_penalty = None
    
    # store manifest file
    def initialize(self, *args) -> None:
        self.bitrate_levels, self.video_size, self.tot_chunks, self.bitrate_resolution, self.buffer_threshold, self.drain_buffer_sleep_time, self.rebuf_penalty, self.smooth_penalty, self.video_data_size = args
        
    '''
    Dont change name of this method, this one is used by client.py
    You need to implement this method   
    '''
    def adapt(self, *args) -> int:
        if args == (None,):
            return np.random.choice(self.bitrate_levels) # Comment this line
            # Write your code here
        else:
            delay, sleep_time, buffer_size, rebuf, end_of_video, reward, throughput = args
            return np.random.choice(self.bitrate_levels) # Comment this line
            # Write your code here
