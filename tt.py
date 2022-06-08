import pandas as pd


ask = [[[1654495985, 24.05],
        [1654495990, 22.32],
        [1654496000, 14.68],
        [1654496005, 10.09],
        [1654496015, 69.63],
        [1654496020, 62.7],
        [1654496030, 62.7],
        [1654496035, 53.82],
        [1654496045, 40.94],
        [1654496050, 0.12]]
]

dd = pd.read_csv('Test_Run_IB_America.csv')
dd['Ask Close'] = ask

dd.to_csv('Test_Run_USA_220602.csv', index=False)