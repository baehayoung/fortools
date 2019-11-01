import pyevtx
import zipfile
import os
import sqlite3
from os import listdir
from PIL import Image
import forlib.collection.signature as sig
from Registry import Registry
import forlib.collection.decompress as decompress
import struct
import pytsk3

def signature_db(path):
    file_extension_recycle = path.split('\\')[-1]
    if file_extension_recycle =='$I':
        return recycle_open(path)
    return sig.sig_check(path)


def evtx_open(path):
    evtx_file = pyevtx.file()
    evtx_file.open(path)
    return evtx_file


def reg_open(path):
    return Registry.Registry(path)

                                        
def zip_open(path):
    file = open(path, 'rb')
    z = zipfile.ZipFile(file, 'r')
    return z

def fs_open(path):
    return pytsk3.Img_Info(path)

def jpeg_open(path):
    return Image.open(path)


def systemp_open(path):
    return path


def binary_open(path):
    return open(path, 'rb')


def normal_file_oepn(path):
    return open(path, 'r')

                                        
def thumb_open(path):
    return path

                                       
def prefetch_open(path):
        file = open(path, 'rb')
        if file.read(3) == b'MAM':
            file.close()
            decompressed = decompress.decompress(path)

            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            base = os.path.splitext(basename)
            basename = base[0]
            exetension = base[-1]
            
            file = open(dirname+'\\'+basename+'-1'+exetension,'wb')
            file.write(decompressed)
            file.close()
            
        file = open(dirname+'\\'+basename+'-1'+exetension,'rb')
        version = struct.unpack_from('I', file.read(4))[0]
            
        if version != 23 and version != 30:
            print ('error: not supported version')

        signature = file.read(4)
        print(signature)
        if signature != b'SCCA':
            print('not prefetch file')
        
        print('Success file open')
        return file
    
    
'''                                  
def superfetch_open(path):
    file = open(path,'rb')
    if file.read(3)  == 'MAM':
        file = decompress.decomp(path)
    return file
'''
                                    
def chrome_open(path):
    open_chrome_file = open(path, "rb")
    format=open_chrome_file.read(15).decode()

    if format=="SQLite format 3":
        return path
    else:
        return open_chrome_file
                                        
        
def firefox_open(path):
    open_firefox_file = open(path, "rb")
    format=open_firefox_file.read(15).decode()

    if format=="SQLite format 3":
        return path
    else:
        return open_firefox_file
                                        
                                        
def lnk_open(path):
    file = open(path,'rb')
    return file

                                        
def recycle_open(path):
    file = open(path,'rb')
    return file

                                        
def jumplist_open(path):
    file = open(path,'rb')
    return file