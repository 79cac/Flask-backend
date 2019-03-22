#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-20 19:52:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import dbconn

def delete_all(attack_id):

	dbconn.delete('`tcphdr`','attack_id', attack_id)
	dbconn.delete('`iphdr`','attack_id',attack_id)
	dbconn.delete('`state`','attack_id',attack_id)
	dbconn.delete('`payload`','attack_id',attack_id)	
	dbconn.delete('`info`','attack_id',attack_id)
	dbconn.delete('`timestamp`','attack_id',attack_id)
	dbconn.delete('`index`','attack_id',attack_id)


if __name__ == '__main__':
	delete_all('3')