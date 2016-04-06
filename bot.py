#!/usr/bin/python
# -*- coding: UTF-8 -*-

# telegram_mon_bot
# Copyright 2016 RNP - Rede Nacional de Ensino e Pesquisa
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

""" 
Codigo principal para o funcionamento do bot, 
escrito conforme especificacoes do wrapper Python
python-telegram-bot sobre a API Telegram.
"""

import logging
import commands
import sys
import datetime
import re

# pacotes de parsing, comunicacao via Livestatus e telegram bot
from ConfigParser import SafeConfigParser
from mk_livestatus import Socket
from telegram import Updater

# configuracoes do log
logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(name)s] [%(levelname)s] %(message)s ')
logger = logging.getLogger(__name__)


def readconf(inifile='./config.ini'):
    """Usa o ConfigParser para ler um arquivo ini com variaveis de configuracao"""
    cp = SafeConfigParser()
    cp.read(inifile)

    if "telegram_mon_bot" in cp.sections():
        conf_values = dict(cp.items('telegram_mon_bot'))
    else:
        conf_values = {}
        print 'Erro lendo arquivo de configuracao. Confira o exemplo em github.com/PoP-PR'
        sys.exit(0)
    return conf_values

config = readconf()


def auth_probe(auth_id_list, update_id, op):
    """Autentica buscando um chat_id dentro de uma lista"""
    if str(update_id) in auth_id_list:
        # abre o socket Livestatus apenas depois da autenticacao
        # e apenas para as operacoes que precisam do socket
        if op in('down'):
            s = Socket(('127.0.0.1', 50000))
            return True, s
        else:
            return True, False
    else:
        return False, False


def start(bot, update, auth_ids=config['authorized_chat_ids'].split(',')):
    """Handler da mensagem start"""
    op = start.__name__
    if auth_probe(auth_ids, update.message.chat_id, op)[0]:
        print auth_probe(auth_ids, update.message.chat_id)[0]
        bot.sendMessage(chat_id=update.message.chat_id, text="Seja bem vindo! Comandos disponiveis: ping, ping6, traceroute e traceroute6.")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Voce nao possui autorizacao para executar comandos.")


def help(bot, update, auth_ids=config['authorized_chat_ids'].split(',')):
    """Handler da mensagem help"""
    op = help.__name__

    # tenta autenticar o ID do remetente na lista de autorizados
    if auth_probe(auth_ids, update.message.chat_id, op)[0]:
        # envio das mensagens de ajuda
        bot.sendMessage(chat_id=update.message.chat_id, text="/ping[6] [PACKETS] [IP|FQDN]: O primeiro argumento deve ser o numero de pacotes no ping. Caso um numero de pacotes nao seja definido, serao enviados 5 pacotes. O segundo argumento deve ser um IP ou FQDN.")
        bot.sendMessage(chat_id=update.message.chat_id, text="/traceroute[6]: O único argumento passado deve ser um IP ou FQDN.")
        bot.sendMessage(chat_id=update.message.chat_id, text="/down: Retorna uma lista com os hosts em estado DOWN no sistema de monitoramento.")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Voce nao possui autorizacao para executar comandos.")


def ping(bot, update, args, auth_ids=config['authorized_chat_ids'].split(',')):
    """Handler da mensagem ping"""
    op = ping.__name__

    # tenta autenticar o ID do remetente na lista de autorizados
    if auth_probe(auth_ids, update.message.chat_id, op)[0]:
        # validacao de sintaxe e parse (1 argumento = 5 pacotes, 2 argumentos = n pacotes)
        if len(args) == 2:
            # executa o ping com n pacotes e envia a resposta
            bot.sendMessage(chat_id=update.message.chat_id, text="Iniciando ping IPv4 para " + args[-1] + " com " + args[-2] + " pacotes. Isto pode demorar!")
            run_ping = commands.getoutput('ping -c %s %s' % (args[-2], args[-1]))
            bot.sendMessage(chat_id=update.message.chat_id, text=run_ping)
        elif len(args) == 1:
            # executa o ping com n pacotes e envia a resposta
            bot.sendMessage(chat_id=update.message.chat_id, text="Iniciando ping IPv4 padrao para " + args[0] + ".")
            run_ping = commands.getoutput('ping -c 5 %s' % (args[0]))
            bot.sendMessage(chat_id=update.message.chat_id, text=run_ping)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Sintaxe invalida. Use o comando /help para mais informacoes. Exemplo: /ping www.rnp.br 5")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Voce nao possui autorizacao para executar comandos.")


