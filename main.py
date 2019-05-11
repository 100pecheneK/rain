""" Создатель - Притыкин Михаил Вячеславович.
    Создана в начале 2019 года.
    Вдохновил Егорушкин Илья.
"""
# ----------------------------Цели----------------------------
# Добавить меню с:
# 	- Старт
# 	- Настройки
# 		- Звук 
# 		- Разрешение экрана
# 		- В окне или во весь экран
# 	- Создатель
# 		- Информация о создателе
# 	- Выход
# -------------------------Цели конец-------------------------

import pygame
import random

pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
# --------------------Инициализация Py Game--------------------
pygame.init()

# Размер окна (стандартно 800x600)
display_width = 800
display_height = 600
display = pygame.display.set_mode((display_width, display_height))

sky = [pygame.image.load('images/sky_0.png')]
dirt = [pygame.image.load('images/dirt_0.png')]
# Название игры и иконка(отсутствует)
pygame.display.set_caption("RAIN")
# icon = pygame.image.load("icon.png")
# pygame.display.set_icon(icon)

# FPS.tick(fps) в конце главной функции
FPS = pygame.time.Clock()
fps = 80
score = 0
# Звуки
# Музыка на задний фон
pygame.mixer.music.load('sound/background.mp3')
pygame.mixer.music.set_volume(0.2)
# Звук прыжка???


# Звуки кнопок: Наведение???, нажатие
# button_sound_hover = pygame.mixer.Sound('sound/hover.wav')
button_sound_pressed = pygame.mixer.Sound('sound/pressed.wav')


# ------------------------Класс кнопок------------------------
class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (0, 0, 0)
        self.active_color = (255, 255, 255)

    # Функция отрисовки кнопки
    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # Курсор на кнопке
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound_pressed)
                pygame.time.delay(1)
                if action is not None:
                    action()
        # Курсор не на кнопке
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))

        print_text(message, x + 10, y + 10)


# ---------------------Конец класса кнопок---------------------

# ----------------------------Игрок----------------------------
player_width = 30
player_height = 50
# Определение координат игрока перенесены в Главную функцию
# player_x = display_width // 2 - player_width / 2
# player_y = display_height - player_height - 100
player_speed = 5
# Картинки идут от самой левой к самой правой
player_image = [pygame.image.load('player_l1.png'), pygame.image.load('player_l2.png'),
                pygame.image.load('player0.png'), pygame.image.load('player_r1.png'),
                pygame.image.load('player_r2.png')
                ]
# Это счётчик текущей картинки
img_counter = 0
# Переменные действия игрока
make_jump = False
# Это максимальная высота прыжка(не менять)(а если менять, то и в функции jump()
jump_counter = 25
# Вправо и влево не идёт, пока не нажата клавиша D/A соответственно
go_right = False
go_left = False
# -------------------------Конец игрока-------------------------

# ----------------------------Враг----------------------------
enemy_speed = 8
# Количество врагов зависит от разрешения чем больше тем больше (можно поставить фиксированное)
enemy_count = display_width * 10 // 800
# Хранит в себе массив врагов
# Перенесён в главную функцию
# enemy_arr = []
# Здесь хранится картинка врага
enemy_img = pygame.image.load('images/enemy.png')


