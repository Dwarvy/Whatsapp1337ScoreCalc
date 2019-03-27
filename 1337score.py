#!/usr/bin/python3
import telebot
import operator
from flask import Flask, request
import time
from subprocess import call
from secrets import * #For all personal information like blacklists, address books, bot_tokens, special urls, etc...
import WhatsappChatExportParser

people = {}
datesChecked = []

bot = telebot.TeleBot(token=bot_token, threaded=False)
bot.remove_webhook()
time.sleep(0.1)
bot.set_webhook(url=url)

app = Flask(__name__)

@app.route('/'+secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

def scoreCalcNL(lines):
    global people
    global datesChecked
    for line in lines:
        if len(line) >= 6:
            if line[2] != "-" or line[5] != "-":
                continue
            line = line.replace('\\xe2\\x80\\xaa', "").replace('\\xe2\\x80\\xac', "")
            date = line[:8]
            if date not in datesChecked:
                time = line[9:14]
                if time == "13:37":
                    message = line[line.find(":",  15)+1:]
                    if message.strip() == "1337":
                        person = line[17:line.find(":",  15)]
                        if person in addressBook:
                            person = addressBook[person]
                        if person not in blacklist:
                            if person not in people:
                                people[person] = 1
                            else:
                                people[person] += 1
                            datesChecked += [date]

def scoreCalcEN(chat):
    global people
    global datesChecked
    WON = 5
    for line in chat.lines:
        pLine = chat.parseLine(line)
        if pLine == "ERROR":
            continue
        WinningConditions = pLine.date not in datesChecked
        
        WinningConditions += pLine.time == "13:37"
        WinningConditions += pLine.message == "1337"
        
        person = pLine.person
        if person in addressBook:
            person = addressBook[person]
            WinningConditions += 1
        
        WinningConditions += person not in blacklist
        
        if WinningConditions == WON:
            if person not in people:
                people[person] = 1
            else:
                people[person] += 1
            datesChecked += [date]

def calculateScore(chat):

    if chat.lang == "NL":
        scoreCalcNL(chat)
    elif chat.lang == "EN":
        scoreCalcEN(chat)

    sorted_people = sorted(people.items(), key=operator.itemgetter(1))

    scoreBoard = ""
    for person in sorted_people:
        scoreBoard += str(person[0]) + ": " + str(person[1]) + "\n"

    scoreBoard += "\n\nDays of 1337: " + str(len(datesChecked))

    return scoreBoard

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'To calculate whatsapp 1337 score, please send me an export of your whatsapp group chat. (export without media)')

@bot.message_handler(commands=['help'])
def start(m):
    bot.send_message(m.chat.id, 'On android: \n-Navigate to your whatsapp chat \n-Tap the three dots \n-Tap "more" \n-Tap "export chat" \n-Share the export with this bot')
    bot.send_message(m.chat.id, '/help - this message')
    
@bot.message_handler(commands=['share'])
def share(m):
    bot.send_message(m.chat.id, my_secret_share_url)

def detectLang(line):
    if line.find(',') < 15:
        lang = "EN"
        print("English detected")    
    elif line.find('-') < 5:
        lang = "NL"
        print("Dutch detected")

@bot.message_handler(content_types=['document'])
def handle_docs_audio(m):
    global people
    global datesChecked
    people = {}
    datesChecked  = []
    file_info = bot.get_file(m.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    chat = WhatsappChatExportParser.WhatsappChat(downloaded_file)

    print("File Info:\n" + str(file_info) + "\n\n")
    
    scoreBoard = calculateScore(chat)
    bot.send_message(m.chat.id, scoreBoard)
    """
    call(["adb", "kill-server"])
    call(["adb", "start-server"])
    call(["/home/pi/scripts/Android/unlockPhone.sh"])
    call(["/home/pi/scripts/Android/homePhone.sh"])
    call(["/home/pi/scripts/Android/wa/startWhatsapp.sh"])
    scoreBoard = scoreBoard.replace("\n", chr(10))
    call(["/home/pi/scripts/Android/typeText.sh", scoreBoard])
    call(["/home/pi/scripts/Android/wa/pressWhatsappSendButton.sh"])
    call(["/home/pi/scripts/Android/wa/exitWhatsapp.sh"])
    call(["/home/pi/scripts/Android/lockPhone.sh"])"""


@bot.message_handler(content_types=['text'])
def start(m):
    bot.send_message(m.chat.id, "I don't know what you mean by that. Type /help for help and send me the export txt file.")

@bot.message_handler(content_types=['photo', 'audio'])
def start(m):
    bot.send_message(m.chat.id, 'I\'m sorry, I cannot handle this message type, just send me the export txt file.')

app.run(
    host="0.0.0.0",
    port=int(port),
    debug=True,
    ssl_context=my_secret_ssl_context
)
#----------------------------------------------------------------------------------------------------------------------
