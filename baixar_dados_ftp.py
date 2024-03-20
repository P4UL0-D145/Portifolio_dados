# ============================================================================= #
# ESSE SCRIPT FOI FEITO PARA BAIXAR DADOS DE UMA FONTE FTP NA SUA MAQUINA LOCAL #
# ============================================================================= #
# import de bibliotecas
import os
import sys
sys.path.append(os.getcwd())
from ftplib import FTP
from baixar_credenciais_blobstorage import credenciais

# ativar variaveis de ambiente
credenciais()

# Defina as informações de conexão FTP
hostname = os.environ['HOST']
username = os.environ['USER']
password = os.environ['PASSWORD']

# Conecte-se ao servidor FTP
ftp = FTP(hostname)
ftp.login(user=username, passwd=password)

# Pasta remota que você deseja acessar
pasta_remota = '/'

# Pasta local onde os arquivos serão salvos
pasta_local = r'sua_pasta_local'
pasta_local = [path.replace("\\", "/") for path in pasta_local]

# criar pasta local caso nao exista
try:
    os.makedirs(pasta_local)
except:
    pass

# Mude para o diretório remoto
ftp.cwd(pasta_remota)

# Lista todos os arquivos na pasta remota
arquivos_remotos = ftp.nlst()

# Baixa cada arquivo da pasta remota para a pasta local
for arquivo in arquivos_remotos:
    caminho_arquivo_local = f"{pasta_local}/{arquivo}"
    with open(caminho_arquivo_local, 'wb') as file:
        ftp.retrbinary(f'RETR {arquivo}', file.write)

# Fecha a conexão FTP
ftp.quit()
