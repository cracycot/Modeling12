import pygame
import numpy as np

# Константы
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
POSITIVE_CHARGE_COLOR = (255, 0, 0)  # Красный
NEGATIVE_CHARGE_COLOR = (0, 0, 255)  # Синий
CHARGE_RADIUS = 5
DIPOLE_COLOR = (0, 255, 0)  # Зеленый
FPS = 30
K = 9e9  # Константа электростатики

# Заряды: (x, y, q, color)
charges = []
current_charge_sign = 1  # 1 для положительного, -1 для отрицательного
current_charge_value = 1  # Величина заряда

# Диполь: положение, момент
dipole_position = None
dipole_moment = 1  # Дипольный момент
dipole_angle = 0  # Угол направления диполя (в градусах)

# Расчет потенциала в точке
def potential(x, y):
    V = 0
    for cx, cy, q, _ in charges:
        distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        if distance != 0:
            V += K * q / distance
    return V

# Расчет электрического поля в точке
def electric_field(x, y):
    Ex, Ey = 0, 0
    for cx, cy, q, _ in charges:
        distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        if distance != 0:
            Ex += K * q * (x - cx) / distance**3
            Ey += K * q * (y - cy) / distance**3
    return Ex, Ey

# Расчет силы и момента на диполь
def calculate_dipole_force_and_moment(x, y, p, angle):
    Ex, Ey = electric_field(x, y)
    E_magnitude = np.sqrt(Ex**2 + Ey**2)
    force = E_magnitude * p  # Сила
    torque = p * E_magnitude * np.sin(np.radians(angle))  # Момент силы
    return force, torque, (Ex, Ey)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Диполь в электростатическом поле")
clock = pygame.time.Clock()

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка ввода мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                dipole_position = (x, y)  # Установка диполя
            else:
                color = POSITIVE_CHARGE_COLOR if current_charge_sign > 0 else NEGATIVE_CHARGE_COLOR
                charges.append((x, y, current_charge_sign * current_charge_value, color))

        # Обработка ввода клавиатуры
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_charge_sign = 1  # Положительный заряд
            elif event.key == pygame.K_DOWN:
                current_charge_sign = -1  # Отрицательный заряд
            elif event.key == pygame.K_RIGHT:
                current_charge_value += 1  # Увеличение величины заряда
            elif event.key == pygame.K_LEFT and current_charge_value > 1:
                current_charge_value -= 1  # Уменьшение величины заряда
            elif event.key == pygame.K_w:
                dipole_moment += 1  # Увеличение дипольного момента
            elif event.key == pygame.K_s and dipole_moment > 1:
                dipole_moment -= 1  # Уменьшение дипольного момента
            elif event.key == pygame.K_a:
                dipole_angle -= 5  # Поворот диполя влево
            elif event.key == pygame.K_d:
                dipole_angle += 5  # Поворот диполя вправо

    screen.fill(BACKGROUND_COLOR)

    # Визуализация эквипотенциальных поверхностей
    for x in range(0, WIDTH, 20):
        for y in range(0, HEIGHT, 20):
            V = potential(x, y)
            color_intensity = min(255, max(0, int(128 + V / 1e8)))
            screen.set_at((x, y), (color_intensity, color_intensity, color_intensity))

    # Визуализация линий напряженности
    for x in range(50, WIDTH, 50):
        for y in range(50, HEIGHT, 50):
            px, py = x, y
            for _ in range(100):
                Ex, Ey = electric_field(px, py)
                magnitude = np.sqrt(Ex**2 + Ey**2)
                if magnitude == 0:
                    break
                px += int(Ex / magnitude * 5)
                py += int(Ey / magnitude * 5)
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    pygame.draw.circle(screen, LINE_COLOR, (px, py), 1)
                else:
                    break

    # Визуализация зарядов
    for cx, cy, q, color in charges:
        pygame.draw.circle(screen, color, (cx, cy), CHARGE_RADIUS)

    # Визуализация диполя
    if dipole_position:
        x, y = dipole_position
        dx = np.cos(np.radians(dipole_angle)) * 20
        dy = np.sin(np.radians(dipole_angle)) * 20
        pygame.draw.line(screen, DIPOLE_COLOR, (x - dx, y - dy), (x + dx, y + dy), 3)
        pygame.draw.circle(screen, POSITIVE_CHARGE_COLOR, (int(x + dx), int(y + dy)), CHARGE_RADIUS)
        pygame.draw.circle(screen, NEGATIVE_CHARGE_COLOR, (int(x - dx), int(y - dy)), CHARGE_RADIUS)

        # Расчет силы и момента на диполь
        force, torque, field_vector = calculate_dipole_force_and_moment(x, y, dipole_moment, dipole_angle)
        font = pygame.font.Font(None, 24)
        text = f"Force: {force:.2e}, Torque: {torque:.2e}, Field: ({field_vector[0]:.2e}, {field_vector[1]:.2e})"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()