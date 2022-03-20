import errno
import os
from resizeImage import main

fileName = 'ip_web_cam_link.txt'


def getUrl():
    try:
        url = ''
        with open(fileName, 'r') as fp:
            url = fp.read()
        return url
    except:
        return ''
        # raise FileNotFoundError(
        #     errno.ENOENT, os.strerror(errno.ENOENT), fileName)
