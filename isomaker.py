import subprocess
import hashlib
import os
from os.path import join

tmp_dir = 'tmp/'
pasta_teste = '/home/dev/Dropbox/'

def gera_hashes(pasta):
    hashes = open(tmp_dir + 'hashes.txt', 'w')
    for dirpath, dirnames, filenames in os.walk(pasta):
        for filename in filenames:
            nome_completo = join(dirpath, filename)
            hashes.write(filename + '=' + hashfile(nome_completo) + '\r\n')
    hashes.close()
    os.rename(tmp_dir + 'hashes.txt', pasta + 'hashes.txt')
    
def gera_iso(pasta, label):
    nome_iso = label + '.iso'
    p = subprocess.Popen(['mkisofs', '-J', '-l', '-R', '-V', label, '-iso-level', '4', '-o', nome_iso, pasta])
    p.communicate()
    return hashfile(nome_iso)

def hashfile(filename, hasher=hashlib.sha256(), blocksize=65536):
    afile = open(filename, 'rb')
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

#gera_hashes(pasta_teste)
#print gera_iso(pasta_teste, 'ISO') 