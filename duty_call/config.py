from pydantic import BaseModel

class ReminderSettings(BaseModel):
    tts: bool = True
    alive_time: int = 45
    times: list[tuple[int, int]]
    text: str = "今日值日的同学有: {}"

class Config(BaseModel):
    schedule: dict[str, list[tuple[str, str]]]
    workAlias: dict[str, str] = {}
    reminder: ReminderSettings

def load_config() -> Config:
    with open("config.json", "r", encoding="utf-8") as f:
        return Config.parse_raw(f.read())
