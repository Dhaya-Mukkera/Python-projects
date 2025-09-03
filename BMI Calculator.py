import tkinter as tk
from tkinter import messagebox
import json
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_FILE = "bmi_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        # User input
        tk.Label(root, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(root, text="Weight (kg):").grid(row=1, column=0, sticky="e")
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=1, column=1)

        tk.Label(root, text="Height (m):").grid(row=2, column=0, sticky="e")
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=2, column=1)

        # Calculate button
        self.calc_button = tk.Button(root, text="Calculate BMI", command=self.calculate_and_store)
        self.calc_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Result display
        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.grid(row=4, column=0, columnspan=2)

        # Show history button
        self.history_button = tk.Button(root, text="Show BMI History", command=self.show_history)
        self.history_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Load existing data
        self.data = load_data()

    def calculate_and_store(self):
        name = self.name_entry.get().strip()
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if not (10 <= weight <= 500):
                raise ValueError("Weight out of range")
            if not (0.5 <= height <= 6.5):
                raise ValueError("Height out of range")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numeric values for weight and height within reasonable ranges.")
            return

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)
        self.result_label.config(text=f"{name}, your BMI is {bmi:.2f} ({category})")

        # Store data with timestamp
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        if name not in self.data:
            self.data[name] = []
        self.data[name].append({"timestamp": timestamp, "weight": weight, "height": height, "bmi": bmi})
        save_data(self.data)

    def show_history(self):
        name = self.name_entry.get().strip()
        if name not in self.data or not self.data[name]:
            messagebox.showinfo("No Data", f"No BMI history found for {name}.")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title(f"{name}'s BMI History")

        # Prepare data for plotting
        timestamps = [entry["timestamp"] for entry in self.data[name]]
        bmis = [entry["bmi"] for entry in self.data[name]]

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.plot(timestamps, bmis, marker='o')
        ax.set_title(f"BMI Trend for {name}")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=history_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
