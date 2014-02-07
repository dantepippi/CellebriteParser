import sys
import zipfile
import os
from os.path import join

asap = open(sys.argv[1], 'r')

import ConfigParser
def get_data_por_extenso(data):
    mes_ext = {1: 'janeiro', 2 : 'fevereiro', 3: 'marco', 4: 'abril', 5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}
    dia, mes, ano = data.split("/")
    return dia + ' de ' + mes_ext[int(mes)] + ' de ' + ano


def abreDoc(arquivo):
    mydoc = zipfile.ZipFile(arquivo)
    mydoc.extractall('/home/tmp/')
    xmlcontent = [mydoc.read('word/document.xml'),  mydoc.read('word/header1.xml')]
    return xmlcontent

def salva_documento(output):
    os.chdir('/home/tmp/')
    os.walk('.')
    document = zipfile.ZipFile(
        output, mode='w', compression=zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            templatefile = join(dirpath, filename)
            archivename = templatefile[2:]
            document.write(templatefile, archivename)
    document.close()

def replace(document, search, replace):
    """
    Replace all occurences of string with a different string, return updated
    document
    """
    newdocument = document.replace(search, replace)
    return newdocument    
    
config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

file_path = '/home/dev/Dropbox/'
document = abreDoc(file_path + 'd1.docx')
newdocument = open('/home/tmp/word/document.xml', 'w')
newheader = open('/home/tmp/word/header1.xml', 'w')


document[0] = replace(document[0], 'NUMLAUDO', config.get('LAUDO', 'NUMERO', 0))
document[1] = replace(document[1], 'NUMLAUDO', config.get('LAUDO', 'NUMERO', 0))
document[0] = replace(document[0], 'DATALAUDO', get_data_por_extenso(config.get('LAUDO', 'DATA', 0)))
document[0] = replace(document[0], 'NOMEPERITO', config.get('LAUDO', 'PCF1', 0).split("|")[0])
document[0] = replace(document[0], 'NUMIPL', config.get('LAUDO', 'NUMERO', 0))
document[0] = replace(document[0], 'IDAUTORIDADE', config.get('SOLICITACAO', 'AUTORIDADE', 0))
document[0] = replace(document[0], 'DOCSOLICITANTE', config.get('SOLICITACAO', 'DOCUMENTO', 0))
document[0] = replace(document[0], 'DTDOC', config.get('SOLICITACAO', 'DATA_DOCUMENTO', 0))
document[0] = replace(document[0], 'NUMSISCRIM', config.get('SOLICITACAO', 'NUMERO_CRIMINALISTICA', 0))
document[0] = replace(document[0], 'DTSISCRIM', config.get('SOLICITACAO', 'DATA_CRIMINALISTICA', 0))
newdocument.write(document[0])
newheader.write(document[1])
newdocument.close()
newheader.close()
salva_documento(file_path + 'd2.docx')





