import argparse
import os
from rich_argparse import RawDescriptionRichHelpFormatter
from typing import *

from operation import *
from write_text import *

epilog = '''\
        示例: InputScripter --key=a --key=b --key=c --time=0.5
             InputScripter --press=2 --press=3 --press=6

        宏写法：
        [
          {
            "trigger": "触发按键",
            "options": [
              操作
            ]
          },
          ...
        ]
        操作写法：
        {"key": "模拟按下的按键", "time": 时间（秒）}
        或
        {"mouse": "模拟按下的鼠标按键", "time": 时间（秒）}
        或
        {"message": "想要键入的文本", "time": 时间（秒）}
        '''

standard_keys: Final[list] = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    'enter', 'esc', 'tab', 'backspace', 'delete', 'space',
    'up', 'down', 'left', 'right',
    'ctrl', 'alt', 'shift', 'win',
    'caps lock', 'num lock', 'scroll lock',
    '\'', ';', '.', ',', '/', '\\', '`'
]
standard_mouse: Final[list] = [
    'left', 'right', 'middle'
]


def main():
    os.makedirs('func', exist_ok=True)

    parser = argparse.ArgumentParser(
        description='快速键入工具 v2.2.3 | By FeSo4a | 使用MIT许可证',
        epilog=epilog,
        formatter_class=RawDescriptionRichHelpFormatter
    )

    # 创建互斥组
    group_click_key = parser.add_argument_group('按键/鼠标点击模式')
    group_click_key.add_argument('-k', '--key', type=str, help='按下按键（支持多次传入）', action='append')
    group_click_key.add_argument('-t', '--time', type=float, help='按下按键间隔（秒）')
    group_click_key.add_argument('-m', '--mouse', type=str, help='按下鼠标（支持多次传入）', action='append')

    group_send_message = parser.add_argument_group('文本输入模式')
    group_send_message.add_argument('-me', '--message', type=str, help='输入文本（不支持多次传入）')

    group_press_key = parser.add_argument_group('按键长按模式')
    group_press_key.add_argument('-p', '--press', type=str, help='模拟持续按下按键（支持多次传入）', action='append')

    group_press_mouse = parser.add_argument_group('鼠标长按模式')
    group_press_mouse.add_argument('-pm', '--pmouse', type=str, help='模拟持续按下鼠标（支持多次传入）', action='append')

    group_view = parser.add_argument_group('查看模式')
    group_view.add_argument('-v', '--view', help='查看可用按键', action='store_true')

    group_func = parser.add_argument_group('宏执行模式')
    group_func.add_argument('-r', '--runfunc', type=str, help='读取宏（只能传入func文件夹里面的一个宏文件名称）')

    group_showfunc = parser.add_argument_group('宏查看模式')
    group_showfunc.add_argument('-s', '--showfunc', help='查看可用宏文件', action='store_true')

    args = parser.parse_args()

    # 验证互斥逻辑
    active_modes = []

    if args.key and args.time:
        active_modes.append('click_key')
    if args.mouse and args.time:
        active_modes.append('click_mouse')
    if args.press:
        active_modes.append('press_key')
    if args.pmouse:
        active_modes.append('press_mouse')
    if args.view:
        active_modes.append('view')
    if args.runfunc:
        active_modes.append('func')
    if args.showfunc:
        active_modes.append('showfunc')
    if args.message:
        active_modes.append('send_message')

    # 检查是否只有一个模式被激活
    if len(active_modes) > 1:
        parser.error(f"参数冲突：检测到多个模式被激活 {', '.join(active_modes)}，这些模式是互斥的")
    if len(active_modes) == 0:
        parser.error(f'缺少传参，使用-h参数查看帮助信息。')

    # 执行对应的操作
    mode = active_modes[0]

    if mode == 'click_key':
        key_click(args)
    elif mode == 'press_key':
        key_press(args)
    elif mode == 'click_mouse':
        mouse_click(args)
    elif mode == 'press_mouse':
        mouse_press(args)
    elif mode == 'view':
        print_view(standard_keys, standard_mouse)
    elif mode == 'func':
        run_func(load_func(args))
    elif mode == 'showfunc':
        view_func()
    elif mode == 'send_message':
        auto_input_text(args.message)


if __name__ == '__main__':
    main()
