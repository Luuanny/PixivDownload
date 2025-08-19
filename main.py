import os

from res import *


def main() -> None:
    while True:
        select = input(f"\n请选择需要执行的操作: \n Enter: 开始 | r: 配置 config | q: 退出 \n>")
        match select:
            case "":
                downloader()
                return None
            case "q":
                return None
            case "r":
                reconfig()
                continue
            case _:
                print("无法识别的操作，请重新输入")
                continue
    return None


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
