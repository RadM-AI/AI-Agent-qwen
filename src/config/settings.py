import os
from typing import Dict, Any

class Settings:
    MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

    EMBENDING_MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"

    TEMPERATURE = 0.001
    MAX_NEW_TOKENS = 1000
    DEVICE = 0
    
    # Пути
    FAISS_INDEX_PATH = "data/faiss_index"
    
    # Настройки валидации
    MAX_INPUT_LENGTH = 1000

settings = Settings()