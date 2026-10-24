import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# =========================================================================
# КВАНТОВАЯ ТЕОРИЯ АОЛОДИНАМИКИ (КТА) - ГРАФИЧЕСКИЙ СИМУЛЯТОР ТОКА И НАГРЕВА
# =========================================================================
# Графическое дополнение к расчетному ядру aol_electric_snake_engine.py
# Визуализация Тезиса №12 Аольной физики. Авторы: Вячеслав (mvnaol2026)
# =========================================================================

class AolCurrentVisualizer:
    def __init__(self):
        # Геометрия кристаллической решетки проводника (пассивные атомы-LEGO)
        self.num_atoms = 5
        self.atom_spacing = 4.0
        self.atoms_x = np.array([2.0, 6.0, 10.0, 14.0, 18.0])
        self.lattice_y = 0.0
        self.atom_radius = 1.2
        self.atoms_vibration = np.zeros_like(self.atoms_x) # Тепловой джиттер КТА
        
        # Параметры бугристой аольной змеи тока (цепочка жестких носителей среды)
        self.num_aols = 25
        self.aol_radius = 0.3
        self.snake_x = np.linspace(-4.0, 16.0, self.num_aols)
        self.base_y = -1.5
        
        # Задаем изначальный волновой рельеф бугров змеи
        self.snake_profile = 0.4 * np.sin(2.0 * np.pi * self.snake_x / 1.8)
        self.snake_y = self.base_y + self.snake_profile
        
        # Силовые параметры тесноты КТА
        self.push_force = 0.15      # Избыточное внешнее давление среды (напряжение)
        self.current_velocity = 0.0
        
    def step(self, dt=0.2):
        # Главный закон движения: ДАВИШЬ - ДВИЖЕТСЯ
        net_force = self.push_force
        mechanical_drag = 0.0
        
        # Сканируем контакты бугров змеи с пассивными атомами решетки
        for i in range(self.num_aols):
            ax = self.snake_x[i]
            ay = self.snake_y[i]
            
            # Находим ближайший атом
            closest_idx = np.argmin(np.abs(self.atoms_x - ax))
            closest_atom_x = self.atoms_x[closest_idx]
            
            # Стереометрия столкновения границ тесноты
            dx = ax - closest_atom_x
            dy = ay - self.lattice_y
            dist = np.sqrt(dx**2 + dy**2)
            collision_dist = self.atom_radius + self.aol_radius
            
            if dist < collision_dist:
                overlap = collision_dist - dist
                # Механическое сопротивление (зацепление бугра за выступ решетки)
                force_direction_x = dx / dist
                drag_component = overlap * 0.8 * (-force_direction_x)
                
                if drag_component < 0:
                    mechanical_drag += np.abs(drag_component)
                
                # Передача импульса давления (раскачивание атома, выделение тепла)
                self.atoms_vibration[closest_idx] += overlap * 0.25

        # Вычитаем силу якорения из толкающего давления среды
        effective_force = max(0.0, net_force - (mechanical_drag * 0.05))
        self.current_velocity = effective_force
        
        # Продвигаем змею по зазорам тесноты
        self.snake_x += self.current_velocity * dt
        
        # Зацикливаем поток для непрерывности кадра
        for i in range(self.num_aols):
            if self.snake_x[i] > 20.0:
                self.snake_x[i] -= 24.0
                
        # Пересчитываем рельеф змеи на новых координатах
        self.snake_profile = 0.4 * np.sin(2.0 * np.pi * self.snake_x / 1.8)
        self.snake_y = self.base_y + self.snake_profile
        
        # Рассеивание избыточного джиттера атомов в окружающую аольную матрицу
        self.atoms_vibration *= 0.92

    def run_and_plot(self, steps=35):
        # Прогон симуляции для накопления динамических эффектов и прогрева
        for _ in range(steps):
            self.step()
            
        # Рендеринг чертежа
        fig, ax = plt.subplots(figsize=(10, 4.5))
        ax.set_xlim(0, 20)
        ax.set_ylim(-3, 3)
        ax.axis('off')
        
        # Рисуем атомы проводника
        for i, x_pos in enumerate(self.atoms_x):
            vib = self.atoms_vibration[i]
            # Цвет переходит в красный при росте вибрации (механический нагрев)
            color_val = min(1.0, vib * 2.0)
            atom_color = (0.3 + 0.7 * color_val, 0.4 * (1.0 - color_val), 0.8 * (1.0 - color_val))
            
            atom = patches.Circle((x_pos, self.lattice_y), self.atom_radius, 
                                  edgecolor='black', facecolor=atom_color, lw=2, zorder=3)
            ax.add_patch(atom)
            
            # Стрелки теплового микроколебания КТА
            if vib > 0.05:
                ax.annotate('', xy=(x_pos + 0.3, self.lattice_y + 0.3), xytext=(x_pos - 0.3, self.lattice_y - 0.3),
                            arrowprops=dict(arrowstyle="<->", color='red', lw=1.5))
                
        # Рисуем винтовую аольную змею тока
        ax.plot(self.snake_x, self.snake_y, color='darkgreen', lw=3, zorder=1)
        for i in range(self.num_aols):
            if 0 <= self.snake_x[i] <= 20:
                aol = patches.Circle((self.snake_x[i], self.snake_y[i]), self.aol_radius, 
                                     edgecolor='darkgreen', facecolor='lime', zorder=2)
                ax.add_patch(aol)
                
        # Вывод данных макро-расчета
        mean_vibe = sum(self.atoms_vibration) / len(self.atoms_vibration)
        temperature = 2.7 + (mean_vibe ** 2) * 450.0
        
        ax.text(1, 2.2, r"$\mathbf{Aol\ Physics:\ Current\ Flow\ \&\ Heat\ Visualizer}$", fontsize=12, family='sans-serif')
        ax.text(1, -2.5, f"Давление среды (Push Force): {self.push_force} аол-ед.", fontsize=9, color='blue')
        ax.text(12, -2.5, f"Итоговая теплота: {temperature:.1f} K", fontsize=9, color='red')
        
        output_file = "aol_current_flow.png"
        plt.savefig(output_file, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"\n[УСПЕХ]: Графический чертеж Аолодинамики тока успешно сохранен в файл: {output_file}")

if __name__ == "__main__":
    visualizer = AolCurrentVisualizer()
    visualizer.run_and_plot()
