#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-01 16:33:10
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import pymysql

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
				statement += '\'' + str(d) + '\','
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
			print condition
			if condition == {}:
				sql = 'SELECT ' + column + ' FROM ' + table + ';'
			else:
				sql = 'SELECT ' + column + ' FROM ' + table + ' WHERE '
				useAnd = False
				for key,value in condition.iteritems():
					if useAnd == False:
						useAnd = True
						sql += key + ' = ' + value
					else:
						sql += ' AND ' + key + ' = ' + value
				sql += ';'
				print sql
			
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