from langchain_ollama import OllamaLLM
from config import get_settings

haiqv = get_settings().haiqv


class HaiqvOllamaLLM(OllamaLLM):
    base_url: str = haiqv.haiqv_url
    model: str = haiqv.haiqv_model

    def model_post_init(self, __context):
        if self.client_kwargs is None:
            object.__setattr__(self, "client_kwargs", {})
        super().model_post_init(__context)


# a single shared instance is fine – Ollama client is thread‑safe
ollama_client = HaiqvOllamaLLM()
