def classify(v):
    match v:
        case {"k": val} if val > 1:
            return val
        case [a, *rest]:
            return a + len(rest)
        case _:
            return 0
if __name__ == "__main__":
    print(classify({"k": 5}), classify([1, 2, 3]), classify(0))
