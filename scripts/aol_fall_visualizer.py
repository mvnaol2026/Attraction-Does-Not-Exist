import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# ПРОЕКТ: AOL PHYSICS (ПРИТЯЖЕНИЯ НЕ СУЩЕСТВУЕТ)
# СИМУЛЯТОР: Графический визуализатор механики падения в тесноте
# АВТОРЫ: Вячеслав (mvnaol2026) & AI-Коллега
# ==============================================================================
# Графическое дополнение к расчетному движку fall_vacuum_vs_air.py.
# Наглядно чертит изотропный прижим среды и молекулярный барьер воздуха.
# ==============================================================================

class AolFallVisualizer:
    def __init__(self):
        self.y_start = 80.0
        self.ground_y = 5.0
        
        # Фиксируем кадр на середине пути для наглядности векторов
        # Вакуум: синхронное падение на одной высоте
        self.vac_heavy_y = 45.0
        self.vac_light_y = 45.0
        
        # Атмосфера: перо отстало из-за большой площади (парусности)
        self.air_heavy_y = 40.0
        self.air_light_y = 65.0

    def render_to_png(self, filename="aol_fall_comparison.png"):
        """Генерация двухпанельного декартова чертежа механики падения КТА."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
        
        # Общие настройки для обеих координатных плоскостей
        for ax in (ax1, ax2):
            ax.set_xlim(-10, 10)
            ax.set_ylim(-2, 100)
            ax.axis('off')
            # Поверхность Земли — пространственный фильтр-заслонка
            ground = patches.Rectangle((-10, 0), 20, self.ground_y, facecolor='#8B4513', edgecolor='#555555', lw=1.5, zorder=3)
            ax.add_patch(ground)
            ax.text(0, 1.5, "Поверхность Земли (Заслонка вибраций)", color='white', fontsize=9, fontweight='bold', ha='center', zorder=4)

        # ======================================================================
        # ПАНЕЛЬ 1: БЕЗВОЗДУШНОЕ ПРОСТРАНСТВО (ВАКУУМ)
        # ======================================================================
        ax1.text(-9, 94, r"$\mathbf{1.\ Безвоздушное\ пространство\ (Вакуум)}$", fontsize=11, fontweight='bold', family='sans-serif')
        ax1.text(-9, 90, "Чистый градиент давления среды космоса сверху вниз", fontsize=9.5, style='italic', color='#555555')
        
        # Отрисовка фоновой матрицы аольного прижима (стрелы давления среды)
        for x in np.linspace(-8, 8, 9):
            ax1.arrow(x, 90, 0, -15, width=0.15, head_width=0.5, head_length=1.5, fc='#FF3333', ec='#FF3333', alpha=0.6, zorder=1)
            
        # Тяжелая компактная гиря (много связанных аолов)
        vac_heavy = patches.Circle((-4, self.vac_heavy_y), 2.2, edgecolor='#333333', facecolor='magenta', lw=2, zorder=3)
        ax1.add_patch(vac_heavy)
        ax1.text(-4, self.vac_heavy_y + 3, "Гиря\n(1000 аолов)", fontsize=8.5, fontweight='bold', ha='center')
        ax1.arrow(-4, self.vac_heavy_y + 8, 0, -4, width=0.2, head_width=0.6, head_length=1.0, fc='red', ec='red', zorder=4)
        
        # Легкое перо (мало аолов, в вакууме парусность воздуха не работает)
        vac_light = patches.Circle((4, self.vac_light_y), 1.2, edgecolor='#333333', facecolor='cyan', lw=2, zorder=3)
        ax1.add_patch(vac_light)
        ax1.text(4, self.vac_light_y + 2, "Перо\n(10 аолов)", fontsize=8.5, fontweight='bold', ha='center')
        ax1.arrow(4, self.vac_light_y + 6, 0, -4, width=0.2, head_width=0.6, head_length=1.0, fc='red', ec='red', zorder=4)
        
        # Демонстрация синхронности хода линией связи
        ax1.plot([-4, 4], [self.vac_heavy_y, self.vac_light_y], 'r--', alpha=0.5, lw=1.2)
        ax1.text(0, self.vac_heavy_y + 1, "СИНХРОННО: Y₁ = Y₂", color='red', fontsize=9, fontweight='bold', ha='center')

        # ======================================================================
        # ПАНЕЛЬ 2: НАЛИЧИЕ АТМОСФЕРЫ (ВОЗДУХ)
        # ======================================================================
        ax2.text(-9, 94, r"$\mathbf{2.\ Наличие\ атмосферы\ (Воздушная\ среда)}$", fontsize=11, fontweight='bold', family='sans-serif')
        ax2.text(-9, 90, "Встречные механические удары молекул воздуха снизу", fontsize=9.5, style='italic', color='#555555')
        
        # Верхний прижим среды остается прежним
        for x in np.linspace(-8, 8, 9):
            ax2.arrow(x, 90, 0, -15, width=0.15, head_width=0.5, head_length=1.5, fc='#FF3333', ec='#FF3333', alpha=0.6, zorder=1)
            
        # Отображение молекулярного барьера воздуха (точечные зацепления тесноты)
        air_x, air_y = np.meshgrid(np.linspace(-9, 9, 20), np.linspace(self.ground_y + 2, 85, 18))
        ax2.scatter(air_x, air_y, color='#87CEFA', s=8, alpha=0.4, zorder=1, label='Молекулы воздуха')
        
        # Компактная гиря в атмосфере (малая площадь — легко пробивает воздух)
        air_heavy = patches.Circle((-4, self.air_heavy_y), 2.2, edgecolor='#333333', facecolor='red', lw=2, zorder=3)
        ax2.add_patch(air_heavy)
        ax2.text(-4, self.air_heavy_y + 3, "Гиря\n(Пробивает)", fontsize=8.5, fontweight='bold', ha='center')
        ax2.arrow(-4, self.air_heavy_y + 8, 0, -4, width=0.2, head_width=0.6, head_length=1.0, fc='red', ec='red', zorder=4)
        # Слабое сопротивление снизу из-за малого сечения
        ax2.arrow(-4, self.air_heavy_y - 5, 0, 2, width=0.1, head_width=0.4, head_length=0.8, fc='blue', ec='blue', zorder=4)
        
        # Широкое перо в атмосфере (большая горизонтальная площадь парусности)
        # Моделируем перо как широкую пластину парусности (area = 4.0)
        air_light = patches.Rectangle((1.5, self.air_light_y - 0.5), 5.0, 1.0, edgecolor='#333333', facecolor='blue', lw=2, zorder=3)
        ax2.add_patch(air_light)
        ax2.text(4, self.air_light_y + 2, "Перо\n(Большая парусность)", fontsize=8.5, fontweight='bold', ha='center')
        ax2.arrow(4, self.air_light_y + 6, 0, -3, width=0.15, head_width=0.5, head_length=0.8, fc='red', ec='red', zorder=4)
        
        # Мощные встречные стрелы сопротивления воздуха в широкое дно пера
        ax2.arrow(2.5, self.air_light_y - 6, 0, 4, width=0.2, head_width=0.5, head_length=1.0, fc='blue', ec='blue', zorder=4)
        ax2.arrow(5.5, self.air_light_y - 6, 0, 4, width=0.2, head_width=0.5, head_length=1.0, fc='blue', ec='blue', zorder=4)
        ax2.text(4, self.air_light_y - 9, "Торможение КТА\n(Парусный барьер)", color='blue', fontsize=8, fontweight='bold', ha='center')

        # Общий вывод теории
        fig.text(0.05, 0.02, "• В вакууме масса (число аолов) не влияет на темп разгона — среда толкает каждый элемент синхронно.\n• В атмосфере отставание вызвано исключительно площадью поперечного сечения (числом лобовых соударений с молекулами).", 
                 fontsize=9.5, style='italic', color='#222222')
        
        plt.savefig(filename, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"\n[ВЕРИФИКАЦИЯ КТА]: Сравнительный чертеж падения тел успешно сохранен в файл: {filename}")

if __name__ == "__main__":
    visualizer = AolFallVisualizer()
    visualizer.render_to_png()
