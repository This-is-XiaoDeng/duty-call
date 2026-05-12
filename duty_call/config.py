from pydantic import BaseModel

class ReminderSettings(BaseModel):
    tts: bool = True
    alive_time: int = 45
    times: list[tuple[int, int]]
    text: str = "今日值日的同学有: {}"
    tts_pause_spaces: int = 3  # TTS 人名间的空格数量，越多停顿越长，设为 1 恢复默认

class Config(BaseModel):
    schedule: dict[str, list[tuple[str, str]]]
    workAlias: dict[str, str] = {}
    reminder: ReminderSettings

def load_config() -> Config:
    with open("config.json", "r", encoding="utf-8") as f:
        return Config.parse_raw(f.read())
