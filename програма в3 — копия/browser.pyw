import os


def open_files():
    """
    Открывает два файла в системе Windows.
    """
    try:
        # Путь к первому файлу
        file1 = r"keybordauto.pyw"  # Укажите путь к первому файлу
        # Путь ко второму файлу
        file2 = r"main.pyw"  # Укажите путь ко второму файлу

        # Открытие файлов с помощью стандартных приложений
        os.startfile(file1)
        os.startfile(file2)

        print("Файлы успешно открыты!")
    except Exception as e:
        print(f"Ошибка при открытии файлов: {e}")


if __name__ == "__main__":
    print("Открываю файлы...")
    open_files()
