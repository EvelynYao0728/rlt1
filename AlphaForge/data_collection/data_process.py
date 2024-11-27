import os
import pandas as pd
import numpy as np
from pathlib import Path

csv_file="rb2405.csv"
output_dir = "AlphaForge/Qlib_data/cn_data_rolling"

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)
os.makedirs(f"{output_dir}/calendars", exist_ok=True)
os.makedirs(f"{output_dir}/instruments", exist_ok=True)
df = pd.read_csv(csv_file)


# 2. 生成 calendars/3s.txt 文件
# 提取时间戳并按升序排序（避免重复）
timestamps = pd.to_datetime(df["date"]).dt.strftime('%Y-%m-%d %H:%M:%S').drop_duplicates().sort_values()

calendar_path = f"{output_dir}/calendars/3s.txt"
with open(calendar_path, 'w') as cal_file:
    for timestamp in timestamps:
        cal_file.write(f"{timestamp}\n")

print(f"Calendar file saved to {calendar_path}")

# 3. 写入 instruments/all.txt 文件
# 合约时间范围为以下日期
contract_name = "rb2405"
start_date = "2024/1/2 9:00:03"
end_date = "2024/4/30 14:59:57"

instrument_path = f"{output_dir}/instruments/all.txt"
with open(instrument_path, 'w') as ins_file:
    ins_file.write(f"{contract_name}\t{start_date}\t{end_date}\n")

print(f"Instrument file saved to {instrument_path}")


# 对于文件中的列Open，Close，High，Low，Volume，Turnover，OI，Openbp1，Openbv1，Openap1，Openav1，Closebp1，Closebv1，Closeap1，Closeav1，Openbp2，Openbv2，Openap2，Openav2，Closebp2，Closebv2，Closeap2，Closeav2，Openbp3，Openbv3，Openap3，Openav3，Closebp3，Closebv3，Closeap3，Closeav3，Openbp4，Openbv4，Openap4，Openav4，Closebp4，Closebv4，Closeap4，Closeav4，Openbp5，Openbv5，Openap5，Openav5，Closebp5，Closebv5，Closeap5，Closeav5，UpperLimit，LowerLimit，每一个列的数据都会在dump_bin操作后，在路径"/Qlib_data/cn_data_rolling/feature/rb2405"里面以“列名.bin”的文件形式存储起来

def dump_bin_from_csv(csv_file, output_dir, columns, date_field="date", freq="3s"):
    """
    将CSV文件的指定列导出为二进制文件存储.

    Parameters:
    - csv_file (str): CSV文件路径
    - output_dir (str): 输出目录
    - columns (list of str): 要提取的列名
    - date_field (str): 日期字段名，用于对齐数据
    - freq (str): 数据频率
    """
    # 读取CSV文件
    df = pd.read_csv(csv_file)
    
    # 日期字段检查与转换
    if date_field not in df.columns:
        raise ValueError(f"指定的日期字段 `{date_field}` 不存在于CSV文件中")
    df[date_field] = pd.to_datetime(df[date_field])
    df.set_index(date_field, inplace=True)

    # 确保输出目录存在
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 遍历需要保存的列
    for col in columns:
        if col not in df.columns:
            print(f"警告: 列 `{col}` 不存在，将跳过")
            continue

        # 获取列数据
        data = df[col].values.astype(np.float32)

        # 输出文件路径
        bin_file = output_path / f"{col.lower()}.{freq}.bin"

        # 保存为二进制
        with open(bin_file, "wb") as f:
            data.tofile(f)
        print(f"已保存列 `{col}` 至 {bin_file}")

# 示例使用
csv_file = "rb2405.csv"
output_dir = "AlphaForge/Qlib_data/cn_data_rolling/feature/rb2405"
columns = [
    "Open", "Close", "High", "Low", "Volume", "Turnover", "OI",
    "Openbp1", "Openbv1", "Openap1", "Openav1",
    "Closebp1", "Closebv1", "Closeap1", "Closeav1",
    "UpperLimit", "LowerLimit"
]
dump_bin_from_csv(csv_file, output_dir, columns)