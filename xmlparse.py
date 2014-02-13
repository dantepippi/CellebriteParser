import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def replace_txt(document, search, replace_txt):
    newdocument = document.replace(search, replace_txt)
    return newdocument

def remove_espacos_exc(chunk):
    return  ' '.join(chunk.split())

def parse_arquivo_xml(arquivo_xml, document):
    tree = ET.ElementTree(file=arquivo_xml)
    root = tree.getroot()
    if root.find('report/general_information/report_type').text == 'cell':
        # pega a segunda parte do split (retira o caminho e deixa so arquivo com extensao) e a primeira parte do splitext(retira a extensao)
        document = replace_txt(document, 'ID_CEL', os.path.splitext(os.path.split(arquivo_xml)[1])[0])
        document = replace_txt(document, 'MARCAMODELO', root.find('report/general_information/selected_manufacture').text + ' ' + root.find('report/general_information/detected_model').text )
        document = replace_txt(document, 'NUM_IMEI1', root.find('report/general_information/imei').text)
    else:
        document = replace_txt(document, 'DESC_OPERADORA', root.find('report/general_information/spn').text)
        document = replace_txt(document, 'NUM_ICC', root.find('report/general_information/iccid').text)
        document = replace_txt(document, 'NUM_IMSI', root.find('report/general_information/imsi').text)    
    """
    for contato in tree.iter(tag='contact'):
        nome = remove_espacos_exc(contato.find('name').text)
        numero = contato.find('phone_number/value')
        print nome, '-', numero.text 
    """
    return document

