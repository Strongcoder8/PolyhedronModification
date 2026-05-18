#!/usr/bin/env python3 -B
from time import time
from common.tk_drawer import TkDrawer
from polyedr import Polyedr

tk = TkDrawer()
try:
    for name in ["ccc", "cube", "box", "king", "cow"]:
        print("=" * 60)
        print(f"Начало работы с полиэдром '{name}'")
        start_time = time()
        poly = Polyedr(f"data/{name}.geom")
        peri = poly.get_partial_visible_perimeter_outside_square()
        print(f"Характеристика: сумма периметров = {peri:.6f}")
        poly.draw(tk)                     # рисует с удалением невидимых линий
        delta_time = time() - start_time
        print(f"Изображение полиэдра '{name}' заняло {delta_time:.2f} сек.")
        input("Нажмите Enter для продолжения...")
except (EOFError, KeyboardInterrupt):
    print("\nОстановлено пользователем")
    tk.close()
