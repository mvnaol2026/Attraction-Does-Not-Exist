# ==============================================================================
# ПРОЕКТ: AOL PHYSICS (ПРИТЯЖЕНИЯ НЕ СУЩЕСТВУЕТ)
# СИМУЛЯТОР: Световой жгут упругого давления в тесноте (Глава 25)
# АВТОРЫ: Вячеслав (mvnaol2026) & AI-Коллега
# ==============================================================================
# Базовый закон движения: ДАВИШЬ — ДВИЖЕТСЯ.
# Фотон устранен. Свет — это дискретный механический удар по цепочке аолов.
# ==============================================================================

import numpy as np
import os
import time

class AolSpaceMatrix:
    def __init__(self, width=60, height=19):
        self.width = width
        self.height = height
        
        # Матрицы давления аольной среды (Декартовы координаты X и Y)
        # Каждая ячейка хранит передаваемый вектор контактного пресса
        self.matrix_px = np.zeros((height, width))
        self.matrix_py = np.zeros((height, width))
        
        # Твёрдость аолов определяет скорость трансляции волны (скорость света 'c')
        self.aol_rigidity = 0.96 
        
    def trigger_atomic_impact(self, frequency_color="red"):
        """Атом-источник совершает структурный толчок, ударяя по среде."""
        mid_y = self.height // 2
        
        # Разный цвет — разная геометрия и глубина исходного удара атома
        if frequency_color == "red":
            impact_radius = 3  # Красный жгут: более широкий профиль
            magnitude = 5.0
        elif frequency_color == "violet":
            impact_radius = 1  # Фиолетовый жгут: узкий, жестко сфокусированный пробой
            magnitude = 8.0
        else:
            impact_radius = 2
            magnitude = 6.0
            
        for dy in range(-impact_radius, impact_radius + 1):
            y = mid_y + dy
            if 0 <= y < self.height:
                # Направление импульса — строго вперед по оси X
                self.matrix_px[y, 0] = magnitude * (1.0 - abs(dy)/(impact_radius + 1))

    def step_aolodynamics(self):
        """Продвижение вектора давления по эстафете близкодействия."""
        new_px = np.copy(self.matrix_px)
        new_py = np.copy(self.matrix_py)
        
        for y in range(self.height):
            for x in range(1, self.width):
                # Аол получает толчок ТОЛЬКО если сосед сзади физически давит на него
                left_pressure = self.matrix_px[y, x-1]
                
                # Боковое ущемление матрицы (верхние и нижние слои поджимают жгут)
                top_confinement = self.matrix_py[y-1, x] if y > 0 else 0
                bottom_confinement = self.matrix_py[y+1, x] if y < self.height-1 else 0
                
                # Трансляция импульса по цепочке тесноты (кинематика колыбели Ньютона)
                if left_pressure > 0.05:
                    new_px[y, x] = left_pressure * self.aol_rigidity
                    # Импульс ушел вперед — исходный аол разгружается (возврат к зажиму фона)
                    new_px[y, x-1] *= (1.0 - self.aol_rigidity)
                    
                # Коррекция бокового самоподдержания пучка под внешним прессом
                if abs(top_confinement - bottom_confinement) > 0.01:
                    new_py[y, x] = (top_confinement + bottom_confinement) * 0.1

        self.matrix_px = new_px
        self.matrix_py = new_py

    def render_beam_to_console(self):
        """Визуализация структуры жгута прямо в текстовой консоли."""
        display = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                p = self.matrix_px[y, x]
                if p > 3.0: row += "█"    # Максимально сжатое ядро жгута
                elif p > 1.5: row += "▓"  # Фронт передачи удара
                elif p > 0.5: row += "░"  # Периферийная парусная зона пучка
                else: row += "."          # Непотревоженная стационарная матрица аолов
            display.append(row)
        return "\n".join(display)

# ==============================================================================
# ЗАПУСК СИМУЛЯЦИИ 
# ==============================================================================
if __name__ == "__main__":
    # Строим участок Вселенной (длина 65 аолов, высота 19 аолов)
    space = AolSpaceMatrix(width=65, height=19)
    
    # Запускаем удар атома («включаем красный свет»)
    space.trigger_atomic_impact("red")
    
    print("ЗАПУСК АОЛОДИНАМИЧЕСКОГО ДВИЖКА... СВЕТОВОЙ ЖГУТ В ДЕЙСТВИИ")
    print("Трансляция механического вектора давления по эстафете контактов.\n")
    
    # Просчитываем 60 итераций хода упругого жгута
    for step in range(60):
        # Очистка экрана для плавной анимации в консоли
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"Итерация движения вектора: {step} | Закон КТА: ДАВИШЬ — ДВИЖЕТСЯ")
        print("=" * 65)
        print(space.render_beam_to_console())
        print("=" * 65)
        
        space.step_aolodynamics()
        time.sleep(0.05) # Пауза для восприятия глазами скорости хода 'c'
