import pygame
import sys
import random

# Функция для добавления текста в консоль
def add_console_line(console_lines, text):
    console_lines.append(text)
    if len(console_lines) > 20:  # Ограничение на количество строк
        console_lines.pop(0)

# Приложение: Пинг-Понг
def pong_game(screen, FONT, add_console_line, console_lines):
    try:
        # Размеры элементов
        paddle_width, paddle_height = 10, 100
        ball_size = 10

        # Позиции элементов
        WIDTH, HEIGHT = 800, 600
        left_paddle = pygame.Rect(30, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
        right_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
        ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_size, ball_size)

        # Скорости
        ball_speed = [5, 5]
        right_paddle_speed = 0
        left_paddle_speed = 5  # Автоматическое движение бота
        bot_direction = 1  # Направление движения бота

        # Счёт
        player_score = 0
        bot_score = 0

        # Флаг игры
        game_running = False

        add_console_line(console_lines, "Pong: Press ENTER to start, BACKSPACE to quit.")
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        add_console_line(console_lines, "Exiting Pong...")
                        return  # Выход из игры по Backspace
                    if event.key == pygame.K_RETURN:
                        game_running = True
                    if event.key == pygame.K_UP:
                        right_paddle_speed = -7
                    if event.key == pygame.K_DOWN:
                        right_paddle_speed = 7

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        right_paddle_speed = 0

            if game_running:
                # Движение мяча
                ball.x += ball_speed[0]
                ball.y += ball_speed[1]

                # Отскок от верхней и нижней границ
                if ball.top <= 0 or ball.bottom >= HEIGHT:
                    ball_speed[1] = -ball_speed[1]

                # Отскок от платформ
                if ball.colliderect(right_paddle) or ball.colliderect(left_paddle):
                    ball_speed[0] = -ball_speed[0]

                # Проверка голов
                if ball.left <= 0:
                    player_score += 1
                    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_size, ball_size)
                    ball_speed = [5 * random.choice([-1, 1]), 5 * random.choice([-1, 1])]
                    game_running = False
                if ball.right >= WIDTH:
                    bot_score += 1
                    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_size, ball_size)
                    ball_speed = [5 * random.choice([-1, 1]), 5 * random.choice([-1, 1])]
                    game_running = False

                # Движение правой платформы
                right_paddle.y += right_paddle_speed
                if right_paddle.top < 0:
                    right_paddle.top = 0
                if right_paddle.bottom > HEIGHT:
                    right_paddle.bottom = HEIGHT

                # Движение бота (вверх-вниз)
                left_paddle.y += left_paddle_speed * bot_direction
                if left_paddle.top <= 0 or left_paddle.bottom >= HEIGHT:
                    bot_direction *= -1

            # Рисуем игровой экран
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (255, 255, 255), left_paddle)
            pygame.draw.rect(screen, (255, 255, 255), right_paddle)
            pygame.draw.ellipse(screen, (255, 255, 255), ball)
            pygame.draw.aaline(screen, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

            # Рисуем счёт
            score_text = FONT.render(f"Player: {player_score}   Bot: {bot_score}", True, (255, 255, 255))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

            pygame.display.flip()
            pygame.time.Clock().tick(60)
    except Exception as e:
        add_console_line(console_lines, f"Error in pong game: {str(e)}")

# Приложение: Калькулятор
def calculator_app(screen, FONT, add_console_line, console_lines):
    try:
        add_console_line(console_lines, "Calculator started. Type 'exit' to quit.")
        current_input = ""
        result = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if current_input.lower() == "exit":
                            add_console_line(console_lines, "Exiting calculator...")
                            return
                        try:
                            result = eval(current_input)
                            add_console_line(console_lines, f"Result: {result}")
                        except Exception as e:
                            add_console_line(console_lines, f"Error: {e}")
                        current_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1]
                    else:
                        current_input += event.unicode

            # Обновление экрана
            screen.fill((0, 0, 0))

            # Показ текущего ввода
            input_text = FONT.render(f"> {current_input}", True, (0, 255, 0))
            screen.blit(input_text, (10, 550))

            # Показ результата
            if result is not None:
                result_text = FONT.render(f"Result: {result}", True, (0, 255, 0))
                screen.blit(result_text, (10, 500))

            pygame.display.flip()
    except Exception as e:
        add_console_line(console_lines, f"Error in calculator: {str(e)}")

# Очистка консоли
def clear_console(console_lines):
    console_lines.clear()
