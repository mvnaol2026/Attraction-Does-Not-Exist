# ==============================================================================
# ПРОЕКТ: AOL PHYSICS (ПРИТЯЖЕНИЯ НЕ СУЩЕСТВУЕТ)
# СИМУЛЯТОР: Оптическая задержка импульса на атомных структурах (Глава 26)
# АВТОРЫ: Вячеслав (mvnaol2026) & AI-Коллега
# ==============================================================================
# Скорость волны в среде аолов ВСЕГДА неизменна.
# Замедление света в стекле — это суммарное время внутренних механических задержек 
# внутри сложных составных атомных LEGO-замков. На выходе скорость снова базовая.
# ==============================================================================

import numpy as np
import os
import time

class AolOpticsEngine:
    def __init__(self, size_x=65, size_y=11):
        self.size_x = size_x
        self.size_y = size_y
        
        # Сетка импульсов давления (0.0 — покоящаяся среда)
        self.matrix_px = np.zeros((size_y, size_x))
        
        # Определение границ оптической среды (Стекло занимает центр: от X=25 до X=45)
        self.glass_start = 25
        self.glass_end = 45
        
        # Внутренние таймеры задержки атомов стекла для каждой ячейки
        self.atom_timers = np.zeros((size_y, size_x), dtype=int)
        
        # Коэффициент задержки атома: сколько шагов симуляции атом «переваривает» удар
        self.atom_delay_steps = 3 

    def trigger_light_pulse(self):
        """Атом-источник генерирует упругий пучок давления на левой границе."""
        mid_y = self.size_y // 2
        for dy in range(-1, 2):
            y = mid_y + dy
            self.matrix_px[y, 0] = 5.0  # Начальный силовой импульс жгута

    def step_optics(self):
        """Детерминированная передача механического давления по эстафете."""
        new_px = np.zeros((self.size_y, self.size_x))
        
        for y in range(self.size_y):
            for x in range(self.size_x):
                current_p = self.matrix_px[y, x]
                
                if current_p <= 0.01:
                    continue
                    
                # Проверяем, находится ли импульс внутри атомной структуры стекла
                if self.glass_start <= x <= self.glass_end:
                    if self.atom_timers[y, x] < self.atom_delay_steps:
                        # Атом удерживает импульс внутри себя, передача заблокирована
                        self.atom_timers[y, x] += 1
                        new_px[y, x] = current_p  # Давление остается в текущей ячейке
                    else:
                        # Таймер задержки истек: атом стекла транслирует удар следующему аолу
                        self.atom_timers[y, x] = 0  # Сброс таймера ячейки
                        if x + 1 < self.size_x:
                            new_px[y, x + 1] = current_p
                else:
                    # Вне стекла (в вакууме) импульс летит без задержек — строго 1 шаг сетки
                    if x + 1 < self.size_x:
                        new_px[y, x + 1] = current_p

        self.matrix_px = new_px

    def render_simulation(self):
        """Отрисовка движения оптического фронта давления в консоли."""
        display =
        for y in range(self.size_y):
            row = ""
            for x in range(self.size_x):
                # Отрисовка физических зон пространства
                is_glass = self.glass_start <= x <= self.glass_end
                p = self.matrix_px[y, x]
                
                if p > 0.1:
                    if is_glass:
                        row += "▓"  # Импульс давления, застрявший внутри структуры атома стекла
                    else:
                        row += "█"  # Свободный упругий жгут давления в аолах вакуума
                else:
                    if is_glass:
                        row += "░"  # Покоящаяся кристаллическая решетка стекла
                    else:
                        row += "."  # Свободная стационарная матрица аолов (вакуум)
            display.append(row)
        return "\n".join(display)

# ==============================================================================
# ВЫПОЛНЕНИЕ СИМУЛЯЦИИ
# ==============================================================================
if __name__ == "__main__":
    engine = AolOpticsEngine()
    engine.trigger_light_pulse()
    
    print("ЗАПУСК ДВИЖКА ОПТИЧЕСКОЙ ПЛОТНОСТИ КТА...")
    print("Наглядное механическое замедление волны без фотонов и квантовой мистики.\n")
    time.sleep(1.5)
    
    for step in range(85):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"Шаг времени: {step} | Глава 26: Скорость в вакууме и стекле по КТА")
        print("=" * 65)
        print(engine.render_simulation())
        print("=" * 65)
        print(". — Вакуум | ░ — Стекло | █ — Волна в вакууме | ▓ — Задержка в атоме")
        
        engine.step_optics()
        time.sleep(0.06)
