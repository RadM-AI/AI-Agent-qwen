from langchain.memory import ConversationBufferMemory

class ManageMemory:
    '''Менеджер памяти'''
    def __init__(self,
                 return_message: bool,
                 memory_key: str,
                 input_key: str):
        
        return ConversationBufferMemory(return_message,
                                        memory_key,
                                        input_key)