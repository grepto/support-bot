import os

from dotenv import load_dotenv
import dialogflow_v2 as dialogflow

load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')


def get_dialog_response(session_id, text, language_code='ru', project_id=DIALOGFLOW_PROJECT_ID):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    dialogflow_response = session_client.detect_intent(session=session, query_input=query_input)
    response = {
        'query_text': dialogflow_response.query_result.query_text,
        'intent': dialogflow_response.query_result.intent.display_name,
        'is_fallback': dialogflow_response.query_result.intent.is_fallback,
        'confidence': dialogflow_response.query_result.intent_detection_confidence,
        'response_text': dialogflow_response.query_result.fulfillment_text,
    }
    return response


def main():
    session_id = 1
    text = 'Почему я забанен'

    print(get_dialog_response(session_id, text)['response_text'])

if __name__ == '__main__':
    main()
