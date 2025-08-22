import os

from res import *


def main() -> None:
    while True:
        select = input(f"\n请选择需要执行的操作:\n Enter: 开始\n c: 查看 config\n q: 退出\n>>>").strip().lower()
        match select:
            case "":
                downloader()
                return None
            case "q":
                return None
            case "c":
                show_config()
                if ask_input("是否重新配置 config？"):
                    reconfig()
                continue
            case _:
                print("无法识别的操作，请重新输入")
                continue
    return None


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
