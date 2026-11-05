class Point:
    x = 1
    y = 2
def f(v):
    match v:
        case Point(x=1, y=2):
            return "hit"
        case _:
            return "miss"
if __name__ == "__main__":
    print(f(Point()))
