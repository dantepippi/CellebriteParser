import hashlib
import glob
import ConfigParser
import codecs

def get_data_por_extenso(data):
    mes_ext = {1: 'janeiro', 2 : 'fevereiro', 3: 'marco', 4: 'abril', 5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}
    dia, mes, ano = data.split("/")
    return dia + ' de ' + mes_ext[int(mes)] + ' de ' + ano

def abre_arquivo_conf(file_path_base):
    config = ConfigParser.ConfigParser()
    # Abre arquivo ASAP (que utiliza encoding LATIN-1)
    for arq in glob.glob(file_path_base + "*.asap"):
        config.readfp(codecs.open(arq, "r", 'LATIN-1'))
    configuracoes = {}
    configuracoes['NUMLAUDO'] = config.get('LAUDO', 'NUMERO', 0).encode('LATIN-1')
    configuracoes['DATALAUDO'] = get_data_por_extenso(config.get('LAUDO', 'DATA', 0)).encode('LATIN-1')
    configuracoes['NOMEPERITO'] = config.get('LAUDO', 'PCF1', 0).split("|")[0].encode('LATIN-1')
    configuracoes['NUMIPL'] = config.get('SOLICITACAO', 'NUMERO_IPL', 0).encode('LATIN-1')
    configuracoes['IDAUTORIDADE'] = config.get('SOLICITACAO', 'AUTORIDADE', 0).encode('UTF-8')
    configuracoes['DOCSOLICITANTE'] = config.get('SOLICITACAO', 'DOCUMENTO', 0).encode('LATIN-1')
    configuracoes['DTDOC'] = config.get('SOLICITACAO', 'DATA_DOCUMENTO', 0).encode('LATIN-1')
    configuracoes['NUMSISCRIM'] = config.get('SOLICITACAO', 'NUMERO_CRIMINALISTICA', 0).encode('LATIN-1')
    configuracoes['DTSISCRIM'] = config.get('SOLICITACAO', 'DATA_CRIMINALISTICA', 0).encode('LATIN-1')
    return configuracoes


def str_replace_dict(texto, mudancas):
    for key in mudancas:
        texto = texto.replace(key, mudancas[key])
    return texto

def arq_replace_strings(arq, mudancas):
    file = open(arq, 'r+')
    texto = file.read()
    texto = str_replace_dict(texto, mudancas)
    file.seek(0)
    file.write(texto)
    file.truncate()
    file.close()

def calcula_hash(filename, blocksize=65536):
    hasher = hashlib.sha256()
    afile = open(filename, 'rb')
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    str_hash = hasher.hexdigest()
    afile.close()
    return str_hash