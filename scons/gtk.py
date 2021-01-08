# SCONS tools to detect GTK on Windows and Linux
# We assume 'pkg-config' is available on the PATH.

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

def generate(env):
	"""
	Detect GTK settings and add them to the environment.
	"""
	try:
		cmd = ['pkg-config','--cflags','--libs','gtk+-2.0','gmodule-2.0']
		old_env = env.Clone()
		env.ParseConfig(cmd)
		print "LIBPATH:",env.get('LIBPATH')
		env['GTK_CPPPATH'] = env.get('CPPPATH') or []
		env['GTK_LIBPATH'] = env.get('LIBPATH') or []
		env['GTK_LIBS'] = env.get('LIBS') or []
		env['GTK_LINKFLAGS'] = env.get('LINKFLAGS') or []

		for i in ['LIBS','LIBPATH','CPPPATH','LINKFLAGS']:
			if old_env.get(i) is None:
				if env.has_key(i):
					del env[i]
			else:
				env[i] = old_env[i]

		env['HAVE_GTK'] = True

	except Exception,e:
		print "Checking for GTK... not found! (%s)" % str(e)
		env['HAVE_GTK'] = False

def exists(env):
	"""
	Make sure this tool exists (and that header files are installed).
	"""
	if not subprocess.call('pkg-config gtk+-2.0 gmodule-2.0 --exists'):
		return True
	return False

# vim: set ts=4 noexpandtab:

