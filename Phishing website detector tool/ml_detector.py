import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import re

def extract_features(url):
    return {
        'url_length': len(url),
        'has_at': int('@' in url),
        'dot_count': url.count('.'),
        'has_hyphen': int('-' in url),
        'has_https': int(url.startswith('https')),
        'suspicious_keywords': int(any(keyword in url.lower() for keyword in ['login', 'verify', 'secure', 'account', 'bank', 'update']))
    }

df = pd.read_csv('PhishingDetector.csv')
df['label'] = df['label'].map({'legitimate': 0, 'phishing': 1})
features = df['url'].apply(extract_features).apply(pd.Series)
X = features
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

def predict_url(url):
    features = pd.DataFrame([extract_features(url)])
    prediction = model.predict(features)[0]
    return "Phishing" if prediction == 1 else "Legitimate"

if __name__ == "__main__":
    test_url = input("Enter URL to check: ")
    result = predict_url(test_url)
    print("Result:", result)
