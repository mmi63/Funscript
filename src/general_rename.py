import os
import glob
import re
import random
import string


def genID():
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(16)]
   return ''.join(randlst)


# replacement list
name_list = []
id_list = []

files = glob.glob('*')
for i, f in enumerate(files, 1):
  if(f.endswith('.mp4')):
    name_list.append(f.removesuffix('.mp4'))
    id_list.append(genID())

for i, f in enumerate(files, 1):
  if(f.endswith('.mp4')):
    suffix = '.mp4'
  elif(f.endswith('.funscript')):
    suffix = '.funscript'
  else:
    continue

  new_name = f
  for i in range(len(name_list)):
    if f == name_list[i] + suffix:
      new_name = id_list[i] + suffix
  os.rename(f, os.path.join('.', new_name))
