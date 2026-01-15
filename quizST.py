from pibody import Button, Buzzer, display, LED
from time import sleep

button_A = Button('A')
button_B = Button('B')
button_C = Button('C')
buttons = [button_A, button_B, button_C]

buzzer = Buzzer('D')
ledGreen = LED('E')
ledRed = LED('F')

leds = [ledGreen, ledRed]

# ---------- ВОПРОСЫ ----------
# correct: 0=A, 1=B, 2=C
quiz = [
    {
        "q": "В каком городе происходит действие?",
        "a": ["Нью-Йорк", "Чикаго", "Хокинс"],
        "correct": 2
    },
    {
        "q": "Как зовут девочку со способностями?",
        "a": ["Макс", "Оди", "Нэнси"],
        "correct": 1
    },
    {
        "q": "Как называется странный мир?",
        "a": ["Изнанка", "Лабиринт", "Параллельный мир"],
        "correct": 0
    },
    {
        "q": "Что Одиннадцать любит есть?",
        "a": ["Пиццу", "Мороженое", "Вафли Eggo"],
        "correct": 2
    },
    {
        "q": "С помощью чего друзья чаще всего общаются?",
        "a": ["Рациями", "Телефонами", "Письмами"],
        "correct": 0
    },
    {
        "q": "Как зовут шерифа Хокинса?",
        "a": ["Стив", "Майк", "Хоппер"],
        "correct": 2
    },
    {
        "q": "Как называется монстр первого сезона?",
        "a": ["Дракон", "Демогоргон", "Паук"],
        "correct": 1
    },
    {
        "q": "Что используют для связи с Изнанкой?",
        "a": ["Радио", "Телевизор", "Гирлянды со светом"],
        "correct": 2
    },
    {
        "q": "Во что любят играть друзья?",
        "a": ["Шахматы", "Футбол", "D&D"],
        "correct": 2
    },
    {
        "q": "Какова главная тема сериала?",
        "a": ["Космос", "Дружба/команда", "Магия"],
        "correct": 1
    },
]

question_index = 0
total_questions = len(quiz)
total_correct = 0
total_incorrect = 0

def wrap_text_by_words(text, max_chars_per_line):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        # +1 учитывает пробел
        if len(current_line) + len(word) + (1 if current_line else 0) <= max_chars_per_line:
            if current_line:
                current_line += " "
            current_line += word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def show_question(question):
    text = question["q"]

    FONT_WIDTH = 12
    FONT_HEIGHT = 24
    DISPLAY_WIDTH = 240

    max_chars = DISPLAY_WIDTH // FONT_WIDTH
    lines = wrap_text_by_words(text, max_chars)

    x = 10
    y = 10

    for i, line in enumerate(lines):
        display.text(
            line,
            x,
            y + i * FONT_HEIGHT,
            font=display.font_large,
            fg=display.color(255, 128, 0)
        )

def show_answers(answers):
    text = answers["a"] 

    # Print of variants A, B, C
    display.text("A)", 10, 100, font=display.font_large, fg=display.color(255, 0, 0))
    display.text("B)", 10, 100 + 24, font=display.font_large, fg=display.color(255, 0, 0))
    display.text("C)", 10, 100 + 24 * 2, font=display.font_large, fg=display.color(255, 0, 0))

    # Print of answers
    for i in range(3):
        display.text(text[i], 40, 103 + 24 * i, font=display.font_medium, fg=display.color(255, 128, 0))

def show_chosen_answer(answers, index, color = None):
    if color is None:
        color = display.color(100, 0, 255)
    text = answers["a"][index]
    display.text(text, 40, 103 + 24 * index, font=display.font_medium, fg=color)

def correct_answer(index):
    ledGreen.on()
    show_chosen_answer(quiz[question_index], index, display.color(0, 255, 0))
    buzzer.make_sound(800, 0.5, 0.05)
    sleep(0.1)
    buzzer.make_sound(1000, 0.5, 0.05)

