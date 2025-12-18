"""Application configuration"""

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings"""
    
    # Application
    debug: bool
    host: str
    port: int = Field(ge=1, le=65535)
    
    # Twitter API
    twitter_bearer_token: str
    twitter_api_base_url: str
    
    # Cache
    cache_enabled: bool
    cache_ttl: int = Field(ge=0, le=3600)
    redis_url: str
    redis_enabled: bool
    
    # Logging
    log_level: str 
    log_format: str
    
    # CORS
    cors_origins: str
    
    @property
    def cors_origins_list(self) -> list[str]:
        if not self.cors_origins or self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


_settings: Settings | None = None


def get_settings() -> Settings:
    """Get application settings singleton"""
    global _settings
    if _settings is None:
        from app.bootstrap.env import load_environment
        env_vars = load_environment()
        _settings = Settings(**env_vars)
    return _settings
