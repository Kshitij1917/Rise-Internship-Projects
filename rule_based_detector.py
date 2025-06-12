import re

def rule_based_check(url):
    suspicious_keywords = ['login', 'verify', 'secure', 'account', 'bank', 'update']

    if '@' in url:
        return "Phishing (contains '@')"
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        return "Phishing (contains suspicious keywords)"
    if url.count('.') > 5:
        return "Phishing (too many dots)"
    if '-' in url:
        return "Phishing (contains hyphen)"
    if len(url) > 75:
        return "Phishing (URL too long)"
    if not url.startswith('https'):
        return "Phishing (not HTTPS)"

    return "Legitimate"

if __name__ == "__main__":
    test_url = input("Enter a URL to check: ")
    result = rule_based_check(test_url)
    print("Result:", result)
