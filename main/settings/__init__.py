# Settings loader file.

import os, sys, glob, re, socket

pwd = os.path.dirname(__file__)
PPATH = os.path.join(pwd,"../..")
# This if fucking ugly!
sys.path.insert(0,os.path.normpath(os.path.join(PPATH,'.dev/')))

# Open and compile each file
machine_name = re.sub('[^A-z0-9._]', '_', socket.gethostname())
for s_file in ['00-base','10-apps','20-email','local',machine_name]:
  try:
    f = 'main/settings/%s.py'%s_file
    exec(compile(open(os.path.abspath(f)).read(), f, 'exec'), globals(), locals())
  except IOError:
    print "Setting file missing. We looked here: %s"%f
