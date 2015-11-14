#!/usr/bin/python

import subprocess
import re
import platform
import os
import sys

class NicInfo():
	def __init__(self):
		self.name = ""
		self.ip = ""
		self.mac = ""
		self.netmask = ""
		self.default_gateway = ""
		self.dns = ""

def get_first_data():
	tmp_file = open('/tmp/g.log','w')
	subprocess.call(['ifconfig'], stdout=tmp_file)
	tmp_file = open('/tmp/g.log','r')
	ifaces = []
	line_str = ""
	for line_raw in tmp_file:
		line = line_raw.rstrip()
		if len(line) > 0:
			line = line + '\n'
                	line_str = line_str + line
        	else:
                	ifaces.append(line_str)
                	line_str = ""
	return ifaces[0]

def get_all_info():
	platform_name = platform.system()
	ipstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
	macstr = '([0-9A-F]{2}:){5}[0-9A-F]{2}'
	maskstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
	ethstr = '\d+'
	emstr = '\d+'
	nic_info_list = []
	if platform_name == "Darwin" or platform_name == "Linux":
		#ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
		#output = ipconfig_process.stdout.read()
		output = get_first_data()
		ip_pattern = re.compile('(inet addr:%s)' % ipstr)
		mac_pattern = re.compile('(HWaddr %s)' % macstr)
		mask_pattern = re.compile('(Mask:%s)' % maskstr)
		eth_pattern = re.compile("(eth%s)" % ethstr)
		em_pattern = re.compile("(em%s)" % emstr)
		
		iplist = []
		maclist = []
		masklist = []
		ethlist = []
		pattern = re.compile(ipstr)
		for ipaddr in re.finditer(ip_pattern, str(output)):
			ip = pattern.search(ipaddr.group())
			if ip.group() != "127.0.0.1":
				iplist.append(ip.group())
		
		pattern = re.compile(macstr)
		for macaddr in re.finditer(mac_pattern, str(output)):
			mac = pattern.search(macaddr.group())
			maclist.append(mac.group())

		pattern = re.compile(maskstr)
		for netmask in re.finditer(mask_pattern, str(output)):
			mask = pattern.search(netmask.group())
			masklist.append(mask.group())

		pattern = re.compile(ethstr)
		for ethname in re.finditer(eth_pattern, str(output)):
			ethlist.append(ethname.group())
		
		## maybe this is a dell server, it's nic name start with em string.
		if len(ethlist) == 0:
			for emname in re.finditer(em_pattern, str(output)):
				ethlist.append(emname.group())
		
		os.system("ip route show > /tmp/route.log")
		default_gateway = "0.0.0.0"	
		tmp_file = open("/tmp/route.log", "r")
		for line_raw in tmp_file:
			start_index = line_raw.find("default via")
			if start_index == -1:
				continue
			sub_str = line_raw[start_index:]
			sub_str_list = sub_str.split(" ")
			default_gateway = sub_str_list[2]

		f = open("/etc/resolv.conf", "r+")
		dns = ""
		for line in f.readlines():
			if line.find("nameserver") != -1:
				dns_list = line.split(' ')
				dns = dns_list[1].strip('\n')
				break
		nic_info_list = []
		for i in range(len(ethlist)):
			nic_info = NicInfo()
			nic_info.name = ethlist[i]
			if len(iplist) > 0:
				nic_info.ip = iplist[i]
			nic_info.mac = maclist[i]
			if len(masklist) > 0:
				nic_info.netmask = masklist[i]
			nic_info.default_gateway = default_gateway
			nic_info.dns = dns
			
			nic_info_list.append(nic_info)
		return nic_info_list

if __name__ == '__main__':
	nic_list = get_all_info()
	nic_info = NicInfo()
	if len(nic_list) > 0:
		nic_info = nic_list[0]
	print "name: " + nic_info.name
	print "ip: " + nic_info.ip
	print "mac: " + nic_info.mac
	print "netmask: " + nic_info.netmask
	print "default_gateway: " + nic_info.default_gateway
	print "dns: " + nic_info.dns

