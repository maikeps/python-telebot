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
operating_mode = 'echo'

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
						print('Changind mode to '+new_mode)
						operating_mode = new_mode
				elif message == '/help':
					bot.sendMessage(chat_id=chat_id, text='Write /set_mode {voice, echo} and start talking to me!')
				elif message[0] != '/':
					if operating_mode == 'echo':
						print('Sending echo')
						bot.sendMessage(chat_id=chat_id, text=message)
					elif operating_mode == 'voice':
						print('Sending audio')
						tts = gTTS(text=message, lang='en')
						tts.save('audio.mp3')

						bot.sendVoice(chat_id=chat_id, voice=open('audio.mp3', 'rb'))

		with open('last_update', 'w') as f:
			f.write(str(LAST_UPDATE_ID))
			f.close()