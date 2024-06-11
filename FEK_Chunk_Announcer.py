import socket
import json
import math
import os
import time

Available_chunks = {"chunks": []}

inpt = input("Enter the available file to divide into chunks : ")

contentname = inpt
filename = contentname + '.png'
c = os.path.getsize(filename)
chunk_size = math.ceil(math.ceil(c)/5)
print(f"Chunks size is : {chunk_size}")
index = 1
with open(filename, 'rb') as infile:
    chunk = infile.read(int(chunk_size))
    while chunk:
        chunkname = contentname + '_' + str(index)
        print("chunkname is : " + chunkname + "\n")
        Available_chunks["chunks"].append(chunkname)
        with open(chunkname, 'wb+') as chunk_file:
            chunk_file.write(chunk)
        index += 1
        chunk = infile.read(int(chunk_size))
#chunk_file.close()

data_filename = "Available_Chunks.txt"


tempr = {'chunks' : []}
if not os.path.exists(data_filename):
    with open(data_filename, 'w') as s:
        dat = json.dumps(tempr)
        s.write(dat)

with open(data_filename, 'r+') as f:
    cont_json = f.read()
    extnd  =[contentname + "_1", contentname + "_2", contentname + "_3", contentname + "_4", contentname + "_5"]
    cont = json.loads(cont_json)
    extnd_set = set(extnd)
    cont_set = set(cont['chunks'])

    if extnd_set.issubset(cont_set):
        print(f"Chunks for {inpt} are already available")
        f.seek(0)
    else:
        cont['chunks'].extend(extnd)
        f.seek(0)
        cont_json = json.dumps(cont)
        f.write(cont_json)


print("Available chunks are : ")

with open(data_filename, 'r+') as f:
    content_json = f.read()
    content = json.loads(content_json)
    print(content)
#for indx in Available_chunks["chunks"]:
#    print(indx + "\n")



print("--------------------START OF CHUNK ANNOUNCEMENT-----------------------")

while True:
    json_data = json.dumps(content)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print("Announcing available chunks...")
        s.sendto(bytes(json_data, 'utf-8'), ('192.168.2.255', 5001))
        print("Available chunks announced.")
    time.sleep(10)
    print("--------------------------------")



'''
json_data = json.dumps(content)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Announcing available chunks...")
    s.sendto(bytes(json_data, 'utf-8'), ('255.255.255.255', 5001))
    print("Available chunks announced.")
'''