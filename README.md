Dnspod International DDNS
=================

Dnspod International Dynamic DNS written in Python

##How to use

###Used in command line

1. Add your domain A record on Dnspod.com
2. Download [dnspod_inter_ddns.py](https://raw.github.com/jenson-shi/dnspod_inter_ddns/master/dnspod_inter_ddns.py)
3. Modify (dnspod_username), (dnspod_password) and (dnspod_domains) to yours
	* dnspod_domains support multi-domain
4. Make the script executable on Unix like system(Linux, Mac OS X, etc.)
	* chmod a+x dnspod_inter_ddns.py
5. You can run script once
	* ./dnspod_inter_ddns.py
6. Of course, also can run in daemon mode. In daemon mode will check IP every 5 minutes
	* ./dnspod_inter_ddns.py daemon

###Used in your program

* Copy dnspod_inter_ddns.py to your program directory
* Licensed under the [MIT License](http://opensource.org/licenses/mit-license.php)

		from dnspod_inter_ddns import dnspod_ddns
	
		dnspod_ddns()

##Links

[中文使用说明](http://shixf.com/dnspod-inter-ddns-cn/)

[Visit Page](http://shixf.com/dnspod-inter-ddns/)