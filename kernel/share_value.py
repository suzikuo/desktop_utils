# shared_data.py

import multiprocessing

Lock = multiprocessing.Lock()
SharedDict = {}


# 创建共享字典
def InitShareValue(shared_dict=None):
    global SharedDict
    if shared_dict is not None:
        SharedDict = shared_dict
    else:
        manager = multiprocessing.Manager()
        SharedDict = manager.dict()
    return SharedDict
