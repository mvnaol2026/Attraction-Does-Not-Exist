import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# ПРОЕКТ: AOL PHYSICS (ПРИТЯЖЕНИЯ НЕ СУЩЕСТВУЕТ)
# СИМУЛЯТОР: Графический визуализатор аольных клиньев инерции (Версия 2.0)
# АВТОРЫ: Вячеслав (mvnaol2026) & AI-Коллега
# ==============================================================================
# Исправлено строго по механике КТА:
# 1. Среда НЕ ОТСТАЕТ и полностью обжимает тело (нет пустоты).
# 2. Клин строго ОДНОСЛОЙНЫЙ.
# 3. Клин создает преобладающее давление между средой и телом.
# ==============================================================================

class AolWedgesVisualizer:
    def __init__(self, size_x=65, size_y=17):
        self.size_x = size_x
        self.size_y = size_y
        
        # Базовый изотропный зажим непотревоженной среды (давление 1.0)
        self.matrix_pressure = np.ones((size_y, size_x)) * 1.0
        
        # Параметры пассивного тела (координаты и радиус парусности)
        self.body_x = 30 
        self.body_y = size_y // 2
        self.body_radius = 4 
        
    def calculate_pressures(self):
        """Строгий расчет по трем пунктам КТА: обжатие, однослойность, преобладание."""
        self.matrix_pressure = np.ones((self.size_y, self.size_x)) * 1.0
        
        # 1. ПЕРЕДНИЙ ФРОНТ: Раздвижение среды (аолы уходят на фланги обтекания)
        front_x = self.body_x + self.body_radius + 1
        for dy in range(-self.body_radius - 1, self.body_radius + 2):
            y = self.body_y + dy
            if 0 <= y < self.size_y and front_x < self.size_x:
                if abs(dy) >= self.body_radius:
                    # Зона, где среда раздвигается и уплотняется, уходя вбок
                    self.matrix_pressure[y, front_x - 1] = 2.0
                
        # 2 и 3. ТЫЛОВОЙ КЛИН: Строго ОДНОСЛОЙНЫЙ зазор обжатия неотстающей среды
        # Клин формируется ровно в один слой (dx_offset = 1) вплотную к границе тела
        rear_x = self.body_x - self.body_radius - 1
        if 0 <= rear_x < self.size_x:
            for dy in range(-self.body_radius, self.body_radius + 1):
                y = self.body_y + dy
                if 0 <= y < self.size_y:
                    if dy == 0:
                        # Острие однослойного клина — пик преобладающего давления (3.5)
                        self.matrix_pressure[y, rear_x] = 3.5  
                    elif abs(dy) <= 2:
                        # Боковые грани однослойного клина между телом и средой (2.6)
                        self.matrix_pressure[y, rear_x] = 2.6
                    else:
                        # Замыкающие точки контакта обжатия (1.8)
                        self.matrix_pressure[y, rear_x] = 1.8

    def render_to_png(self, filename="aol_wedges_inertia.png"):
        """Генерация высокоточного чертежа инерционного хода по трем законам КТА."""
        self.calculate_pressures()
        
        fig, ax = plt.subplots(figsize=(14, 5.5))
        ax.set_xlim(0, self.size_x)
        ax.set_ylim(0, self.size_y)
        ax.axis('off')
        
        # Отрисовка матрицы аолов
        for y in range(self.size_y):
            for x in range(self.size_x):
                # Исключаем пространство, занятое самим пассивным телом
                if (x - self.body_x)**2 + (y - self.body_y)**2 <= self.body_radius**2:
                    continue
                    
                p = self.matrix_pressure[y, x]
                
                # Цветовая кодировка сил давления в тесноте
                if p >= 3.0:
                    color = '#FF1E1E'  # Красный: Острие ОДНОСЛОЙНОГО толкающего клина
                    size = 130
                elif p >= 2.0:
                    color = '#FF8C00'  # Оранжевый: Зоны преобладающего давления клина и флангов раздвижения
                    size = 90
                elif p >= 1.5:
                    color = '#FFD700'  # Желтый: Точки полного обжатия неотстающей среды
                    size = 60
                else:
                    color = '#DCDCDC'  # Серый: Стационарная сжатая матрица аолов Вселенной
                    size = 25
                    
                ax.scatter(x, y, color=color, s=size, edgecolors='none', alpha=0.8, zorder=2)
        
        # Пассивное тело-заслонка
        body = patches.Circle((self.body_x, self.body_y), self.body_radius, 
                              edgecolor='#333333', facecolor='#555555', lw=3, zorder=3)
        ax.add_patch(body)
        
        # Вектор вынужденного движения от преобладающего давления
        ax.arrow(self.body_x, self.body_y, 6, 0, width=0.2, head_width=0.8, head_length=1.2, 
                 fc='#333333', ec='#333333', zorder=4)
        
        # Текстовые аннотации
        ax.text(1, self.size_y - 1.5, r"$\mathbf{Aol\ Physics:\ Pure\ Mechanical\ Inertia\ Engine}$", 
                fontsize=13, fontweight='bold', family='sans-serif')
        
        # Чертим четкие указатели векторов по твоим трем пунктам
        ax.annotate('1. Среда НЕ ОТСТАЕТ и полностью обжимает контур', 
                    xy=(self.body_x - 1, self.body_y + self.body_radius + 0.5), xytext=(self.body_x - 12, self.size_y - 4),
                    arrowprops=dict(facecolor='yellow', shrink=0.05, width=1.2, headwidth=5),
                    fontsize=9.5, fontweight='bold', color='#B8860B')
        
        ax.annotate('2. Строго ОДНОСЛОЙНЫЙ аольный клин', 
                    xy=(self.body_x - self.body_radius - 1, self.body_y + 1), xytext=(self.body_x - 25, self.body_y + 4),
                    arrowprops=dict(facecolor='red', shrink=0.05, width=1.2, headwidth=5),
                    fontsize=9.5, fontweight='bold', color='red')

        ax.annotate('3. Преобладающее давление вдавливания клина (Толкатель)', 
                    xy=(self.body_x - self.body_radius - 1, self.body_y), xytext=(self.body_x - 28, self.body_y - 5),
                    arrowprops=dict(facecolor='darkred', shrink=0.05, width=1.2, headwidth=5),
                    fontsize=9.5, fontweight='bold', color='darkred')
        
        plt.savefig(filename, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"[ВЕРИФИКАЦИЯ КТА]: Чертеж обновлен строго по 3 пунктам соавтора и сохранен в {filename}")

if __name__ == "__main__":
    visualizer = AolWedgesVisualizer()
    visualizer.render_to_png()
