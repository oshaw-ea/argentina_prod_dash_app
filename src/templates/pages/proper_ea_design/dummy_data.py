import pandas as pd
import string
from datetime import datetime


def make_dummy_data():
    """make dummy data as if it was coming out of a database"""
    cols = list(string.ascii_lowercase)[0:5]
    df_dict = {}
    for label, increment in zip(cols, list(range(len(cols)))):
        df_dict.update({label: [int(100 * (1 + increment / 100) ** i) for i in range(20)]})
    df = pd.DataFrame.from_dict(df_dict)
    df.index = pd.date_range(periods=len(df.index), start=datetime.now().date(), freq='MS')
    return df
