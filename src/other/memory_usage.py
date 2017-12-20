import os
import psutil
import time
import matplotlib.pyplot as plt

import src.other.pickle_usage as pck


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


def track_memory_usage(time_gap, queue):
    own_pid = os.getpid()
    master_pid = os.getppid()

    memory_usage_list = []

    while(True):
        process_to_check = psutil.process_iter(attrs=['pid', 'name'])
        for p in process_to_check:
            mem_dict = {}
            try:
                pid_ = p.info['pid']
                name_ = p.info['name']
            except:
                continue
            # if name_ == "python3" and pid_ != own_pid and pid_ != master_pid :
            if name_ == "Python":
                try:
                    infos = p.memory_info()
                except:
                    continue
                # in Mo
                memory_usage = int(infos.rss / (1024 ** 3) * 1000)
                mem_dict[pid_] = memory_usage
        memory_usage_list.append(mem_dict)

        if not queue.empty() :
            break

        time.sleep(time_gap)

    pck.pickle_store("memory_usage", memory_usage_list, "")


def plot_memory_usage():
    try:
        memory_usage_list = pck.pickle_load("memory_usage", "")
    except:
        print("ERROR, no file for memory usage")
        return ""

    print(memory_usage_list)

    memory_usage_plotlist = []
    for mem_dict in memory_usage_list:
        sum_ = 0
        for val in mem_dict.values():
            sum_ += val

        memory_usage_plotlist.append(sum_)

    smooth_list = smoothing(memory_usage_plotlist, 30, min_=True)
    smooth_list = smoothing(smooth_list, 10, min_=False)

    plt.plot(smooth_list)
    plt.show()


def smoothing(Ly, p, min_=False):
    '''Fonction qui débruite une courbe par une moyenne glissante
    sur 2P+1 points'''
    Lyout = []
    for index in range(p, len(Ly) - p):
        average = sum(Ly[index - p: index + p + 1]) / (2 * p + 1)
        if min_:
            Lyout.append(minimum(average,Ly[index]))
        else:
            Lyout.append(average)

    return Lyout

def minimum(a,b):
    if b <= a and b != 0:
        return b
    else:
        return a

if __name__ == '__main__':
    pass
