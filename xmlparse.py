import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def replace_txt(conteudo, search, replace_txt):
    newdocument = conteudo.replace(search, replace_txt)
    return newdocument

def remove_espacos_exc(chunk):
    return  ' '.join(chunk.split())

def adiciona_contatos(tree, diretorio):
    contacts = ''
    for contato in tree.iter(tag='contact'):
        nome = remove_espacos_exc(contato.find('name').text)
        numero = contato.find('phone_number/value')
        txt_contatos = '<tr><td class="origem">' + diretorio + '</td><td class="numero">' + numero + '</td><td class="nome">' + nome + '</td> </tr>'

def parse_arquivo_xml(arquivo_xml, conteudo, diretorio):
    tree = ET.ElementTree(file=arquivo_xml)
    root = tree.getroot()
    adiciona_contatos(diretorio, tree)
    conteudo = replace_txt(conteudo, 'ID_CEL', diretorio)
    if root.find('report/general_information/report_type').text == 'cell':
        conteudo = replace_txt(conteudo, 'MARCAMODELO', root.find('report/general_information/selected_manufacture').text + ' ' + root.find('report/general_information/detected_model').text )
        conteudo = replace_txt(conteudo, 'NUM_IMEI1', root.find('report/general_information/imei').text)
    else:
        conteudo = replace_txt(conteudo, 'DESC_OPERADORA', root.find('report/general_information/spn').text)
        conteudo = replace_txt(conteudo, 'NUM_ICC', root.find('report/general_information/iccid').text)
        conteudo = replace_txt(conteudo, 'NUM_IMSI', root.find('report/general_information/imsi').text)    
    return conteudo

