
import re
import getpass
from pathlib import Path
from zxcvbn import zxcvbn


def load_common_passwords():
    file_path = Path(__file__).parent / "common_passwords.txt"

    if not file_path.exists():
        return set()

    with open(file_path, "r", encoding="utf-8") as file:
        return {line.strip().lower() for line in file if line.strip()}


def analyze_password(password):
    common_passwords = load_common_passwords()
    result = zxcvbn(password)

    warnings = []
    suggestions = []

    # 1. Length check
    if len(password) < 8:
        warnings.append("Password is shorter than 8 characters.")
        suggestions.append("Use at least 12 characters.")

    elif len(password) < 12:
        suggestions.append("Consider using 12 or more characters.")

    # 2. Character variety
    character_types = {
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "numbers": bool(re.search(r"\d", password)),
        "symbols": bool(re.search(r"[^a-zA-Z0-9]", password))
    }

    for character_type, present in character_types.items():
        if not present:
            suggestions.append(f"Consider including {character_type} characters.")

    if sum(character_types.values()) == 1:
        warnings.append("Password uses only one character type.")

    # 3. Common password check
    if password.lower() in common_passwords:
        warnings.append("Password appears in the common-password list.")

    # 4. Repeated characters
    if re.search(r"(.)\1{2,}", password):
        warnings.append("Password contains repeated consecutive characters.")

    # 5. Repeated sequences, e.g. abcabc
    if re.search(r"(.{2,})\1+", password, re.IGNORECASE):
        warnings.append("Password contains a repeated sequence.")

    # 6. Predictable sequences and keyboard patterns
    patterns = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]

    lowered = password.lower()

    for pattern in patterns:
        for i in range(len(pattern) - 3):
            sequence = pattern[i:i + 4]

            if sequence in lowered:
                warnings.append("Password contains a predictable sequence.")
                break

        if warnings and warnings[-1] == "Password contains a predictable sequence.":
            break

    # 7. Library strength estimate
    score = result["score"]

    strength_levels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Strong",
        4: "Very Strong"
    }

    # 8. Separate custom-check status
    review_status = "Review recommended" if warnings else "No custom flags detected"

    return {
        "length": len(password),
        "score": score,
        "strength": strength_levels[score],
        "review_status": review_status,
        "warnings": warnings,
        "suggestions": suggestions,
        "feedback": result["feedback"]
    }


def display_results(results):
    print("\n" + "=" * 48)
    print("             PASSWORD ANALYSIS REPORT")
    print("=" * 48)

    print(f"Password Length       : {results['length']} characters")
    print(f"Library Strength      : {results['strength']}")
    print(f"Library Score         : {results['score']}/4")
    print(f"Custom Check Status   : {results['review_status']}")

    print("\n--- Security Warnings ---")

    if results["warnings"]:
        for warning in results["warnings"]:
            print(f"[!] {warning}")
    else:
        print("No custom checks were triggered.")

    print("\n--- Recommendations ---")

    if results["suggestions"]:
        for suggestion in results["suggestions"]:
            print(f"[*] {suggestion}")
    else:
        print("No additional character or length recommendations.")

    feedback = results["feedback"]

    if feedback["warning"]:
        print("\n--- Library Feedback ---")
        print(feedback["warning"])

    if feedback["suggestions"]:
        for suggestion in feedback["suggestions"]:
            print(f"[*] {suggestion}")

    print("\nNote: A high library score does not guarantee security.")
    print("=" * 48)


def main():
    print("=" * 48)
    print("              PYTHON PASSWORD ANALYZER")
    print("=" * 48)
    print("Password analysis happens locally.")
    print("Your password is not displayed or stored.")

    password = getpass.getpass("\nEnter password to analyze: ")

    if not password:
        print("Error: Password cannot be empty.")
        return

    results = analyze_password(password)
    display_results(results)


if __name__ == "__main__":
    main()