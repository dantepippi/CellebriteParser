import sys
import zipfile
import os
import codecs
from os.path import join
import ConfigParser
import isomaker

tmp_dir = 'tmp/'
file_path = '/home/dev/Dropbox/'

def get_data_por_extenso(data):
    mes_ext = {1: 'janeiro', 2 : 'fevereiro', 3: 'marco', 4: 'abril', 5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}
    dia, mes, ano = data.split("/")
    return dia + ' de ' + mes_ext[int(mes)] + ' de ' + ano

def abreDoc(arquivo):
    """
    Abre o documento no diretorio temporario e retorna um array com o conteudo
    dos dois arquivos de interesse (document e header)
    """
    mydoc = zipfile.ZipFile(arquivo)
    mydoc.extractall(tmp_dir)
    xmlcontent = [mydoc.read('word/document.xml'),  mydoc.read('word/header1.xml')]
    return xmlcontent

def salva_documento(output):
    os.chdir(tmp_dir)
    os.walk('.')
    document = zipfile.ZipFile(
        output, mode='w', compression=zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            nome_arquivo = join(dirpath, filename)
            archivename = nome_arquivo[2:]
            document.write(nome_arquivo, archivename)
            os.remove(nome_arquivo)
    document.close()

def replace(document, search, replace):
    newdocument = document.replace(search, replace)
    return newdocument    
    
def abre_arquivo_conf():
    config = ConfigParser.ConfigParser()
    # Abre arquivo ASAP (que utiliza encoding LATIN-1)
    config.readfp(codecs.open(sys.argv[1], "r", 'LATIN-1'))
    return config


document = abreDoc(file_path + 'd1.docx')
newdocument = open(tmp_dir + 'word/document.xml', 'w')
newheader = open(tmp_dir + 'word/header1.xml', 'w')
# Substitui os valores do ASAP no documento
config = abre_arquivo_conf()
document[0] = replace(document[0], 'NUMLAUDO', config.get('LAUDO', 'NUMERO', 0))
document[0] = replace(document[0], 'DATALAUDO', get_data_por_extenso(config.get('LAUDO', 'DATA', 0)))
document[0] = replace(document[0], 'NOMEPERITO', config.get('LAUDO', 'PCF1', 0).split("|")[0])
document[0] = replace(document[0], 'NUMIPL', config.get('LAUDO', 'NUMERO', 0))
document[0] = replace(document[0], 'IDAUTORIDADE', config.get('SOLICITACAO', 'AUTORIDADE', 0))
document[0] = replace(document[0], 'DOCSOLICITANTE', config.get('SOLICITACAO', 'DOCUMENTO', 0))
document[0] = replace(document[0], 'DTDOC', config.get('SOLICITACAO', 'DATA_DOCUMENTO', 0))
document[0] = replace(document[0], 'NUMSISCRIM', config.get('SOLICITACAO', 'NUMERO_CRIMINALISTICA', 0))
document[0] = replace(document[0], 'DTSISCRIM', config.get('SOLICITACAO', 'DATA_CRIMINALISTICA', 0))

# Substitui o numero do laudo no header
document[1] = replace(document[1], 'NUMLAUDO', config.get('LAUDO', 'NUMERO', 0))

newdocument.write(document[0])
newheader.write(document[1])
newdocument.close()
newheader.close()
salva_documento(file_path + 'd2.docx')
