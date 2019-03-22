#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-29 14:12:54
# @Author  : Wangyue 
# @Link    : http://example.org
# @Version : $1.0$

import xml.etree.cElementTree as ET

def readXML():
	DOMTree = ET.parse("../script/wins_heap.xml")
	root = DOMTree.getroot()
	root = root[0]
	for child in root:
   		print child.tag, child.attrib






if __name__ == '__main__':
	readXML()