import os

class Config:
    entrez_email: str = os.getenv("ENTREZ_EMAIL", "")
    amthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

cfg = Config()