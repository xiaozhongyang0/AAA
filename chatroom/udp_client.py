from socket import *
import os
import sys

s = socket(AF_INET,SOCK_DGRAM)
IP = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (IP,PORT)
# 处理发送消息
def do_child():
    while True:
        ss = input("输入：")
        if ss == "Q":
            msg = "%s %s " % (ss,name)
            s.sendto(msg.encode(),ADDR)
            break
        else:
            msg = "C %s " % name + ss
            s.sendto(msg.encode(), ADDR)
# 处理接收消息
def do_parent():
    while True:
        data,addr = s.recvfrom(1024)
        print(data.decode())

while True:
    name = input("输入用户名：")
    msg = "L " + name
    s.sendto(msg.encode(),ADDR)
    data,addr = s.recvfrom(1024)
    if data.decode() == "OK":
        print("已进入聊天室")
        break
    else:
        print(data.decode())

pid = os.fork()
if pid < 0:
    print("create child process failed")
elif pid == 0:
    do_child()
else:
    do_parent()
