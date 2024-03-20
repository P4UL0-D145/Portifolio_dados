# ================================================================ #
# ESSE SCRIPT FOI FEITO PARA CARREGAR DADOS LOCAIS NO BLOB STORAGE #
# ================================================================ #
# import de bibliotecas
import os
from azure.storage.blob import BlobServiceClient

# Definição de pasta local
raiz = r'C:\Users\Taking\Downloads\Dowload_blob\__pycache__'

# Configurar credenciais
account_name = ''
account_key = ''
container_name = ''

# Criar um cliente BlobService
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# Referenciar o container de destino
container_client = blob_service_client.get_container_client(container_name)

# pegando arquivos da pasta raiz
for root, dirs, files in os.walk(raiz):
    # percorrendo arquivos da pasta
    for file_name in files:
        # Ajustando as barras do caminho do arquivo se for necessario
        caminho_local = os.path.join(root, file_name).replace('\\', '/')
        
        # Apontando para o Blob Storage de acordo com o arquivo local
        caminho_blob = (
            '/' # caminho do container que deseja subir o arquivo
            + '/'.join(caminho_local.split('/')[4:])
            )
        
        # fazendo carga dos arquivos da pasta
        container_client.upload_blob(
            name= caminho_blob
            ,data=caminho_local
            )
        
        print(f'Arquivo novo {file_name} carregado no blob.')