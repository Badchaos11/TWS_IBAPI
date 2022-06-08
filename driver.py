import time

import pyautogui as pg
from datetime import datetime

# Открытие программы
pg.hotkey('winleft')
time.sleep(2)
pg.typewrite('tws')
time.sleep(5)
pg.hotkey('enter')
pg.sleep(15)

# Ввод логина и пароля, закрытие входных окон
pg.moveTo(948, 524)
pg.click()
pg.typewrite('diaman454')
pg.hotkey('tab')
pg.typewrite('malarama53')
pg.hotkey('enter')
time.sleep(30)
pg.hotkey('enter')

# Экспорт данных в CSV
pg.moveTo(1695, 795)
time.sleep(2)
pg.rightClick()
pg.moveTo(1743, 996)
time.sleep(5)
pg.moveTo(1470, 998)
time.sleep(2)
pg.leftClick()
pg.moveTo(854, 590)
pg.leftClick()
pg.typewrite(f"{datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')}")
time.sleep(5)
pg.hotkey('enter')

pg.position()
