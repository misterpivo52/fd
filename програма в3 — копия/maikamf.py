import os  # Для запуска файла
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw, ImageFont
from pynput.keyboard import Listener as KeyboardListener
import threading
import re

# Глобальные переменные
current_question_index = 0
current_answer_index = 0
questions = []
show_custom_icon = False  # Флаг для пользовательской иконки
custom_image_path = "ikonka.png"  # Указание пути к изображению

def load_questions(filename):
    """
    Загружает вопросы и ответы из файла.
    Формат: номер: вопрос: [ответ1, ответ2, ...]
    """
    global questions
    questions = []
    try:
        with open(filename, "r", encoding="windows-1251") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) >= 3:
                    number, question, answer = parts[0].strip(), parts[1].strip(), parts[2].strip()
                    if answer.startswith("[") and answer.endswith("]"):
                        answers = eval(answer)
                        answers = [filter_letters(ans) for ans in answers]
                    else:
                        answers = [filter_letters(answer)]
                    questions.append({"number": number, "question": question, "answers": answers})
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")


def filter_letters(text):
    """
    Убирает из текста все, кроме букв и цифр.
    """
    return re.sub(r"[^a-zA-Zа-яА-ЯёЁ0-9]", "", text)


def create_text_image(question_index, answer_index, width=64, height=64):
    """
    Создает изображение для значка с текущим вопросом и ответом или пользовательскую иконку.
    """
    global show_custom_icon

    if show_custom_icon:  # Если нужно отобразить пользовательскую иконку
        try:
            custom_image = Image.open(custom_image_path).convert("RGBA")
            return custom_image.resize((width, height))
        except Exception as e:
            print(f"Ошибка загрузки пользовательской иконки: {e}")
            return Image.new("RGBA", (width, height), (255, 0, 0, 255))  # Красная заглушка на случай ошибки

    if not questions:
        return Image.new("RGBA", (width, height), (0, 0, 0, 0))

    question_data = questions[question_index]
    question_number = question_data["number"]
    answers = question_data["answers"]
    current_answer = answers[answer_index]

    first_letter = current_answer[0].lower() if len(current_answer) > 0 else " "
    last_letter = current_answer[-1].lower() if len(current_answer) > 0 else " "


    image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    font_size = 30
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    first_line = f"{question_number}{first_letter}{last_letter}"
    bbox1 = draw.textbbox((0, 0), first_line, font=font)
    text_x1 = (width - (bbox1[2] - bbox1[0])) // 2
    text_y1 = (height // 2) - (bbox1[3] - bbox1[1]) // 2
    draw.text((text_x1, text_y1), first_line, fill="black", font=font)

    return image


def update_icon(icon):
    """Обновляет значок с текущими данными."""
    global current_question_index, current_answer_index
    icon.icon = create_text_image(current_question_index, current_answer_index)


def toggle_icon(icon):
    """Переключает отображение пользовательской иконки или текста."""
    global show_custom_icon
    show_custom_icon = not show_custom_icon
    update_icon(icon)


def next_answer_or_question(icon):
    """
    Переключает на следующий ответ или вопрос.
    Если ответы закончились, переключается на следующий вопрос.
    """
    global current_question_index, current_answer_index

    if not questions:
        return

    question_data = questions[current_question_index]
    total_answers = len(question_data["answers"])

    if current_answer_index + 1 < total_answers:
        current_answer_index += 1
    else:
        current_answer_index = 0
        current_question_index = (current_question_index + 1) % len(questions)

    update_icon(icon)


def on_key_press(key):
    """Обрабатывает нажатие клавиш."""
    global icon
    try:
        if hasattr(key, 'vk') and key.vk == 96:  # Проверка на Numpad 0
            toggle_icon(icon)
        elif hasattr(key, 'char') and key.char == '0':  # Проверка на обычный 0
            toggle_icon(icon)
        elif hasattr(key, 'vk') and key.vk == 97:  # Проверка на Numpad 1
            next_answer_or_question(icon)
        elif hasattr(key, 'char') and key.char == '1':  # Проверка на обычный 1
            next_answer_or_question(icon)
    except Exception as e:
        print(f"Ошибка: {e}")


def start_keyboard_listener():
    """Запускает отслеживание нажатий клавиш."""
    with KeyboardListener(on_press=on_key_press) as listener:
        listener.join()


def quit_program(icon, item):
    """Закрывает программу."""
    icon.stop()

def run_nvidia_app(icon, item):
    """Запускает NVIDIA приложение."""
    try:
        file_path = r"C:\Program Files\NVIDIA Corporation\NVIDIA app\CEF\NVIDIA app.exe"
        os.startfile(file_path)  # Запускает указанный файл
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Ошибка при запуске файла: {e}")

def mainx(filename):
    global icon

    load_questions(filename)
    menu = Menu(
        MenuItem("Nvidia app", run_nvidia_app),  # Кнопка запуска NVIDIA
        # MenuItem("", quit_program)               # Кнопка выхода
    )

    icon = Icon(
        "Текстовый значок",
        create_text_image(current_question_index, current_answer_index),
        f"Nvidia utility0",
        menu
    )

    keyboard_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    keyboard_thread.start()

    icon.run()


if __name__ == "__main__":
    mainx("ou1tput.txt")