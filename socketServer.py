#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-09 
# @Author  : Wangyue 
# @Link    : http://example.org
# @Version : $1.0$

import logging
import time
import json
from websocket_server import WebsocketServer

def release(data):
    global connectingClient
    if connectingClient.get(data['srcIP'],None) == None:
        print 'Error! client is not connecting!'
        return
    if connectingClient.get(data['dstIP'],None) == None:
        print 'Error! client is not connecting!'
        return
    hackerHandler = connectingClient.get(data['srcIP'],None)[1]
    serverHandler = connectingClient.get(data['dstIP'],None)[1]
    data['isAttacker'] = 1
    server.send_message(hackerHandler, json.dumps(data))
    data['isAttacker'] = 0
    server.send_message(serverHandler, json.dumps(data))

def register(message,client):
    hackerIP = message.split(',')[0]
    serverIP = message.split(',')[1]
    isAttack = message.split(',')[2]
    attack_name = message.split(',')[3]

    if isAttack == '-1':
        #single mode
        registerGroup = {}
        registerGroup['hackerIP'] = hackerIP
        registerGroup['hackerHandler'] = client
        registerGroup['packageNumber'] = packageList['id']
        registerGroup['attack_name'] = attack_name
        # for not conflict
        registerGroup['listid'] = -1
        registerList[registerList['id']] = registerGroup
        registerList['id'] += 1
        packageList[packageList['id']] = []
        packageList['id'] += 1
        return True,{},registerList['id']-1,attack_name

    for registerGroup in registerList.values():
        if type(registerGroup) != dict or registerGroup.get('listid',False) == -1:
            continue
        if isAttack == '1':
            if registerGroup['serverIP'] == serverIP and registerGroup['hackerIP'] == '' and registerGroup['attack_name'] == attack_name and registerGroup['packageNumber'] == -1:
                registerGroup['hackerIP'] = hackerIP
                registerGroup['hackerHandler'] = client
                registerGroup['packageNumber'] = packageList['id']                
                packageList[packageList['id']] = []
                packageList['id'] += 1
                return True,registerGroup['serverHandler'],registerGroup['listid'],attack_name
            elif registerGroup['hackerHandler'] == client:
                return False,{},0,''

        elif isAttack == '0':
            if registerGroup['serverIP'] == '' and registerGroup['hackerIP'] == hackerIP and registerGroup['attack_name'] == attack_name and registerGroup['packageNumber'] == -1:
                registerGroup['server'] = serverIP
                registerGroup['serverHandler'] = client
                registerGroup['packageNumber'] = packageList['id']                
                packageList[packageList['id']] = []
                packageList['id'] += 1
                return True,registerGroup['hackerHandler'],registerGroup['listid'],attack_name
            elif registerGroup['serverHandler'] == client:
                return False,{},0,''
        else:
            print 'isAttack error'
    registerGroup = {}
    registerGroup['serverIP'] = ''
    registerGroup['hackerIP'] = ''
    registerGroup['packageNumber'] = -1
    registerGroup['hackerHandler'] = {}
    registerGroup['serverHandler'] = {}
    registerGroup['attack_name'] = attack_name
    if isAttack == '1':
        registerGroup['hackerIP'] = hackerIP
        registerGroup['hackerHandler'] = client
    if isAttack == '0':
        registerGroup['serverIP'] = serverIP
        registerGroup['serverHandler'] = client
    registerGroup['listid'] = registerList['id']
    registerList[registerList['id']] = registerGroup  
    registerList['id'] += 1
    print registerList
    return False,{},0,''

def new_client(client, server):
    pass
    
def receive_message(client, server, message):
    print message
    global userHandler
    global connectingClient
    global taskList
    if message == 'Client':
        address = client['address'][0]
        connectingClient[address] = [0,client,'0%','0%']
    if message[0:7] == 'update:':
        #update deviceinfo
        data = json.loads(message[7:])
        address = client['address'][0]
        connectingClient[address][2] = data[0]
        connectingClient[address][3] = data[1]
        print connectingClient
    if message[0:8] == 'release:':
        data = json.loads(message[8:])
        release(data)
    if message[0:4] == 'Ins:':
        userHandler = client
        #get device information
        if message[4:] == 'device':
            outcome = []
            for key,value in connectingClient.iteritems():
                data = [key,value[0],value[2],value[3]]
                outcome.append(data)
            server.send_message(userHandler,json.dumps(outcome))
        return
    if message[0:9] == 'Register:':
        registerFinished,another,registerId,attack_name = register(message[9:],client)
        if registerFinished:
            print 'Register success!'
            #print packageList
            if another == {}:
                #single mode
                server.send_message(client,'Register success!' + str(registerId))
                if userHandler != {}:
                    server.send_message(userHandler,'Register success!' + attack_name)
            else:
                #double mode
                server.send_message(client,'Register success!' + str(registerId))
                server.send_message(another,'Register success!'+ str(registerId))
                if userHandler != {}:
                    server.send_message(userHandler,'Register success!' + attack_name)
            #print registerList
        else:
            #print registerList
            server.send_message(client,'Need to wait another one.')
        return 
    if message[0:5] == 'Data:':
        # packageInfo = {}
        arr = message[5:].split(',')
        # packageInfo['num'] = arr[0]
        # packageInfo['length'] = arr[1]
        # packageInfo['time'] = time.time()
        # packageInfo['isAttacker'] = arr[2]
        registerListId = int(arr[3])
        #packageId = registerList[registerListId]['packageNumber']
        if arr[2] == '1':
            dstHandler = registerList[registerListId]['serverHandler']
        elif arr[2] == '0':
            dstHandler = registerList[registerListId]['hackerHandler']
        else:
            #single mode
            if userHandler != {}:
                server.send_message(userHandler,message[5:] + ',' +  str(time.time()))
            return 
        #packageList[packageId].append(packageInfo)
        if userHandler != {}:
            server.send_message(userHandler,message[5:] + ',' +  str(time.time()))
        server.send_message(dstHandler,message[5:])
        return
    if message[0:4] == 'End:':
        registerListId = int(message[4:])
        if (registerList.get(registerListId,'') != ''):
            packageId = registerList[registerListId]['packageNumber']
            if (packageList.get(packageId,'') != ''):
                del packageList[packageId]
            del registerList[registerListId]
        #print registerList
    if message[0:9] == 'Finished:':
        if userHandler != {}:
            server.send_message(userHandler,message)

def client_left(client, server):
    pass

taskList = []
userHandler = {}
registerList = {}
registerList['id'] = 0
packageList = {}
packageList['id'] = 0
connectingClient = {}
server = WebsocketServer(host='192.168.233.150',port=1338)
server.set_fn_new_client(new_client)
server.set_fn_message_received(receive_message)
server.set_fn_client_left(client_left)
server.run_forever()