#coding=utf-8

'''
date:2019-8
introduce:Chatroom server
env:python3.5
'''

from socket import *
import os,sys

#登录判断
def do_login(s,user,name,addr):
    if (name in user) or name=='管理员':
        s.sendto('该用户已存在'.encode(),addr)
        return
    s.sendto(b'ok',addr)

    msg='\n欢迎 %s 进入聊天室'%name 
    for i in user:
        s.sendto(msg.encode(),user[i])
    user[name]=addr

def do_chat(s,user,name,text):
    msg="\n%s : %s"%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])

def do_quit(s,user,name):
    msg='\n'+name+"退出了聊天室"
    for i in user:
        if i ==name:
            s.sendto(b'EXIT',user[i])
        else:
            s.sendto(msg.encode(),user[i])
    del user[name]

#接收客户端请求
def do_parent(s):
    user={}
    while True:
        msg,addr=s.recvfrom(1024)
        msglist=msg.decode().split(' ')

        if msglist[0]=="L":
            do_login(s,user,msglist[1],addr)
        elif msglist[0]=="C":
            do_chat(s,user,msglist[1],
                ' '.join(msglist[2:]))
        elif msglist[0]=="Q":
            do_quit(s,user,msglist[1])

#管理员喊话
def do_child(s,addr):
    while True:
        msg=input("管理员消息：")
        msg='C 管理员 '+msg
        s.sendto(msg.encode(),addr)

def main():
    #server address
    ADDR=("0.0.0.0",8888)
    s=socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)

    pid=os.fork()

    if pid<0:
        sys.exit("Create process failed")
    elif pid==0:
        do_child(s,ADDR)
    else:
        do_parent(s)
       



if __name__=='__main__':
    main()