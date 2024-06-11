import ast
import socket
import json
import os


filename = 'The_Content_Dictionary.txt'
tempr = {}

if not os.path.exists(filename):
    with open(filename, 'w') as flm:
        dat = json.dumps(tempr)
        flm.write(dat)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('0.0.0.0', 5001))
    while True:
        message, adress = s.recvfrom(1024)
        data = json.loads(message.decode('utf-8'))
        print(f"recieved from {adress[0]} : {data}")
        if os.path.exists(filename):
            with open(filename, 'r+') as f:
                content_json = f.read()
                content = json.loads(content_json)
                for prt in content:
                    for lst in content[prt]:
                        print(prt + " : " + lst)
                print(content)
                print("---------------------------------------------------")
                for itr in data['chunks']:
                    #content.setdefault(itr, adress[0])
                    if itr in content:
                        if adress[0] in content[itr]:
                            continue
                        else:
                            content[itr].append(adress[0])
                    else:
                        content[itr] = [adress[0]]
                f.seek(0)
                f.truncate()
                f.write(json.dumps(content))




        '''
         else:
            with open(filename, 'w+') as f:
                f.write(json.dumps(tempr))
        '''


        '''
        tempr.setdefault(f"{adress[0]}", [])
        print(f"{adress[0]}" + " : ")
        for chunk in data["chunks"]:
            print(chunk)
            tempr[adress[0]].append(chunk)

        if os.path.exists(filename):
            with open(filename, 'r+') as f:
                content_json = f.read()
                chunks = json.loads(content_json)

            if adress[0] in chunks:
                for itr in tempr[adress[0]]:
                    chunks[adress[0]].append(itr)
            elif adress[0] not in chunks:
                chunks.setdefault(f"{adress[0]}", [])
                for itr in tempr[adress[0]]:
                    chunks[adress[0]].append(itr)
            with open(filename, 'w+') as f:
                f.write(json.dumps(chunks))
        else:
            with open(filename, 'w+') as f:
                f.write(json.dumps(tempr))

        '''






