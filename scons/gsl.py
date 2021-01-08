# SCONS tools to detect GSL on Windows and Linux
# For windows, we assume that GSL-1.11 for MinGW is
# being used, see here:
# http://ascendwiki.cheme.cmu.edu/Binary_installer_for_GSL-1.11_on_MinGW
# For Linux, we assume standard Linux packages are used,
# and hence that gsl-config will be present on the PATH.

import os, os.path, platform, subprocess
from SCons.Script import *

munge = lambda s: s

try:
	# if we have access to GetShortPathName, we'll use it...
	import win32api
	def munge1(s):
		s1 = s
		try:
			# we can only munge the path if it actually exists
			s1 = win32api.GetShortPathName(s)
		except:
			# if it doesn't exist, we just return the un-munged path
			pass
		return s1
	munge = munge1 
except:
	pass

def winpath(path):
	"""
	Convert a MSYS path to a native Windows path, so that we can pass values correctly to GCC
	"""
	import subprocess
	import os
	#print "path = %s"%path
	fn = "scons%d" % os.getpid()
	while os.path.exists(fn):
		fn = fn + "0"
	try:
		f = file(fn,"w")
		f.write("#!python\nimport sys\nprint sys.argv[1]")
		f.close()
		#print "FILE %s FOUND? %d"%(fn,os.path.exists(fn))
		p1 = subprocess.Popen(["sh.exe","-c","%s %s"%(fn,path)], stdout=subprocess.PIPE)
		#p1 = subprocess.Popen(["sh.exe","-c","echo hello"], stdout=subprocess.PIPE)
		out = p1.communicate()[0].strip()
		#print "NEW PATH IS '%s'" % out
	except Exception,e:
		print "FAILED: %s"%str(e)
	finally:
		#print "Deleting %s" % fn
		os.unlink(fn)
	return out


# TODO detect if static libs are actually available...

def generate(env):
	"""
	Detect GSL settings and add them to the environment.
	"""
	try:
		if platform.system()=="Windows":
			try:
				import _winreg
				x=_winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
				y= _winreg.OpenKey(x,r"SOFTWARE\gsl")
				BIN,t = _winreg.QueryValueEx(y,"INSTALL_BIN")
				LIB,t = _winreg.QueryValueEx(y,"INSTALL_LIB")
				INCLUDE,t = _winreg.QueryValueEx(y,"INSTALL_INCLUDE")

				env['GSL_CPPPATH'] = [munge(INCLUDE)]
				env['GSL_LIBPATH'] = [munge(LIB)]
				env['HAVE_GSL'] = True		
				env['GSL_STATICLIBS'] = [os.path.join(munge(LIB),"lib%s.a"%i) for i in ["gsl","gslcblas"]]
				env['GSL_LIBS'] = ['gsl']
			except WindowsError:					
				cmd = ['sh.exe','-c','"gsl-config --libs --cflags"']
				env1 = env.Clone()
				env1['CPPPATH'] = None
				env1['LIBPATH'] = None
				env1['LIBS'] = None
				print "RUNNING gsl-config"
				env1.ParseConfig(cmd)
				env['GSL_CPPPATH'] = winpath(env1.get('CPPPATH')[0])
				env['GSL_LIBPATH'] = winpath(env1.get('LIBPATH')[0])
				env['GSL_LIBS'] = env1.get('LIBS')
				env['GSL_STATICLIBS'] = [os.path.normcase(os.path.join(winpath(env1.get('LIBPATH')[0]),"lib%s.a"%i)) for i in ["gsl","gslcblas"]]
				env['HAVE_GSL'] = True						
		else:
			cmd = ['gsl-config','--cflags','--libs']
			old_env = env.Clone()
			env.ParseConfig(cmd)
			env['GSL_CPPPATH'] = env.get('CPPPATH')
			env['GSL_LIBPATH'] = env.get('LIBPATH')

			print "GSL_STATIC =",env.get('GSL_STATIC')

			if env.get('GSL_STATIC'):
				env['GSL_STATICLIBS'] = [os.path.join(env.get('GSL_LIBPATH')[0],"lib%s.a"%i) for i in ["gsl","gslcblas"]]
			else:
				env['GSL_LIBS'] = env.get('LIBS')

			for i in ['LIBS','LIBPATH','CPPPATH']:
				if old_env.get(i) is None:
					if env.has_key(i):
						del env[i]
				else:
					env[i] = old_env[i]

			env['HAVE_GSL'] = True

			# on Ubuntu, remove gslcblas if present 
			# NO... this causes errors, unless we link gslcblas later on.
			#if platform.system()=="Linux":
			#	if platform.dist()[0]=="Ubuntu":
			#		if 'gslcblas' in env['GSL_LIBS']:
			#			env['GSL_LIBS'].remove('gslcblas')

		print "GSL_LIBS =",env.get('GSL_LIBS')
		print "GSL_LIBPATH =",env.get('GSL_LIBPATH')
		print "GSL_CPPPATH =",env.get('GSL_CPPPATH')
		print "GSL_STATICLIBS =",env.get('GSL_STATICLIBS')

	except Exception,e:
		print "Checking for GSL... not found! (%s)" % str(e)
		env['HAVE_GSL'] = False

def exists(env):
	"""
	Make sure this tool exists (and that header files are installed).
	"""
	if platform.system()=="Windows":
		try:
			import _winreg
			x=_winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
			y= _winreg.OpenKey(x,r"SOFTWARE\gsl")
			INCLUDE,t = _winreg.QueryValueEx(y,'INSTALL_INCLUDE')
			return True
		except:
			return False
	else:
		if not subprocess.call('pkg-config libgvc libagraph --exists'):
			return True
		return False

# vim: set ts=4 noexpandtab:

