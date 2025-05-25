from langchain_ollama import OllamaLLM

from config import get_settings

haiqv_setting = get_settings().haiqv

HAIQV_URL = haiqv_setting.haiqv_url
HAIQV_MODEL = haiqv_setting.haiqv_model


class HaiqvOllamaLLM(OllamaLLM):
    """OllamaLLM configured for HaiQV proxy."""

    base_url: str = HAIQV_URL
    model: str = HAIQV_MODEL

    def model_post_init(self, __context):
        if self.client_kwargs is None:
            object.__setattr__(self, "client_kwargs", {})
        super().model_post_init(__context)
