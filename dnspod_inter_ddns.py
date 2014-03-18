#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
  Copyright (c) 2014 Jenson Shi <jenson.shixf@gmail.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
  
        http://shixf.com/
'''

import urllib
import urllib2
import json

dnspod_api = 'https://www.dnspod.com/api/'
dnspod_username = 'your username'
dnspod_password = 'your password'
dnspod_domain = [
	{
		'domain'		:	'example.com',
		'sub_domain'	:	['@', '*']
	}
]

_dnspod_myip = '127.0.0.1'
_dnspod_cookie = None


def api_call(api):
	api_url = dnspod_api + api

	if api == 'auth':
		return api_url + '?email=' + dnspod_username + '&password=' + dnspod_password
	elif api == 'records':
		return api_url + '/'


def url_read(url, postdata = None):
	result = None

	print(url)

	try:
		req = urllib2.Request(url, data = postdata)
		if not _dnspod_cookie is None:
			req.add_header('Cookie', _dnspod_cookie)
			print('Add Cookie' + _dnspod_cookie)
		urlItem = urllib2.urlopen(req, timeout = 10)
		result = urlItem.read()
		urlItem.close()
	except urllib2.URLError as e:
		print(e.reason)
	except urllib2.HTTPError as e:
		print(e.reason)
	except:
		print('UnknownError')

	return result


def get_myip():
	myip = url_read('http://shixf.com/api/getip')
	if not myip is None:
		global _dnspod_myip
		if myip != _dnspod_myip:
			_dnspod_myip = myip
			return _dnspod_myip
	return None


def dnspod_login():
	login_status = url_read(api_call('auth'))
	if not login_status is None:
		global _dnspod_cookie
		_dnspod_cookie = urllib.urlencode(json.loads(login_status))
		return True
	return False
	

def dnspod_records(domain):
	records = None
	records_status = url_read(api_call('records') + domain)
	if not records_status is None:
		records = json.loads(records_status)
		if type(records) != type(list()):
			if type(records) == type(dict()):
				print(records['error'])
			else:
				print('UnknownError')
	return records


def dnspod_record_modify(domain, record_id):
	postdata = {
		'sub_domain'	:	'test',
		'area'			:	'default',
		'record_type'	:	'A',
		'value'			:	'2.0.1.2'
	}


if __name__ == '__main__':
	print('My IP is: ' + get_myip())
	if dnspod_login():
		records = dnspod_records('example.com')
		for record in records:
			print('status = {0}'.format(record['status']))
			print('area = {0}'.format(record['area']))
			print('value = {0}'.format(record['value']))
			print('id = {0}'.format(record['id']))
			print('record_type = {0}'.format(record['record_type']))
			print('sub_domain = {0}'.format(record['sub_domain']))
			print('ttl = {0}'.format(record['ttl']))
			print('updated_on = {0}'.format(record['updated_on']))
			print('domain_id = {0}'.format(record['domain_id']))
			print('')
