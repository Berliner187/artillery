# -*- coding: UTF-8 -*-
import math
import time

G = 9.81
T = 20


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\n[***] {func.__name__} --- {round(end_time - start_time, 3)} сек")
        return result
    return wrapper


class ArtilleryWeapon:
    def __init__(self, name, caliber, weight_projectile, v0):
        self.name = name
        self.caliber = caliber
        self.weight_projectile = weight_projectile
        self.v0 = v0
        print(f"--- ИНИЦИАЛИЗИРОВАННОЕ ОРУДИЕ {name} ---")
        print(f"- КАЛИБР: {caliber} мм")
        print(f"- ВЕС СНАРЯДА: {weight_projectile} кг")
        print(f"- НАЧАЛЬНАЯ СКОРОСТЬ: {v0} м/с\n")

    def get_corner(self, start_range, end_range):
        start_cor, end_cor = 5, 89
        _corner = 0
        while start_cor < end_cor:
            _d = abs((self.v0 ** 2 * math.sin(2 * start_cor)) / G)
            # print("start_cor", start_cor, _d)
            # print(round(d))
            if start_range <= round(_d, 3) <= end_range:
                _corner = start_cor
            start_cor += 0.01
        print(f"Полученный угол: {_corner}")
        return _corner

    def formula_distance(self, _corner):
        _corner_in_radians = math.radians(_corner)
        # abs((self.v0**2 * math.sin(2 * _corner)) / G)
        # 2v₀²sin(α)cos(α)
        # return abs(self.v0 * math.cos(_corner))
        return abs((self.v0**2 * math.sin(2 * _corner_in_radians)) / G)
        # return abs((2 * self.v0**2 * math.sin(_corner_in_radians) * math.cos(_corner_in_radians)) / G)
        # return abs((self.v0**2 * math.sin(2 * _corner)) / G)

    def distance(self, _corner, target):
        suitable_data = {}
        d = 0
        if _corner == 0:
            start_cor, end_cor = -7, 70
            while start_cor <= end_cor:
                _d = self.formula_distance(start_cor)
                # print(round(d))
                if target-10 <= _d <= target+10:
                    _corner = start_cor
                    suitable_data[_d] = _corner
                start_cor += 0.01

            if _corner > 0:
                min_difference = target
                for key, value in suitable_data.items():
                    difference = abs(target - key)
                    if difference < min_difference:
                        min_difference = key

                print(f"Полученный угол: {round(_corner, 4)}°")
                d = min_difference
            else:
                print("ВНЕ ЗОНЫ ДЕЙСТВИЯ")
        else:
            d = self.formula_distance(_corner)
        print(f"Расстояние до цели: {round(d / 1000, 3)} км, ({round(d, 4)} м)")
        return d, _corner

    def time_approach(self, _corner):
        # 2v₀sin(α) / g
        # t = abs((2 * self.v0 * math.sin(_corner)) / G)
        t_max_height = abs((self.v0 * math.sin(_corner)) / G)
        t = t_max_height * 2
        print(f"\nВремя подлета: {get_format_time(t)}")
        return t


def get_format_time(seconds):
    if 0 < seconds < 60:
        return f"{round(seconds, 1)} с"
    elif 60 <= seconds < 3600:
        minutes = seconds // 60
        return f"{round(minutes)} мин, {round(seconds - (minutes * 60), 1)} с"
    else:
        return "-"


@timing_decorator
def main():
    d_30 = ArtilleryWeapon("Д-30", 122, 21.8, 690)
    distance, corner = d_30.distance(87, 34583)
    d_30.time_approach(corner)


if __name__ == '__main__':
    main()
