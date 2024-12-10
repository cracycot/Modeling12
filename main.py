import pygame
import numpy as np

# Константы
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
POSITIVE_CHARGE_COLOR = (255, 0, 0)  # Красный для положительных зарядов
NEGATIVE_CHARGE_COLOR = (0, 0, 255)  # Синий для отрицательных зарядов
CHARGE_RADIUS = 5
FPS = 30

# Заряды: (x, y, q, color)
charges = []
current_charge_sign = 1  # 1 для положительного, -1 для отрицательного
current_charge_value = 1  # Величина заряда

# Расчет потенциала в точке
def potential(x, y):
    k = 9e9  # Коэффициент
    V = 0
    for cx, cy, q, _ in charges:
        distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        if distance != 0:
            V += k * q / distance
    return V

# Расчет электрического поля в точке
def electric_field(x, y):
    Ex, Ey = 0, 0
    for cx, cy, q, _ in charges:
        distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        if distance != 0:
            Ex += q * (x - cx) / distance ** 3
            Ey += q * (y - cy) / distance ** 3
    return Ex, Ey

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Визуализация эквипотенциальных поверхностей")
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
            for _ in range(100):  # Увеличено количество шагов
                Ex, Ey = electric_field(px, py)
                magnitude = np.sqrt(Ex ** 2 + Ey ** 2)
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

    # Вывод текущих параметров заряда
    font = pygame.font.Font(None, 36)
    sign_text = f"Charge: {'+' if current_charge_sign > 0 else '-'}{current_charge_value}"
    text_surface = font.render(sign_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()