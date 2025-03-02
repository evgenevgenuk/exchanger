import customtkinter as ctk
from tkinter import messagebox

def update_slider(value):
    entry_denomination.delete(0, 'end')
    entry_denomination.insert(0, int(float(value)))

def update_slider_from_entry(*args):
    try:
        value = int(entry_denomination.get())
        if 0 <= value <= 1000:
            slider.set(value)
    except ValueError:
        pass

def add_denomination():
    try:
        value = int(entry_denomination.get())
        if value > 0:
            if value in denominations:
                messagebox.showwarning("Увага", f"Номінал {value} вже доданий.")
            else:
                denominations.append(value)
                update_denominations_list()
        else:
            messagebox.showerror("Помилка", "Номінал має бути більше 0")
    except ValueError:
        messagebox.showerror("Помилка", "Введіть коректний номінал")

def update_denominations_list():
    for widget in denominations_frame.winfo_children():
        widget.destroy()

    for i, denom in enumerate(denominations):
        label = ctk.CTkLabel(denominations_frame, text=f"Монета: {denom}")
        label.grid(row=i, column=0, padx=5, pady=5)

def clear_denominations():
    denominations.clear()
    update_denominations_list()

def calculate_change():
    def calculate():
        try:
            amount = int(entry_amount.get())
            if amount <= 0:
                messagebox.showerror("Помилка", "Сума має бути більше 0")
                return

            # Функція для знаходження комбінацій зі збільшенням кількості монет
            def find_combinations(coins, target):
                from itertools import combinations_with_replacement

                # Сортуємо монети за спаданням
                coins_sorted = sorted(coins, reverse=True)

                # Починаємо з мінімальної кількості монет
                for num_coins in range(1, target + 1):
                    # Генеруємо всі можливі комбінації з num_coins монет
                    for combo in combinations_with_replacement(coins_sorted, num_coins):
                        if sum(combo) == target:
                            # Знайдено комбінацію
                            return combo
                return None  # Якщо комбінація не знайдена

            # Знаходимо комбінацію
            combination = find_combinations(denominations, amount)

            if combination:
                # Підраховуємо кількість монет кожного номіналу
                from collections import defaultdict
                count = defaultdict(int)
                for coin in combination:
                    count[coin] += 1
                # Формуємо результат
                result_text = "\n".join([f"{v} монет по {k}" for k, v in count.items()])
            else:
                result_text = "Неможливо розміняти суму з даними номіналами."

            # Вікно з результатом
            result_window = ctk.CTkToplevel(calculate_window)
            result_window.title("Результат розміну")
            result_window.geometry("400x300")

            textbox = ctk.CTkTextbox(result_window, wrap="word")
            textbox.insert("1.0", result_text)
            textbox.configure(state="disabled")
            textbox.pack(fill="both", expand=True, padx=10, pady=10)

        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректну суму")

    calculate_window = ctk.CTkToplevel(app)
    calculate_window.title("Розмін")
    calculate_window.geometry("300x150")

    label_amount = ctk.CTkLabel(calculate_window, text="Введіть суму для розміну")
    label_amount.pack(pady=10)

    entry_amount = ctk.CTkEntry(calculate_window)
    entry_amount.pack(pady=10)

    button_calculate = ctk.CTkButton(calculate_window, text="Порахувати", command=calculate)
    button_calculate.pack(pady=10)

def change_language(lang):
    if lang == "Українська":
        label_denomination.configure(text="Номінал монети")
        button_add.configure(text="Додати монету")
        button_calculate.configure(text="Порахувати")
        button_clear.configure(text="Очистити список")
    elif lang == "English":
        label_denomination.configure(text="Denomination")
        button_add.configure(text="Add coin")
        button_calculate.configure(text="Calculate")
        button_clear.configure(text="Clear list")

def change_theme(theme):
    ctk.set_appearance_mode(theme)

app = ctk.CTk()
app.title("Гроші")
app.geometry("500x400")

denominations = []

language_var = ctk.StringVar(value="Українська")
language_menu = ctk.CTkOptionMenu(app, values=["Українська", "English"], command=change_language)
language_menu.pack(pady=10)

theme_var = ctk.StringVar(value="Light")
theme_menu = ctk.CTkOptionMenu(app, values=["Light", "Dark", "System"], command=change_theme)
theme_menu.pack(pady=10)

label_denomination = ctk.CTkLabel(app, text="Номінал монети")
label_denomination.pack(pady=5)

entry_denomination = ctk.CTkEntry(app, placeholder_text="Введіть номінал")
entry_denomination.pack(pady=5)
entry_denomination.bind("<KeyRelease>", update_slider_from_entry)

slider = ctk.CTkSlider(app, from_=0, to=1000, command=update_slider)
slider.pack(pady=5)

button_add = ctk.CTkButton(app, text="Додати монету", command=add_denomination)
button_add.pack(pady=10)

button_clear = ctk.CTkButton(app, text="Очистити список", command=clear_denominations)
button_clear.pack(pady=10)

button_calculate = ctk.CTkButton(app, text="Порахувати", command=calculate_change)
button_calculate.pack(pady=10)

denominations_frame = ctk.CTkFrame(app)
denominations_frame.pack(pady=10, fill="both", expand=True)

app.mainloop()