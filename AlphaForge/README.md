step1:git clone https://github.com/EvelynYao0728/RLalphaminer-master.git (private repo)
step2:pip install pyqlib 
step3:git clone https://github.com/microsoft/qlib.git
step4:cd qlib
step5:pip install .
step6:pip install baostock
step7:python data_collection/collect_data.py
step8:set path
step9:python train.py --instruments=all --train_end_year=2020 --seeds=[0,1] --save_name=test --zoo_size=10
step10:python combine.py --instruments=all --train_end_year=2020 --seeds=[0,1] --save_name=test --n_factors=10 --window=inf
