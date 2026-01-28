def reverse_string(s: str) -> str:
    return s[::-1]

if __name__ == "__main__":
    test_string = "i love india"
    print(f"Original: {test_string}")
    print(f"Reversed: {reverse_string(test_string)}")