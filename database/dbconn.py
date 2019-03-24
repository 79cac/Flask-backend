#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-01 16:33:10
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import pymysql
from scapy import *
def connection():
	conn = pymysql.connect(host='127.0.0.1', user='root',\
		passwd='wangyue', db='attack_flow')	
	return conn

def insert(table,column,data):
	try:
		conn = connection()
		with conn.cursor() as cursor:
			statement = ''
			for d in data:
				if type(d) == int:
					statement += str(d) +  ','
				elif type(d) == unicode or type(d) == str:
					statement += '\'' + d + '\','
				else:
					pass
			statement = statement[:-1]
			sql = 'INSERT INTO ' + table + '( ' + \
			column + ') VALUES (' + statement + ');'
			cursor.execute(sql)
			conn.commit()

	except Exception as e:
		print('Error db insert',e)
	else:
		pass
	finally:
		conn.close()

def query(table,column,condition={}):
	try:
		conn = connection()
		with conn.cursor() as cursor:
			if condition == {}:
				sql = 'SELECT ' + column + ' FROM ' + table + ';'
			else:
				sql = 'SELECT ' + column + ' FROM ' + table + ' WHERE '
				useAnd = False
				for key,value in condition.iteritems():
					if type(value) == int:
						value = str(value)
					else:
						value = '\'' + value + '\''
					if useAnd == False:
						useAnd = True
						sql += key + ' = ' + value
					else:
						sql += ' AND ' + key + ' = ' + value
				sql += ';'
			
			cursor.execute(sql)
			results = cursor.fetchall()
			return results
	except Exception as e:
		print('Error db query',e)
	else:
		pass
	finally:
		conn.close()

def delete(table, column, data):
	try:
		conn = connection()
		with conn.cursor() as cursor:
			sql = 'DELETE FROM ' + table + ' WHERE ' + column \
			+ '=' + data + ';'
			cursor.execute(sql)
			conn.commit()
	except Exception as e:
		print('Error db delete',e)
	else:
		pass
	finally:
		conn.close()

def update(table, data, condition={}):
	try:
		conn = connection()
		with conn.cursor() as cursor:
			statement = ''
			for key,value in data.iteritems():
				if type(value) == int:
					value = str(value)
				else:
					value = '\'' + value + '\''
				statement += key + ' = ' + value + ','
			statement = statement[:-1]
			wherestatement = ''
			if condition != {}:
				useAnd = False
				for key,value in condition.iteritems():
					if type(value) == int:
						value = str(value)
					else:
						value = '\'' + value + '\''
					if useAnd == False:
						useAnd = True
						wherestatement += ' WHERE ' + key + ' = ' + value
					else:
						wherestatement += ' AND ' + key + ' = ' + value
			sql = 'UPDATE ' + table + ' SET ' + statement + wherestatement + ';'			
			cursor.execute(sql)
			conn.commit()
	except Exception as e:
		print('Error db query',e)
	else:
		pass
	finally:
		conn.close()