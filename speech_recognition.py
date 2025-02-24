import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3
import tkinter as tk
from tkinter import ttk
import requests

# **190+ Countries with Official Languages**
COUNTRY_LANGUAGE_MAP = {
    "Afghanistan": "Pashto (ps)", "Albania": "Albanian (sq)", "Algeria": "Arabic (ar)", "Argentina": "Spanish (es)",
    "Australia": "English (en)", "Austria": "German (de)", "Bangladesh": "Bengali (bn)", "Belgium": "Dutch (nl)",
    "Brazil": "Portuguese (pt)", "Canada": "English (en)", "China": "Chinese (zh-cn)", "Colombia": "Spanish (es)",
    "Denmark": "Danish (da)", "Egypt": "Arabic (ar)", "Ethiopia": "Amharic (am)", "Finland": "Finnish (fi)",
    "France": "French (fr)", "Germany": "German (de)", "Greece": "Greek (el)", "Hungary": "Hungarian (hu)",
    "India": "Hindi (hi)", "Indonesia": "Indonesian (id)", "Iran": "Persian (fa)", "Iraq": "Arabic (ar)",
    "Ireland": "Irish (ga)", "Israel": "Hebrew (he)", "Italy": "Italian (it)", "Japan": "Japanese (ja)",
    "Kazakhstan": "Kazakh (kk)", "Kenya": "Swahili (sw)", "Malaysia": "Malay (ms)", "Mexico": "Spanish (es)",
    "Nepal": "Nepali (ne)", "Netherlands": "Dutch (nl)", "New Zealand": "English (en)", "Nigeria": "English (en)",
    "Norway": "Norwegian (no)", "Pakistan": "Urdu (ur)", "Philippines": "Filipino (tl)", "Poland": "Polish (pl)",
    "Portugal": "Portuguese (pt)", "Qatar": "Arabic (ar)", "Russia": "Russian (ru)", "Saudi Arabia": "Arabic (ar)",
    "South Africa": "English (en)", "South Korea": "Korean (ko)", "Spain": "Spanish (es)", "Sri Lanka": "Sinhala (si)",
    "Sweden": "Swedish (sv)", "Switzerland": "German (de)", "Thailand": "Thai (th)", "Turkey": "Turkish (tr)",
    "Ukraine": "Ukrainian (uk)", "United Arab Emirates": "Arabic (ar)", "United Kingdom": "English (en)",
    "United States": "English (en)", "Vietnam": "Vietnamese (vi)", "Yemen": "Arabic (ar)"
}

# **Function to Get User's Location**
def get_location_language():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        country = data.get("country", "Unknown")
        state = data.get("region", "Unknown")
        return COUNTRY_LANGUAGE_MAP.get(country, "English (en)"), state, country
    except:
        return "English (en)", "Unknown", "Unknown"

# **Translation Function**
def translate_text(text, src_lang, target_lang):
    return GoogleTranslator(source=src_lang, target=target_lang).translate(text)

# **Speech Recognition & TTS**
engine = pyttsx3.init()

def listen_and_translate():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        label.config(text="🎙️ Listening... Speak now!", fg="blue")
        root.update()
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language=source_lang_var.get().split("(")[-1][:-1])

                label.config(text="Translating...", fg="green")
                root.update()

                translated_text = translate_text(text, source_lang_var.get().split("(")[-1][:-1], target_lang_var.get().split("(")[-1][:-1])

                translation_label.config(text=f"🔁 {translated_text}", fg="black")
                root.update()

                engine.say(translated_text)
                engine.runAndWait()

            except sr.UnknownValueError:
                label.config(text="❌ Could not understand. Speak again.", fg="red")
            except sr.RequestError:
                label.config(text="⚠️ Network Error! Check your connection.", fg="red")
                break
            except Exception as e:
                label.config(text=f"⚠️ Error: {str(e)}", fg="red")
                break

# **Function to Update Language When Country is Selected**
def update_language(event):
    selected_country = country_var.get()
    if selected_country in COUNTRY_LANGUAGE_MAP:
        source_lang_var.set(COUNTRY_LANGUAGE_MAP[selected_country])

# **GUI Code**
root = tk.Tk()
root.title("Real-Time Speech Translator")
root.geometry("650x500")
root.configure(bg="white")

label = tk.Label(root, text="Select Country & Language", font=("Arial", 14), bg="white")
label.pack(pady=10)

# **User Location Display**
default_lang, user_state, user_country = get_location_language()
location_label = tk.Label(root, text=f"📍 Location: {user_state}, {user_country}", font=("Arial", 12, "bold"), bg="white")
location_label.pack()

# **Country Selection**
country_list = list(COUNTRY_LANGUAGE_MAP.keys())
country_var = tk.StringVar()
country_dropdown = ttk.Combobox(root, textvariable=country_var, values=country_list, state="readonly", width=40)
country_dropdown.set(user_country if user_country in COUNTRY_LANGUAGE_MAP else "Select a Country")
country_dropdown.pack()
country_dropdown.bind("<<ComboboxSelected>>", update_language)

# **Language Selection**
source_lang_var = tk.StringVar(value=default_lang)
source_lang_dropdown = ttk.Combobox(root, textvariable=source_lang_var, values=list(COUNTRY_LANGUAGE_MAP.values()), state="readonly", width=40)
source_lang_dropdown.pack()

target_lang_var = tk.StringVar(value="English (en)")
target_lang_dropdown = ttk.Combobox(root, textvariable=target_lang_var, values=list(COUNTRY_LANGUAGE_MAP.values()), state="readonly", width=40)
target_lang_dropdown.pack()

# **Start Listening Button**
btn = tk.Button(root, text="🎤 Start Listening", font=("Arial", 14), command=listen_and_translate, bg="blue", fg="white")
btn.pack(pady=10)

# **Translation Display**
translation_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="white")
translation_label.pack(pady=20)

root.mainloop()
