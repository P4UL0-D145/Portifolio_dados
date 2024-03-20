# ============================================================================ #
# ESSE SCRIPT FOI FEITO PARA BAIXAR AS CREDENCIAS DE UM ARQUIVO NO BLOBSTORAGE #
# ============================================================================ #
# import de bibliotecas
from azure.storage.blob import BlobServiceClient
import os

def credenciais():
    # =========================================================================
    # Baixando as credenciais
    account_name = ''
    account_key = ''
    container_name = ''
    
    blob_name = 'caminho_da_sua_credencial'
    local_file_path = os.getcwd()
    local_file_path = local_file_path.replace('\\', '/')
    local_file_path = local_file_path + '/'
    
    file_name = blob_name.split('/')[-1]
    
    # Cliente do serviço de blob
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
    
    # Referência ao contêiner
    container_client = blob_service_client.get_container_client(container_name)
    
    # Referência para o blob
    blob_client = container_client.get_blob_client(blob_name)
    
    # Download do blob para um arquivo local
    with open(local_file_path + file_name, "wb") as my_blob:
        blob_data = blob_client.download_blob()
        my_blob.write(blob_data.readall())
        
    # =========================================================================
    # Ativando as credenciais
    
    arquivo = local_file_path + file_name
    
    # Abrindo arquivo
    with open(arquivo, 'r') as file:
        # Pegando conteudo do arquivo e quebrando por linha
        for linha in file.read().split('\n'):
            # Separando cada linha por chave e valor
            valores_linha = linha.split('=')
            # Conferindo se valor na linha é valido
            if len(valores_linha) > 1:
                # Pegando a chave
                chave = valores_linha[0]
                # Pegando o valor
                valor = '='.join(valores_linha[1:])
    
                # Defindo a variável de ambiente
                os.environ[chave] = valor
    
    # =========================================================================
    # Apagando arquivos
    os.remove(local_file_path + file_name)