def ping6(bot, update, args, auth_ids=config['authorized_chat_ids'].split(',')):
    """Handler da mensagem ping6"""
    op = ping6.__name__

    # tenta autenticar o ID do remetente na lista de autorizados
    if auth_probe(auth_ids, update.message.chat_id, op)[0]:
        # validacao de sintaxe e parse (1 argumento = 5 pacotes, 2 argumentos = n pacotes)
        if len(args) == 2:
            # executa o ping com n pacotes e envia a resposta
            bot.sendMessage(chat_id=update.message.chat_id, text="Iniciando ping IPv4 para " + args[-1] + " com " + args[-2] + " pacotes. Isto pode demorar!")
            run_ping = commands.getoutput('ping6 -c %s %s' % (args[-2], args[-1]))
            bot.sendMessage(chat_id=update.message.chat_id, text=run_ping)
        elif len(args) == 1:
            # executa o ping com 5 pacotes e envia a resposta
            bot.sendMessage(chat_id=update.message.chat_id, text="Iniciando ping IPv6 padrao para " + args[0] + ".")
            run_ping = commands.getoutput('ping6 -c 5 %s' % (args[0]))
            bot.sendMessage(chat_id=update.message.chat_id, text=run_ping)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Sintaxe invalida. Use o comando /help para mais informacoes. Exemplo: /ping6 www.rnp.br 5")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Voce nao possui autorizacao para executar comandos.")


def traceroute(bot, update, args, auth_ids=config['authorized_chat_ids'].split(',')):
    """Handler da mensagem traceroute"""
    op = traceroute.__name__

    # tenta autenticar o ID do remetente na lista de autorizados
    if auth_probe(auth_ids, update.message.chat_id, op)[0]:
        # validacao de sintaxe
        if len(args) == 1:
            # executa o traceroute e envia a resposta
            bot.sendMessage(chat_id=update.message.chat_id, text="Iniciando traceroute IPv4 para " + args[0] + ". Isto pode demorar!")
            run_traceroute = commands.getoutput('traceroute -I %s' % (args[0]))
            bot.sendMessage(chat_id=update.message.chat_id, text=run_traceroute)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Sintaxe invalida. Use o comando /help para mais informacoes. Exemplo: /traceroute www.rnp.br")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Voce nao possui autorizacao para executar comandos.")


def traceroute6(bot, update, args, auth_ids=config['authorized_chat_ids'].split(',')):
    """Handler da mensagem traceroute6"""
    op = traceroute6.__name__

    # tenta autenticar o ID do remetente na lista de autorizados
    if auth_probe(auth_ids, update.message.chat_id, op)[0]:
        # validacao de sintaxe
        if len(args) == 1:
            # executa o traceroute e envia a resposta
            bot.sendMessage(chat_id=update.message.chat_id, text="Iniciando traceroute IPv6 para " + args[0] + ". Isto pode demorar!")
            run_traceroute = commands.getoutput('traceroute6 -I %s' % (args[0]))
            bot.sendMessage(chat_id=update.message.chat_id, text=run_traceroute)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Sintaxe invalida. Use o comando /help para mais informacoes. Exemplo: /traceroute6 www.rnp.br")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Voce nao possui autorizacao para executar comandos.")


def down(bot, update, auth_ids=config['authorized_chat_ids'].split(',')):
    """Handler da mensagem down"""
    op = down.__name__
    socket = auth_probe(auth_ids, update.message.chat_id, op)[1]

    # tenta autenticar o ID do remetente na lista de autorizados
    if auth_probe(auth_ids, update.message.chat_id, op)[0]:
        # envia a requisicao para o livestatus
        q = socket.hosts.columns('name').filter('state = 1').filter('acknowledged = 0')
        # parse da resposta
        r = str(q.call())
        r = eval(r)
        l = ""
        for host in r:
            l += "%s\n" % (host["name"])
        # envio da resposta
        bot.sendMessage(chat_id=update.message.chat_id, text="\nHosts offline em " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M') + "\n\n" + l)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Voce nao possui autorizacao para executar comandos.")

def error(bot,update,error):
    """Imprime o erro no log"""
    logger.warn('Update %s causou erro %s' % (update, error))

def main():
    updater = Updater(config['bot_id'], workers=5)
    dispatcher = updater.dispatcher
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addTelegramCommandHandler('ping', ping)
    dispatcher.addTelegramCommandHandler('ping6', ping6)
    dispatcher.addTelegramCommandHandler('traceroute', traceroute)
    dispatcher.addTelegramCommandHandler('traceroute6', traceroute6)
    dispatcher.addTelegramCommandHandler('down', down)
    dispatcher.addErrorHandler(error)
    updater.start_polling()


if __name__ == '__main__':
    main()
