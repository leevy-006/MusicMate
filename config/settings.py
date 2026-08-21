import os
from dotenv import load_dotenv

load_dotenv()

LLM_CONFIGS = {
    "qwen": {
        "model": "Qwen/Qwen3-Next-80B-A3B-Instruct",
        "api_key": os.getenv("QWEN_API_KEY"),
        "base_url": "https://integrate.api.nvidia.com/v1",
    },
    "deepseek": {
        "model": "deepseek-ai/deepseek-v4-flash-0731",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "base_url": "https://integrate.api.nvidia.com/v1",
    },
    "minimax": {
        "model": "minimaxai/minimax-m3",
        "api_key": os.getenv("MINIMAX_API_KEY"),
        "base_url": "https://integrate.api.nvidia.com/v1",
    },
    "openAI": {
        "model": "openai/gpt-oss-120b",
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": "https://integrate.api.nvidia.com/v1",
    },    
}

# ACE_STEP_REMOTE_URL = os.getenv("ACE_STEP_URL", "http://lees-mac-mini.local:7860")
# ACE_STEP_REMOTE_URL = os.getenv("ACE_STEP_URL", "http://192.168.0.12:7860")
ACE_STEP_REMOTE_URL = os.getenv("ACE_STEP_URL", "https://9fc168b32b454634b541440325da7a71--8001.ap-shanghai2.cloudstudio.club")