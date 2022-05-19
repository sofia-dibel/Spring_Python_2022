import requests

name = input('Введите имя: ')
while True:
    text = input('Введите сообщение: ')
    response = requests.post('https://52d4-80-250-174-190.eu.ngrok.io/send',
                             json={
                                 'name': name,
                                 'text': text
                             }
                            )
