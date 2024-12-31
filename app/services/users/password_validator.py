def password_validator(password):
    if not password:
        return "Password can't be empty."
    
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    
    if not any(char.isalpha() for char in password):
        return "Password must contain at least one letter."
    
    if not any(char in "!@#$%^&*(),.?\":{}|<>" for char in password):
        return "Password must contain at least one special character."
    
    return None
