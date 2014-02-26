import re
import sys
import zipfile
import os
from os.path import join
from isomaker import gera_iso, gera_contents_frame, gera_case_information
import glob
import shutil
import my_config
from xmlparse import parse_arquivo_xml, replace_txt
from my_config import tmp_dir, file_path_backup, file_path_base, file_path_midia

def altera_docx(lista_dirs, config):
    num_laudo = config['NUMLAUDO']
    for arq in glob.glob(tmp_dir + 'word/*.xml'):
        file = open(arq, 'r+')
        conteudo = file.read()
        if 'document' in arq:
            conteudo = cria_secoes_tabela(conteudo, lista_dirs)
            hash_iso = gera_iso(file_path_backup, file_path_base, 'L' + num_laudo.replace("/", "_"))
            conteudo = replace_txt(conteudo, 'HASHISO', hash_iso.upper())
            conteudo = my_config.str_replace_dict(conteudo, config)
        conteudo = replace_txt(conteudo, 'NUMLAUDO', num_laudo)
        file.seek(0)
        file.write(conteudo)
        file.truncate()
        file.close()

def abreDoc(arquivo):
    mydoc = zipfile.ZipFile(arquivo)
    mydoc.extractall(tmp_dir)

def salva_documento(output):
    os.chdir(tmp_dir)
    conteudo = zipfile.ZipFile(
        output, mode='w', compression=zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            nome_arquivo = join(dirpath, filename)
            archivename = nome_arquivo[2:]
            conteudo.write(nome_arquivo, archivename)
            os.remove(nome_arquivo)
    conteudo.close()

def percorre_arquivos_xml(conteudo, diretorio, contacts):
    for arq in glob.glob(file_path_backup + diretorio + "/*.xml"):
        conteudo = parse_arquivo_xml(arq, conteudo, diretorio, contacts)
        os.remove(arq)
    return conteudo

def copia_arquivo_imagem():
    for arq in glob.glob(file_path_base + "*.png"):
        shutil.copyfile(arq, tmp_dir + 'word/media/image2.png')

def get_lista_diretorios():
    return sorted([name for name in os.listdir(file_path_backup) if (os.path.isdir(os.path.join(file_path_backup, name)) and 'Supporting' not in name)])

def cria_secoes_tabela(conteudo, lista_dirs):
    primeiro = True
    contacts = {}
    contacts['LISTA_CONTATOS'] = ''
    for diretorio in lista_dirs:
        if 'CELULAR' in diretorio:
            if primeiro:
                conteudo_tabela = open('./template_first.txt').read()
                primeiro = False
            else:
                conteudo_tabela = open('./template_cel.txt').read()
        else:
            conteudo_tabela = open('./template_sim_avulso.txt').read()
        conteudo_tabela = conteudo_tabela.replace('\n', '')
        conteudo = insere_tabela(conteudo, conteudo_tabela)
        conteudo = percorre_arquivos_xml(conteudo, diretorio, contacts)
    my_config.arq_replace_strings(file_path_backup + 'SupportingFiles/busca/busca.htm', contacts)
    return conteudo 
 
def insere_tabela(conteudo, tabela):
    posicao = re.search(r'<w:p w:rsidR="00F00A10" w:rsidRDefault="00FA64C5"><w:pPr><w:pStyle w:val="LLeg"/><w:jc w:val="both"/></w:pPr><w:r><w:rPr><w:b/><w:iCs/><w:spacing w:val="-3"/></w:rPr><w:t>Legenda:</w:t>', conteudo).start()
    return conteudo[:posicao] + tabela + conteudo[posicao:]
   
def backup_arquivos_midia():
    shutil.copytree(file_path_midia, file_path_backup)  
    
def remove_extra_dirs():
    shutil.rmtree(tmp_dir, True)
    shutil.rmtree(file_path_backup, True)
    
#arq_replace_strings('template_sim_avulso.txt', '\n', '')
remove_extra_dirs()
abreDoc(file_path_base + 'd1.docx')
copia_arquivo_imagem()
backup_arquivos_midia()
lista_dirs = get_lista_diretorios()
configuracoes = my_config.abre_arquivo_conf(file_path_base)
gera_contents_frame(lista_dirs, file_path_backup)
gera_case_information(configuracoes, file_path_backup)
altera_docx(lista_dirs, configuracoes) # aqui esta sendo gerada a midia, qualquer arquivo que deva ser inserido na midia tem que ser editado antes
salva_documento(file_path_base + 'd2.docx')
remove_extra_dirs()
