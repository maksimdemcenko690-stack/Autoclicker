import threading
import time
import tkinter as tk
from tkinter import ttk

from pynput import keyboard, mouse

mouse_ctl = mouse.Controller()


class AutoClicker:
    def __init__(self, root):
        self.root = root
        root.title("Автокликер")
        root.geometry("340x220")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        self.running = False
        self.cps_value = 10.0
        self.btn_value = mouse.Button.left

        self.cps = tk.StringVar(value="10")
        self.choice = tk.StringVar(value="Левая")
        self.status = tk.StringVar(value="Выключен")

        frame = ttk.Frame(root, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Кликов в секунду (1-50):").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(frame, from_=1, to=50, textvariable=self.cps, width=6).grid(
            row=0, column=1, padx=10, pady=5
        )

        ttk.Label(frame, text="Кнопка мыши:").grid(row=1, column=0, sticky="w")
        ttk.Combobox(
            frame,
            textvariable=self.choice,
            values=["Левая", "Правая"],
            state="readonly",
            width=8,
        ).grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(frame, text="Старт / Стоп", command=self.toggle).grid(
            row=2, column=0, columnspan=2, pady=12, sticky="ew"
        )

        ttk.Label(frame, textvariable=self.status, font=("Segoe UI", 11, "bold")).grid(
            row=3, column=0, columnspan=2
        )
        ttk.Label(frame, text="Z - вкл,  X - выкл,  Esc - авостоп", foreground="gray").grid(
            row=4, column=0, columnspan=2, pady=(8, 0)
        )

        threading.Thread(target=self.click_loop, daemon=True).start()
        keyboard.Listener(on_press=self.on_press).start()
        self.refresh()

    def toggle(self):
        self.running = not self.running

    def on_press(self, key):
        try:
            ch = key.char.lower()
        except AttributeError:
            ch = None

        if ch == "z":
            self.running = True
        elif ch == "x":
            self.running = False
        elif key == keyboard.Key.esc:
            self.running = False

    def click_loop(self):
        while True:
            if self.running:
                mouse_ctl.click(self.btn_value)
                time.sleep(1.0 / self.cps_value)
            else:
                time.sleep(0.05)

    def refresh(self):
        try:
            value = float(self.cps.get())
            self.cps_value = min(max(value, 1.0), 50.0)
        except ValueError:
            pass
        if self.choice.get() == "Левая":
            self.btn_value = mouse.Button.left
        else:
            self.btn_value = mouse.Button.right
        self.status.set("ВКЛЮЧЁН" if self.running else "Выключен")
        self.root.after(100, self.refresh)


if __name__ == "__main__":
    root = tk.Tk()
    AutoClicker(root)
    root.mainloop()
