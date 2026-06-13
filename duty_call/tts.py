
TTS_SCRIPT = """Set spVoice = CreateObject("SAPI.SpVoice")
Set args = WScript.Arguments
For Each text In args
   spVoice.Speak text
Next
"""


from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def extract_file() -> None:
    with open("tts.vbs", "w") as f:
        f.write(TTS_SCRIPT)

def set_system_volume(percent: int) -> None:
    """设置 Windows 系统主音量（0-100）"""
    if percent < 0 or percent > 100:
        return
    try:
        # 获取默认音频输出设备
        devices = AudioUtilities.GetSpeakers()
        if devices is None:
            print("设置音量失败: 未找到音频输出设备")
            return

        # 直接使用 AudioDevice 的 EndpointVolume 属性
        volume = devices.EndpointVolume
        if volume is None:
            print("设置音量失败: 无法访问音量控制接口")
            return

        # 设置主音量（0.0 - 1.0）
        volume.SetMasterVolumeLevelScalar(percent / 100, None)
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
