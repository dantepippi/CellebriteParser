import re
import sys
import zipfile
import os
import codecs
from os.path import join
import ConfigParser
from isomaker import gera_iso, gera_contents_frame
import glob
import shutil
import my_config
from xmlparse import parse_arquivo_xml, replace_txt

file_path_base = sys.argv[1]
file_path_midia = file_path_base + 'midia/'
file_path_backup = file_path_base + 'backup/'
tmp_dir = file_path_base + 'tmp/'

def altera_docx(lista_dirs):
    config = abre_arquivo_conf()
    num_laudo = config.get('LAUDO', 'NUMERO', 0).encode('UTF-8')
    for arq in glob.glob(tmp_dir + 'word/*.xml'):
        file = open(arq, 'r+')
        conteudo = file.read()
        if 'document' in arq:
            conteudo = cria_secoes_tabela(conteudo, lista_dirs)
            hash_iso = gera_iso(file_path_backup, file_path_base, 'L' + num_laudo.replace("/", "_"))
            conteudo = replace_txt(conteudo, 'HASHISO', hash_iso.upper())
            conteudo = replace_txt(conteudo, 'DATALAUDO', get_data_por_extenso(config.get('LAUDO', 'DATA', 0)))
            conteudo = replace_txt(conteudo, 'NOMEPERITO', config.get('LAUDO', 'PCF1', 0).split("|")[0])
            conteudo = replace_txt(conteudo, 'NUMIPL', config.get('SOLICITACAO', 'NUMERO_IPL', 0))
            conteudo = replace_txt(conteudo, 'IDAUTORIDADE', config.get('SOLICITACAO', 'AUTORIDADE', 0))
            conteudo = replace_txt(conteudo, 'DOCSOLICITANTE', config.get('SOLICITACAO', 'DOCUMENTO', 0))
            conteudo = replace_txt(conteudo, 'DTDOC', config.get('SOLICITACAO', 'DATA_DOCUMENTO', 0))
            conteudo = replace_txt(conteudo, 'NUMSISCRIM', config.get('SOLICITACAO', 'NUMERO_CRIMINALISTICA', 0))
            conteudo = replace_txt(conteudo, 'DTSISCRIM', config.get('SOLICITACAO', 'DATA_CRIMINALISTICA', 0))
        conteudo = replace_txt(conteudo, 'NUMLAUDO', num_laudo)
        file.seek(0)
        file.write(conteudo)
        file.truncate()
        file.close()

def get_data_por_extenso(data):
    mes_ext = {1: 'janeiro', 2 : 'fevereiro', 3: 'marco', 4: 'abril', 5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}
    dia, mes, ano = data.split("/")
    return dia + ' de ' + mes_ext[int(mes)] + ' de ' + ano

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

def abre_arquivo_conf():
    config = ConfigParser.ConfigParser()
    # Abre arquivo ASAP (que utiliza encoding LATIN-1)
    for arq in glob.glob(file_path_base + "*.asap"):
        config.readfp(codecs.open(arq, "r", 'LATIN-1'))
    return config

def percorre_arquivos_xml(conteudo, diretorio):
    for arq in glob.glob(file_path_backup + diretorio + "/*.xml"):
        conteudo = parse_arquivo_xml(arq, conteudo, diretorio)
        os.remove(arq) 
    return conteudo

def copia_arquivo_imagem():
    for arq in glob.glob(file_path_base + "*.png"):
        shutil.copyfile(arq, tmp_dir + 'word/media/image2.png')

def get_lista_diretorios():
    return sorted([name for name in os.listdir(file_path_backup) if (os.path.isdir(os.path.join(file_path_backup, name)) and 'Supporting' not in name)])

def cria_secoes_tabela(conteudo, lista_dirs):
    primeiro = True
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
        conteudo = percorre_arquivos_xml(conteudo, diretorio)
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
gera_contents_frame(lista_dirs, file_path_backup)
altera_docx(lista_dirs) # aqui esta sendo gerada a midia, qualquer arquivo que deva ser inserido na midia tem que ser editado antes
salva_documento(file_path_base + 'd2.docx')
remove_extra_dirs()
