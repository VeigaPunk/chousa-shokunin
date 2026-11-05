def deco(fn):
    def wrap(*a):
        return fn(*a) + 1
    return wrap
@deco
def g(x):
    return x
if __name__ == "__main__":
    print(g(41))
