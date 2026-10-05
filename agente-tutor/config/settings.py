from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Gemini / ADK Configuration
    google_genai_api_key: str = Field(default="", validation_alias="GOOGLE_GENAI_API_KEY")
    tutor_model: str = Field(default="gemini-2.5-flash", validation_alias="TUTOR_MODEL")

    # Knowledge Agent (A2A) Configuration
    knowledge_agent_card_url: str = Field(
        default="http://localhost:8001/.well-known/agent-card.json",
        validation_alias="KNOWLEDGE_AGENT_CARD_URL"
    )
    knowledge_agent_mock_fallback: bool = Field(
        default=True,
        validation_alias="KNOWLEDGE_AGENT_MOCK_FALLBACK"
    )
    mock_kb_port: int = Field(default=8001, validation_alias="MOCK_KB_PORT")

    # Directories
    base_dir: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = base_dir / "data" / "missions"

    # Execution flags
    debug: bool = Field(default=True, validation_alias="DEBUG")


settings = Settings()
