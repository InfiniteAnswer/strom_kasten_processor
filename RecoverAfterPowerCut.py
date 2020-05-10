import pandas as pd
import numpy as np

def make_correction():
    df = pd.read_csv('dump.txt')
    print(df.head())

    df.columns = ['ms', 'H', 'A']

    df['dif'] = df['ms'].diff()
    df['correction'] = np.where(df['dif'] > 0, df['dif'], df['ms'])
    #df['corrected'] = df['dif'].rolling(2).sum().shift(-1) + df['correction']
    df['corrected'] = df['correction'].cumsum()
    df['corrected'].iloc[0] = df['ms'].iloc[0]
    df = df.drop(columns=['dif', 'correction'])
    df['ms'] = df['corrected']
    df = df.drop(columns=['corrected'])
    print(df.head())
    df.to_csv('corrected.csv', index=False, header=False)