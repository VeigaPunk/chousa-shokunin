import sys
VALUE = 42
def get():
    return getattr(sys.modules[__name__], "VALUE")
if __name__ == "__main__":
    print(get())
