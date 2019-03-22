#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-10 23:33:10
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import dbconn

def searchByAttackId(id):
	result = dbconn.query('`index`', 'attack_id, attack_name, plat_info, target_info, proto, src_ip, dst_ip, ts_type',id)
	return result

def searchByAttackName(name):
    return 

def listAll():
    result = dbconn.query('`index`','attack_id, attack_name, plat_info, target_info, proto, src_ip, dst_ip, ts_type')
    return result

def showDetails(attack_id):
    timestamp_info = dbconn.query('timestamp','pkt_num, delta_sec, delta_usec',attack_id)
    result = []
    for i in timestamp_info:
		package = []
		package.append(i[0])
		package.append(i[1])
		package.append(i[2])
		proto = dbconn.query('`state`','proto',attack_id,i[0])[0][0].split('_')

		if proto[0] == '0800':
			#IP
			protocal = 'IP'
			ip_info = dbconn.query('iphdr','ip_src, ip_dst',attack_id,i[0])[0]
			package.append(ip_info[0])
			package.append(ip_info[1])

			if proto[1] == '6':
				# TCP
				protocal = 'TCP'
				tcp_info = dbconn.query('tcphdr', 'tcp_sport, tcp_dport, tcp_flags',attack_id,i[0])[0]
				package.append(tcp_info[0])
				package.append(tcp_info[1])
				data = 'TCP flags: ' + tcp_info[2]

				if proto[2] == '1':
					#payload
					payload = dbconn.query('payload','data',attack_id,i[0])[0]
					data += ' DATA: ' + payload[0]

		package.append(protocal)
		package.append(data)
		result.append(package)
    return result

