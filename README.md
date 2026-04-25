# 📅 DutyCall

这是一个把值日表展示并大声念出来的程序，主要为希沃一体机设计，部分功能仅支持 Windows 系统。

## 配置

```json
{
    "schedule": {           // 值日表
        "0": [              // 星期
            ["1", "XXX"],   // 值日的学生，第一位为工作（名字或别名），第二位为名字
        ]
    },
    "workAlias": {          // 工作的别名
        "1": "课室/拖地",
    },
    "reminder": {           // 提醒设置
        "tts": true,        // 是否启用 TTS 语音提醒
        "times": [          // 提醒的时间
            [16, 20]        // 第一位为小时，第二位为分钟
        ],
        "alive_time": 45    // 提醒持续时间（秒），超过该时间后提醒窗口会关闭，但是 TTS 会持续播放。
    }
}
```

## 许可

```
DutyCall - A program to read duty schedule aloud.
Copyright (C) 2026  SunaōkamiNya

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```