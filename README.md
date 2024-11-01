# API de Automação Residencial

## Visão Geral

Esta é uma API HTTP local projetada para automação residencial e assistência pessoal. Atualmente implementada com feedback de voz e sistemas de alarme, esta API serve como base para uma solução abrangente de automação residencial.

## Começando

1. Clone o repositório
2. Instale as dependências necessárias
3. Configure seu nome de usuário e senha no script
4. Execute o servidor: `python main.py`
5. A API estará disponível em `http://localhost:8000`

## Funcionalidades Atuais

### 1. Serviço de Texto para Voz (`api/speak`)

- Converte texto em voz em vários idiomas (padrão: Português)
- Suporte para:
  - Conversão regular de texto para voz
  - Conversão de áudio em código Morse
  - Anúncios em loop (útil para testes ou notificações periódicas)
  - Funcionalidade de parada de alarme

### 2. Sistema de Alarme (`api/alarm`)

- Agende alarmes usando formato 24 horas (HH_MM)
- Agendamento automático para o próximo dia se o horário especificado já passou
- Confirmação por voz quando o alarme é definido
- Som de alarme personalizável

## Segurança

- Autenticação Básica implementada
- Todos os endpoints requerem autenticação
- Nome de usuário e senha configuráveis

## Detalhes Técnicos

- Construído com `http.server` do Python
- Usa gTTS (Google Text-to-Speech) para síntese de voz
- FFplay para reprodução de áudio
- Comunicação baseada em JSON

## Possíveis Aplicações Futuras

### Sistemas de Segurança

- Notificações de detector de movimento
- Integração com câmeras de segurança
- Alertas de sensores de portas/janelas
- Controle de portão de garagem
- Integração com campainha com anúncios de voz

### Automação Residencial

- Controle de iluminação inteligente
- Monitoramento de temperatura e controle de HVAC
- Sistemas automatizados de irrigação
- Monitoramento de consumo de energia
- Controle de eletrodomésticos inteligentes

### Assistente Pessoal

- Anúncios de agenda diária
- Atualizações meteorológicas
- Resumos de notícias
- Lembretes de medicação
- Notificações de reuniões

### Entretenimento

- Controle de reprodução de música
- Integração com Smart TV
- Controle de voz para sistemas de jogos
- Controle de iluminação para festas

### Automação de Utilidades

- Sistemas de backup automatizados
- Monitoramento de rede
- Verificações de saúde do servidor
- Tarefas periódicas de manutenção

## Exemplos de Uso da API

### Texto para Voz

```bash
curl -X POST http://localhost:8000/api/speak \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -H "Content-Type: application/json" \
  -d '{"phrase": "Olá Mundo", "lang": "pt"}'
```

### Configurando um Alarme

```bash
curl -X POST http://localhost:8000/api/alarm \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -H "Content-Type: application/json" \
  -d '{"alarm": true, "time": "07_30"}'
```

## Acesso Remoto

Embora esta API seja projetada para execução local, ela pode ser exposta com segurança à internet usando [Tailscale](https://tailscale.com/). O Tailscale fornece uma rede mesh segura e criptografada que permite acessar sua API de automação residencial de qualquer lugar do mundo, sem comprometer a segurança.

Benefícios do uso do Tailscale:

- Criptografia ponta a ponta
- VPN sem configuração
- Não requer redirecionamento de porta
- Controle de acesso e autenticação
- Suporte a autenticação multifator

## Requisitos de Instalação

- Python 3.x
- gTTS (`pip install gTTS`)
- FFplay (parte do FFmpeg)
- Tailscale (opcional, para acesso remoto)


## Contribuindo

Sinta-se à vontade para fazer um fork deste projeto e adicionar suas próprias funcionalidades de automação. A natureza modular da API facilita a extensão com novos endpoints e funcionalidades.

## Melhorias Técnicas Propostas

### Alta Prioridade

1. **Refatoração da Estrutura Base**
   - Separar handlers em classes específicas (`SpeakHandler`, `AlarmHandler`)
   - Implementar padrão de configuração usando `dotenv` ou `yaml`
   - Mover credenciais para variáveis de ambiente
   - Criar classe base para gerenciamento de áudio

2. **Gerenciamento de Arquivos**
   - Implementar sistema de limpeza automática de arquivos MP3
   - Criar diretório temporário dedicado para arquivos de áudio
   - Usar `tempfile` para nomes únicos de arquivos
   - Implementar mecanismo de cache para frases comuns

3. **Tratamento de Erros**
   - Adicionar logging estruturado com `logging`
   - Implementar tratamento específico para erros de gTTS
   - Melhorar mensagens de erro para o cliente
   - Validar parâmetros de entrada com schemas

4. **Melhorias no Sistema de Alarme**
   - Implementar persistência de alarmes
   - Adicionar suporte a alarmes recorrentes
   - Criar sistema de fila para múltiplos alarmes
   - Melhorar o gerenciamento de processos do `ffplay`

5. **Segurança**
   - Implementar rate limiting por IP
   - Adicionar sistema de tokens JWT
   - Criar diferentes níveis de acesso
   - Implementar HTTPS

6. **Otimização de Performance**
   - Implementar pool de threads para processos longos
   - Adicionar cache para requisições frequentes
   - Otimizar chamadas do sistema de arquivos
   - Implementar timeout para requisições

7. **Documentação e Testes**
   - Adicionar docstrings em todas as funções
   - Criar testes unitários
   - Implementar documentação OpenAPI/Swagger
   - Adicionar exemplos de uso em `curl` e `Python`

8. **Funcionalidades Adicionais**
   - Suporte a diferentes vozes/engines TTS
   - Sistema de notificação de status
   - Interface web simples
   - Endpoints de healthcheck

9. **Melhorias na API**
   - Versionamento de API (`v1/`, `v2/`)
   - Respostas HTTP mais detalhadas
   - Suporte a CORS
   - Paginação para endpoints futuros

10. **DevOps**
    - Dockerização da aplicação
    - Scripts de backup
    - Monitoramento de recursos
    - Logs estruturados em JSON

## Licença

Este projeto é de código aberto, sinta-se à vontade para usar e modificar conforme suas necessidades.
