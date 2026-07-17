import keyboard
import platform
import pyperclip
import time
from song import *


def auto_input_text(text: str) -> None:
    """
    将任意字符串通过「剪贴板 + 粘贴」方式自动输入
    :param text: 要输入的文本（支持中文/英文/符号）
    :param delay: 复制后等待时间（秒），防止粘贴失败
    """
    # 1. 复制到剪贴板（保存先前内容）
    temp_text = pyperclip.paste()

    pyperclip.copy(text)
    print('键入将在2s后开始')
    time.sleep(2)
    beep_sound()

    # 2. 根据系统选择粘贴快捷键
    system = platform.system()
    if system == 'Darwin':  # macOS
        keyboard.send('cmd+v')
    else:  # Windows / Linux
        keyboard.send('ctrl+v')

    time.sleep(0.03)
    # 恢复
    pyperclip.copy(temp_text)