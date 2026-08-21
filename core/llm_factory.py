from langchain_openai import ChatOpenAI
from config.settings import LLM_CONFIGS


class LLMFactory:
    @staticmethod
    def get_llm(model_name: str, temperature: float = 0.7, max_tokens: int = 2000) -> ChatOpenAI:
        """
        Get the corresponding LLM instance based on the model name.
        All providers use the OpenAI-compatible protocol.
        """
        if model_name not in LLM_CONFIGS:
            supported = ", ".join(LLM_CONFIGS.keys())
            raise ValueError(f"Unsupported model: {model_name}. Available: {supported}")

        config = LLM_CONFIGS[model_name]
        return ChatOpenAI(
            model=config["model"],
            openai_api_key=config["api_key"],
            openai_api_base=config["base_url"],
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=True,
            timeout=60,
            max_retries=2,
        )