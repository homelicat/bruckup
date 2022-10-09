#!/usr/bin/python3
import hashlib,os,shutil

#defines
localpath="local"
backpath="backup"
ignorepath="ignore.txt"
hashpath="hash.txt"

#prepare backup directory
shutil.rmtree(backpath)
os.mkdir(backpath)

#load ignore list
ignores=list()
with open(ignorepath,"r") as f:
	for line in f:
		ignores.append(line)

#scan local for files
for dirpath, dirnames, filenames in os.walk(localpath):
	#check for ignores
	isign=False
	for ign in ignores:
		if dirpath[:len(ign)]==ign:
			isign=True
	#do if not ignores
	if not isign:
		for filename in filenames:
			name = os.path.join(dirpath,filename)
			#count new hash
			newhash=0
			with open(name,'rb') as f:
				newhash=hashlib.sha256(f.read()).hexdigest()
			#save new hash
			with open("nhash.txt","a") as f:
				f.write(name+' '+newhash+'\n')
			#search file in old hash
			newa=True
			with open(hashpath,"r") as f:
				for line in f:
					if line[:len(name)+1]==name+' ':
						#check hash
						newa=newhash!=line[len(name)+1:-1]
					else:
						continue
					break
			#backup file
			if newa:
				fname = dirpath.split("/")
				fname[0]=backpath
				for i in range(1,len(fname)):
					fname[i]=fname[i-1]+'/'+fname[i]
					try:
						os.mkdir(fname[i])
					except:
						pass
				shutil.copy(name,fname[-1]+'/'+filename)
#finish hash list
os.rename("nhash.txt",hashpath)