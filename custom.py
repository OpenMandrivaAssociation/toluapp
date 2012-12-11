## BEGIN custom.py

CCFLAGS = ['-I/usr/include/', '-O2', '-ansi']
LIBPATH = ['/usr/lib64', '/usr/lib']
LIBS = ['lua']
tolua_lib = 'tolua++5.1'
shared = True
prefix = '/usr'

## END custom.py

