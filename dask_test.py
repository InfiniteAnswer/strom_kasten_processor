import dask.dataframe as dd
import pyarrow
import parquet


df = dd.read_csv('dump.txt')
df.columns = ['ms', 'H', 'A']

print(df.head())

df.to_parquet('dump_parquet.parquet', engine='pyarrow')