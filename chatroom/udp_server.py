from socket import *
import os

s = socket(AF_INET,SOCK_DGRAM)
ADDR = ("127.0.0.1",8888)
s.bind(ADDR)

# 处理客户端的各种请求
def do_child():
    user = {}
    while True:
        data,addr = s.recvfrom(1024)
        li = data.decode().split(" ")
        name = li[1]
        if li[0] == "L":
            if name in user or name == "管理员":
                s.sendto("用户名重复".encode(),addr)
            else:
                s.sendto(b'OK',addr)
                msg = "欢迎%s进入聊天室" % name
                for i in user:
                    s.sendto(msg.encode(),user[i])
                user[name] = addr
        elif li[0] == "C":
            msg = name + "说:" + " ".join(li[2:])
            for i in user:
                if i != name:
                    s.sendto(msg.encode(),user[i])

        elif li[0] == "Q":
            msg = "%s退出了聊天室" % name
            del user[name]
            for i in user:
                s.sendto(msg.encode(),user[i])

# 发送管理员公告
def do_parent():
    while True:
        g = input("输入公告：")
        gonggao = "C 管理员 " + g
        s.sendto(gonggao.encode(),ADDR)

pid = os.fork()
if pid < 0:
    print("create child process failed")
elif pid == 0:
    do_child()
else:
    do_parent()

