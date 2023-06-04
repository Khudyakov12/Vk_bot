# импорты
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from core import VkTools
from data_store import add_user, check_user


class BotInterface():

    def __init__(self, comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.params = None
        self.offset = 0

    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id()
                               }
                              )
    def this_hometown(self, command):  # this hometown?
        i = self.params['bdate']
        j = self.params['hometown']
        self.params['bdate'] = "20"
        self.params['hometown'] = command.title()
        users = self.api.search_users(self.params, self.offset)
        if len(users) == 0:
            self.params['bdate'] = i
            self.params['hometown'] = j
            return False
        else:
            self.params['bdate'] = i
            self.params['hometown'] = j
            return True


    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'здравствуй {self.params["name"]}')
                    if(self.params['hometown'] == None):
                        self.message_send(event.user_id, f'Введите ваш город')

                elif (self.params != None and self.params['hometown'] == None):
                    if (command.title().isalpha() and self.this_hometown(command)):
                        self.params['hometown'] = command.title()
                        print(self.params)
                        if (self.params['bdate'] == None):
                            self.message_send(event.user_id, f'Введите ваш возраст')
                        else:
                            self.message_send(event.user_id, f'Все готово для поиска')
                    else:
                        self.message_send(event.user_id, f'Неверно введен город')

                elif (self.params != None and self.params['bdate'] == None and self.params['hometown'] != None):
                    if command.isdigit():
                        self.params['bdate'] = command
                        self.message_send(event.user_id, f'Все готово для поиска')
                        print(self.params)
                    else:
                        self.message_send(event.user_id, f'Неверно введен возраст')



                elif command == 'поиск':
                    self.message_send(event.user_id,f'Идет поиск...')
                    users = self.api.search_users(self.params, self.offset)
                    self.offset += 10
                    while len(users) == 0:
                        print(len(users))
                        users = self.api.search_users(self.params, self.offset)
                    user = users.pop()

                    # здесь логика для проверки бд
                    while check_user(self.params['id'], user["id"]):
                        users = self.api.search_users(self.params, self.offset)
                        user = users.pop()
                        self.offset += 10
                        print(user['name'])

                    photos_user = self.api.get_photos(user['id'])

                    attachment = ''
                    for num, photo in enumerate(photos_user):
                        attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                        if num == 2:
                            break
                    self.message_send(event.user_id,
                                      f'Встречайте {user["name"]} \n vk.com/id{user["id"]}',
                                      attachment=attachment
                                      )
                    # здесь логика для добавленяи в бд
                    add_user(self.params['id'], user["id"])

                elif command == 'пока':
                    self.message_send(event.user_id, 'пока')
                elif (self.params == None or self.params['hometown'] != None and self.params['bdate'] != None):
                    self.message_send(event.user_id, 'команда не опознана')


if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()


