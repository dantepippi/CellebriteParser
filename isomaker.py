import subprocess
import hashlib
import os
from os.path import join
import my_config

tmp_dir = 'tmp/'
arq_contents = 'contents.htm'

def gera_contents_frame(lista_dirs, file_path_backup):
    str_categorias = ''
    for dir in lista_dirs:
        str_categorias += '<p><a href="' + dir + '" class="SmallText2" target="ReportPage">' + dir + '</a></p>'
    my_config.arq_replace_strings(file_path_backup + arq_contents, 'STR_CATEGORIAS', str_categorias)

def grava_hashes(pasta):
    hashes = open(tmp_dir + 'hashes.txt', 'w')
    for dirpath, dirnames, filenames in os.walk(pasta):
        for filename in filenames:
            nome_completo = join(dirpath, filename)
            hashes.write(my_config.calcula_hash(nome_completo) + ' ?SHA256*' + nome_completo.replace(pasta,'') + '\r\n')
    hashes.close()
    os.rename(tmp_dir + 'hashes.txt', pasta + 'hashes.txt')
    
def gera_iso(pasta_origem, pasta_destino, label):
    grava_hashes(pasta_origem)
    nome_iso = pasta_destino + label + '.iso'
    p = subprocess.Popen(['mkisofs', '-J', '-l', '-R', '-V', label, '-iso-level', '4', '-o', nome_iso, pasta_origem])
    p.communicate()
    return my_config.calcula_hash(pasta_origem + 'hashes.txt')

