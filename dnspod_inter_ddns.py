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


dnspod_username = 'your username'
dnspod_password = 'your password'
dnspod_domains = [
	{
		'domain'		:	'example.com',
		'sub_domain'	:	['@', '*']
	}
]

_dnspod_api = 'https://www.dnspod.com/api/'
_dnspod_myip = '127.0.0.1'
_dnspod_cookie = None


def api_call(api):
	api_url = _dnspod_api + api

	if api == 'auth':
		return api_url + '?email=' + dnspod_username + '&password=' + dnspod_password
	elif api == 'records':
		return api_url + '/'


def url_read(url, postdata = None, method = None):
	result = None

	print(url)

	try:
		req = urllib2.Request(url, data = postdata)
		req.add_header('Content-type', 'application/json')
		if not method is None:
			req.get_method = lambda: method
		if not _dnspod_cookie is None:
			req.add_header('Cookie', _dnspod_cookie)
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


def dnspod_record_modify(domain, record_id, postdata):
	modify_status = url_read('{0}{1}/{2}'.format(api_call('records'), domain, record_id), json.dumps(postdata), 'PUT')
	print(modify_status)
	if not modify_status is None:
		modify_result = json.loads(modify_status)
		print(postdata['sub_domain'] + '.' + domain + ' Change IP: ' + postdata['value'])
		print(modify_result['message'])


if __name__ == '__main__':
	print('My IP is: ' + get_myip())
	if dnspod_login():
		for domain in dnspod_domains:
			records = dnspod_records(domain['domain'])
			for record in records:
				if record['sub_domain'] in domain['sub_domain']:
					if record['record_type'] == 'A' or record['record_type'] == 'AAAA':
						if record['value'] != _dnspod_myip:
							postdata = {
								'sub_domain'	:	record['sub_domain'],
								'area'			:	'0',
								'record_type'	:	record['record_type'],
								'value'			:	_dnspod_myip,
								'ttl'			:	record['ttl']
							}
							dnspod_record_modify(domain['domain'], record['id'], postdata)
