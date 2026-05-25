
# 硬编码到程序中防篡改
TTS_SCRIPT = """Set spVoice = CreateObject("SAPI.SpVoice")
Set args = WScript.Arguments
For Each text In args
   spVoice.Speak text
Next
"""

def extract_file() -> None:
    with open("tts.vbs", "w") as f:
        f.write(TTS_SCRIPT)

def set_system_volume(percent: int) -> None:
    """设置 Windows 系统主音量（0-100）"""
    if percent < 0 or percent > 100:
        return
    try:
        import ctypes
        winmm = ctypes.windll.winmm
        vol = int(percent / 100 * 0xFFFF)
        winmm.waveOutSetVolume(0, vol | (vol << 16))
        print(f"系统音量已设置为 {percent}%")
    except Exception as e:
        print(f"设置音量失败: {e}")

def tts(text: str, volume: int = 60) -> None:
    import os
    import subprocess
    if volume > 0:
        set_system_volume(volume)
    extract_file()
    args = ["wscript.exe", "tts.vbs", text]
    print(args)
    subprocess.run(args)
