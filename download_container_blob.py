# ============================================================================================== #
# ESSE SCRIPT FOI FEITO PARA BAIXAR DADOS DE UM CONTAINER NO BLOB STORAGE PARA SUA MAQUINA LOCAL #
# ============================================================================================== #
# import de bibliotecas
import os
from azure.storage.blob import BlobServiceClient

# Configurar credenciais
account_name = ''
account_key = ''
container_name = ''

# definição de variaveis utilizada no processo
chunk_size = 1000 * 1024 * 1024  # baixar arquivos de 1 em 1 Giga bytes
pasta_download_base = r'C:\Users\Public\Downloads'  # pasta base
pasta_download_base = pasta_download_base.replace("\\", "/")  # substitua "\\" por "/" se desejar

# Criar um cliente BlobService
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# Listando arquivos no blob
blob_list = blob_service_client.get_container_client(container=container_name)
blob_list = blob_list.list_blobs()

# lista com diretorios e pastas de arquivos
arquivos_blob = [x.name for x in blob_list if '/' in x.name] # no lugar da barra pode colocar um caminho especifico

# lista somente com arquivos
arquivos = [item for item in arquivos_blob if '.' in item]

# verificar se tem arquivos no container blob
if len(arquivos) > 0:
  # baixar arquivos do blobstorage
  for arquivo in arquivos:
    # montar path para download do arquivo
    caminho_completo = os.path.join(pasta_download_base, arquivo)
    caminho_completo = caminho_completo.replace("\\", "/")

    # obtendo o diretório pai do caminho completo
    diretorio_pai = os.path.dirname(caminho_completo)

    # criar diretório para baixar os arquivos
    try:
        os.makedirs(diretorio_pai)
    except:
        pass
    
    # conectar com o cliete blob para baixar arquivos
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=arquivo)
    blob_properties = blob_client.get_blob_properties()
    blob_size = blob_properties.size

    # baixar arquivos blob na maquina local
    with open(caminho_completo, "wb") as file:
        offset = 0
        while offset < blob_size:
            end = min(offset + chunk_size, blob_size) - 1
            data = blob_client.download_blob(offset=offset, length=end - offset + 1)
            data.readinto(file)
            offset += chunk_size
            print(offset)
    
    print(f'arquivo baixado nesse diretório: {caminho_completo}')

else:
    print('sem arquivos no container')