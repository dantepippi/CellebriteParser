import subprocess
import hashlib
import os
from os.path import join

tmp_dir = 'tmp/'

def grava_hashes(pasta):
    hashes = open(tmp_dir + 'hashes.txt', 'w')
    for dirpath, dirnames, filenames in os.walk(pasta):
        for filename in filenames:
            nome_completo = join(dirpath, filename)
            hashes.write(calcula_hash(nome_completo) + ' ?SHA256*' + nome_completo.replace(pasta,'') + '\r\n')
    hashes.close()
    os.rename(tmp_dir + 'hashes.txt', pasta + 'hashes.txt')
    
def gera_iso(pasta, label):
    grava_hashes(pasta)
    nome_iso = pasta + 'resultado' + label + '.iso'
    p = subprocess.Popen(['mkisofs', '-J', '-l', '-R', '-V', label, '-iso-level', '4', '-o', nome_iso, pasta])
    p.communicate()
    os.remove(pasta + 'hashes.txt')
    return calcula_hash(nome_iso)

def calcula_hash(filename, blocksize=65536):
    hasher = hashlib.sha256()
    afile = open(filename, 'rb')
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    str_hash = hasher.hexdigest()
    afile.close()
    return str_hash

#grava_hashes(pasta_teste)
#print gera_iso(pasta_teste, 'ISO') 