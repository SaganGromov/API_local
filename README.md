# API de Síntese de Voz

## Funcionalidades
- Conversão de texto para fala
- Suporte a múltiplos idiomas
- Autenticação básica HTTP
- Reprodução automática do áudio gerado

## Instalação
1. Clone o repositório
2. Instale as dependências Python:
```bash
pip install gtts
```
3. Instale o FFmpeg (necessário para o FFplay):
```bash
sudo apt-get install ffmpeg
```


## Configuração
As credenciais padrão são:
- Usuário: `user`
- Senha: `pass`

Para alterar as credenciais, modifique as constantes `USERNAME` e `PASSWORD` na classe `APIHandler`.

## Uso

### Iniciando o servidor
Execute o script Python:
```bash
python main.py
```
O servidor iniciará na porta 8000.

### Fazendo requisições
Para fazer uma requisição à API, use o seguinte formato:
```bash
curl -X POST http://localhost:8000/api/speak -H "Authorization: Basic dXNlcjpwYXNz" -H "Content-Type: application/json" -d '{"text": "Olá, como você está?"}'
```


#### Parâmetros
- `phrase`: Texto que será convertido em fala (obrigatório)
- `lang`: Código do idioma (opcional, padrão: "pt")
  - Exemplos: "pt" (português), "en" (inglês), "es" (espanhol), etc.

#### Resposta
A API retornará um JSON com o status da operação:

Sucesso:
```json
{
  "status": "success",
  "message": "Audio played for phrase: Olá, mundo! in language: pt"
}
```


## Códigos de Status HTTP
- 200: Requisição bem-sucedida
- 400: Parâmetros inválidos ou ausentes
- 401: Autenticação necessária ou inválida
- 404: Endpoint não encontrado
- 500: Erro interno do servidor

## Segurança
- A API utiliza autenticação básica HTTP
- Todas as requisições devem incluir um cabeçalho de autorização válido
- As credenciais são codificadas em base64

## Limitações
- O áudio é reproduzido no servidor, não no cliente
- Necessita de uma conexão com a internet para usar o serviço gTTS

## Expondo a API para Internet

Existem várias maneiras de disponibilizar a API para acesso externo. Você pode, por exemplo, utilizar o Ngrok. Após iniciar localmente o servidor da API via `python main.py`, você pode expor a API para acesso externo via:
```bash
ngrok http 8000
```
O Ngrok então fornecerá uma URL pública para acessar a API, por exemplo: `https://<id>.ngrok.app/api/speak`.
### Fazendo requisições externas
Para fazer uma requisição à API exposta externamente, use a URL fornecida pelo Ngrok no lugar de `localhost` na requisição original. Por exemplo:
```bash
curl -X POST \
  https://92832de0.ngrok.io/api/speak \
  -H 'Authorization: Basic dXNlcjpwYXNz' \
  -H 'Content-Type: application/json' \
  -d '{
    "phrase": "Olá, mundo!",
    "lang": "pt"
  }'
```
