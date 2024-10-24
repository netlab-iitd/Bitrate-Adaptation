import pickle
import numpy as np
from http.server import BaseHTTPRequestHandler, HTTPServer


BITRATE_LEVELS = 8
TOTAL_CHUNKS = 50
CHUNK_LENGTH = 5
SERVER_PORT = 8080
SERVER_IP = 'localhost'
CONSTANT = True
MAX_CHUNK_LENGTH = 10

'''
do_GET() handles request from client
Requests can be for manifest or video chunks
Manifest request is handled by handle_manifest_request()
Video chunk request is handled by handle_video_chunk_request()

bitrate_levels: Number of resolutions available
tot_chunks : Total chunks for video
video_size : Size of each chunk in seconds for each resolution as matrix of number of resolutions x total chunks
bitrate_resolution : Resolution in Kbps for each resolution
video_data_size : Size of each chunk in bytes for each resolution as matrix of number of resolutions x total chunks

Each chunk length is of constant length CHUNK_LENGTH
'''


class VideoServer(BaseHTTPRequestHandler):
    
    def initialize_server_data(self):
        
        self.bitrate_levels = BITRATE_LEVELS
        self.tot_chunks = TOTAL_CHUNKS
        
        self.video_size = [[] for i in range(self.bitrate_levels)]
        for i in range(self.bitrate_levels):
            for j in range(self.tot_chunks):
                if CONSTANT:
                    self.video_size[i].append(CHUNK_LENGTH) # chunk length in seconds
                else:
                    self.video_size[i].append(np.random.randint(1, MAX_CHUNK_LENGTH+1))
        self.video_data_size = [[] for i in range(self.bitrate_levels)]
        
        self.bitrate_resolution = [125, 250, 375, 500, 625, 750, 875, 1000]
        
        for i in range(self.bitrate_levels):
            for j in range(self.tot_chunks):
                self.video_data_size[i].append((self.video_size[i][j])*(self.bitrate_resolution[i]))
                

    def do_GET(self):
        self.initialize_server_data()

        if self.path == '/manifest':
            self.handle_manifest_request()

        elif self.path.startswith('/video/'):
            self.handle_video_chunk_request()

    def handle_manifest_request(self):
        data = [self.bitrate_levels, self.video_size, self.bitrate_resolution, self.video_data_size]

        serialized_data = pickle.dumps(data)

        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Length', len(serialized_data))
        self.end_headers()

        self.wfile.write(serialized_data)

    def handle_video_chunk_request(self):
        path_parts = self.path.split('/')
        quality = int(path_parts[2])
        chunk_idx = int(path_parts[3])

        chunk_size = self.video_data_size[quality][chunk_idx]

        # Generating dummy video chunk data
        video_chunk_data = b'10' * (chunk_size//2) * 1024

        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Length', len(video_chunk_data))
        self.end_headers()

        self.wfile.write(video_chunk_data)

def run(server_class=HTTPServer, handler_class=VideoServer, server_address=SERVER_IP, server_port=SERVER_PORT):
    server = server_class((server_address, server_port), handler_class)
    print(f'Starting server at http://{server_address}:{server_port}')
    server.serve_forever()

if __name__ == "__main__":
    run()
