import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# ПРОЕКТ: AOL PHYSICS (ПРИТЯЖЕНИЯ НЕ СУЩЕСТВУЕТ)
# СИМУЛЯТОР: Графический визуализатор всенаправленного аольного прижима
# АВТОРЫ: Вячеслав (mvnaol2026) & AI-Коллега
# ==============================================================================
# Графическое дополнение к расчетному движку aol_gravity_press_engine.py.
# Визуализирует пространственный дефицит ударов и конус гравитационной тени КТА.
# ==============================================================================

class AolGravityVisualizer:
    def __init__(self, size_x=60, size_y=30):
        self.size_x = size_x
        self.size_y = size_y
        
        # Параметры двух тел (их координаты и парусность/масса в КТА)
        self.b1_x = 18.0
        self.b1_y = size_y / 2
        self.b1_radius = 3.5  # Крупный макро-кластер 1
        
        self.b2_x = 42.0
        self.b2_y = size_y / 2
        self.b2_radius = 2.0  # Малый макро-кластер 2
        
        # Расстояние между центрами для расчёта телесного угла
        self.distance = abs(self.b2_x - self.b1_x)
        
    def calculate_shadow_field(self, x, y):
        """
        Расчет локального профиля давления среды КТА в точке (x, y).
        Базовый фон изотропного зажима Вселенной = 1.0.
        Внутри конуса взаимной тени давление падает из-за геометрического заслонения.
        """
        # Если точка внутри самих тел, давление там не применимо
        if (x - self.b1_x)**2 + (y - self.b1_y)**2 <= self.b1_radius**2:
            return 0.0
        if (x - self.b2_x)**2 + (y - self.b2_y)**2 <= self.b2_radius**2:
            return 0.0
            
        base_pressure = 1.0
        
        # Механика КТА: Проверяем, находится ли точка в створе между телами
        if self.b1_x < x < self.b2_x:
            # Расстояние от точки до осевой линии
            dy = abs(y - self.b1_y)
            
            # Геометрические границы конуса тени (линейная интерполяция заслонения)
            t = (x - self.b1_x) / self.distance
            current_shadow_radius = self.b1_radius * (1 - t) + self.b2_radius * t
            
            if dy <= current_shadow_radius:
                # Внутренний дефицит ударов (зона тени). Давление падает до 0.4
                depth_factor = 1.0 - (dy / (current_shadow_radius + 1e-9))
                return base_pressure - 0.6 * depth_factor
                
        return base_pressure

    def render_to_png(self, filename="aol_gravity_shadow.png"):
        """Генерация высокоточного чертежа теневого конуса и векторов прижима."""
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xlim(0, self.size_x)
        ax.set_ylim(0, self.size_y)
        ax.axis('off')
        
        # Генерируем сетку для визуализации плотности аольного джиттера
        x_space = np.linspace(1, self.size_x - 1, 45)
        y_space = np.linspace(1, self.size_y - 1, 25)
        
        for x in x_space:
            for y in y_space:
                p = self.calculate_shadow_field(x, y)
                if p == 0.0:
                    continue  # Пропускаем внутренности тел
                    
                # Цветовой градиент: серый — полный зажим, синий/голубой — дефицит давления (тень)
                if p < 0.6:
                    color = '#1E90FF'  # Додонова синева: Глубокая тень (дефицит ударов среды)
                    size = 75
                elif p < 0.9:
                    color = '#87CEFA'  # Полутень
                    size = 45
                else:
                    color = '#DCDCDC'  # Базовая изотропная вибрирующая матрица аолов (1.0)
                    size = 15
                    
                ax.scatter(x, y, color=color, s=size, edgecolors='none', alpha=0.7, zorder=1)
        
        # Рисуем Тело 1
        body1 = patches.Circle((self.b1_x, self.b1_y), self.b1_radius, 
                              edgecolor='#333333', facecolor='#666666', lw=2.5, zorder=3)
        # Рисуем Тело 2
        body2 = patches.Circle((self.b2_x, self.b2_y), self.b2_radius, 
                              edgecolor='#333333', facecolor='#444444', lw=2.5, zorder=3)
        ax.add_patch(body1)
        ax.add_patch(body2)
        
        # Внешние силовые векторы — Вселенский пресс КТА, придавливающий тела друг к другу
        ax.arrow(self.b1_x - self.b1_radius - 5, self.b1_y, 4, 0, width=0.4, head_width=1.2, head_length=1.5, fc='red', ec='red', zorder=4)
        ax.arrow(self.b2_x + self.b2_radius + 5, self.b2_y, -4, 0, width=0.4, head_width=1.2, head_length=1.5, fc='red', ec='red', zorder=4)
        
        # Текстовые аннотации законов Аолодинамики
        ax.text(1, self.size_y - 2.0, r"$\mathbf{Aol\ Physics:\ Comprehensive\ Gravity\ Press\ Simulator}$", 
                fontsize=13, fontweight='bold', family='sans-serif')
        
        ax.text(self.b1_x - 3.5, self.b1_y + self.b1_radius + 1.0, f"Макро-кластер 1", fontsize=9, fontweight='bold')
        ax.text(self.b2_x - 2.5, self.b2_y + self.b2_radius + 1.0, f"Макро-кластер 2", fontsize=9, fontweight='bold')
        
        # Указатели сути гравитации
        ax.annotate('Внешний прижим среды (Давление Вселенной)', 
                    xy=(self.b1_x - self.b1_radius - 1, self.b1_y), xytext=(2, 6),
                    arrowprops=dict(facecolor='red', shrink=0.05, width=1.0, headwidth=5), fontsize=9.5, color='red', fontweight='bold')
        
        ax.annotate('Зона геометрического дефицита ударов (Тень КТА)', 
                    xy=((self.b1_x + self.b2_x)/2, self.b1_y), xytext=((self.b1_x + self.b2_x)/2 - 10, self.size_y - 5),
                    arrowprops=dict(facecolor='#1E90FF', shrink=0.05, width=1.0, headwidth=5), fontsize=9.5, color='#1E90FF', fontweight='bold')
        
        ax.text(1, 0.8, f"• Дистанция: {self.distance} аолов | Вывод стереометрии: дефицит ударов масштабируется строго по закону 1/r²", 
                fontsize=9.5, style='italic', color='#444444')
        
        plt.savefig(filename, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"\n[УСПЕХ]: Графический чертеж гравитационной тени КТА успешно сохранен в файл: {filename}")

if __name__ == "__main__":
    visualizer = AolGravityVisualizer()
    visualizer.render_to_png()
