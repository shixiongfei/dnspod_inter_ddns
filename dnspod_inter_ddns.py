#!/usr/bin/env python
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
import sys
import time
import signal


dnspod_username = 'your_username'
dnspod_password = 'your_password'
dnspod_domains = [
	{
		'domain'		:	'example.com',
		'sub_domain'	:	['@', '*']
	}
]
dnspod_daemon = 300


_dnspod_api = 'https://www.dnspod.com/api/'
_dnspod_myip = '127.0.0.1'
_dnspod_cookie = None
_dnspod_lasterror = {
	'error': 'Success',
	'message': ''
}


def api_call(api):
	api_url = _dnspod_api + api

	if api == 'auth':
		return api_url + '?email=' + dnspod_username + '&password=' + dnspod_password
	elif api == 'records':
		return api_url + '/'


def url_read(url, postdata = None, method = None):
	result = None

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
		_dnspod_lasterror['error'] = 'URLError'
		_dnspod_lasterror['message'] = e.reason
	except urllib2.HTTPError as e:
		_dnspod_lasterror['error'] = 'HTTPError'
		_dnspod_lasterror['message'] = e.reason
	except:
		_dnspod_lasterror['error'] = 'FetchError'
		_dnspod_lasterror['message'] = 'HTTP data fetch error.'

	return result


def get_myip():
	myip = url_read('http://shixf.com/api/getip')
	if not myip is None:
		global _dnspod_myip
		if myip != _dnspod_myip:
			_dnspod_myip = myip
			return _dnspod_myip
	return None


def output_lasterror():
	print('{0} : {1}'.format(_dnspod_lasterror['error'], _dnspod_lasterror['message']))


def dnspod_login():
	login_status = url_read(api_call('auth'))
	if not login_status is None:
		auth = json.loads(login_status)
		if not auth.has_key('error'):
			global _dnspod_cookie
			_dnspod_cookie = urllib.urlencode(auth)
			return True
		else:
			_dnspod_lasterror['error'] = 'DnspodError'
			_dnspod_lasterror['message'] = auth['error']

	return False
	

def dnspod_records(domain):
	records = None
	records_status = url_read(api_call('records') + domain)
	if not records_status is None:
		records = json.loads(records_status)
		if type(records) != type(list()):
			_dnspod_lasterror['error'] = 'DnspodError'
			if type(records) == type(dict()):
				_dnspod_lasterror['message'] = records['error']
			else:
				_dnspod_lasterror['message'] = 'UnknownError'
	return records


def dnspod_record_modify(domain, record_id, postdata):
	modify_status = url_read('{0}{1}/{2}'.format(api_call('records'), domain, record_id), json.dumps(postdata), 'PUT')
	if not modify_status is None:
		modify_result = json.loads(modify_status)
		_dnspod_lasterror['error'] = 'Success'
		_dnspod_lasterror['message'] = '{0}.{1} has changed IP to {2}, {3}'.format(postdata['sub_domain'], domain, 
																				postdata['value'], modify_result['message'])
		return True
	return False



def dnspod_ddns():
	get_myip()

	if dnspod_login():
		for domain in dnspod_domains:
			records = dnspod_records(domain['domain'])
			if not records is None:
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
								output_lasterror()
			else:
				output_lasterror()
	else:
		output_lasterror()


def _signal_handler(signal, frame):
	print 'Exiting...'
	sys.exit(0)

if __name__ == '__main__':
	if len(sys.argv) >= 2 and sys.argv[1] == 'daemon':
		signal.signal(signal.SIGINT, _signal_handler)
		print('You may pressed Ctrl + C to exit.')
		while(True):
			dnspod_ddns()
			time.sleep(dnspod_daemon)
	else:
		dnspod_ddns()
