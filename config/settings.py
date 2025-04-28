# Configuration Settings
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenRouterConfig:
    API_KEY = os.getenv("OPENAI_API_KEY")
    BASE_URL = os.getenv("BASE_URL")  # should be https://openrouter.ai/api/v1
    DEFAULT_MODEL = "openai/gpt-4o"  # valid OpenRouter model name
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7

    @classmethod
    def get_headers(cls):
        return {
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Multi-Agent Research System",
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json"
        }

    @classmethod
    def get_completion_config(cls):
        return {
            "model": cls.DEFAULT_MODEL,
            "max_tokens": cls.MAX_TOKENS,
            "temperature": cls.TEMPERATURE
        }
