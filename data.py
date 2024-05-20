import pandas as pd

data_path = 'info.csv'
HEADER = ["name", "account", "password", "balance"]


def read_data(file_name):
    with open(file_name, 'r+', encoding='utf-8') as f:
        try:
            reader = pd.read_csv(f, dtype=str)
        except pd.errors.EmptyDataError:
            print("用户数据丢失,已重写文件")
            # 写入文件
            _data = pd.DataFrame(columns=HEADER)
            _data.to_csv(f, index=False)
            return None
        if reader.empty:
            return None
    reader["balance"] = pd.to_numeric(reader["balance"], downcast="integer", errors='coerce',).fillna(0)
    reader = reader.astype({"balance": "int64"})
    return reader


def write_data(file_name, info):
    _data = read_data(file_name)
    # 如果info是元组类型
    if isinstance(info, tuple) or isinstance(info, list):
        for user in info:
            _data.loc[user.index] = user
    else:
        _data.loc[info.index] = info
    with open(file_name, 'w', encoding='utf-8') as f:
        _data.to_csv(f, index=False)
        return True


if __name__ == '__main__':
    data = read_data('info.csv')
    print(data)
