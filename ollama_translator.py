from ollama import AsyncClient
from pydantic import BaseModel, Field

class TranslationResult(BaseModel):
    translation: str = Field(..., description="Translated text")

class LanguageDetectionResult(BaseModel):
    language: str = Field(..., description="Detected language in ISO 639-1 code")

class AsyncTranslator:
    def __init__(self, model: str, base_url: str):
        self.model = model
        self.base_url = base_url
        self.client = AsyncClient(host=self.base_url)

    async def translate(self, text: str, lang_tgt: str = "auto", lang_src: str = "auto") -> str:
        system_prompt = (
            "You are a professional translator. Your task is to translate text between languages."
        )

        if lang_src == "auto":
            user_prompt = (
                f"Translate the following text to {lang_tgt}:\n\n{text}"
            )
        else:
            user_prompt = (
                f"Translate the following text from {lang_src} to {lang_tgt}:\n\n{text}"
            )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = await self.client.chat(
            model=self.model,
            messages=messages,
            format=TranslationResult.model_json_schema(),
            stream=False
        )

        translation_result = TranslationResult.model_validate_json(response.message.content)
        return translation_result.translation
    
    async def detect(self, text: str) -> list[str]:
        system_prompt = (
            "You are a language detector. Your job is to analyze a given text "
            "and return the language code it is written in."
        )

        user_prompt = f"Detect the language of the following text:\n\n{text}"

        response = await self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            format=LanguageDetectionResult.model_json_schema(),
            stream=False
        )

        detection_result = LanguageDetectionResult.model_validate_json(response.message.content)
        return [detection_result.language]
