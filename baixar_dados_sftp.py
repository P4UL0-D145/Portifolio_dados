# ============================================================================== #
# ESSE SCRIPT FOI FEITO PARA BAIXAR DADOS DE UMA FONTE SFTP NA SUA MAQUINA LOCAL #
# ============================================================================== #
# import de bibliotecas
import paramiko
import os
import sys
sys.path.append(os.getcwd())
from baixar_credenciais_blobstorage import credenciais

# ativar variaveis de ambiente
credenciais()

# Defina as informações de conexão SFTP
hostname = os.environ['HOST']
port = os.environ['PORT']
port = int(port)
username = os.environ['USER']
password = os.environ['PASSWORD']

# Crie uma conexão SFTP
transport = paramiko.Transport((hostname, port))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

# # Pasta remota que você deseja baixar
pasta_remota = '/'

# Pasta local onde os arquivos serão salvos
pasta_local = r'sua_pasta_local'
pasta_local = [path.replace("\\", "/") for path in pasta_local]

# criar pasta local caso nao exista
try:
    os.makedirs(pasta_local)
except:
    pass

# lista para guardar arquivos local
lista_local = []

# loop para buscar todos os arquivos existente em pasta_local
if os.path.exists(pasta_local):
    # Percorre o diretório e suas subpastas
    for pasta_atual, sub_pastas, arquivos in os.walk(pasta_local):
        # Salva os arquivos existentes na lista
        for arquivo in arquivos:
            caminho_completo = os.path.join(pasta_atual, arquivo)
            caminho_completo = caminho_completo.replace("\\", "/")
            caminho_completo = caminho_completo.split("/")
            partes_selecionadas = caminho_completo[-1:]
            novo_caminho = "/".join(partes_selecionadas)
            lista_local.append(novo_caminho)

# Lista todos os arquivos na pasta remota
arquivos_remotos = sftp.listdir(pasta_remota)

# loop para remover arquivos existente local
for i in lista_local:
    arquivos_remotos = [y for y in arquivos_remotos if i not in y] # limpa arquivos duplicados

if len(arquivos_remotos) > 0:
  # Baixa cada arquivo da pasta remota para a pasta local
  for arquivo in arquivos_remotos:
      caminho_arquivo_remoto = f"{pasta_remota}/{arquivo}"
      caminho_arquivo_local = f"{pasta_local}/{arquivo}"
      sftp.get(caminho_arquivo_remoto, caminho_arquivo_local)
      print(f"Arquivo {arquivo} foi salvo no diretorio {pasta_local}")
else:
  print("Sem arquivos novos")

# Fecha a conexão SFTP
sftp.close()
transport.close()