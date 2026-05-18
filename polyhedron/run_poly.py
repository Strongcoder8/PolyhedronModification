#!/usr/bin/env python3
from time import time
from common.tk_drawer import TkDrawer
from polyedr import Polyedr

tk = TkDrawer()
for name in ["ccc", "cube", "box", "king", "cow"]:
    print(f"--- {name} ---")
    poly = Polyedr(f"data/{name}.geom")
    peri = poly.get_partial_visible_perimeter_outside_square()
    print(f"Характеристика: сумма периметров = {peri:.6f}")
    poly.draw(tk)
    input("Нажмите Enter для продолжения...")
