import os
import psutil


def memory_usage():
    """
    Return memory usage for the current process in Mo
    :return: memory_usage:
    """
    memory_usage = -1
    pid = os.getpid()  # this process pid
    infos = None
    for p in psutil.process_iter(attrs=['pid']):
        if p.info['pid'] == pid:
            infos = p.memory_info()
    if infos:
        # in Mo
        memory_usage = int(infos.rss / (1024 ** 3) * 1000)

    if memory_usage < 0:
        print("Error with memory calculation")
        return -1
    else:
        return memory_usage


# TODO: process to look at memory usage on all processes


if __name__ == '__main__':
    pass
