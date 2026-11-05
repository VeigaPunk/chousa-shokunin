def callee(count):
    return count
if __name__ == "__main__":
    print(callee(**{"count": 5}))
