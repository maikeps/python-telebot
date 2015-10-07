import telegram
from gtts import gTTS

# Init
with open('token', 'r') as token_file:
	token = token_file.readline()

LAST_UPDATE_ID = 0
with open('last_update', 'r') as f:
    LAST_UPDATE_ID = int(f.readline().strip())
    f.close()

bot = telegram.Bot(token)

modes = ['echo', 'voice']
languages = ['af', 'sq', 'ar', 'hy', 'ca', 'zh-CN', 'zh-TW', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'fi', 'fr', 'de', 'el', 'ht', 'hi', 'hu', 'is', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'no', 'pl', 'pt', 'ru', 'sr', 'sk', 'es', 'sw', 'sv', 'ta', 'th', 'tr', 'vi', 'cy']
operating_mode = 'echo'
language = 'en'

# Operation
while True:
	updates = bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10)
	for update in updates:
		if LAST_UPDATE_ID < update.update_id:
			LAST_UPDATE_ID = update.update_id
			chat_id = update.message.chat_id
			message = update.message.text

			if message:
				if '/set_mode' in message:
					new_mode = message.replace('/set_mode ', '', 1)
					if new_mode in modes:
						print('Changing mode to '+new_mode)
						operating_mode = new_mode
					else:
						bot.sendMessage(chat_id=chat_id, text='Sorry, I don\'t know what is this mode you wanted :(')

				elif '/set_language' in message:
					new_language = message.replace('/set_language ', '', 1)
					if new_language in languages:
						print('Changing language to '+new_language)
						language = new_language
					else:
						bot.sendMessage(chat_id=chat_id, text='Sorry, I don\'t speak this language :(')						

				elif message == '/help':
					bot.sendMessage(chat_id=chat_id, text='Write /set_mode {voice, echo} and start talking to me!\nPlus, you can set my language with /set_language <language code>.')

				elif message[0] != '/':
					if operating_mode == 'echo':
						print('Sending echo')
						bot.sendMessage(chat_id=chat_id, text=message)

					elif operating_mode == 'voice':
						print('Sending audio')
						tts = gTTS(text=message, lang=language)
						tts.save('audio.mp3')

						bot.sendVoice(chat_id=chat_id, voice=open('audio.mp3', 'rb'))

		with open('last_update', 'w') as f:
			f.write(str(LAST_UPDATE_ID))
			f.close()