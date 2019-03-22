# -*- coding: utf-8 -*-
# @Date    : 2018-03-29 14:12:54
# @Author  : Wangyue 
# @Link    : http://example.org
# @Version : $1.0$

from xml.dom.minidom import Document

def write2Xml(filename):
	doc = Document()
	#root element
	threatSignature = doc.createElement('threatSignature')
	doc.appendChild(threatSignature)

	#first layer
	layer1 = ['ThreatProperties','Variables','state']

	for e in layer1:
		threatSignature.appendChild(doc.createElement(e))

	#second layer	
	layer2Properties = ['name','execDesc','engineDesc','id','style','protocal']
	for i in range(len(layer2Properties)):
		threatSignature.childNodes[0].appendChild(doc.createElement(layer2Properties[i]))
		threatSignature.childNodes[0].childNodes[i].setAttribute('value','')

	VariablesName = ['sourceMac','destMac','sourceIP','destIP','sourcePort','destPort']
	for i in range(6):
		threatSignature.childNodes[1].appendChild(doc.createElement('NamedVar'))
		threatSignature.childNodes[1].childNodes[i].setAttribute('name', VariablesName[i])
		threatSignature.childNodes[1].childNodes[i].setAttribute('display', '')
		threatSignature.childNodes[1].childNodes[i].setAttribute('type', '')
		threatSignature.childNodes[1].childNodes[i].setAttribute('value', '')

	stateName = ['1','2']
	for i in range(len(stateName)):
		threatSignature.childNodes[2].appendChild(doc.createElement('for'))
		threatSignature.childNodes[2].childNodes[i].setAttribute('index',stateName[i])
	
	for i in range(len(stateName)):
		threatSignature.appendChild(doc.createElement('Output'))
		output = threatSignature.childNodes[i+3]
		output.setAttribute('Index',stateName[i])
		output.setAttribute('Feedback','False')
		output.appendChild(doc.createElement('Ethernet'))
		output.childNodes[0].setAttribute('srcMac','')
		output.childNodes[0].setAttribute('dstMac','')
		output.childNodes[0].setAttribute('ethType','')

		if True:#hasIP()
			output.childNodes[0].appendChild(doc.createElement('IP'))
			ip = output.childNodes[0].childNodes[0]
			ip.setAttribute('version','')
			ip.setAttribute('TypeofService','')
			ip.setAttribute('Identification','')
			ip.setAttribute('FragmentOffset','')
			ip.setAttribute('TTL','')
			ip.setAttribute('Protocol','')
			ip.setAttribute('srcIP','')
			ip.setAttribute('destIP','')
			ip.setAttribute('flags','')

			if True: #hasudp()
				ip.appendChild(doc.createElement('tcp'))
				tcp = ip.childNodes[0]
				tcp.setAttribute('srcport','')
				tcp.setAttribute('dstport','')
				tcp.setAttribute('seq','')
				tcp.setAttribute('ack','')
				tcp.setAttribute('flags','')
				tcp.setAttribute('window','')
				tcp.setAttribute('dataofs','')
				tcp.setAttribute('reserved','')
				tcp.setAttribute('urgptr','')
				tcp.setAttribute('options','')
				tcp.setAttribute('payload','')


	with open(filename, 'w') as f:
		f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))

if __name__ == '__main__':
	write2Xml('1.xml')