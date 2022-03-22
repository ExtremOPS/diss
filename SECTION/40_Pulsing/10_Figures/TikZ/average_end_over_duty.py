import pandas as pd


df = pd.read_csv('end_over_duty.dat', sep=' ')

for fp in [1000, 5000, 10000]:
    for index in ['y', 'z']:
        columns = []
        for y in [4, 5, 6]:
            col = f'fp_{fp:1.0f}_{index}_m{y:02.0f}'
            columns.append(col)

        df[f'fp_{fp:1.0f}_{index}'] = df[columns].mean(axis=1)
        for col in columns:
            df = df.drop(col, axis=1)

df.to_csv('avg_end_over_duty.dat', float_format='%+.4e', index=False, sep=' ')
