from google.cloud import language

class LanguageClient(object):
    def __init__(self):
        self.client = language.LanguageServiceClient()
    
    def request(self, text):
        return language.types.Document(content=text, type=language.enums.Document.Type.PLAIN_TEXT)