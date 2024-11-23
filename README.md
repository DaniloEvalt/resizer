# AWS Lambda S3 Image Resizer

Este projeto é uma função AWS Lambda que redimensiona imagens carregadas em um bucket S3 de origem e salva as imagens redimensionadas em um bucket de destino. Ele usa o SDK AWS boto3 e a biblioteca Python Pillow (PIL) para manipulação de imagens.

## Visão Geral

1. Uma imagem é carregada no bucket S3 de origem.
2. Um evento do S3 aciona a função Lambda.
3. A função Lambda baixa a imagem, redimensiona para um máximo de 800x800 pixels e faz o upload para o bucket de destino.

---

## Pré-requisitos

- **AWS Account** com permissões para Lambda e S3.
- **Buckets S3**:
  - Bucket de origem (para upload das imagens).
  - Bucket de destino (para salvar as imagens redimensionadas).
- **Função Lambda** com a seguinte configuração:
  - **Runtime:** Python 3.10.
  - **Role IAM:** Com permissões para acessar os buckets S3.
- **Dependências** Adicionadas via Layer:
  - `boto3`
  - `Pillow`

---

## Configuração

### 1. Configurar os Buckets no S3
- Crie dois buckets no S3:
  - Um bucket de **origem** para armazenar as imagens originais.
  - Um bucket de **destino** para armazenar as imagens redimensionadas.

### 2. Configurar a Função Lambda
1. Crie uma função Lambda no console da AWS.
2. Faça upload do código Python para a função.
3. Configure as variáveis de ambiente:
   - `SOURCE_BUCKET`: Nome do bucket de origem.
   - `DESTINATION_BUCKET`: Nome do bucket de destino.
4. Adicione um gatilho S3 ao bucket de origem para eventos de upload (`s3:ObjectCreated:*`).
5. Adicione um Layer apontando para o ARN arn:aws:lambda:sa-east-1:770693421928:layer:Klayers-p310-Pillow:9 que ira resolver as dependencias do projeto.
6. Aumente o timeout da funcao, por padrao esta em 3 segundos e no meu caso foi aumentado para 30 segundos.

## Estrutura do codigo
.

├── lambda_function.py  # Código principal da função Lambda

├── requirements.txt    # Dependências do projeto

└── README.md           # Documentação do projeto

└── iam.json            # Modelo de role


## Logs e Debugging
Verifique os logs da Lambda no CloudWatch Logs em caso de falhas.
Mensagens comuns de erro:
Timeout: Aumente o timeout da Lambda se o processamento da imagem for lento.
Permissões S3: Certifique-se de que a policy IAM inclui acesso aos buckets.

## Contribuições
Sinta-se à vontade para abrir Issues ou enviar Pull Requests com melhorias e correções!

## Licença
Este projeto está licenciado sob a MIT License.
