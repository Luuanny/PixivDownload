from sys import stdout


# ======================
# 进度条组件
# ======================

def progress_bar(current: int, total: int, bar_length: int = 50, show_count=True, fill_char="█", empty_char="-",
                 prefix="", suffix=" "):
    """ 通用进度条显示函数。
    :param current: 当前进度 (int)
    :param total:   总进度 (int)
    :param bar_length:  进度条长度 (int)
    :param show_count:  是否显示计数 (bool)
    :param fill_char:   已完成部分样式 (str)
    :param empty_char:  未完成部分样式 (str)
    :param prefix:  进度条前缀 (str)
    :param suffix:  进度条后缀 (str)
    """
    if not isinstance(current, int) or not isinstance(total, int) or bar_length <= 0:
        return
    if total <= 0:
        percent = 0
        filled_length = 0
    else:
        current = min(max(current, 0), total)
        percent = current / total
        filled_length = int(bar_length * percent)
    bar = fill_char * filled_length + empty_char * (bar_length - filled_length)
    percent_str = f"{percent:.2%}"
    count_str = f" ({current}/{total})" if show_count else ""
    end = "\n" if current == total else ""
    stdout.write(f"\r{prefix}|{bar}| {percent_str}{count_str}{suffix}{end}")
    stdout.flush()
