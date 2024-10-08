from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk
import requests
import pyperclip
import json
import os

history_file = "upload_history.json"


# сохраняем список загруженных файлов в формате JSON
def save_history(file_path, link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    history.append({"file_path": os.path.basename(file_path), 'download_link': link})
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)


def upload():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()
                link = response.json()['link']  # получаем ссылку
                entry.delete(0, END)  # удаляем поле с предыдущей ссылкой перед выводом новой
                entry.insert(0, link)  # показываем ссылку в entry
                pyperclip.copy(link)  # скопировали ссылку в буфер обмена
                save_history(filepath, link)
                mb.showinfo("Ссылка скопирована", f"Ссылка {link} успешно скопирована в буфер обмена")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")


# показываем историю загрузок
def show_history():
    if not os.path.exists(history_file):
        mb.showinfo("История", "История загрузок пуста")
        return

    history_window = Toplevel(window)
    history_window.title("История загрузок")

    # Создаем две колонки с отображением истории загрузок
    files_listbox = Listbox(history_window, width=50, height=20)
    files_listbox.grid(row=0, column=0, padx=(10, 0), pady=10)

    links_listbox = Listbox(history_window, width=50, height=20)
    links_listbox.grid(row=0, column=1, padx=(0, 10), pady=10)

    with open(history_file, 'r') as f:
        history = json.load(f)  # в history положим то, что загрузим из json
        for item in history:  # перебираем список словарей
            files_listbox.insert(END, item['file_path'])  # вставляем в конец элементы из item по ключу
            links_listbox.insert(END, item['download_link'])



window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry("400x200")

button = ttk.Button(text="Загрузить файл", command=upload)
button.pack()

entry = ttk.Entry()
entry.pack()

history_button = ttk.Button(text="Показать историю", command=show_history)
history_button.pack()

window.mainloop()
