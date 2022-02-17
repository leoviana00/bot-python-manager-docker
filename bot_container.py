# -------------------
# imports
# -------------------
from urllib import response
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import randint
from credentials import *
from functions import *
import docker
import os
import logging
from colorama import init, Fore, Style
init()
import asyncio

# Configure logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# ------------------------
# Docker - Integração
# ------------------------
HOST_DOCKER = 'unix://var/run/docker.sock'
client = docker.DockerClient(base_url=HOST_DOCKER)

# -------------------
# Integração Telegram
# -------------------
bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

# ------------------------
# Inicializando o bot
# ------------------------
if os.name == 'posix':
    print(Fore.YELLOW +'DEVOPS - DOCKER MANAGEMENT .', Style.RESET_ALL)
    print(Fore.YELLOW +'APLICAÇÃO PYTHON PARA GERENCIAR CONTAINER.', Style.RESET_ALL)
    input('Pressione ENTER para inicializar o bot...\n') 

if os.name != 'nt' and os.name != 'posix':
    print(Fore.RED +'Seu sistema operacional não é compatível.', Style.RESET_ALL)
    os._exit(0)


# -------------------
# Keyboard
# -------------------
keyboard_inline = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("📝 Listar containers", "🚫 Parar containers", "🤖 Verificar Comandos", "❇️ Docker Version")


#--------------------
# Lista de comandos
#--------------------
server = '192.168.0.20'
commands_list = """
/start
/help
"""

#--------------------
# DevOps
#--------------------
@dp.message_handler(commands=['start'], state = '*')
async def devops(message: types.Message):
    with open('data/devops.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption=f'🖥  Servidor: {server} \n👻  DevOps estão aqui! \n🕹  Comandos: \n {commands_list}')

#--------------------
# Start - Help
#--------------------
@dp.message_handler(commands=['help'], state = '*')
async def welcome(message: types.Message):
    await message.reply(f"""
    Olá! Seja bem vindo ao grupo de gerenciamento de aplicações docker que estão no server {server}, escolha uma das opções abaixo para continuar: """
    , reply_markup=keyboard_inline)

#--------------------
# list - stop - commands - docker version
#--------------------
@dp.message_handler()
async def manager_answer(message: types.Message):

    if message.text == '🤖 Verificar Comandos':
        await message.reply(f'Lista de comandos: {commands_list}')

    elif message.text == '❇️ Docker Version':
        await message.reply(info())

    elif message.text == '📝 Listar containers':
        await message.reply(list())

    elif message.text == '🚫 Parar containers':
        texto = ''
        buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        container_list = client.containers.list() 
        for container in container_list:
            texto = container.name
            button = InlineKeyboardButton(texto, callback_data = 'callback')
            buttons.add(button) 
        await message.reply("Qual container que deseja parar?", reply_markup=buttons) 

    else:
        container = client.containers.get(f'{message.text}')
        container.stop()
        await message.reply(f"Container `{message.text}` foi parado! Caso deseje voltar para o menu, clique aqui:  /menu")


async def notify_message():
    await bot.send_message(chat_id,'🤖 Bot inicializado...\n🕹 Comandos: \n /start \n /help')
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(notify_message()) # Function to execute
    executor.start_polling(dp, skip_updates=True)
