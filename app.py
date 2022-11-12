import kivy, os, tempfile, shutil, sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from zipfile import ZipFile
import os.path

PY3K = sys.version_info >= (3, 0)
if PY3K:
  import urllib.request as ulib
  import urllib.parse as urlparse
else:
  import urllib as ulib
  import urlparse

kivy.require('1.9.0')

dict_url = {"MITM":"https://github.com/code404nul/Pie-of-Spies/archive/refs/heads/main.zip"}

def create_folder(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("The new directory is created!")

def unzip(zip_file):

    with ZipFile(zip_file, 'r') as zfile:
        zfile.extractall(path="APP")

def filename_fix_existing(filename):

    dirname = u'.'
    name, ext = filename.rsplit('.', 1)
    names = [x for x in os.listdir(dirname) if x.startswith(name)]
    names = [x.rsplit('.', 1)[0] for x in names]
    suffixes = [x.replace(name, '') for x in names]

    suffixes = [x[2:-1] for x in suffixes
                   if x.startswith(' (') and x.endswith(')')]
    indexes  = [int(x) for x in suffixes
                   if set(x) <= set('0123456789')]
    idx = 1
    if indexes:
        idx += sorted(indexes)[-1]
    return '%s (%d).%s' % (name, idx, ext)


def download(url, out=None):
    outdir = None
    if out and os.path.isdir(out):
        outdir = out
        out = None

    prefix = ".zip"
    (fd, tmpfile) = tempfile.mkstemp(".tmp", prefix=prefix, dir=".")
    os.close(fd)
    os.unlink(tmpfile)

    callback = None

    if PY3K:

        binurl = list(urlparse.urlsplit(url))
        binurl[2] = urlparse.quote(binurl[2])
        binurl = urlparse.urlunsplit(binurl)
    else:
        binurl = url
    (tmpfile, headers) = ulib.urlretrieve(binurl, tmpfile, callback)
    filename = ".zip"
    if outdir:
        filename = outdir + "/" + filename


    if os.path.exists(filename):
        filename = filename_fix_existing(filename)
    shutil.move(tmpfile, filename)


    return filename

class GameView(BoxLayout):

    
    def __init__(self):
        super(GameView, self).__init__()
        create_folder("APP")
        self.zip_num = 0
    
    def install_Pie_of_Spies(self):

        try:
            download(dict_url["MITM"])
            os.rename(".zip", "MITM.zip")
            unzip("MITM.zip")
        except: print("don't work please write a commit")

class checkmate(App):
    def build(self):
        return GameView()



BAD_PHONE_MAIN = checkmate()
BAD_PHONE_MAIN.run()