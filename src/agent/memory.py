from langchain.memory import ConversationBufferMemory

class ManageMemory:
    '''Менеджер памяти'''

    def __init__(self):
        
        self.return_message: bool = True
        self.memory_key: str = "history"
        self.input_key: str = "input"
        self.memory = ConversationBufferMemory(return_messages = self.return_message,
                                        memory_key = self.memory_key,
                                        input_key = self.input_key)