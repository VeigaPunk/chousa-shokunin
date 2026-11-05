def outer():
    acc = 0
    def inner():
        nonlocal acc
        acc += 5
        return acc
    inner()
    return acc
if __name__ == "__main__":
    print(outer())
