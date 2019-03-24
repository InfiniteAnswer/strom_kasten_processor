import pandas as pd
import numpy as np
import datetime

df = pd.DataFrame(np.arange(12).reshape(3,4), columns=['A', 'B', 'C', 'D'])

# new_df = df['A'].copy(deep=True)
# new_df.reset_index(drop=True, inplace=True)
new_df = pd.DataFrame(data=df, columns=['A'])
new_df.drop(df.index[df['A'] >4], inplace = True)

target_date_time_ms = 2000  # or whatever
base_datetime = datetime.datetime(1970, 1, 1, 14, 25, 10)
delta = datetime.timedelta(0, 0, 0, target_date_time_ms)
target_date = base_datetime + delta
print(target_date)


a = pd.to_datetime('now')
b = pd.Timestamp(datetime.datetime(1970, 1, 1, 0, 0, 0))
c = (a-b).total_seconds()

df['datetime'] = pd.to_datetime(3600+c+df['A'], unit='s')
df['corrected'] = df['datetime']

print(df)
print(new_df)