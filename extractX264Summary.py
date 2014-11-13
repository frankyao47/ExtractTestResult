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
	if os.path.isfile(path) and os.path.splitext(path)[1] == '.log':
		yuvFileList.append(path)
	elif os.path.isdir(path):
		files = os.listdir(path)
		for f in files:
			if os.path.isdir(os.path.join(path, f)):
				yuvFileList.extend(getYuvFileList(os.path.join(path, f)))
			elif os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1] == '.log':
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
	while True:
		dataline = fin.readline()
		if dataline.startswith("x264 [info]: PSNR Mean"):
			PSNR = dataline.split()[4:8]
			YPSNR, UPSNR, VPSNR, Avg = [info.split(':')[1] for info in PSNR]
			#print PSNR

			fin.readline()
			dataline = fin.readline()

			Time, Bitrate = dataline.split()[3], dataline.split()[5]
			#print Time, Bitrate

			info = ','.join([fileName, Bitrate, YPSNR, UPSNR, VPSNR, Time])
			break

	fout.write(info)
	fout.write('\n')

	fin.close()


def writeCmd(fout):
	yuvFileList = searchYuvFile([os.getcwd()]) #it must be type 'list'

	#print yuvFileList
	title = ','.join(["Filename", "Bitrate", "YPSNR", "UPSNR", "VPSNR", "FPS"])
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
	filename = "x264result"
	curTime = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
	suffix = ".csv"

	fout = file(filename + '_' + curTime + suffix, 'wb')
	writeCmd(fout)

if __name__ == '__main__':
	main()
