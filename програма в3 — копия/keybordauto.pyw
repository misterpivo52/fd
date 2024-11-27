import pyautogui
import keyboard
import time


def perform_actions():
    """
    Выполняет последовательность действий:
    - Ctrl + L
    - Ctrl + C
    - Ctrl + Alt + A
    - Левый клик мыши
    """
    try:
        print("Выполняю действия...")

        # Нажатие Ctrl + L
        pyautogui.hotkey('ctrl', 'l')
        # Нажатие Ctrl + C
        pyautogui.hotkey('ctrl', 'c')
        # time.sleep(1)
        # pyautogui.hotkey('f4')

        # Левый клик мыши
        pyautogui.click()

        print("Все действия выполнены!")
    except Exception as e:
        print(f"Ошибка: {e}")


def mai():
    print("Программа запущена. Нажмите F4 для выполнения действий или ESC для выхода.")

    # Бесконечный цикл для ожидания нажатий клавиш
    while True:
        try:
            # Если нажата F4, выполняем действия
            if keyboard.is_pressed('num 3'):
                perform_actions()
                # Ждем, чтобы избежать повторных срабатываний
                time.sleep(1)

            # Если нажата ESC, завершаем программу
        except Exception as e:
            print(f"Ошибка: {e}")
            break


if __name__ == "__main__":
    mai()
