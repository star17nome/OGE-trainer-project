import json
import random
import tkinter as tk
from textwrap import fill
from tkinter import ttk, messagebox
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# Функции
def show_task():
    global current_task
    selected_number = int(task_number.get().split()[1])
    proper_tasks = [task for task in tasks if task['number'] == selected_number]

    if len(proper_tasks) == 0:
        task_label.config(
            text=(
                f"Для задания №{selected_number}"
                f"в базе пока нет вопросов."
            )
        )
        answer_entry.delete(0, tk.END)
        result_var.set("")
        return

    current_task = random.choice(proper_tasks)

    task_label.config(
        text=(
            f"Задание №{current_task['number']}\n"
            f"Тема: {current_task['topic']}\n\n"
            f"{current_task['text']}"
        )
    )
    answer_entry.delete(0, tk.END)
    result_var.set('Введите ответ и нажмите "проверить"')

def check_answer():
    user_answer = answer_entry.get().strip().lower()
    correct_answer = current_task["answer"].strip().lower()

    if user_answer == "":
        messagebox.showwarning("Нет ответа", "Сначала введитие ответ")
        return
    if user_answer == correct_answer:
        result_var.set("Верно, отличная работа")
    else:
        result_var.set(
            f"Неверно. Правильный ответ: {correct_answer}"
            
            f"{current_task['explanation']}"
        )
        return

# Задания
try:
    with open("tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
except FileNotFoundError:
    messagebox.showwarning(
        "Ошибка",
        "Файл tasks.json не найден. /n"
        "Проверьте, что он находится в одной директории с main.py"
    )
    tasks = []
except json.JSONDecodeError:
    messagebox.showwarning(
        "Ошибка",
        "В файле tasks.json есть ошибка"
    )
    tasks = []

current_task = None

# Главное окно
window = tk.Tk()
window.title('Тренажёр ОГЭ по информатике')
window.geometry('1000x900')

# "Выберите номер задания"
main_label = ttk.Label(
    window,
    text = 'Выберите номер задания',
    font = ('Arial', 20)
)
main_label.pack(pady=10)

# Номера заданий
task_number = ttk.Combobox(
    window,
    values = [
        "Задание 1 (Оценка информационного объёма текстовых данных)",
        "Задание 2 (Кодирование и декодирование информации)",
        "Задание 3 (Значение логического выражения)",
        "Задание 4 (Взвешенные графы)",
        "Задание 5 (Алгоритмы для исполнителей с набором команд)",
        "Задание 6 (Анализ программ, записанных на языках программирования)",
        "Задание 7 (Принципы адресации в сети Интернет)",
        "Задание 8 (Принципы поиска информации в Интернете поисковыми запросами)",
        "Задание 9 (Взвешенные ориентированные графы)",
        "Задание 10 (Сравнение и запись чисел в различных системах счисления)",
    ],
    state = 'readonly',
    width = 65
)
task_number.current(0)
task_number.pack(pady=30)
sel_num = int(task_number.get().split()[1])

# Кнопка показать задание
show_button = ttk.Button(
    window,
    text = "Показать задание",
    command = show_task
)
show_button.pack(pady=0)

# Окно задания
task_label = ttk.Label(
    window,
    text = "",
    font = ("Arial", 14),
    wraplength = 650,
    justify = "left"
)
task_label.pack(pady=60)

# Окно ответа
answer_lable = ttk.Label(
    window,
    text = "Ваш ответ:",
    font = ("Arial", 18)
)
answer_lable.pack(pady=60, padx=55, anchor="nw")

# Поле ввода
answer_entry = ttk.Entry(window)
answer_entry.pack(pady=0, padx=55, anchor="nw")

# Кнопка проверки
check_button = ttk.Button(
    window,
    text="Проверить ответ",
    command=check_answer
)
check_button.pack(pady=30, padx=55, anchor="nw")

# Проверка
result_var = tk.StringVar(
    value = ""
)

result_lable = ttk.Label(
    window,
    textvariable = result_var,
    wraplength = 650,
    justify = 'left',
    font = ("Arial", 16)
)
result_lable.pack(pady=20, padx=55, anchor="nw")

window.mainloop()