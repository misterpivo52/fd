import time
import threading
import keyboard  # Для отслеживания клавиш
from chrome import main_loop
from databaza import DATABASE
from Questionnc import extract_first_sentence
from compilator import process_file
from virt import extract_and_write_questions
from maikamf import mainx

# Флаги для контроля выполнения
is_running_sequence = False
is_running_mainx = False

def execute_sequence():
    """Выполняет цепочку операций с заданными задержками."""
    global is_running_sequence
    try:
        y = "visible_text.txt"
        fds = "extracted_questions.txt"
        dfgdgf = "output.txt"
        zro = "ou1tput.txt"

        print("Запуск extract_and_write_questions через 2 секунд...")
        time.sleep(2)
        extract_and_write_questions(y, fds)
        print("extract_and_write_questions выполнена.")

        print("Запуск extract_first_sentence через 2 секунды...")
        time.sleep(2)
        extract_first_sentence(fds, dfgdgf)
        print("extract_first_sentence выполнена.")

        print("Запуск process_file через 2 секунды...")
        time.sleep(2)
        process_file(dfgdgf, zro, DATABASE)
        print("process_file выполнена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Сбрасываем флаг после завершения
        is_running_sequence = False

def execute_mainx():
    """Выполняет mainx отдельно."""
    global is_running_mainx
    try:
        zro = "ou1tput.txt"
        print("Запуск mainx...")
        mainx(zro)
        print("mainx выполнена.")
    except Exception as e:
        print(f"Произошла ошибка в mainx: {e}")
    finally:
        # Сбрасываем флаг после завершения
        is_running_mainx = False

def listen_for_hotkey():
    """Отслеживает нажатие горячих клавиш для включения/выключения функций."""
    global is_running_sequence, is_running_mainx
    print("Ожидаю нажатия клавиш 'num3' для execute_sequence или 'num4' для mainx...")
    while True:
        if keyboard.is_pressed("num 3"):  # Нажата клавиша `]`
            time.sleep(15)
            if not is_running_sequence:
                print("Запуск execute_sequence...")
                is_running_sequence = True
                threading.Thread(target=execute_sequence, daemon=True).start()
            else:
                print("execute_sequence уже выполняется. Ожидание завершения...")
            time.sleep(1)  # Избегаем множественного срабатывания

        if keyboard.is_pressed("num 4"):  # Нажата клавиша `[`
            if not is_running_mainx:
                print("Запуск mainx...")
                is_running_mainx = True
                threading.Thread(target=execute_mainx, daemon=True).start()
            else:
                print("mainx уже выполняется. Ожидание завершения...")
            time.sleep(1)  # Избегаем множественного срабатывания

def main():
    # Запуск потока для отслеживания горячих клавиш
    hotkey_thread = threading.Thread(target=listen_for_hotkey, daemon=True)
    hotkey_thread.start()
    main_loop()
   # Запускает основную логику программы
    # Основной цикл программы
    while True:
        time.sleep(1)  # Поддерживает основной поток активным

if __name__ == "__main__":
    main()
