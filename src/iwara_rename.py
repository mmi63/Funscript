import os
import glob
import re

files = glob.glob('*')
for i, f in enumerate(files, 1):
  if (f.endswith('.mp4')):
    postfix = '.mp4'
  elif (f.endswith('.funscript')):
    postfix = '.funscript'
  else:
    continue
  pattern = '(?<=\[).*?(?=\])'
  blockList = re.findall(pattern, f)
  if len(blockList) == 0:
    print('Name error: ' + f)
  elif blockList[-1] == 'Source':
    iwaraID = blockList[-2]
    os.rename(f, os.path.join('.', iwaraID + postfix))
  else:
    iwaraID = blockList[-1]
    os.rename(f, os.path.join('.', iwaraID + postfix))
