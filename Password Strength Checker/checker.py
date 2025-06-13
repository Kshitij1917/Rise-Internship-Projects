import re

def check_password_strength(password):
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        errors.append("Include at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Include at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        errors.append("Include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Include at least one special character.")

    if len(errors) >= 4:
        return "Weak", errors
    elif len(errors) >= 2:
        return "Moderate", errors
    else:
        return "Strong", errors
