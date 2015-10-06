import json
import requests



last_update = 0
with open('last_update', 'r') as f:
    last_update = int(f.readline().strip())
    f.close()

with open('token', 'r') as token_file:
	token = token_file.readline()
	
url = 'https://api.telegram.org/bot'+token+'/'

while True:
	get_updates = json.loads(requests.get(url + 'getUpdates', params=dict(offset=last_update)).content.decode('utf-8'))

	for update in get_updates['result']:
		if last_update < update['update_id']:
			last_update = update['update_id']

			print('message received')

			if 'message' in update:
				requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text=update['message']['text']))

			
			with open('last_update', 'w') as f:
				f.write(str(last_update))
				f.close()