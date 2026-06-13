
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess
import tempfile
import os

def set_system_volume(percent: int) -> None:
    if percent < 0 or percent > 100:
        return
    try:
        devices = AudioUtilities.GetSpeakers()
        if devices is None:
            print("设置音量失败: 未找到音频输出设备")
            return
        volume = devices.EndpointVolume
        if volume is None:
            print("设置音量失败: 无法访问音量控制接口")
            return
        volume.SetMasterVolumeLevelScalar(percent / 100, None)
        print(f"系统音量已设置为 {percent}%")
    except Exception as e:
        print(f"设置音量失败: {e}")

def tts(text: str | list[str], volume: int = 60, pause_ms: int = 0) -> None:
    if volume > 0:
        set_system_volume(volume)
    parts = text if isinstance(text, list) else [text]
    lines = ['Set spVoice = CreateObject("SAPI.SpVoice")']
    for i, part in enumerate(parts):
        if i > 0 and pause_ms > 0:
            lines.append(f"WScript.Sleep {pause_ms}")
        escaped = part.replace('"', '""')
        lines.append(f'spVoice.Speak "{escaped}"')
    script = "\n".join(lines)
    fd, path = tempfile.mkstemp(suffix=".vbs")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(script)
        print(["wscript.exe", path])
        subprocess.run(["wscript.exe", path])
    finally:
        os.remove(path)
