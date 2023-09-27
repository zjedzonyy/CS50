from cs50 import get_string

s = get_string("Greeting: ")
s = s.lower()
s = s.strip()

if s.startswith("hello"):
    print("$0")

elif "h" == s[0] and s != "hello":
    print("$20")

else:
    print("$100")
