# @Time : 2022/8/2 14:42 
# @Author : NineMeet
# @File : scan.py
import socket
from socket import *
import argparse
import re
from IPy import IP
# 1、怎么通过参数来判断执行哪个函数同时也能将参数添加进去
# 关于报错信息的记录
#    'module' object is not callable 模块对象不可调用 加一个from可以解决问题

# 对数据进行简单分析 转换域名/IP地址为IP地址
ip_list = []
port_list = []

#将域名简单转化为IP地址，但是不排除存在CDN的可能
def dataMnalysis(host):
    IP = gethostbyname(host)
    return IP

# 对IP段进行处理
def ipSplit1(host): # 判断192.168.1.1-255 其中存在-的数字 返回列表
    start_ip = host.split('.')
    end = start_ip[3].split('-')
    # print(end[0])
    for i in range(int(end[0]),(int(end[1]))+1):
        ip =start_ip[0] + "." + start_ip[1] + "." + start_ip[2] + "." + str(i)
        ip_list.append(ip)
    return ip_list

def ipSplit2(host): # 判断192.168.1.1，1，2 其中存在‘，’的数字
    start_ip = host.split('.')
    end = start_ip[3].split(',')
    for i in range(len(end)):
        ip = start_ip[0] + "." + start_ip[1] + "." + start_ip[2] + "." + end[i]
        ip_list.append(ip)
    return ip_list

def ipSplit3(host):    #192.168.1.0/24 返回列表
    try:
        ip = IP(host)
        for i in ip:
            ip_list.append(str(i))
        return ip_list
    except:
        print("请检查IP地址及子网掩码是否正确")
        exit()

def ipSplit4(host):    #192.168.1.1,192.168.3.2
    ip_list = host.split(',')#返回列表
    return ip_list

# 端口扫描
def portSocketScan(host,port):
    for i in host:
        for j in port:
            try:
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((str(i),int(j)))
                print(f"端口{j}的状态为 open".format(j))
                s.close()
            except:
                pass
#IP段选择函数方法
def portManage(port):
    if ',' in port:
        for i in port.split(','):
            port_list.append(i)
        return port_list
    else:
        ports = port.split('-')
        for i in range(int(ports[0]), int(ports[1]) + 1):
            port_list.append(i)
        return port_list

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-d','--host',default='192.168.2.13')
    parse.add_argument('-p','--port',default="80,443")
    args = parse.parse_args()
    host = args.host
    port = args.port
    ports = portManage(port)
    if(len(re.findall(r'[a-z]',host)) == 0):#判断是IP地址还是网址
        if '-' in host:
            ip = ipSplit1(host)
            portSocketScan(ip,ports)
        elif host.count('.') == 3 and '-' not  in host:
            ip = ipSplit2(host)
            portSocketScan(ip, ports)
        elif host.count('.') > 3:
            ip = ipSplit3(host)
            portSocketScan(ip, ports)
        else:
            ip = ipSplit4(host)
            portSocketScan(ip, ports)
    else:
        ip = dataMnalysis(host)
        portSocketScan(ip, port)