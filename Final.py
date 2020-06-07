#!/usr/bin/python3
#Yasin Pesdereli

import os , sys , requests , uuid , hashlib
from multiprocessing import Process
from multiprocessing import Pool

#Q1)Create a new child process with syscall and print its PID

print("PID of the script : ", os.getpid())
child = os.fork()
if child == 0:
	print("PID of the child process : ", os.getpid())
	os._exit(0)
child_proc_exit_status = os.wait()
print("child exit with status: ", child_proc_exit_status[1])	
print("Current process id : " , os.getpid())
#Q2)With the child process download the files via given URL list

url =['http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg' ,
'https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png',
'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg',
'http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg',
'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg']

def download_file ( url , file_name= None ):
	r = requests.get ( url , allow_redirects= True )
	file = file_name if file_name else str (uuid.uuid4())
	open ( file , 'wb' ) .write ( r.content )
	return file
downloaded_files = []    
for i in range(len(url)) :
	downloaded_files.append(download_file(url[i]))
	
half_size = int(len(downloaded_files))
print(downloaded_files)  ##	in this list we keep the downloaded files names for next process

#Q3)How can you avoid the orphan process situation with the syscall ?
#os.wait() , os.kill(PID,-15) , os.kill(PID,-9) 

#Q4)Control duplicate files within the downloaded files of your python code.You should do it by using multiprocessing techniques.

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
print(os.getpid())

a = []
def pool_handler():
	p = Pool(4) #Number of processes to work 
	a.append(p.map(md5_hash, downloaded_files))
	return a

hashes2d = pool_handler()
hashes = []
for i in range(len(hashes2d[0])):
	hashes.append(hashes2d[0][i])
print("hash values : " , hashes)
my_dict = {i:hashes.count(i) for i in hashes}	
for ha, counts in my_dict.items():				#load them in to directory with the occurance counts	
	print(ha, ' occurs ', counts , ' times')		#printing the hash name and its occurance counts



