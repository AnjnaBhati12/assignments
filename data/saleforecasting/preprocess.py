
import pandas as pd
import numpy as np


def DateToYearMonthDay(df,attribute):
    df['Year'] = pd.DatetimeIndex(df[attribute]).year
    df['Month'] = pd.DatetimeIndex(df[attribute]).month
    df['Day'] = pd.DatetimeIndex(df[attribute]).day

