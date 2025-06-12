import tkinter as tk
from tkinter import messagebox
import pandas as pd
import re
from sklearn.ensemble import RandomForestClassifier
import requests

API_KEY = 'AIzaSyDEFus7nkRWfypzCBDErK5iHLUadiPYUys'

def extract_features(url):
    return {
        'url_length': len(url),
        'has_at': int('@' in url),
        'dot_count': url.count('.'),
        'has_hyphen': int('-' in url),
        'has_https': int(url.startswith('https')),
        'suspicious_keywords': int(any(keyword in url.lower() for keyword in ['login', 'verify', 'secure', 'account', 'bank', 'update']))
    }

def train_model():
    df = pd.read_csv('PhishingDetector.csv')
    df['label'] = df['label'].map({'legitimate': 0, 'phishing': 1})
    features = df['url'].apply(extract_features).apply(pd.Series)
    X = features
    y = df['label']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def check_with_google_safe_browsing(url):
    api_url = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}'
    payload = {
        "client": {"clientId": "yourcompanyname", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        response = requests.post(api_url, json=payload)
        data = response.json()
        return "Phishing" if data.get('matches') else "Legitimate"
    except Exception as e:
        print("API error:", e)
        return "Unknown (API error)"

model = train_model()

def check_url():
    url = entry.get()
    if not url:
        messagebox.showerror("Input Error", "Please enter a URL.")
        return
    try:
        api_result = check_with_google_safe_browsing(url)
        if api_result == "Phishing":
            label_result.config(text="Result: Phishing (Google API)", fg="red")
            return
        features = pd.DataFrame([extract_features(url)])
        prediction = model.predict(features)[0]
        result = "Phishing" if prediction == 1 else "Legitimate"
        color = "red" if result == "Phishing" else "green"
        label_result.config(text=f"Result: {result} (ML Model)", fg=color)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

app = tk.Tk()
app.title("Phishing URL Detector")
app.geometry("400x250")
app.resizable(False, False)
app.config(bg="#f7f7f7")

tk.Label(app, text="Enter URL:", font=("Arial", 12), bg="#f7f7f7").pack(pady=10)
entry = tk.Entry(app, font=("Arial", 12), width=40)
entry.pack(pady=5)

tk.Button(app, text="Check URL", font=("Arial", 12), bg="#4CAF50", fg="white", command=check_url).pack(pady=15)
label_result = tk.Label(app, text="", font=("Arial", 14), bg="#f7f7f7")
label_result.pack(pady=10)

app.mainloop()
