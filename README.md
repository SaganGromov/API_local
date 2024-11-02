# API Residencial Assistente - Documentação

Este documento detalha todas as funcionalidades presentes na API residencial assistente, exemplos de uso com `curl`, funcionalidades futuras que podem ser implementadas, e melhorias técnicas propostas.

## Funcionalidades Atuais

### 1. /api/speak
- **Descrição**: Converte texto em áudio e reproduz na saída de áudio.
- **Parâmetros**:
  - `phrase` (obrigatório): Texto a ser convertido e reproduzido.
  - `lang` (opcional): Idioma para o áudio gerado (padrão: `pt`).
  - `loop` (opcional): Define se o áudio deve ser repetido três vezes.
  - `morse` (opcional): Converte e toca a frase em código Morse.
- **Exemplo**:

```bash
curl -X POST http://localhost:8000/api/speak \
     -u user:pass \
     -H "Content-Type: application/json" \
     -d '{"phrase": "Bom dia!", "lang": "pt", "loop": true}'
```

### 2. /api/alarm
- **Descrição**: Configura um alarme para reproduzir um som em um horário específico.
- **Parâmetros**:
  - `time` (obrigatório): Horário do alarme no formato `HH_MM`.
  - `alarm` (obrigatório): Indica a configuração do alarme.
- **Exemplo**:

```bash
curl -X POST http://localhost:8000/api/alarm \
     -u user:pass \
     -H "Content-Type: application/json" \
     -d '{"alarm": true, "time": "08_30"}'
```

### 3. /api/disable_alarms
- **Descrição**: Desativa todos os alarmes ativos e pendentes, interrompendo qualquer áudio em execução.
- **Exemplo**:

```bash
curl -X POST http://localhost:8000/api/disable_alarms \
     -u user:pass \
     -H "Content-Type: application/json"
```

## Funcionalidades Futuras (Sugestões)

Aqui estão algumas funcionalidades criativas e naturais que podem ser implementadas no futuro:

1. **Controle de iluminação**: Integração com dispositivos de iluminação para acender/apagar luzes via comandos da API.
2. **Controle de temperatura**: Ajuste de termostatos para regular a temperatura ambiente.
3. **Controle de cortinas**: Abrir e fechar cortinas de forma remota.
4. **Automatização de segurança**: Ativação de alarmes e fechaduras de portas.
5. **Notificações de eventos**: Envio de notificações para atividades suspeitas, visitantes, ou alarmes importantes.
6. **Integração com assistentes de voz**: Conectar a API com Google Assistant ou Alexa.
7. **Modo de economia de energia**: Reduzir a iluminação e ajustar a temperatura quando ninguém estiver em casa.
8. **Monitoramento de qualidade do ar**: Exibir dados sobre poluição e alertar para ventilação quando necessário.
9. **Controle de entretenimento**: Comandos para TV e dispositivos de streaming.
10. **Integração com calendário**: Programação de alarmes com base em eventos de calendário.

## Seção de TODOs - Melhorias Técnicas

Abaixo estão melhorias técnicas sugeridas para aprimorar a API, listadas em ordem de prioridade:

1. **Adicionar autenticação JWT** para maior segurança.
2. **Gerenciamento de sessões e limite de requisições** para prevenir abuso da API.
3. **Implementar logging avançado** para monitoramento de requisições e respostas.
4. **Gerenciamento de processos aprimorado** para interromper comandos específicos de `sleep` e `ffplay`.
5. **Testes unitários e de integração** para validar funcionalidades.
6. **Configuração de variáveis de ambiente** para facilitar o uso em diferentes ambientes.
7. **Integração com banco de dados** para salvar logs e preferências do usuário.
8. **Implementar fila de tarefas** para agendamento e gerenciamento de comandos de longo prazo.
9. **Suporte a WebSocket** para atualizações em tempo real.
10. **Adicionar documentação Swagger** para visualização de endpoints.

## Expondo a API para Controle Externo Seguro

É possível expor esta API para acesso externo de forma segura utilizando [Tailscale](https://tailscale.com/), uma VPN simples de configurar que permite acesso seguro à sua rede local pela internet.
- **Configuração**: Após instalar e configurar o Tailscale, você pode expor o endereço local da API (por exemplo, `http://localhost:8000`) e controlá-la remotamente com segurança.
- **Benefícios**: Isso torna possível monitorar e controlar os dispositivos conectados à API, como alarmes e outros dispositivos automatizados, de qualquer lugar com segurança.
