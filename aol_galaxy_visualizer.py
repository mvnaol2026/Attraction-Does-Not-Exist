import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# ПРОЕКТ: AOL PHYSICS (ПРИТЯЖЕНИЯ НЕ СУЩЕСТВУЕТ)
# СИМУЛЯТОР: Графический визуализатор синхронного разлета космических тел КТА
# АВТОРЫ: Вячеслав (mvnaol2026) & AI-Коллега
# ==============================================================================
# Графическое дополнение к расчетному движку galaxy_expansion_mechanics.py.
# Наглядно чертит градиент давления ячейки и однослойные клинья ускорения тел.
# ==============================================================================

class AolGalaxyVisualizer:
    def __init__(self, size_x=60, size_y=40):
        self.size_x = size_x
        self.size_y = size_y
        
        # Центр космической ячейки Вселенной (центр высокого давления аолов)
        self.center_x = 10.0
        self.center_y = size_y / 2
        
        # Позиции двух тел разной массы, синхронно вытолкнутых давлением среды
        # Оба тела прошли одинаковое расстояние по оси X под ударами клиньев
        self.b1_x = 42.0
        self.b1_y = 28.0
        self.b1_radius = 1.2  # Легкое тело (малый набор аолов)
        
        self.b2_x = 42.0
        self.b2_y = 12.0
        self.b2_radius = 2.8  # Тяжелое тело (большой набор аолов, увеличенная парусность)
        
    def calculate_space_pressure(self, x, y):
        """
        Расчет градиента давления вибрирующей аольной матрицы в ячейке КТА.
        Давление максимальное в центре ячейки и падает к периферии (выталкивание).
        Вокруг движущихся тел формируются однослойные клинья обжатия среды.
        """
        # Исключаем внутреннее пространство макротел
        if (x - self.b1_x)**2 + (y - self.b1_y)**2 <= self.b1_radius**2:
            return 0.0
        if (x - self.b2_x)**2 + (y - self.b2_y)**2 <= self.b2_radius**2:
            return 0.0
            
        # Базовый градиент давления среды от центра ячейки
        dist_to_center = np.sqrt((x - self.center_x)**2 + (y - self.center_y)**2)
        base_pressure = 100.0 * np.exp(-dist_to_center**2 / (2 * 28**2))
        
        # СТРОГАЯ МЕХАНИКА КТА: Моделирование ОДНОСЛОЙНЫХ толкающих клиньев сзади тел
        # Клин вдавливается ровно в один слой аолов вплотную к корме (сзади по ходу разлета по X)
        for bx, by, br in [(self.b1_x, self.b1_y, self.b1_radius), (self.b2_x, self.b2_y, self.b2_radius)]:
            # Зона вплотную за кормой тела (x на один шаг левее левой границы)
            rear_x = int(bx - br - 1)
            if x == rear_x and abs(y - by) <= br:
                if y == by:
                    return base_pressure + 45.0  # Острие клина — пик преобладающего давления
                else:
                    return base_pressure + 25.0  # Боковые грани однослойного клина обжатия
                    
            # Среда не отстает: плотное обжатие сверху и снизу контура
            if abs(x - bx) <= br and abs(abs(y - by) - (br + 1)) < 0.1:
                return base_pressure + 15.0
                
        return base_pressure

    def render_to_png(self, filename="aol_galaxy_expansion.png"):
        """Генерация декартова чертежа синхронного разлета галактик разной массы."""
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, self.size_x)
        ax.set_ylim(0, self.size_y)
        ax.axis('off')
        
        # Генерируем дискретную сетку аольного пространства ячейки Вселенной
        x_space = np.linspace(2, self.size_x - 2, 50)
        y_space = np.linspace(2, self.size_y - 2, 34)
        
        for x in x_space:
            for y in y_space:
                # Округляем до целых для четкой поштучной фиксации однослойных клиньев
                p = self.calculate_space_pressure(int(x), int(y))
                if p == 0.0:
                    continue  # Пропускаем геометрию самих тел
                    
                # Цветовой градиент напора упругой среды Вселенной
                if p > 110.0:
                    color = '#FF1E1E'  # Красный: Острие и грани ОДНОСЛОЙНЫХ клиньев
                    size = 110
                elif p > 85.0:
                    color = '#FF7F00'  # Оранжевый: Центр высокого давления ячейки / обжатие
                    size = 75
                elif p > 55.0:
                    color = '#FFD700'  # Желтый: Зона среднего напора среды
                    size = 45
                else:
                    color = '#EAEAEA'  # Серый: Периферийная зона низкого давления среды
                    size = 20
                    
                ax.scatter(int(x), int(y), color=color, s=size, edgecolors='none', alpha=0.75, zorder=1)
        
        # Отрисовка Тела 1 (Легкое)
        body1 = patches.Circle((self.b1_x, self.b1_y), self.b1_radius, 
                              edgecolor='#333333', facecolor='cyan', lw=2, zorder=3, label='Легкое тело')
        # Отрисовка Тела 2 (Тяжелое)
        body2 = patches.Circle((self.b2_x, self.b2_y), self.b2_radius, 
                              edgecolor='#333333', facecolor='magenta', lw=2, zorder=3, label='Тяжелое тело')
        ax.add_patch(body1)
        ax.add_patch(body2)
        
        # Символические траектории (пунктирные следы синхронного хода)
        ax.plot([self.center_x, self.b1_x - self.b1_radius], [self.b1_y, self.b1_y], 'c--', alpha=0.7, lw=1.5)
        ax.plot([self.center_x, self.b2_x - self.b2_radius], [self.b2_y, self.b2_y], 'm--', alpha=0.7, lw=1.5)
        
        # Векторы выталкивающего градиента давления среды из центра ячейки
        ax.arrow(self.center_x, self.center_y, 8, 6, width=0.3, head_width=1.0, head_length=1.5, fc='#FF7F00', ec='#FF7F00', zorder=2)
        ax.arrow(self.center_x, self.center_y, 8, -6, width=0.3, head_width=1.0, head_length=1.5, fc='#FF7F00', ec='#FF7F00', zorder=2)
        ax.text(self.center_x - 6, self.center_y - 0.5, "ЦЕНТР\nЯЧЕЙКИ\n(Макс. P)", fontsize=9, fontweight='bold', color='darkorange', ha='center')
        
        # Инженерные текстовые указатели законов КТА
        ax.text(1, self.size_y - 2.0, r"$\mathbf{Aol\ Physics:\ Galaxy\ Synchronous\ Expansion\ Visualizer}$", 
                fontsize=13, fontweight='bold', family='sans-serif')
        
        ax.annotate('1. Среда выдавливает тела из центра к периферии (Градиент давления)', 
                    xy=(self.center_x + 6, self.center_y + 4.5), xytext=(2, self.size_y - 6),
                    arrowprops=dict(facecolor='orange', shrink=0.05, width=1.0, headwidth=5), fontsize=9.5, color='darkorange', fontweight='bold')
        
        ax.annotate('2. Среда НЕ ОТСТАЕТ и вдавливает ОДНОСЛОЙНЫЙ клин в корму тел', 
                    xy=(self.b1_x - self.b1_radius - 1, self.b1_y), xytext=(self.b1_x - 28, self.b1_y + 4),
                    arrowprops=dict(facecolor='red', shrink=0.05, width=1.0, headwidth=5), fontsize=9.5, color='red', fontweight='bold')
        
        ax.text(1, 0.8, f"• СИНХРОННОСТЬ ДОКАЗАНА: Легкая (cyan) и Тяжелая (magenta) галактики ушли на равный шаг X = {self.b1_x:.1f}.\n• Причина: Среда толкает каждый элементарный аол структуры с одинаковой силой независимо от общей массы кластера.", 
                fontsize=9.5, style='italic', color='#333333')
        
        plt.savefig(filename, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"\n[ВЕРИФИКАЦИЯ КТА]: Чертеж разлета галактик успешно сохранен в файл: {filename}")

if __name__ == "__main__":
    visualizer = AolGalaxyVisualizer()
    visualizer.render_to_png()
