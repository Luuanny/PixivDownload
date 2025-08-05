def ask_input(msg: str = "是否继续?") -> bool:
    """ 等待用户确认执行， Enter 或 y 视为 True 。
    :param msg: 提示信息 (str)
    :return: 返回结果 (bool)
    """
    print(msg, end=" (Enter or y): ")
    ans = input().strip().lower()
    return ans in ("", "y")
