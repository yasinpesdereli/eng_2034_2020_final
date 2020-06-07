#!/usr/bin/python3
#Yasin Pesdereli

import os , sys , requests , uuid , hashlib
from multiprocessing import Process
from multiprocessing import Pool

files = os.listdir()

def md5_hash(filename) : 
	hashmd5 = hashlib.md5()
	file = open(filename, "rb")
	content = file.read()
	hashmd5.update(content)
	digest = hashmd5.hexdigest()
	print("Worker process id for {0}: {1}".format(filename, os.getpid()))	
	return(digest)

'''
child_proc_exit_status = os.wait()
print("child exit with status: ", child_proc_exit_status[1])
'''

a = []
def pool_handler():
	p = Pool(4) #Number of processes to work 
	a.append(p.map(md5_hash, files))
	return a

hashes2d = pool_handler()
hashes = []
for i in range(len(hashes2d[0])):
	hashes.append(hashes2d[0][i])
my_dict = {i:hashes.count(i) for i in hashes}	
for ha, counts in my_dict.items():				#load them in to directory with the occurance counts	
	print(ha, ' occurs ', counts , ' times')		#printing the hash name and its occurance counts


