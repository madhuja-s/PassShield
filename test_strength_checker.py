from strength_checker import calculate_strength


test_passwords = [
    "123456",
    "password",
    "password123",
    "Hello123",
    "Maddy@2026",
    "X7!kP9#qL2@z"
]


print("========== PassShield Testing ==========")


for password in test_passwords:

    result = calculate_strength(password)

    print("\nPassword:", password)
    print("Strength:", result["strength"])
    print("Score:", result["score"], "/ 4")