#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-24
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import dbconn

def logInTime(data):
    data.append(-1)
    dbconn.insert('`userinfo`', 'username, logInTime, logOutTime', data)

def logOutTime(data):
    condition = {'username': data[0], 'logOutTime': -1}
    result = dbconn.query('`userinfo`', 'logInTime', condition)
    if len(result) == 0:
        print 'Log Time Error'
        return
    # we chooose the last one which has no logOutTime if this condition happens
    dbconn.update('`userinfo`', {'logOutTime':data[1]}, {'logInTime': result[-1][0]})

def addTask(username, task_name, attack_info):
    for i in attack_info:
        data = [username,task_name,i['flowName'],i['Number'],i['isFeedback']]
        dbconn.insert('`taskindex`','username, task_name, attack_name, times, feedback',data)

def publish(username,task_name,attack_info,starttime,srcIP,dstIP):
    if task_name == '' or task_name == None:
        result = dbconn.query('`taskinfo`','task_id')
        task_name = 'task-' + str(len(result) + 1)
    print task_name
    data = [username, task_name, srcIP, dstIP, starttime, -1, 0]
    dbconn.insert('`taskinfo`','username, task_name, srcIP, dstIP, starttime, endtime, status',data)
    #get task_id
    result = dbconn.query('`taskinfo`','task_id')
    task_id = len(result)
    for i in attack_info:
        data = [username,task_id,i['flowName'],i['Number'],i['isFeedback'],0]
        dbconn.insert('`taskprogress`','username, task_id, attack_name, times, feedback, status',data)