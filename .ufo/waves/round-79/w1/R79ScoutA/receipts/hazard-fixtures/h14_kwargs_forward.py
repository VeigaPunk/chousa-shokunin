def callee(count):
    return count * 2
def caller(kwargs):
    return callee(**kwargs)
if __name__ == "__main__":
    print(caller({"count": 21}))
