try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def remove_espacos_exc(chunk):
    return  ' '.join(chunk.split())

def parse_arquivo_xml(arquivo_xml):
    tree = ET.ElementTree(file=arquivo_xml)
    root = tree.getroot()
    for contato in tree.iter(tag='contact'):
        nome = remove_espacos_exc(contato.find('name').text)
        numero = contato.find('phone_number/value')
        print nome, '-', numero.text 

