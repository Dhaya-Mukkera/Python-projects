import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = 'your_openweathermap_api_key'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather():
    location = entry.get()
    units = 'metric' if var.get() == 'C' else 'imperial'
    params = {'q': location, 'appid': API_KEY, 'units': units}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description'].capitalize()
        icon_code = data['weather'][0]['icon']

        label_temp.config(text=f"Temperature: {temp}°{var.get()}")
        label_humidity.config(text=f"Humidity: {humidity}%")
        label_wind.config(text=f"Wind Speed: {wind_speed} m/s")
        label_desc.config(text=f"Conditions: {description}")

        # Fetch and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        label_icon.config(image=icon_photo)
        label_icon.image = icon_photo

    except requests.exceptions.HTTPError:
        messagebox.showerror("Error", "Could not retrieve weather data. Check the location.")
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network problem.")
    except KeyError:
        messagebox.showerror("Error", "Unexpected response format.")

root = tk.Tk()
root.title("Weather App")

tk.Label(root, text="Enter city or ZIP code:").pack()
entry = tk.Entry(root)
entry.pack()

var = tk.StringVar(value='C')
tk.Radiobutton(root, text="Celsius", variable=var, value='C').pack()
tk.Radiobutton(root, text="Fahrenheit", variable=var, value='F').pack()

tk.Button(root, text="Get Weather", command=fetch_weather).pack()

label_temp = tk.Label(root, text="")
label_temp.pack()
label_humidity = tk.Label(root, text="")
label_humidity.pack()
label_wind = tk.Label(root, text="")
label_wind.pack()
label_desc = tk.Label(root, text="")
label_desc.pack()
label_icon = tk.Label(root)
label_icon.pack()

root.mainloop()
