
def welcome():
    print("Welcome to the Custom Encryption Program")
    print("This program encrypts and decrypts text files.\n")


# ---------------- ENCRYPT CHARACTER ----------------
def encrypt_char(ch, shift1, shift2):
    # lowercase a-m → forward by shift1 * shift2
    if 'a' <= ch <= 'm':
        return chr((ord(ch) - 97 + shift1 * shift2) % 26 + 97)

    # lowercase n-z → backward by shift1 + shift2 (MARKED as UPPERCASE)
    elif 'n' <= ch <= 'z':
        encrypted = chr((ord(ch) - 97 - (shift1 + shift2)) % 26 + 97)
        return encrypted.upper()

    # uppercase A-M → backward by shift1
    elif 'A' <= ch <= 'M':
        return chr((ord(ch) - 65 - shift1) % 26 + 65)

    # uppercase N-Z → forward by shift2² (MARKED as lowercase)
    elif 'N' <= ch <= 'Z':
        encrypted = chr((ord(ch) - 65 + (shift2 ** 2)) % 26 + 65)
        return encrypted.lower()

    # other characters unchanged
    else:
        return ch


# ---------------- DECRYPT CHARACTER ----------------
def decrypt_char(ch, shift1, shift2):
    # lowercase → either a-m or marked N-Z
    if ch.islower():
        pos = ord(ch) - 97

        # assume original was a-m
        candidate1 = chr((pos - shift1 * shift2) % 26 + 97)
        if 'a' <= candidate1 <= 'm':
            return candidate1

        # assume original was N-Z (marked lowercase)
        candidate2 = chr((pos - (shift2 ** 2)) % 26 + 65)
        return candidate2

    # uppercase → either marked n-z or A-M
    elif ch.isupper():
        pos = ord(ch) - 65

        # assume original was n-z (marked uppercase)
        candidate1 = chr((pos + (shift1 + shift2)) % 26 + 97)
        if 'n' <= candidate1 <= 'z':
            return candidate1

        # assume original was A-M
        candidate2 = chr((pos + shift1) % 26 + 65)
        return candidate2

    else:
        return ch


# ---------------- ENCRYPT FILE ----------------
def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r") as infile, open("encrypted_text.txt", "w") as outfile:
        for line in infile:
            for ch in line:
                outfile.write(encrypt_char(ch, shift1, shift2))


# ---------------- DECRYPT FILE ----------------
def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r") as infile, open("decrypted_text.txt", "w") as outfile:
        for line in infile:
            for ch in line:
                outfile.write(decrypt_char(ch, shift1, shift2))


# ---------------- VERIFY FUNCTION ----------------
def verify_decryption():
    with open("raw_text.txt", "r") as f1, open("decrypted_text.txt", "r") as f2:
        if f1.read() == f2.read():
            print("Decryption Successful: Files match.")
        else:
            print("Decryption Failed: Files do not match.")


# ---------------- GET SHIFT VALUES ----------------
def get_shifts():
    while True:
        s1 = input("Enter shift1 value: ")
        s2 = input("Enter shift2 value: ")
        if s1.isdigit() and s2.isdigit():
            return int(s1), int(s2)
        else:
            print("Invalid input. Please enter numeric values.")


# ---------------- MAIN FUNCTION ----------------
def main():
    welcome()

    shift1, shift2 = get_shifts()

    print("\nEncrypting file...")
    encrypt_file(shift1, shift2)
    print("Encrypted text written to encrypted_text.txt")

    print("\nDecrypting file...")
    decrypt_file(shift1, shift2)
    print("Decrypted text written to decrypted_text.txt")

    print("\nVerifying decryption...")
    verify_decryption()

    print("\nThanks for using the program!")


main()
