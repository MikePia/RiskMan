import os
from shutil import copyfile
import subprocess
import zipfile
import shutil

if os.path.exists('build'):
    shutil.rmtree('build')

if os.path.exists('dist'):
    shutil.rmtree('dist')


command = 'python setup.py sdist'
os.system(command)

try:
    command = 'python setup.py install'
    os.system(command)
except:
    print("FAIL")
    exit()



command = 'pyinstaller  --windowed --onefile -n RiskMan.exe  .\RiskMan.exe.spec'
ret = os.system(command)
if ret != 0:
    print('pyinstaller completed with errocode: ', ret)
    exit()
idest = 'dist/Riskman/images'
isrc = 'riskman/images'
if not os.path.exists(idest):
    os.makedirs('dist/Riskman/images')

if not os.path.exists(os.path.join(idest, 'choose-font.png')):
    source = [os.path.join(isrc, 'choose-font.png'),
              os.path.join(isrc, 'money-bag.png'),
              os.path.join(isrc, 'riskMask.png'),
              os.path.join(isrc, 'stop-train.png')]
    destination =[os.path.join(idest, 'choose-font.png'),
              os.path.join(idest, 'money-bag.png'),
              os.path.join(idest, 'riskMask.png'),
              os.path.join(idest, 'stop-train.png')]

    for src, dst in zip(source, destination):
        copyfile(src, dst)

if os.path.exists('dist/RiskMan.exe'):
    if os.path.exists('dist/Riskman/Riskman.exe'):
        os.remove('dist/Riskman/Riskman.exe')
    os.rename('dist/Riskman.exe', 'dist/Riskman/Riskman.exe')


def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print ('zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname))
            zf.write(absname, arcname)
    zf.close()

if os.path.exists('dist/Riskman'):
    zip("dist/Riskman", "dist/Riskman")