#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-01 14:12:54
# @Author  : Wangyue 
# @Link    : http://example.org
# @Version : $1.0$

import os
import sys
from scapy.all import *
import dbconn
import json
import base64

def save_payload(packet,attack_id,pkt_num):
	# payload needs encode
	data = [attack_id,pkt_num,len(str(packet['Raw'])),base64.b64encode(str(packet['Raw']))]
	dbconn.insert('`payload`','attack_id, pkt_num, data_len,'+\
		'data',data)

def save_tcphdr(packet,attack_id,pkt_num):
	if packet.haslayer(Raw):
		proto = '6_1'
		save_payload(packet,attack_id,pkt_num)
	else:
		proto = '6_0'

	# TCP options needs encode 
	
	data = [attack_id, pkt_num, packet['TCP'].sport,\
		packet['TCP'].dport, packet['TCP'].seq, packet['TCP'].ack,\
		str(packet['TCP'].flags), packet['TCP'].window, packet['TCP'].dataofs,\
		packet['TCP'].reserved, packet['TCP'].urgptr,\
	json.dumps(packet['TCP'].options)]
	dbconn.insert('`tcphdr`','attack_id, pkt_num, tcp_sport,' + \
		'tcp_dport, tcp_seq, tcp_ack, tcp_flags, tcp_win,' + \
		'dataofs, reserved, urgptr, options',data) 
	return proto

def save_iphdr(packet,attack_id,pkt_num,hacker,server):
	if packet['IP'].src == hacker and packet['IP'].dst == server:
		op_code = 1
	elif packet['IP'].src == server and packet['IP'].dst == hacker:
		op_code = 2
	else:
		return 0,'0_0_0'

	if packet.haslayer(TCP):
		proto = '0800_'+save_tcphdr(packet,attack_id,pkt_num)
	elif packet['IP'].proto == 1:
		proto = '0800_'+save_icmphdr(packet)
	elif packet['IP'].proto == 17:
		proto = '0800_'+save_udphdr(packet)
	else:
		proto = '0800_0_0'
		print 'more protocals to be added'

	#insert into `iphdr` tables
	data = [attack_id ,pkt_num, packet['IP'].version,\
		packet['IP'].src, packet['IP'].dst, packet['IP'].tos, \
		packet['IP'].id, str(packet['IP'].flags), packet['IP'].frag, \
		packet['IP'].ttl, packet['IP'].proto]
	dbconn.insert('`iphdr`','attack_id, pkt_num, ip_version,' + \
		'ip_src, ip_dst, ip_tos, ip_id, ip_flags ,ip_frag' + \
		' ,ip_ttl ,ip_proto',data)

	return op_code,proto


def save_packet(pcap, attack_info):
	if len(pcap) == 0:
		print 'there is no packet!'
		return

	# insert into `index` table
	data = [attack_info[2],attack_info[3],attack_info[4],attack_info[5],attack_info[0],attack_info[1],'us']
	dbconn.insert('`index`','attack_name, plat_info, target_info, proto, src_ip, dst_ip, ts_type',data)

	# get attack_id recently insert
	result = dbconn.query('`index`','attack_id')
	attack_id  = 1
	for i in result:
		if i[0] > attack_id:
			attack_id = i[0]
			
	pkt_num = 1
	num = 1
	tmp_time = 0.0
	for packet in pcap:
		if packet.haslayer(IP):
			# this is a IP packet
			op_code, proto = save_iphdr(packet,attack_id,pkt_num,attack_info[0],attack_info[1])
		else:
			# other prtocal type TODO
			op_code, proto = 0,'0_0_0'
			pass

		if op_code != 0:
			#insert into `state` table
			next_1 = pkt_num + 1 		
			data = [attack_id, pkt_num, op_code, proto, next_1, 0]
			dbconn.insert('`state`','attack_id, pkt_num, op_code,' + \
				'proto, next_1, next_2',data)
			#insert into `timestamp` table
			delta_time = packet.time - tmp_time
			tmp_time = packet.time
			data = [attack_id, pkt_num, int(delta_time), int((delta_time - int(delta_time))* 1000000)]
			dbconn.insert('timestamp','attack_id, pkt_num, delta_sec, delta_usec', data)
			# increase pkt_num
			pkt_num = pkt_num + 1
			print 'package ',num,' is stored'
		else:
			print 'package ',num,' is a useless packet'
			pass
		num = num + 1
	data = [attack_id, pkt_num, -1]
	dbconn.insert('`state`','attack_id, pkt_num, next_1', data)
	print 'store finished'
	
	return attack_id

if __name__ == '__main__':
	file = sys.argv[1]
	rawPcap = rdpcap("../pcap_flow/" + file)

	#sourceIP = raw_input('input the source IP: ')
	#dstIP = raw_input('input the dst IP: ')
	attack_name = raw_input('input the attack_name: ')
	plat_info = raw_input('input the plat_info: ')
	target_info = raw_input('input the target_info: ')
	proto = raw_input('input the proto: ')
	feedback = raw_input('input the feedback(1 for yes,0 for no): ')
	sourceIP = '192.168.233.128'
	dstIP = '192.168.233.138'
	attack_info = [sourceIP,dstIP,attack_name,plat_info,target_info,proto]
	
	print save_packet(rawPcap, attack_info)

