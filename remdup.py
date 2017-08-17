import os
import requests
import sys, tty, termios
import pickle

def list_files(directory, includeSubdirs = True):
    ext = ('mkv','avi','mp4')
    r = []
    if includeSubdirs:
            subdirs = [x[0] for x in os.walk(directory)]
            for subdir in subdirs:
                files = os.walk(subdir).next()[2]
                if (len(files) > 0):
                    for f in files:
                        if f.split('.')[-1:][0] in ext:
                                r.append([f,subdir])
    else:
           files = os.walk(directory).next()[2]
           if (len(files) > 0):
                    for f in files:
                        if f.split('.')[-1:][0] in ext:
                                r.append([f,directory])
    return r

def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

ex = list_files('/Volumes/Multimedia/Movies',False)
up = list_files('/Volumes/Multimedia/UPLOADS')
up_files = [x[0] for x in list_files('/Volumes/Multimedia/UPLOADS')]
ex_files = [x[0] for x in list_files('/Volumes/Multimedia/Movies',False)]

i = 0
#print ex_files
#print up_files
for f in up_files:
	if f in ex_files:
		print f
		upFileName = os.path.join(up[up_files.index(f)][1],f)
		exFileName = os.path.join(ex[ex_files.index(f)][1], ex_files[ex_files.index(f)])
		#print upFileName + ' = ' + str(os.stat(upFileName).st_size)
		if os.stat(upFileName).st_size == os.stat(exFileName).st_size:
			i += 1
			#print upFileName
			#os.remove(upFileName)
print i
