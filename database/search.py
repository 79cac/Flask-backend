#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-10 23:33:10
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import dbconn

def searchByAttackId(condition):
	result = dbconn.query('`index`', 'attack_id, attack_name, plat_info, target_info, proto, src_ip, dst_ip, ts_type',condition)
	return result

def searchByAttackName(condition):
	result = dbconn.query('`index`', 'attack_id, attack_name, plat_info, target_info, proto, src_ip, dst_ip, ts_type',condition)
	return result

def listAll():
    result = dbconn.query('`index`','attack_id, attack_name, plat_info, target_info, proto, src_ip, dst_ip, ts_type')
    return result

def verifyLog(condition):
	result = dbconn.query('`user`', 'password', condition)
	return result

def logInfo(condition):
	result = dbconn.query('`userinfo`', 'logInTime, logOutTime', condition)
	# only list 5 record
	result = result[:-1]
	result = result[::-1]
	if len(result) <= 5:
		return result
	else:
		return result[:5]

def getFlowList():
	result = dbconn.query('`index`','attack_name')
	return result

def getTaskList(condition):
	result = dbconn.query('`taskindex`','task_name', condition)
	new_result = []
	for i in result:
		if i in new_result:
			pass
		else:
			new_result.append(i)
	return new_result

def loadTask(condition):
	result = dbconn.query('`taskindex`','attack_name, times, feedback', condition)
	print result
	return result

def getReleaseInfo(condition):
    result = dbconn.query('`taskinfo`','task_name, srcIP, dstIP, starttime, endtime, status', condition)
    return result

def showDetails(condition):
    timestamp_info = dbconn.query('timestamp','pkt_num, delta_sec, delta_usec',condition)
    result = []
    for i in timestamp_info:
		package = []
		package.append(i[0])
		package.append(i[1])
		package.append(i[2])
		newcondition = condition
		newcondition['pkt_num'] = i[0]
		proto = dbconn.query('`state`','proto',newcondition)[0][0].split('_')

		if proto[0] == '0800':
			#IP
			protocal = 'IP'
			ip_info = dbconn.query('iphdr','ip_src, ip_dst',newcondition)[0]
			package.append(ip_info[0])
			package.append(ip_info[1])

			if proto[1] == '6':
				# TCP
				protocal = 'TCP'
				tcp_info = dbconn.query('tcphdr', 'tcp_sport, tcp_dport, tcp_flags',newcondition)[0]
				package.append(tcp_info[0])
				package.append(tcp_info[1])
				data = 'TCP flags: ' + tcp_info[2]

				if proto[2] == '1':
					#payload
					payload = dbconn.query('payload','data',newcondition)[0]
					data += ' DATA: ' + payload[0]

		package.append(protocal)
		package.append(data)
		result.append(package)
    return result

