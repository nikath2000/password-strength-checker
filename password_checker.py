import re

COMMON_PATTERNS = ["1234", "password", "qwerty", "1111", "abcd", "letmein"]

def assess_password(password: str) -> dict:
    score = 0
    feedback = []

    length = len(password)

    # Length scoring (max 30)
    if length < 8:
        score += 5
        feedback.append("Make it at least 8 characters.")
    elif length < 12:
        score += 15
        feedback.append("Good length, consider 12+ for more safety.")
    elif length < 16:
        score += 22
    else:
        score += 30
        feedback.append("Great length — excellent!")

    # Character variety (max 40)
    if re.search(r'[a-z]', password):
        score += 8
    else:
        feedback.append("Add lowercase letters.")
    if re.search(r'[A-Z]', password):
        score += 8
    else:
        feedback.append("Add uppercase letters.")
    if re.search(r'\d', password):
        score += 8
    else:
        feedback.append("Add numbers.")
    if re.search(r'[^A-Za-z0-9]', password):
        score += 16
    else:
        feedback.append("Add special characters (e.g. !@#$%).")

    # Penalties (max -30)
    lowered = password.lower()
    for pat in COMMON_PATTERNS:
        if pat in lowered:
            score -= 20
            feedback.append(f"Avoid common pattern: '{pat}'.")
            break

    # all same char
    if length >= 3 and len(set(password)) == 1:
        score -= 20
        feedback.append("Don't use the same character repeatedly.")

    # sequential like 'abcd' or '1234'
    def is_sequential(s):
        # check increasing sequences of letters or digits of length >=4
        if len(s) < 4:
            return False
        ords = [ord(c) for c in s]
        # check for consecutive grows of 1
        return all(ords[i+1] - ords[i] == 1 for i in range(len(ords)-1))

    # slide over substrings to detect simple sequences
    lowered = password.lower()
    for i in range(len(lowered)-3):
        sub = lowered[i:i+4]
        if sub.isalpha() or sub.isdigit():
            if is_sequential(sub):
                score -= 15
                feedback.append("Avoid sequential characters like 'abcd' or '1234'.")
                break

    # Bound score 0-100
    final = max(0, min(100, score))

    # Compute label
    if final < 25:
        label = "Very weak"
    elif final < 45:
        label = "Weak"
    elif final < 65:
        label = "Fair"
    elif final < 85:
        label = "Strong"
    else:
        label = "Very strong"

    if not feedback:
        feedback.append("Good password! Minor improvement possible.")

    return {
        "password": password,
        "score": final,
        "label": label,
        "feedback": feedback
    }

# Example
if __name__ == "__main__":
    for p in ["password123", "P@ssw0rd!", "abcde", "ThisIs@VeryLongPassword2025"]:
        res = assess_password(p)
        print(res)
