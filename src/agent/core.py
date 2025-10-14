from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.prompts import PromptTemplate

from ..config.settings import settings
from ..config.prompts import main_prompt, ask_result_prompt
from .memory import ManageMemory
from .response_processor import ResponseProcessor
from ..tools.registry import ToolRegistry


