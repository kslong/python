#!/usr/bin/env python 

'''
                    Space Telescope Science Institute


Synopsis:  
	grid_royal.py root num
	

Description:  

	This is a program that generates commands to run a series of
	python models on Royal

Arguments:  

	None

Returns:
	A new output file 

Notes:
									   
History:
07sep	ksl	Coded


'''

import os
import sys
import glob

def pfcheck(pflist):
	i=0
	pfgood=[]
	while i<len(pflist):
		try:
			f=open(pflist[i],'r')
		except IOError :
			print "This file does not exist:", pflist[i]
		        sys.exit(0)
		lines=f.readlines()
		j=0
		good=1
		while j<len(lines):
			z=lines[j]
			zz=z.split()
			if zz[0][0]!='#':
				if len(zz)<2:
					good=0
				if zz[1]=='$':
					good=0
			j=j+1
		if good==1:
			pfgood=pfgood+[pflist[i]]
		else:
			print 'Dropping: ',pflist[i]
		f.close()
		i=i+1
	return pfgood

def make_pbs(root,pffiles):
	pbsfile='Knox_'+root+'.pbs'
	jobname='Knox_'+root
	runfile='Knox_'+root+'.run'

	f=open(pbsfile,'w')
	f.write('#PBS -N %s\n' % jobname)
	f.write('#PBS -l walltime=%d:00:00\n'% (3*len(pffiles)))
	f.write('#PBS -l mem=1024mb\n')
	f.write('#PBS -M long@stsci.edu\n')
	f.write('#PBS -m a\n')    # Onlly send a message if the job aborts
#	f.write('#PBS -m bea\n')
	f.write('echo -n \"The job\'s unique ID: \"\n')
	f.write('echo $PBS_JOBID1 \n')
	f.write('cd  $PBS_O_WORKDIR\n')
	f.write('pwd\n')
	f.write('%s\n' % runfile)
	f.write('exit 0\n')


	f.close()
	return pbsfile

def make_rfile(root,pffiles):
	runfile='Knox_'+root+'.run'
	working_dir='Dir_'+root

	f=open(runfile,'w')


	# Section with commands to run
	f.write('mkdir %s\n'%working_dir)
	f.write('cd %s\n'%working_dir)
	f.write('Setup_Py_Dir\n')
	i=0
	while i<len(pffiles):
		f.write('cp ../%s .\n' % pffiles[i])
		f.write('py %s\n\n' % pffiles[i])
		i=i+1
	f.write('mv *.pf *.diag *.spec* *.wind_save ../outputs\n')
	f.close()
	os.system('chmod +x '+runfile)


argc=len(sys.argv)

if argc!=3:
	print "usage grid_royal.py root num.per.runfile"
	sys.exit()

root=sys.argv[1]
num=int(sys.argv[2])

pfnames=root+'*pf'

pflist=glob.glob(pfnames)

print pflist

#eliminate any parameter files that do not pass certain simple tests

pfgood=pfcheck(pflist)

print pfgood

msubfile='Knox_'+root+'.msub'
msub=open(msubfile,'w')
msub.write('mkdir outputs\n')

i=0
k=0
while i<len(pfgood):
	imin=i
	imax=min(i+num,len(pfgood))
	pfnow=[]
	while imin<imax:
		pfnow=pfnow+[pfgood[imin]]
		imin=imin+1
	pbsname='%s_%03d'%(root,k)
	print imin,imax,pbsname,pfnow
	make_rfile(pbsname,pfnow)
	pbsfile=make_pbs(pbsname,pfnow)
	msub.write('msub %s\n' % pbsfile)
	k=k+1
	i=i+num
msub.close()
os.system('chmod +x '+msubfile)