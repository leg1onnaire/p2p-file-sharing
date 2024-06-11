import socket
import json
import os
import time
from datetime import datetime

UPLOAD_IP = '192.168.2.204'
UPLOAD_PORT = 5000
LOG_FILE = 'Upload_log.txt'

def handle_request(request):
    filename = request['requested_content']
    file_path = f"{filename}"

    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as file:
            data = file.read()
            return {'success': True, 'file_size': file_size, 'data': data}
    else:
        return {'success': False, 'error': f"File '{filename}' not found."}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((UPLOAD_IP, UPLOAD_PORT))
    server_socket.listen(1)

    print("Uploader started and listening for connections...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")

        with conn:
            request_data = conn.recv(1024)
            request = json.loads(request_data.decode('utf-8'))

            print(f"Requested: {request['requested_content']}")

            response = handle_request(request)

            if response['success']:
                file_size = response['file_size']
                current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                log_entry = f"{request['requested_content']} | {addr[0]} | {current_time}"

                print(f"Sending {request['requested_content']} ({file_size} bytes) to {addr}")
                with open(LOG_FILE, 'a') as log_file:
                    log_file.write(log_entry + "\n")

                conn.sendall(response['data'])
            else:
                print(f"Failed to send {request['requested_content']} to {addr}: {response['error']}")