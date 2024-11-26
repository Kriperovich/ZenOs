import pygame
import sys
import time
from commands import pong_game, calculator_app, add_console_line, clear_console

# Инициализация Pygame
pygame.init()

# Размер окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ZenOS")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Шрифт
FONT = pygame.font.Font(None, 36)

# Главный цикл
running = True
console_lines = ["ZenOS v2.3 - Type 'help' to get started"]  # Обновлена версия на 2.3
current_command = ""
cursor_visible = True
last_cursor_blink = time.time()

# Проверка на запрещённые слова
def check_for_prohibited_words(command):
    prohibited_words = ["nigger"]  # Запрещённое слово на английском
    if any(word in command.lower() for word in prohibited_words):
        return True
    return False

while running:
    screen.fill(BLACK)

    # Отображаем название "ZenOS"
    title_text = FONT.render("ZenOS", True, GREEN)
    screen.blit(title_text, (10, 10))

    # Обновляем курсор каждые 0.5 секунды
    if time.time() - last_cursor_blink > 0.5:
        cursor_visible = not cursor_visible
        last_cursor_blink = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if current_command.lower() == "exit":
                add_console_line(console_lines, "Shutting down ZenOS...")
                running = False
            elif event.key == pygame.K_RETURN:
                # Проверка на запрещённое слово
                if check_for_prohibited_words(current_command):
                    add_console_line(console_lines, "Forbidden word detected! Shutting down...")
                    running = False
                    break

                if current_command.lower() == "help":
                    add_console_line(console_lines, "Available commands:")
                    add_console_line(console_lines, "  help - Show this help message")
                    add_console_line(console_lines, "  calc - Open calculator")
                    add_console_line(console_lines, "  game - Play Pong")
                    add_console_line(console_lines, "  clear - Clear the console")
                    add_console_line(console_lines, "  exit - Exit ZenOS")
                elif current_command.lower() == "calc":
                    add_console_line(console_lines, "Opening calculator...")
                    calculator_app(screen, FONT, add_console_line, console_lines)
                elif current_command.lower() == "game":
                    add_console_line(console_lines, "Starting Pong game...")
                    pong_game(screen, FONT, add_console_line, console_lines)
                elif current_command.lower() == "clear":
                    clear_console(console_lines)
                else:
                    add_console_line(console_lines, f"Unknown command: {current_command}")

                current_command = ""  # Очистить команду после выполнения

            elif event.key == pygame.K_BACKSPACE:
                current_command = current_command[:-1]
            else:
                current_command += event.unicode

    # Отображаем строки консоли
    y = 50
    for line in console_lines:
        console_text = FONT.render(line, True, GREEN)
        screen.blit(console_text, (10, y))
        y += 30

    # Отображаем строку ввода
    command_text = FONT.render(current_command, True, GREEN)
    screen.blit(command_text, (10, HEIGHT - 50))

    # Отображаем курсор
    if cursor_visible:
        cursor_x = 10 + FONT.size(current_command)[0]
        pygame.draw.rect(screen, GREEN, (cursor_x, HEIGHT - 50 + 10, 10, 20))

    pygame.display.flip()

pygame.quit()
