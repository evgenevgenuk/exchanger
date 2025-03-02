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
            denominations.append(value)
            update_denominations_list()
    except ValueError:
        pass


def update_denominations_list():
    for widget in denominations_frame.winfo_children():
        widget.destroy()

    for i, denom in enumerate(denominations):
        label = ctk.CTkLabel(denominations_frame, text=f"Купюра: {denom}")
        label.grid(row=i, column=0, padx=5, pady=5)


def calculate_change():
    def calculate():
        try:
            amount = int(entry_amount.get())
            if amount <= 0:
                messagebox.showerror("Помилка", "Сума має бути більше 0")
                return

            result = []
            remaining = amount
            for denom in sorted(denominations, reverse=True):
                if remaining >= denom:
                    count = remaining // denom
                    result.append(f"{count} купюр по {denom}")
                    remaining -= count * denom

            if remaining == 0:
                messagebox.showinfo("Результат", "\n".join(result))
            else:
                messagebox.showinfo("Результат", f"Неможливо розміняти повністю. Залишок: {remaining}")
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
        label_denomination.configure(text="Номінал купюри")
        button_add.configure(text="Додати купюру")
        button_calculate.configure(text="Порахувати")
    elif lang == "English":
        label_denomination.configure(text="Denomination")
        button_add.configure(text="Add bill")
        button_calculate.configure(text="Calculate")


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

label_denomination = ctk.CTkLabel(app, text="Номінал купюри")
label_denomination.pack(pady=5)

entry_denomination = ctk.CTkEntry(app, placeholder_text="Введіть номінал")
entry_denomination.pack(pady=5)
entry_denomination.bind("<KeyRelease>", update_slider_from_entry)

slider = ctk.CTkSlider(app, from_=0, to=1000, command=update_slider)
slider.pack(pady=5)

button_add = ctk.CTkButton(app, text="Додати купюру", command=add_denomination)
button_add.pack(pady=10)

button_calculate = ctk.CTkButton(app, text="Порахувати", command=calculate_change)
button_calculate.pack(pady=10)

denominations_frame = ctk.CTkFrame(app)
denominations_frame.pack(pady=10, fill="both", expand=True)

app.mainloop()