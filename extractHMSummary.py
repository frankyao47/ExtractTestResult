#!/usr/bin/env python

import os
import time
import platform

######################################################################################
#####	get yuv files logic
#####
######################################################################################
def getYuvFileList(path):
	'''
	Return all the .yuv files found from the given path.
	Directory and single file both supported.
	'''
	yuvFileList = []
	if os.path.isfile(path) and os.path.splitext(path)[1] == '.txt':
		yuvFileList.append(path)
	elif os.path.isdir(path):
		files = os.listdir(path)
		for f in files:
			if os.path.isdir(os.path.join(path, f)):
				yuvFileList.extend(getYuvFileList(os.path.join(path, f)))
			elif os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1] == '.txt':
				yuvFileList.append(os.path.join(path, f))
			else:
				pass
	#print yuvFileList
	return yuvFileList

def searchYuvFile(dirList):
	yuvFileList = []
	#print '\n'.join(searchList)
	#print dirList
	for i in dirList:
		yuvFileList.extend(getYuvFileList(i))

	fileWithNoDupes = []
	[fileWithNoDupes.append(i) for i in yuvFileList if not fileWithNoDupes.count(i)] # remove dupes
	return fileWithNoDupes


######################################################################################
#####	write cmd logic
#####
######################################################################################
def writeSubCmd(fout, yuvFile):
	fin = file(yuvFile, 'rb')
	fileName = os.path.basename(yuvFile)
	while not (fin.readline().startswith("SUMMARY")):
		pass

	fin.readline() #title
	dataline = fin.readline()
	
	Bitrate, YPSNR, UPSNR, VPSNR = dataline.split()[2:]
	info = ','.join([fileName, Bitrate, YPSNR, UPSNR, VPSNR])
	#print fileName, Bitrate, YPSNR, UPSNR, VPSNR
	fout.write(info)
	fout.write('\n')

	fin.close()


def writeCmd(fout):
	yuvFileList = searchYuvFile([os.getcwd()]) #it must be type 'list'

	#print yuvFileList
	title = ','.join(["Filename", "Bitrate", "YPSNR", "UPSNR", "VPSNR"])
	fout.write(title)
	fout.write('\n')
	
	for yuvFile in yuvFileList:
		writeSubCmd(fout, yuvFile)	

	fout.close()


######################################################################################
#####	main
#####
######################################################################################
def main():
	filename = "HMresult"
	curTime = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
	suffix = ".csv"

	fout = file(filename + '_' + curTime + suffix, 'wb')
	writeCmd(fout)

if __name__ == '__main__':
	main()
