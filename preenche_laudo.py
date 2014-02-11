import re
import sys
import zipfile
import os
import codecs
from os.path import join
import ConfigParser
from isomaker import gera_iso
import glob
from xmlparse import parse_arquivo_xml, replace_txt

tmp_dir = 'tmp/'
file_path = sys.argv[1]

def get_data_por_extenso(data):
    mes_ext = {1: 'janeiro', 2 : 'fevereiro', 3: 'marco', 4: 'abril', 5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}
    dia, mes, ano = data.split("/")
    return dia + ' de ' + mes_ext[int(mes)] + ' de ' + ano

def abreDoc(arquivo):
    """
    Extrai os arquivos do documento no diretorio temporario e retorna um array com o conteudo
    dos dois arquivos de interesse (document.xml e header1.xml)
    """
    mydoc = zipfile.ZipFile(arquivo)
    mydoc.extractall(tmp_dir)
    (document, header) = (mydoc.read('word/document.xml'),  mydoc.read('word/header1.xml'))
    return (document, header)

def salva_documento(output):
    os.chdir(tmp_dir)
    document = zipfile.ZipFile(
        output, mode='w', compression=zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            nome_arquivo = join(dirpath, filename)
            archivename = nome_arquivo[2:]
            document.write(nome_arquivo, archivename)
            os.remove(nome_arquivo)
    document.close()

def abre_arquivo_conf():
    config = ConfigParser.ConfigParser()
    # Abre arquivo ASAP (que utiliza encoding LATIN-1)
    for arq in glob.glob(file_path + "*.asap"):
        config.readfp(codecs.open(arq, "r", 'LATIN-1'))
    return config

def percorre_arquivos_xml(document, dir):
    for arq in glob.glob(file_path + dir + "/*.xml"):
        document = parse_arquivo_xml(arq, document)
        #os.remove(arq)
    return document

def get_lista_diretorios():
    return sorted([name for name in os.listdir(file_path) if os.path.isdir(os.path.join(file_path, name))])

def cria_secoes_tabela(document, lista_dirs):
    cont = 0
    for dir in lista_dirs:
        cont += 1
        conteudo_tabela = open('./template_tabela.txt').read()
        document = insere_tabela(document, conteudo_tabela)
        #document = replace_txt(document, 'CONT_TABELA' + str(cont), conteudo_tabela)
        document = percorre_arquivos_xml(document, dir)
    return document
 
def insere_tabela(document, tabela):
     posicao = re.search(r'<w:tbl', document).start()
     return document[:posicao] + tabela + document[posicao:]
     
        
(document, header) = abreDoc(file_path + 'd1.docx')
newdocument = open(tmp_dir + 'word/document.xml', 'w')
newheader = open(tmp_dir + 'word/header1.xml', 'w')
# Substitui os valores do ASAP no documento
config = abre_arquivo_conf()
document = cria_secoes_tabela(document, get_lista_diretorios())
num_laudo = config.get('LAUDO', 'NUMERO', 0).encode('UTF-8')
hash_iso = gera_iso(file_path, 'L'+ num_laudo.replace("/", "_"))
document = replace_txt(document, 'NUMLAUDO', num_laudo)
document = replace_txt(document, 'DATALAUDO', get_data_por_extenso(config.get('LAUDO', 'DATA', 0)))
document = replace_txt(document, 'NOMEPERITO', config.get('LAUDO', 'PCF1', 0).split("|")[0])
document = replace_txt(document, 'NUMIPL', config.get('SOLICITACAO', 'NUMERO_IPL', 0))
document = replace_txt(document, 'IDAUTORIDADE', config.get('SOLICITACAO', 'AUTORIDADE', 0))
document = replace_txt(document, 'DOCSOLICITANTE', config.get('SOLICITACAO', 'DOCUMENTO', 0))
document = replace_txt(document, 'DTDOC', config.get('SOLICITACAO', 'DATA_DOCUMENTO', 0))
document = replace_txt(document, 'NUMSISCRIM', config.get('SOLICITACAO', 'NUMERO_CRIMINALISTICA', 0))
document = replace_txt(document, 'DTSISCRIM', config.get('SOLICITACAO', 'DATA_CRIMINALISTICA', 0))
document = replace_txt(document, 'HASHISO', hash_iso.upper())

# Substitui o numero do laudo no header
header = replace_txt(header, 'NUMLAUDO', config.get('LAUDO', 'NUMERO', 0))

newdocument.write(document)
newheader.write(header)
newdocument.close()
newheader.close()
salva_documento(file_path + 'd2.docx')