def incorrect_answer(index):
    ledRed.on()
    show_chosen_answer(quiz[question_index], index, display.color(255, 0, 0))
    buzzer.make_sound(400, 0.5, 0.05)
    sleep(0.1)
    buzzer.make_sound(300, 0.5, 0.05)

def check_answer(index):
    global total_correct, total_incorrect, question_index
    if index == quiz[question_index]["correct"]:
        total_correct += 1
        correct_answer(index)
    else:
        total_incorrect += 1
        incorrect_answer(index)
    question_index += 1

def show_score():
    text = str(f"Правильно: {total_correct} из {total_questions}")
    x = (240 - (len(text) * 8)) // 2
    display.text(text, x, 300, fg=display.color(255, 50, 0))

def play_congrats_sound():
    volume = 0.5

    buzzer.make_sound(freq=950, volume=volume, duration=0.1)
    sleep(0.05)
    buzzer.make_sound(freq=1200, volume=volume, duration=0.15)
    sleep(0.05)
    buzzer.make_sound(freq=1500, volume=volume, duration=0.3)
    sleep(0.05)


def show_final_score():
    display.fill(0)

    # Надпись "Поздравляем!"
    text = "Поздравляем!"
    x = (240 - (len(text) * 16)) // 2
    display.text(text, x, 100, font=display.font_bold, fg=display.color(255, 50, 0))

    # Кол-во правильных ответов
    display.text("Правильных ответов:", 10, 144, font=display.font_large, fg=display.color(255, 255, 255))
    text = str(f"{total_correct} из {total_questions}")
    x = (240 - (len(text) * 8)) // 2
    display.text(text, x, 144 + 24, fg=display.color(255, 255, 255))
    play_congrats_sound()

def check_buttons():
    for button in buttons:
        if button.value():
            return True
    return False

def start_display():
    display.fill(0)
    
    display.jpg("st_r.jpg", 0, 110)
    for i in range(3):
        display.hline(0, 109 + i, 240, display.color(200, 0, 0))

    Y = 24
    HEIGHT = 32

    display.hline(53, Y - 3, 134, display.color(200, 0, 0))
    display.hline(53, Y - 1, 134, display.color(200, 0, 0))

    display.hline(53, Y + HEIGHT * 2, 134, display.color(200, 0, 0))
    display.hline(53, Y + HEIGHT * 2 + 2, 134, display.color(200, 0, 0))

    # Надпись "STRANGE"
    text = "STRANGE"
    x = (240 - (len(text) * 16)) // 2
    display.text(text, x, Y, font=display.font_bold, fg=display.color(200, 0, 0))

    # Надпись "TECH LAB"
    text = "TECH LAB"
    x = (240 - (len(text) * 16)) // 2
    display.text(text, x, Y + HEIGHT, font=display.font_bold, fg=display.color(200, 0, 0))

    display.text("Press any button", 10, 300-16, fg=display.color(255, 255, 255))
    display.text("Нажмите любую кнопку", 10, 300, fg=display.color(255, 255, 255))

def start_game():
    while not check_buttons():
        sleep(0.1)

    display.fill(0)
    show_question(quiz[question_index])
    show_answers(quiz[question_index])
    show_score()

    while check_buttons():
        sleep(0.1)

    sleep(0.5)

def game_loop():
    while True:
        for button in buttons:
            if button.value():
                show_chosen_answer(quiz[question_index], buttons.index(button))
                sleep(0.5)
                check_answer(buttons.index(button))
                while button.value():
                    sleep(0.1)
                for led in leds:
                    led.off()
                if question_index >= total_questions:
                    sleep(1)
                    show_final_score()
                    break
                display.fill(0)
                show_question(quiz[question_index])
                show_answers(quiz[question_index])
                show_score()
                sleep(1)

def main():
    start_display()
    start_game()
    game_loop()

main()
