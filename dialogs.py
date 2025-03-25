from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:
    test: str = "Привет {name}. Работаю..."


msg = Messages()

import tkinter as tk
from tkinter import messagebox, simpledialog

# Создаем основное окно (можно скрыть, если нужно только диалог)
root = tk.Tk()
root.withdraw()  # Скрыть главное окно

# Окно с информационным сообщением
messagebox.showinfo("Приветствие", "Привет, мир!")

# Окно для ввода текста
name = simpledialog.askstring("Ввод", "Как вас зовут?")
print(f"Привет, {name}")
