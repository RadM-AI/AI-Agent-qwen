from src.agent.core import AIAgent
from src.config.settings import settings

settings.MODEL_NAME = 'D:\model'


agent = AIAgent()

while True:
    input_ = input("Вы:")

    if input_.lower().strip() == "выход":
        break

    else:
        print(agent.chat(input_)) 