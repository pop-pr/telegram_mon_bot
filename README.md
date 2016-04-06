# telegram_mon_bot

Bot para realizar ping, traceroute e consultas em sistemas de monitoramento com suporte a Livestatus via Telegram. Realiza os comandos definidos apenas para os chat_ids autorizados definidos em um arquivo config.ini. 

### Dependências
* [python-telegram-bot] - Wrapper Python para a API do Telegram.
* [python-mk-livestatus] - Wrapper Python para a API Livestatus.

Caso utilize o pip, basta utilizar o comando `sudo pip install -r requirements.txt` para instalar as dependências.

### Configuração

1. Inserir o token da API HTTP do bot na variável "bot_id" do arquivo "config.ini"
2. Inserir os chat_ids autorizados a utilizar o bot na variável "authorized_chat_ids" do arquivo "config.ini", separados por vírgula.
3. Executar o arquivo "bot.py" via nohup ou cron.

### Comandos disponíveis

* /down: Consulta os hosts offline no monitoramento via Livestatus.
* /ping: Realiza ping IPv4.
    *  /ping 8 www.google.com: 8 pacotes
    *  /ping www.google.com: 5 pacotes (padrão)
* /ping6: Realiza ping IPv6.
    *  /ping6 8 www.google.com: 8 pacotes
    *  /ping6 www.google.com: 5 pacotes (padrão)
* /traceroute: Traceroute ICMP IPv4.
* /traceroute6: Traceroute ICMP IPv6.


### Observações

1. A máquina hospedeira do bot deve ter IPv6 configurado para que os comandos que utilizam IPv6 funcionem.
2. Caso não utilize o bot no mesmo host de sua API Livestatus, modifique a abertura do socket de 127.0.0.1 para o endereço correspondente na função auth_probe.


   [python-telegram-bot]: <https://pypi.python.org/pypi/python-telegram-bot>
   [python-mk-livestatus]:  <https://pypi.python.org/pypi/python-mk-livestatus/0.3>
