from typing import Dict



class AgentRegistry():
    def __init__(self):
        self.agents: Dict[str, 'AIAgent'] = {}


    def register_agent(self, agent: 'AIAgent'):
        """Регистрирует новый инструмент"""
        self.agents[agent.name] = agent
