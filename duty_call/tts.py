
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

def tts(text: str) -> None:
    import os
    import subprocess
    extract_file()
    args = ["wscript.exe", "tts.vbs", text]
    print(args)
    subprocess.run(args)
