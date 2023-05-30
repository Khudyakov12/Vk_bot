import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = "vk1.a.HMdCBEMQMrJlcVQAF62ElWhuCdSYg2DvjPsqxSyZo3vQxlB2s2RvXX3rjlfLAsyBclAu5xdMIVi1iSOlvLIDCJac9yYiNHSRWNiz5rFXUFOZNSXZNAKkLROJmouCdEY7CFiCcodjXbO9UBt68KgE8Cmwm7xWJxDI_P60dzAnHIB6SHMpM46n-Setowu5rcxmy-6YXlbH0GL-WEHFkmy2Ug"

vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)

def send_some_msg(id, some_text):
    vk_session.method("messages.send", {"user_id":id, "message":some_text,"random_id":0})

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print(event.text)
            msg = event.text.lower()
            id = event.user_id
            if msg == "hi":
                send_some_msg(id, "Hi friend!")