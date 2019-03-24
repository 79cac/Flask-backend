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
    # we chooose the last one which has no logOutTime if this condition happens
    dbconn.update('`userinfo`', {'logOutTime':data[1]}, {'logInTime': result[-1][0]})

def addTask(username, task_name, attack_info):
    for i in attack_info:
        data = [username,task_name,i['flowName'],i['Number'],i['isFeedback']]
        dbconn.insert('`taskindex`','username, task_name, attack_name, times, feedback',data)
