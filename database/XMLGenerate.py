# -*- coding: utf-8 -*-
# @Date    : 2018-03-29 14:12:54
# @Author  : Wangyue 
# @Link    : http://example.org
# @Version : $1.0$

from xml.dom.minidom import Document
import dbconn

def write2Xml(attack_id):
	doc = Document()
	#index table info
	condition = {'attack_id':attack_id}
	indexinfo = dbconn.query('`index`','attack_name,plat_info,target_info,proto,src_ip,dst_ip,ts_type',condition)
	indexinfo = indexinfo[0]
	#root element
	threatSignature = doc.createElement('threatSignature')
	doc.appendChild(threatSignature)

	#first layer
	layer1 = ['ThreatProperties','Variables','Dataflow']

	for e in layer1:
		threatSignature.appendChild(doc.createElement(e))

	#second layer	ThreatProperties
	ThreatProperties = ['name','execPlat','enginePlat','protocal']
	ThreatValue = [indexinfo[0],indexinfo[1],indexinfo[2],indexinfo[3]]
	for i in range(len(ThreatProperties)):
		threatSignature.childNodes[0].appendChild(doc.createElement(ThreatProperties[i]))
		threatSignature.childNodes[0].childNodes[i].setAttribute('value',ThreatValue[i])

	#second layer	Variables
	VariablesName = ['sourceIP','destIP','ts_type']
	VariablesValue = [indexinfo[4],indexinfo[5],indexinfo[6]]
	for i in range(len(VariablesName)):
		threatSignature.childNodes[1].appendChild(doc.createElement(VariablesName[i]))
		threatSignature.childNodes[1].childNodes[i].setAttribute('value',VariablesValue[i])

	stateinfo = dbconn.query('`state`','pkt_num,op_code,proto,next_1',condition)
	for i in range(len(stateinfo)):
		threatSignature.childNodes[2].appendChild(doc.createElement('package'))
		package = threatSignature.childNodes[2].childNodes[i]
		package.setAttribute('state',str(stateinfo[i][0]))
		package.setAttribute('nextstate',str(stateinfo[i][3]))
		package.setAttribute('proto',stateinfo[i][2])
		package.setAttribute('op_code',str(stateinfo[i][1]))
		
		if stateinfo[i][2] == '' or stateinfo[i][2] == None:
			break
		packageProtocal = stateinfo[i][2].split('_')
		if packageProtocal[0] == '0800':
			#IP
			package.appendChild(doc.createElement('IP'))
			ip = package.childNodes[0]
			condition = {'attack_id':attack_id, 'pkt_num': stateinfo[i][0]}
			ipinfo = dbconn.query('`iphdr`','ip_version,ip_tos,ip_id,ip_flags,ip_frag,ip_ttl,ip_proto',condition)[0]
			ip.setAttribute('version',str(ipinfo[0]))
			ip.setAttribute('TypeofService',str(ipinfo[1]))
			ip.setAttribute('Identification',str(ipinfo[2]))
			ip.setAttribute('FragmentOffset',str(ipinfo[4]))
			ip.setAttribute('TTL',str(ipinfo[5]))
			ip.setAttribute('Protocol',str(ipinfo[6]))
			ip.setAttribute('flags',str(ipinfo[3]))

			if packageProtocal[1] == '6':
				# TCP
				ip.appendChild(doc.createElement('TCP'))
				tcp = ip.childNodes[0]
				tcpinfo = dbconn.query('`tcphdr`','tcp_sport,tcp_dport,tcp_flags,tcp_seq,tcp_ack,tcp_win,dataofs,reserved,urgptr,options',condition)[0]
				tcp.setAttribute('srcport',str(tcpinfo[0]))
				tcp.setAttribute('dstport',str(tcpinfo[1]))
				tcp.setAttribute('seq',str(tcpinfo[3]))
				tcp.setAttribute('ack',str(tcpinfo[4]))
				tcp.setAttribute('flags',str(tcpinfo[2]))
				tcp.setAttribute('window',str(tcpinfo[5]))
				tcp.setAttribute('dataofs',str(tcpinfo[6]))
				tcp.setAttribute('reserved',str(tcpinfo[7]))
				tcp.setAttribute('urgptr',str(tcpinfo[8]))
				tcp.setAttribute('options',str(tcpinfo[9]))

				if packageProtocal[2] == '1':
					# PAYLOAD
					tcp.appendChild(doc.createElement('Payload'))
					payload = tcp.childNodes[0]
					payloadinfo = dbconn.query('`payload`','data',condition)[0]
					payload.setAttribute('data',str(payloadinfo[0]))
				

	text = doc.toprettyxml(indent='\t', encoding='utf-8')
	return text
	# with open('1.xml', 'w') as f:	
	# 	f.write(text)

if __name__ == '__main__':
	write2Xml(1)