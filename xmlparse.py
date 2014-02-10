
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def replace(document, search, replace):
    if replace is None:
        return document
    newdocument = document.replace(search, replace)
    return newdocument

def remove_espacos_exc(chunk):
    return  ' '.join(chunk.split())

def parse_arquivo_xml(arquivo_xml, document):
    tree = ET.ElementTree(file=arquivo_xml)
    root = tree.getroot()
    document = replace(document, 'MARCAMODELO', root.find('report/general_information/selected_manufacture'))
    document = replace(document, 'NUM_IMEI1', root.find('report/general_information/imei'))
    document = replace(document, 'DESC_OPERADORA', root.find('report/general_information/spn'))
    document = replace(document, 'NUM_ICC', root.find('report/general_information/iccid'))
    document = replace(document, 'NUM_IMSI', root.find('report/general_information/imsi'))    
    
    for contato in tree.iter(tag='contact'):
        nome = remove_espacos_exc(contato.find('name').text)
        numero = contato.find('phone_number/value')
        print nome, '-', numero.text 
    return document

