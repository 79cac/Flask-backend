#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-09 
# @Author  : Wangyue 
# @Link    : http://example.org
# @Version : $1.0$

import logging
import time
from websocket_server import WebsocketServer

def register(message,client):
    hackerIP = message.split(',')[0]
    serverIP = message.split(',')[1]
    isAttack = message.split(',')[2]

    if isAttack == '-1':
        #single mode
        registerGroup = {}
        registerGroup['hackerIP'] = hackerIP
        registerGroup['hackerHandler'] = client
        registerGroup['packageNumber'] = packageList['id'] 
        registerList[registerList['id']] = registerGroup
        registerList['id'] += 1
        packageList[packageList['id']] = []
        packageList['id'] += 1
        return True,{},registerList['id']-1

    for registerGroup in registerList.values():
        if type(registerGroup) != dict:
            continue
        if isAttack == '1':
            if registerGroup['serverIP'] == serverIP and registerGroup['hackerIP'] == '' and registerGroup['packageNumber'] == -1:
                registerGroup['hackerIP'] = hackerIP
                registerGroup['hackerHandler'] = client
                registerGroup['packageNumber'] = packageList['id']                
                packageList[packageList['id']] = []
                packageList['id'] += 1
                return True,registerGroup['serverHandler'],registerList['id']-1
            elif registerGroup['hackerHandler'] == client:
                return False,{},0

        elif isAttack == '0':
            if registerGroup['serverIP'] == '' and registerGroup['hackerIP'] == hackerIP and registerGroup['packageNumber'] == -1:
                registerGroup['server'] = serverIP
                registerGroup['serverHandler'] = client
                registerGroup['packageNumber'] = packageList['id']                
                packageList[packageList['id']] = []
                packageList['id'] += 1
                return True,registerGroup['hackerHandler'],registerList['id']-1
            elif registerGroup['serverHandler'] == client:
                return False,{},0
        else:
            print 'isAttack error'
    registerGroup = {}
    registerGroup['serverIP'] = ''
    registerGroup['hackerIP'] = ''
    registerGroup['packageNumber'] = -1
    registerGroup['hackerHandler'] = {}
    registerGroup['serverHandler'] = {}
    if isAttack == '1':
        registerGroup['hackerIP'] = hackerIP
        registerGroup['hackerHandler'] = client
    if isAttack == '0':
        registerGroup['serverIP'] = serverIP
        registerGroup['serverHandler'] = client
    registerList[registerList['id']] = registerGroup
    registerList['id'] += 1
    return False,{},0

def new_client(client, server):
    pass

def receive_message(client, server, message):
    global userHandler
    print message
    if message[0:9] == 'Register:':
        registerFinished,another,registerId = register(message[9:],client)
        if registerFinished:
            #print packageList
            if another == {}:
                #single mode
                server.send_message(client,'Register success!' + str(registerId))
            else:
                #double mode
                server.send_message(client,'Register success!' + str(registerId))
                server.send_message(another,'Register success!'+ str(registerId))
        else:
            #print registerList
            server.send_message(client,'Need to wait another one.')
        return 
    if message[0:5] == 'Data:':
        packageInfo = {}
        arr = message[5:].split(',')
        packageInfo['num'] = arr[0]
        packageInfo['length'] = arr[1]
        packageInfo['time'] = time.time()
        packageInfo['isAttacker'] = arr[2]
        registerListId = int(arr[3])
        packageId = registerList[registerListId]['packageNumber']
        if arr[2] == '1':
            dstHandler = registerList[registerListId]['serverHandler']
        elif arr[2] == '0':
            dstHandler = registerList[registerListId]['hackerHandler']
        else:
            #single mode
            server.send_message(userHandler,message[5:] + ',' +  str(packageInfo['time']))
            return 
        packageList[packageId].append(packageInfo)
        server.send_message(userHandler,message[5:] + ',' +  str(packageInfo['time']))
        server.send_message(dstHandler,message[5:])

    if message[0:4] == 'End:':
        registerListId = int(message[4:])
        if (registerList.get(registerListId,'') != ''):
            packageId = registerList[registerListId]['packageNumber']
            if (packageList.get(packageId,'') != ''):
                del packageList[packageId]
                packageList['id'] -= 1
            del registerList[registerListId]
            registerList['id'] -= 1
        print registerList
    if message[0:5] == 'User:':
        userHandler = client

def client_left(client, server):
    print 'A client left!'

userHandler = {}
registerList = {}
registerList['id'] = 0
packageList = {}
packageList['id'] = 0
server = WebsocketServer(host='192.168.233.150',port=1338)
server.set_fn_new_client(new_client)
server.set_fn_message_received(receive_message)
server.set_fn_client_left(client_left)
server.run_forever()