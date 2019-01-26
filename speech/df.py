import dialogflow

class DialogflowClient(object):
    def __init__(self, 
                language_code="en-US", 
                project_id="huddle72", 
                session_id="1"):
        self.language_code = language_code
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(project_id, session_id)

    def detect_intent(self, text):
        text_input = dialogflow.types.TextInput(
            text=text, language_code=self.language_code
        )
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = self.session_client.detect_intent(
            session=self.session, query_input=query_input)
        intent = response.query_result.intent.display_name
        entities = response.query_result.parameters

        return intent, entities

        