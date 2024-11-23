import boto3
from PIL import Image
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Extrair informações do evento S3
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        source_key = event['Records'][0]['s3']['object']['key']
        destination_bucket = '${destination_bucket}'
        destination_key = f"resized-{source_key}"

        # Caminhos temporários no ambiente Lambda
        download_path = f"/tmp/{os.path.basename(source_key)}"
        resized_path = f"/tmp/resized-{os.path.basename(source_key)}"

        print(f"Download do arquivo {source_key} do bucket {source_bucket}")
        
        # Fazer download do arquivo do bucket de origem
        s3_client.download_file(source_bucket, source_key, download_path)

        print(f"Arquivo {source_key} baixado com sucesso. Redimensionando...")

        # Abrir e redimensionar a imagem
        with Image.open(download_path) as img:
            img = img.convert("RGB")  # Certifica que está no formato RGB
            img.thumbnail((800, 800))  # Ajustar para no máximo 800x800
            img.save(resized_path, "JPEG")  # Salvar como JPEG

        print(f"Imagem redimensionada salva em {resized_path}. Fazendo upload...")

        # Fazer upload do arquivo redimensionado para o bucket de destino
        with open(resized_path, "rb") as resized_file:
            s3_client.upload_fileobj(resized_file, destination_bucket, destination_key)

        print(f"Arquivo redimensionado enviado para {destination_bucket} como {destination_key}.")
        
        return {
            'statusCode': 200,
            'body': f"Arquivo {destination_key} salvo com sucesso no bucket {destination_bucket}."
        }

    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Erro ao processar arquivo: {str(e)}"
        }
