import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# ПРОЕКТ: AOL PHYSICS (ПРИТЯЖЕНИЯ НЕ СУЩЕСТВУЕТ)
# СИМУЛЯТОР: Графический визуализатор светового жгута (Версия 5.0 - Сплошная линия)
# АВТОРЫ: Вячеслав (mvnaol2026) & AI-Коллега
# ==============================================================================
# Исправлено: Атом давит непрерывно, формируя сплошную линию до самого кружка.
# ==============================================================================

class AolLightVisualizer:
    def __init__(self, width=65, height=19):
        self.width = width
        self.height = height
        self.matrix_px = np.zeros((height, width))
        self.matrix_py = np.zeros((height, width))
        self.aol_rigidity = 0.96
        
    def trigger_atomic_impact(self):
        """Атом осуществляет непрерывное постоянное давление в точку контакта."""
        mid_y = self.height // 2
        # Точка контакта на правой стенке атома (x=2) стабильно подпитывается давлением
        self.matrix_px[mid_y, 2] = 8.0

    def step_aolodynamics(self):
        """Продвижение вектора давления по эстафете близкодействия."""
        new_px = np.copy(self.matrix_px)
        mid_y = self.height // 2
        
        # Передача импульса идет строго по центральной оси
        for x in range(3, self.width):
            left_pressure = self.matrix_px[mid_y, x-1]
            if left_pressure > 0.05:
                # Передаем давление вперед с учетом жесткости среды
                new_px[mid_y, x] = left_pressure * self.aol_rigidity
                # Часть давления остается в цепи, формируя сплошное тело жгута
                new_px[mid_y, x-1] = left_pressure * 0.98

        self.matrix_px = new_px

    def render_to_png(self, filename="aol_light_beam.png", iterations=28):
        # ИСПРАВЛЕНО: Атом давит на КАЖДОМ шаге, заполняя линию целиком
        for _ in range(iterations):
            self.trigger_atomic_impact()
            self.step_aolodynamics()
            
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.set_xlim(-2, self.width)
        ax.set_ylim(-1, self.height)
        ax.axis('off')
        
        mid_y = self.height // 2
        
        # Отрисовка матрицы аолов среды
        for y in range(self.height):
            for x in range(self.width):
                # Исключаем пространство внутри самого Атома
                if x < 2 and y in range(mid_y - 2, mid_y + 3):
                    continue
                    
                px = self.matrix_px[y, x]
                
                # Градиент упругого сжатия сплошного жгута
                if px > 3.0:
                    color = '#FF1E1E'  # Ярко-красный: Сплошное тело жгута давления
                    size = 110
                    alpha = 1.0
                elif px > 0.5:
                    color = '#FF6666'  # Розовый: Стабилизирующий шлейф
                    size = 75
                    alpha = 0.8
                else:
                    color = '#EAEAEA'  # Серый: Непотревоженная стационарная матрица Вселенной
                    size = 20
                    alpha = 0.4
                    
                ax.scatter(x, y, color=color, s=size, edgecolors='none', alpha=alpha, zorder=2)
                
        # Рисуем Атом-источник (x=0, y=mid_y, радиус 2)
        atom_source = patches.Circle((0, mid_y), 2.0, 
                                     edgecolor='#333333', facecolor='#666666', lw=2.5, zorder=3)
        ax.add_patch(atom_source)
        ax.text(-0.8, mid_y - 0.3, "Атом", fontsize=10, fontweight='bold', color='white', zorder=4)
        
        ax.text(1, self.height - 1.2, r"$\mathbf{Aol\ Physics:\ Continuous\ Light\ Beam\ Visualizer}$", 
                fontsize=13, fontweight='bold', family='sans-serif')
        
        # Указатели механики тесноты
        ax.annotate('Постоянный механический привод Атома', 
                    xy=(2.0, mid_y), xytext=(4, self.height - 4),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1.0, headwidth=5),
                    fontsize=9.5, color='#333333')
        
        # Стрелка указывает на сплошную линию контакта
        ax.annotate('Сплошной жгут давления (Цепь соударений дотянута до Атома)', 
                    xy=(iterations // 2, mid_y), xytext=((iterations // 2) - 8, mid_y - 4),
                    arrowprops=dict(facecolor='red', shrink=0.05, width=1.2, headwidth=5),
                    fontsize=9.5, color='red', fontweight='bold')
        
        plt.savefig(filename, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"[ВЕРИФИКАЦИЯ КТА]: Сплошной линейный чертеж сохранен в файл: {filename}")

if __name__ == "__main__":
    visualizer = AolLightVisualizer()
    visualizer.render_to_png(iterations=28)
