from mathgenerator import mathgen
from aiogram import Bot, Dispatcher, executor, types
import cherrypy

API_TOKEN = '1365149697:AAFEpRi2sX9a6nfGNt-CerZv_1UyPCpkLds'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

WEBHOOK_HOST = '195.211.140.191'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '195.211.140.191'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет, вы ведь понимаете почему пришли ко мне?")

@dp.message_handler(commands=['gen'])
async def generator(message:types.Message):
    global problem, solution
    problem, solution = mathgen.division()
    await bot.send_message(message.from_user.id, problem + 'x')
    print('Ответ: ' + solution)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Бот, для мучений.\nНужно решить n+n предметов, и тогда всё получится.\nНо пытливый ум спросит, зачем всё это?\nЯ отвечу: "Сам не знаю, бог меня сюда послал.."')

@dp.message_handler(content_types=['text'])
async def gen(message: types.Message):
    if message.text == solution:
        await message.reply('Gений.. /gen')
    if message.text != solution:
        await message.reply('Плохой из тебя калькулятор.\n- Сложно? \n- /gen')


# Наш webhook-сервер 
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

if __name__ == '__main__':
    executor.start_polling(dp)
