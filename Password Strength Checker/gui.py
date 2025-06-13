import tkinter as tk
from tkinter import ttk
from checker import check_password_strength
from utils import suggest_improvements
# from nltk_words import is_dictionary_word  # Optional

def analyze_password(event=None):
    pwd = entry.get()

    if not pwd:
        result_text.set("")
        suggest_text.set("")
        strength_bar["value"] = 0
        strength_bar_label.config(text="")
        return

    strength, errors = check_password_strength(pwd)
    suggestions = suggest_improvements(errors)
    update_result_display(strength)
    suggest_text.set("\n".join(suggestions) if suggestions else "✅ Your password is strong!")

    strength_values = {"Weak": 33, "Moderate": 66, "Strong": 100}
    strength_colors = {"Weak": "red", "Moderate": "orange", "Strong": "green"}
    value = strength_values.get(strength, 0)
    color = strength_colors.get(strength, "black")
    strength_bar["value"] = value
    strength_bar_label.config(text=f"{value}%", fg=color)

def toggle_password():
    if show_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

def update_result_display(strength):
    colors = {"Weak": "red", "Moderate": "orange", "Strong": "green"}
    result_label.config(text=f"Strength: {strength}", fg=colors.get(strength, "black"))

root = tk.Tk()
root.title("🔐 Password Strength Checker")
root.geometry("460x430")
root.resizable(False, False)
root.configure(bg="#f9fafb")

FONT_MAIN = ("Segoe UI", 12)
FONT_RESULT = ("Segoe UI", 14, "bold")

tk.Label(root, text="Enter your password:", font=FONT_MAIN, bg="#f9fafb").pack(pady=10)

entry = ttk.Entry(root, width=35, font=FONT_MAIN, show="*")
entry.pack(pady=5)
entry.bind("<KeyRelease>", analyze_password)

show_var = tk.BooleanVar()
show_checkbox = tk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle_password,
                               bg="#f9fafb", font=("Segoe UI", 10))
show_checkbox.pack(pady=5)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=FONT_RESULT, bg="#f9fafb")
result_label.pack(pady=5)

tk.Label(root, text="Strength Meter:", font=("Segoe UI", 11), bg="#f9fafb").pack()
strength_bar = ttk.Progressbar(root, length=250, mode='determinate')
strength_bar.pack(pady=3)

strength_bar_label = tk.Label(root, text="", font=("Segoe UI", 11), bg="#f9fafb")
strength_bar_label.pack()

suggest_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
suggest_frame.pack(pady=15, padx=20, fill="both", expand=True)

tk.Label(suggest_frame, text="Suggestions:", font=FONT_MAIN, bg="#ffffff").pack(anchor="w", padx=10, pady=5)
suggest_text = tk.StringVar()
tk.Label(suggest_frame, textvariable=suggest_text, bg="#ffffff", justify="left",
         wraplength=400, font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=5)

root.mainloop()