# Класс Врага
class Enemy:
    def __init__(self, x, y, width, height, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.speed = speed

    def move(self):
        # global enemy_arr
        # Если положение по Y меньше или равно земле, то отрисовать врага и опускать его до земли
        if self.y <= display_height - 100:
            display.blit(self.image, (self.x, self.y - self.height))
            self.y += self.speed
        else:
            # Враг удаляется из массива врага и создаётся новый
            enemy_arr.remove(self)
            create_enemy_arr(enemy_arr)


# -------------------------Конец врага-------------------------
# Запуск музыки
pygame.mixer.music.play(-1)


# -----------------------Главная функция-----------------------
def run_game():
    global fps, make_jump, jump_counter, go_right, go_left, enemy_arr, score, player_x, player_y, jump_counter

    # Важная переменная game
    game = True
    score = 0
    # Вызов функции отрисовки всех врагов из массиве
    enemy_arr = []
    create_enemy_arr(enemy_arr)
    # Координаты определены тут, потому что после проигрыша координаты должны обновиться
    player_x = display_width // 2 - player_width / 2
    player_y = display_height - player_height - 100
    # Что бы при смерте в прыжке не прыгал в начале новой игры и не падал под текстуры
    jump_counter = 25
    make_jump = False

    button = Button(100, 50)

    while game:
        # Проверяет события
        for event in pygame.event.get():
            # Если нажата кнопка выхода, то завершить игру
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Нажатая кнопка
        keys = pygame.key.get_pressed()
        # Esc - пауза
        if keys[pygame.K_ESCAPE]:
            pause()
        # Space - Прыжок
        if keys[pygame.K_SPACE]:
            make_jump = True
        # D - Вправо
        if keys[pygame.K_d]:
            go_right = True
        # A - Влево
        if keys[pygame.K_a]:
            go_left = True

        if make_jump:
            jump()
        if go_right:
            right()
        if go_left:
            left()

        # Отрисовка неба
        display.blit(sky[0], (0, 0))
        # Отрисовка земли
        display.blit(dirt[0], (0, display_height - 100))
        # Отрисовка врага
        draw_enemy_arr(enemy_arr)
        # Отрисовка игрока
        draw_player()
        # Обработка столкновения - если True, то игра закончится и будет выбор между Return и Esc

        button.draw(display_width / 2, display_height / 2, 'test')

        if collision(enemy_arr):
            game = False
        # Считаёт очки игрока до тех пор, пока игрок не проиграет
        score += 0.5
        if game:
            print_text(str(score), 50, 50)
        # Обновление экрана
        pygame.display.update()
        # Количество тиков == 80
        FPS.tick(fps)
    # Если game == False, то вызовет функцию которая отвечает за проигрыш
    return game_over()


# --------------------КОНЕЦ ГЛАВНОЙ ФУНКЦИИ--------------------

def jump():
    global player_y, make_jump, jump_counter
    # Если счётчик больше -25, то игрок будет взлетать, а счётчик уменьшаться
    if jump_counter >= -25:
        player_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 25
        make_jump = False


def right():
    global player_x, go_right, player_speed
    # Если игрок не у правой стены, то идёт вправо со скоростью player_speed
    if player_x < display_width - player_width:
        player_x += player_speed
        go_right = False
    else:
        go_right = False


def left():
    global player_x, go_left, player_speed
    # Если игрок не у левой стены, то идёт вправо со скоростью player_speed
    if player_x > 0:
        player_x -= player_speed
        go_left = False
    else:
        go_left = False


def create_enemy_arr(array):
    global enemy_speed, enemy_count, enemy_img
    # Создавать новых врагов, пока их количество не будет == enemy_count(Можно изменить в блоке с врагом)
    while len(array) <= enemy_count:
        # Нас случайной координате X и Y создаётся враг
        array.append(
            Enemy(random.randrange(-10, display_width), random.randrange(-200, 0), 10, 20, enemy_img, enemy_speed))


def draw_enemy_arr(array):
    # Вызывает для каждого врага из массива функцию move() класса Enemy
    for enemy in array:
        enemy.move()


def collision(array):
    """ Проверяются все враги.
        Если координата врага по Y между координатами игрока по Y, то проверится условие:
        Если левая или правая координата врага X входит в координаты игрока X, то
        Вернётся True и в функции run_game() game = False и будет вызвана game_over()
        Иначе False и игра продолжается
    """
    for enemy in array:
        if player_y <= enemy.y <= player_y + player_height:
            if player_x <= enemy.x <= player_x + player_width or player_x <= enemy.x + enemy.width <= player_x + player_width:
                return True
    return False


def draw_player():
    global img_counter
    # Анимация замедлена - каждые 10 значений счётчика будет изменяться скорость анимации. Наверное зависит от fps
    if img_counter == 50:
        img_counter = 0
    display.blit(player_image[img_counter // 10], (player_x, player_y))
    img_counter += 1


def print_text(message, x, y, font_color=(255, 255, 255), font_type='fonts/font.ttf', font_size=30):
    # Обязательно Получает сообщение и координаты и выводит текст
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True

    # Пауза музыки
    pygame.mixer.music.pause()
    # Если нажата кнопка выхода, то завершить игру
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text("Press Return for continue, or Tab to exit", 100, 100)
        # Нажатая кнопка
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        if keys[pygame.K_TAB]:
            pygame.quit()
            quit()

        pygame.display.update()
        FPS.tick(15)
    # Продолжение музыки
    pygame.mixer.music.unpause()


def game_over():
    global score
    while True:
        for event in pygame.event.get():
            # Если нажата кнопка выхода, то завершить игру
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text("Score = " + str(score), 50, 50)
        print_text("Press Return to play again, or Esc to exit", 100, 100)
        # Нажатая кнопка
        keys = pygame.key.get_pressed()
        # В конце концов возвращает значение в цикл while в блоке START GAME
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        FPS.tick(15)


# -------------------------START GAME-------------------------
# Если game_over() вернёт True то игра не закрывается.
# В случае проигрыша предлагается выбор Return - продолжить или Esc - выйти
while run_game():
    pass
pygame.quit()
quit()
