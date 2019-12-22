import vk_api.vk_api
import random
import urllib.request, json 
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import requests
import time, os
import string
import datetime
import requests
import lxml.html as html
import apiai #ИИ
class Server:

            def __init__(self, api_token, group_id, server_name: str="Empty"):

                # Даем серверу имя
                self.server_name = server_name

                # Для Long Poll
                self.vk = vk_api.VkApi(token=api_token)

                self.upload = vk_api.VkUpload(self.vk)

                # Для использования Long Poll API
                self.long_poll = VkBotLongPoll(self.vk, group_id)

                # Для вызова методов vk_api
                self.vk_api = self.vk.get_api()

            def send_img(self, send_id, message):
                """
                Отправка сообщения через метод messages.send
                :param send_id: vk id пользователя, который получит сообщение
                :param message: содержимое отправляемого письма
                :return: None
                """
                self.vk_api.messages.send(peer_id=send_id,
                                          attachments=attachments,
                                          random_id=123456 + random.randint(1,27))

            def send_msg(self, send_id, message):
                """
                Отправка сообщения через метод messages.send
                :param send_id: vk id пользователя, который получит сообщение
                :param message: содержимое отправляемого письма
                :return: None
                """
                self.vk_api.messages.send(peer_id=send_id,
                                          message=message,
                                          random_id=123456 + random.randint(1,27))
            def start(self):
                for event in self.long_poll.listen():
                    print(event.object.text, " ", event.object.from_id)
                    lst = event.object.text
                    if event.object.from_id>0:
                        
                        request = apiai.ApiAI('e495f56e5266410ab8a0ab4f6081f003').text_request() # Токен API к Dialogflow
                        request.lang = 'ru' # На каком языке будет послан запрос
                        request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
                        request.query = lst # Посылаем запрос к ИИ с сообщением от юзера
                        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
                        response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
                        # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
                        try:
                            self.send_msg(event.object.peer_id, response)
                        except:
                            self.send_msg(event.object.peer_id, 'Я Вас не совсем понял!')



if __name__ ==  "__main__":
    server1 = Server("токен группы", id группы, "server1")
    server1.start()
