from src.agent.core import AIAgent
from src.config.settings import settings
from src.config.prompts import wheather_prompt
from transformers import pipeline
from src.agent.registr_agent import AgentRegistry
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
model = ChatHuggingFace(llm=HuggingFacePipeline(pipeline=pipeline(
    "text-generation",
    "Qwen/Qwen2.5-3B-Instruct",
    temperature=0.001,
    max_new_tokens=1000,
    device=0,
)))




weather_agent = AIAgent(
    name="WeatherAgent",
    model=model,
    sys_prompt=wheather_prompt
)
reg = AgentRegistry()
reg.register_agent(weather_agent)
coordinator = AIAgent(
    name="Coordinator",
    model=model,
    agent=reg.agents
)

while True:
    input_ = input("Вы:")

    if input_.lower().strip() == "выход":
        break

    else:
        print(coordinator.chat(input_)) 