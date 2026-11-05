class Holder:
    label = "L"
    def __init__(self):
        self.value = 5
    def show(self):
        return self.label + str(self.value)
if __name__ == "__main__":
    print(Holder().show())
