# -*- coding: utf-8 -*-
import SoCon as con
import time
import pickle
import cv2
import struct
port = int(input("Port:"))
client = con.client("144.122.137.19",port)
client.connect_server()


data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += client.clinetSocket.recv(4096)
        print("Loop1")
    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        print("Loop2")
        data += client.clinetSocket.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    ID=input("ID:")
    if ID == "exit":
        break
    cv2.imwrite("Images/"+ID+".png",frame)

    