
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    entrez_email: str = os.getenv("ENTREZ_EMAIL", "")
    max_papers_per_query: int = int(os.getenv("MAX_PAPERS_PER_QUERY", "20"))
    max_agent_iterations: int = int(os.getenv("MAX_AGENT_ITERATIONS", "8"))
    model: str = "claude-opus-4-5"

cfg = Config()