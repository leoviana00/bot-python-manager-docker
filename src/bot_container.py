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


# -------------------
# Novo keyboard
# -------------------
keyboard_inline = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("📝 Listar containers", "🚫 Parar containers", "🤖 Verificar Comandos", "📝 Docker Info")


#--------------------
# Lista de comandos
#--------------------
commands_list = """
/start
/help
/menu  # Lista todos os botões disponíveis até o momento
"""

#--------------------
# Menu
#--------------------
@dp.message_handler(commands=['menu'])
async def random_answer(message: types.Message):
    await message.reply("Selecione a opção desejada:", reply_markup=keyboard_inline)

#--------------------
# Start - Help
#--------------------
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Olá! Eu sou o Docker Bot, Escolha uma das opções abaixo para continuar", reply_markup=keyboard_inline)

#--------------------
# list - stop - commands - docker info
#--------------------
@dp.message_handler()
async def manager_answer(message: types.Message):
    if message.text == '🤖 Verificar Comandos':
        await message.reply(f'Lista de comandos: {commands_list}')
    elif message.text == '📝 Docker Info':
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


executor.start_polling(dp)