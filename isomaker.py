import subprocess

def gera_iso(pasta, label):
    subprocess.call(['mkisofs', '-J', '-l', '-R', '-V', label, '-iso-level', '4', '-o', '/home/dev/Dropbox/output.iso', pasta])

gera_iso('/home/web2py', 'ISO') 