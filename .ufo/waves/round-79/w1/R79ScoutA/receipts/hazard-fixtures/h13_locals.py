def f():
    loc = 11
    return locals()["loc"]
if __name__ == "__main__":
    print(f())
