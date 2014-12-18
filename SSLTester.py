#!/usr/bin/python
#author: Raithe Davion
#Version: 0.1
#Version Date: 12/17/2014

#change log
##	shell=False supposedly protects against shell injection
## added a check to see if port is open before it runs sslscan and testsslserver.jar

import sys, getopt, argparse, subprocess, socket

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument("ifile", help="input file")
	parser.add_argument("testsslpath", help="path to TestSSLServer.jar")
	parser.add_argument("-p", "--ports", default="443", help="specify ports for scan")
	args = parser.parse_args()
	inputfile = args.ifile
	javaPath = args.testsslpath
   	if args.ports:
   		ports = args.ports
   	else:
   		ports = 443
   	portList = ports.split(",")
	f=open(inputfile, 'r')
	for line in f:
		for port in portList:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((line.replace("\n",""),int(port)))
			if result == 0:
				sslScanCmd = "sslscan --no-failed %s:%s" % (line.replace("\n",""),port)
				sslScanIP = "%s:%s" % (line.replace("\n",""), port)
				javaScanCmd = "java -jar %s %s %s" % (javaPath,line.replace("\n",""),port)
				print sslScanCmd
				sslScanResult = subprocess.Popen(["sslscan", "--no-failed", sslScanIP ], shell=False, stdout=subprocess.PIPE)
				sslScanOutput, err = sslScanResult.communicate()
				print sslScanOutput
				print javaScanCmd
				javaScanResult = subprocess.Popen(["java", "-jar", javaPath, line.replace("\n",""), port], shell=False, stdout=subprocess.PIPE)
				javaScanOutput, err = javaScanResult.communicate()
				print javaScanOutput
			else:
				print "Port %s not open on %s " % (port,line.replace("\n",""))
			
if __name__ == "__main__":
	main(sys.argv[1:])
