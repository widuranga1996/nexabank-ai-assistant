from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    pinecone_api_key: str
    pinecone_index_name: str = "nexabank-knowledge"

    langchain_api_key: str | None = None
    langchain_tracing_v2: bool = True
    langchain_project: str = "nexabank-ai-assistant"

    app_env: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()