class Holder:
    pass
h = Holder()
setattr(h, "attr", 9)
if __name__ == "__main__":
    print(getattr(h, "attr"))
