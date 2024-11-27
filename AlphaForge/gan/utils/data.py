from alphagen_generic.features import open_
from gan.utils import Builders
from alphagen_generic.features import *
from alphagen.data.expression import *

import os

def get_data_by_dates(
    train_start="2024-01-02 09:00:03", train_end="2024-04-20 09:00:03",
    test_start="2024-04-20 09:00:06", test_end="2024-04-30 14:59:57",
    instruments=None, target=None, freq=None
):
    QLIB_PATH = {
        'day': 'AlphaForge/Qlib_data/cn_data_rolling/',
    }

    from gan.utils import load_pickle, save_pickle
    # from gan.utils.qlib import get_data_my
    get_data_my = StockData

    name = instruments + '_pkl_' + str(target).replace('/', '_').replace(' ', '') + '_' + freq
    name = f"{name}_{train_start}_{train_end}_{test_start}_{test_end}"
    try:
        data = load_pickle(f'pkl/{name}/data.pkl')
        data_test = load_pickle(f'pkl/{name}/data_test.pkl')
    except:
        print('Data not exist, load from qlib')
        data = get_data_my(instruments, train_start, train_end, raw=True, qlib_path=QLIB_PATH, freq=freq)
        data_test = get_data_my(instruments, test_start, test_end, raw=True, qlib_path=QLIB_PATH, freq=freq)

        os.makedirs(f"pkl/{name}", exist_ok=True)
        save_pickle(data, f'pkl/{name}/data.pkl')
        save_pickle(data_test, f'pkl/{name}/data_test.pkl')
    
    try:
        data_all = load_pickle(f'pkl/{name}/data_all.pkl')
    except:
        data_all = get_data_my(instruments, train_start, test_end, raw=True, qlib_path=QLIB_PATH, freq=freq)
        save_pickle(data_all, f'pkl/{name}/data_all.pkl')
    
    return data_all, data, data_test, name