import re
import os

def extract_first_sentence(input_file, output_file):
    try:
        # Проверяем, существует ли входной файл
        if not os.path.exists(input_file):
            print(f"Ошибка: входной файл {input_file} не существует.")
            return

        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        if not lines:
            print(f"Ошибка: файл {input_file} пуст.")
            return

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for line in lines:
                # Ищем номер строки и первое предложение
                match = re.match(r"(\d+):\s*(.+?)[.!?]", line)
                if match:
                    number, first_sentence = match.groups()

                    # Проверяем наличие фразы "Refer to the exhibit"
                    if "Refer to the exhibit" in line:
                        # Ищем второе предложение
                        sentences = re.split(r"[.!?]", line)
                        second_sentence = sentences[1].strip() if len(sentences) > 2 else ""
                        outfile.write(f"{number}: {first_sentence.strip()} {second_sentence}\n")
                    else:
                        outfile.write(f"{number}: {first_sentence.strip()}\n")
                else:
                    print(f"Предложение не найдено в строке: {line.strip()}")

        print(f"Обработка завершена. Результат сохранен в файле {output_file}.")
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    input_file = "extracted_questions.txt"
    output_file = "output.txt"
    extract_first_sentence(input_file, output_file)
