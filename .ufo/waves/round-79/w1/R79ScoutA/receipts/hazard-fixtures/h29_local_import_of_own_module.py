import sys
VALUE = 42
if __name__ == "__main__":
    print(getattr(sys.modules[__name__], "VALUE", "ABSENT"))
