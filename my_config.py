import hashlib

def arq_replace_strings(arq, search, replace):
    file = open(arq, 'r+')
    texto = file.read()
    texto = texto.replace(search, replace)
    file.seek(0)
    file.write(texto)
    file.truncate()
    file.close()

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