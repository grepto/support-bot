import os
import json
import logging

from dotenv import load_dotenv
import dialogflow_v2 as dialogflow
from google.protobuf.json_format import MessageToDict

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
QUESTIONS_FILE = os.getenv('QUESTIONS_FILE')

logger = logging.getLogger('train_bot')


def create_intent(name, training_phrases, messages, parameters=None, project_id=DIALOGFLOW_PROJECT_ID):
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)
    intent = {
        'display_name': name,
        'training_phrases': training_phrases,
        'parameters': parameters,
        'messages': messages,
    }
    response = intents_client.create_intent(parent, intent, intent_view=dialogflow.enums.IntentView.INTENT_VIEW_FULL)

    return response


def delete_intent(name, project_id=DIALOGFLOW_PROJECT_ID):
    intent = get_intent(name, project_id)
    intent_id = intent['name'].split('/')[-1]
    intents_client = dialogflow.IntentsClient()
    intent_path = intents_client.intent_path(project_id, intent_id)
    intents_client.delete_intent(intent_path)


def get_intent(name, project_id=DIALOGFLOW_PROJECT_ID):
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(project_id)
    intents = client.list_intents(parent, intent_view=dialogflow.enums.IntentView.INTENT_VIEW_FULL)
    try:
        intent = [intent for intent in intents if intent.display_name == name][0]
    except IndexError:
        return None
    return MessageToDict(intent, preserving_proto_field_name=True)


def train_bot(training_set_file, is_rewrite_answers=False):
    logger.info('Training bot process has been started')

    with open(training_set_file, 'r') as training_set_file:
        training_set = json.load(training_set_file)

    for intent_name, intent_training_set in training_set.items():
        training_phrases = []
        messages = []
        parameters = []
        logger.info(f'Starting training for set {intent_name}')
        intent = get_intent(intent_name)
        if intent:
            training_phrases.extend(intent.get('training_phrases', []))
            messages = intent.get('messages', [])
            parameters = intent.get('parameters', [])
            delete_intent(intent_name)

        training_set_questions = [{'type': 'EXAMPLE', 'parts': [{'text': question}]} for question in
                                  intent_training_set['questions']]
        training_phrases.extend(training_set_questions)

        training_set_answer = intent_training_set['answer']
        if not messages or is_rewrite_answers:
            messages = [{'text': {'text': [training_set_answer]}}]

        create_intent(intent_name, training_phrases, messages, parameters)
        logger.info(f'Bot has been trained on set {intent_name}')

    logger.info('Training bot process has been finished')


def main():
    train_bot(QUESTIONS_FILE, True)


if __name__ == '__main__':
    main()
