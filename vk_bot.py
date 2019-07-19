import os
import logging
import random

from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog import get_dialog_response

load_dotenv()
VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.DEBUG)
logger = logging.getLogger(__name__)


def response(event, vk_api):
    response = get_dialog_response(event.user_id, event.text)
    logger.debug(response)
    if response['intent'] != 'Default Fallback Intent':
        vk_api.messages.send(
            user_id=event.user_id,
            message=response['response_text'],
            random_id=random.randint(1, 1000)
        )


def bot():
    try:
      logger.info('VK bot started')
      vk_session = vk_api.VkApi(token=VK_GROUP_TOKEN)
      api = vk_session.get_api()
      longpoll = VkLongPoll(vk_session)
      for event in longpoll.listen():
          if event.type == VkEventType.MESSAGE_NEW and event.to_me:
              response(event, api)
    except vk_api.exceptions.ApiError as error:
      logger.error(error)


if __name__ == "__main__":
    bot()
