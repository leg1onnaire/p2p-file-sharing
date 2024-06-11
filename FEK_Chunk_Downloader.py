import socket
import json
import os
import math
import datetime

user_inpt = input("what content do you want to download : ")

def update_avaliable_chunks(user_input_in):

    data_filename = "Available_Chunks.txt"

    with open(data_filename, 'r+') as f:
        cont_json = f.read()
        extnd = [user_inpt + "_1", user_inpt + "_2", user_inpt + "_3", user_inpt + "_4", user_inpt + "_5"]
        cont = json.loads(cont_json)
        extnd_set = set(extnd)
        cont_set = set(cont['chunks'])

        if extnd_set.issubset(cont_set):
            print(f"Chunks for {user_inpt} are already available")
            f.seek(0)
        else:
            cont['chunks'].extend(extnd)
            f.seek(0)
            cont_json = json.dumps(cont)
            f.write(cont_json)

print("------------------------------------------------------------")

data = {"requested_content" : "colors_1"}

filename = 'The_Content_Dictionary.txt'
file_log = 'Download_Log.txt'
data_filename = "Available_Chunks.txt"
tempr = {}
tempr2 = {'chunks' : []}

if not os.path.exists(filename):
    with open(filename, 'w') as s:
        dat = json.dumps(tempr)
        s.write(dat)

if not os.path.exists(file_log):
    with open(file_log, 'w') as s:
        s.close()

if not os.path.exists(data_filename):
    with open(data_filename, 'w') as s:
        dat = json.dumps(tempr2)
        s.write(dat)

downloaded = 0
Flag = True
Flag_Success = False
Flag_Key_Error = False
itr = 1
'''
def tcp_connect(ip, itr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, 5000))
        str = "{}{}{}".format(user_inpt, "_", itr)
        print(f"Requesting : {str}")
        data['requested_content'] = str
        json_data = json.dumps(data)
        s.send(bytes(json_data, 'utf-8'))
        while True:
            chunk_recv = s.recv(20866)
            print(f"Recieved chunk {str}")
            timestamp = datetime.datetime.now().timestamp()
            with open(str + '_recv', 'wb+') as chunk_file:
                chunk_file.write(chunk_recv)
                downloaded = 1
                itr += 1
                Flag_Success = True
                break

'''

while itr <= 5:
    downloaded = 0
    Flag_Success = 0
    with open(filename, 'r+') as fl:
        ips_json = fl.read()
        ips = json.loads(ips_json)
        indx = "{}{}{}".format(user_inpt, "_", itr)
        try:
            for ip in ips[indx]:
                try:
                    # tcp_connect(ip, itr)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((ip, 5000))
                        str = "{}{}{}".format(user_inpt, "_", itr)
                        print(f"Requesting : {str}")
                        data['requested_content'] = str
                        json_data = json.dumps(data)
                        s.send(bytes(json_data, 'utf-8'))
                        while True:
                            chunk_recv = s.recv(262144)
                            print(f"Recieved chunk {str}")
                            print("------------------------------------------------------------")
                            timestamp = datetime.datetime.now().timestamp()
                            time_normal = datetime.datetime.fromtimestamp(timestamp)
                            form_time = time_normal.strftime('%d-%m-%Y %H:%M:%S')
                            with open(file_log, 'a') as log_file:
                                log_data = "{} | {} | {} | {}".format(timestamp, str, ip, form_time)
                                log_data_json = json.dumps(log_data)
                                log_file.write(log_data_json)
                                log_file.write("\n")
                            #with open(str + '_recv', 'wb+') as chunk_file:
                            with open(str , 'wb+') as chunk_file:
                                chunk_file.write(chunk_recv)
                                downloaded = 1
                                itr += 1
                                Flag_Success = True
                                break
                except TimeoutError:
                    print(f"No repeat from {ip}")
                    print(f"Cannot download chunk {user_inpt}_{itr} from peer {ip}")
                    print(f"Trying other peers...")
                    print("------------------------------------------------------------")
                    downloaded = 0
                except ConnectionRefusedError:
                    print(f"Connection refused by {ip}, try opening Chunk_Uploader in {ip}")
                    print(f"Cannot download chunk {user_inpt}_{itr} from peer {ip}")
                    print(f"Trying other peers...")
                    print("------------------------------------------------------------")
                    downloaded = 0

                if Flag_Success == True:
                    break

                if ip == ips[indx][len(ips[indx]) - 1] and downloaded == 0:
                    Flag = False
                    print(f"CHUNK {user_inpt}_{itr} CANNOT BE DOWNLOADED FROM ONLINE PEERS.")
                    break
        except KeyError:
            print(f"Content {user_inpt} is not available in peers")
            print("------------------------------------------------------------")
            Flag_Key_Error = True
            break
    if Flag == False:
        break

if Flag == True and Flag_Key_Error == False:

    update_avaliable_chunks(user_inpt)

    # STITCH IMAGE BACK TOGETHER
    # # Normally this will be in another location to stitch it back together

    content_name = user_inpt  # again, this'll be the name of the content that used wanted to download from the network.
    chunknames = [content_name + '_1', content_name + '_2', content_name + '_3', content_name + '_4',
                  content_name + '_5']

    # with open(content_name+'.png', 'w') as outfile:
    with open(content_name +'.png', 'wb') as outfile:  # in your code change 'ece.png' to content_name+'.png'
        for chunk in chunknames:
            with open(chunk, 'rb') as infile:
                outfile.write(infile.read())
            infile.close()


'''

                            with open(file_log, 'r+') as log:
                                line = "".format(timestamp, str, ip)
                                line_json = json.dumps(line)
                                log.write(line_json)

chnks  = [1,2,3,4,5]

for itr in chnks:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.2.110', 5000))
        str = "{}{}{}".format(user_inpt, "_", itr)
        print(f"Requesting : {str}")
        data['requested_content'] = str
        json_data = json.dumps(data)
        s.send(bytes(json_data, 'utf-8'))
        while True:
            chunk_recv = s.recv(20866)
            print(f"Recieved chunk {str}")
            with open(str + '_recv', 'wb+') as chunk_file:
                chunk_file.write(chunk_recv)
                break
'''


'''                
        data = {"requested_content": f"valley_{itr}"}

        json_data = json.dumps(data)
        print(f"Requesting chunk valley_{itr}...")
        #json_dat = json.dumps(itr)
        s.send(bytes(json_data, 'utf-8'))


    while True:
        chunk_recv = s.recv(20866)
        print(f"Recieved chunk {data['requested_content']}")
        with open(data['requested_content'] + 'recv', 'wb+') as chunk_file:
            chunk_file.write(chunk_recv)
            break
'''

