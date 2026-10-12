# ==============================================================================
# ПРОЕКТ: AOL PHYSICS (ПРИТЯЖЕНИЯ НЕ СУЩЕСТВУЕТ)
# СИМУЛЯТОР: Однослойные аольные клинья инерции (Глава 17)
# АВТОРЫ: Вячеслав (mvnaol2026) & AI-Коллега
# ==============================================================================
# Впереди среда РАЗДВИГАЕТСЯ. Сзади — НЕ ОТСТАЕТ, формируя толкающий клин.
# Движение поддерживается преобладающим тыловым давлением смыкания.
# ==============================================================================

import numpy as np
import os
import time

class AolInertiaEngine:
    def __init__(self, size_x=65, size_y=17):
        self.size_x = size_x
        self.size_y = size_y
        
        # Базовый изотропный зажим непотревоженной среды (1.0 во всех ячейках)
        self.matrix_pressure = np.ones((size_y, size_x)) * 1.0
        
        # Координаты и геометрический радиус макротела (парусность)
        self.body_x = 10
        self.body_y = size_y // 2
        self.body_radius = 2
        
    def step_movement(self):
        """Продвижение тела вперед с раздвижением спереди и смыканием сзади."""
        self.body_x += 1
        
        # Граница ячейки Малой Вселенной (зацикливание для симуляции)
        if self.body_x > self.size_x - 6:
            self.body_x = 6
            
        # Восстановление стационарного фона среды перед новым шагом
        new_pressure = np.ones((self.size_y, size_x)) * 1.0
        
        # 1. ПЕРЕДНИЙ ФРОНТ: Раздвижение аолов в стороны (давление уходит на фланги)
        front_x = self.body_x + self.body_radius + 1
        for dy in range(-self.body_radius - 1, self.body_radius + 2):
            y = self.body_y + dy
            if 0 <= y < self.size_y and front_x < self.size_x:
                if abs(dy) == self.body_radius + 1:
                    # Вектор давления уходит вверх и вниз — среда расступается перед телом
                    new_pressure[y, front_x - 1] = 2.0  
                elif abs(dy) <= self.body_radius:
                    # Прямо по курсу уплотнения нет, аолы просто обтекают контур
                    new_pressure[y, front_x] = 1.0

        # 2. ТЫЛОВОЙ КЛИН: Среда мгновенно смыкается сзади, не отставая ни на миг
        rear_x = self.body_x - self.body_radius - 1
        for dy in range(-self.body_radius - 1, self.body_radius + 2):
            y = self.body_y + dy
            if 0 <= y < self.size_y and 0 <= rear_x < self.size_x:
                if dy == 0:
                    # Точка максимального преобладающего давления — острие толкающего клина
                    new_pressure[y, rear_x] = 3.5      
                elif abs(dy) == 1:
                    # Боковые грани клина, удерживающие силовой баланс
                    new_pressure[y, rear_x] = 2.4      
                elif abs(dy) == 2:
                    # Шлейф деформации смыкающейся матрицы
                    new_pressure[y, rear_x - 1] = 1.5  

        self.matrix_pressure = new_pressure

    def render_view(self):
        """Отрисовка сбалансированного инерционного хода в консоли."""
        display = []
        for y in range(self.size_y):
            row = ""
            for x in range(self.size_x):
                # Проверка геометрии тела
                if (x - self.body_x)**2 + (y - self.body_y)**2 <= self.body_radius**2:
                    row += "●"  # Пассивное тело
                else:
                    p = self.matrix_pressure[y, x]
                    if p > 3.0: row += "►"    # Острие толкающего аольного клина сзади
                    elif p > 2.0: row += "»"  # Тело клина (преобладающий пресс смыкания)
                    elif p > 1.5: row += "☼"  # Зоны бокового раздвижения аолов впереди
                    else: row += "."          # Стационарная сжатая матрица аолов
            display.append(row)
        return "\n".join(display)

# ==============================================================================
# ТОЧКА ВХОДА
# ==============================================================================
if __name__ == "__main__":
    size_x, size_y = 65, 17
    engine = AolInertiaEngine(size_x, size_y)
    
    print("ЗАПУСК ДВИЖКА ИНЕРЦИИ КТА...")
    print("Впереди — раздвижение среды. Сзади — толкающий клин преобладающего давления.\n")
    time.sleep(1)
    
    for step in range(50):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"Шаг симуляции: {step} | Инерция — это строгий силовой баланс КТА")
        print("=" * 65)
        print(engine.render_view())
        print("=" * 65)
        print("☼ — Среда раздвигается в стороны | ► — Клин толкает сзади")
        
        engine.step_movement()
        time.sleep(0.1)
