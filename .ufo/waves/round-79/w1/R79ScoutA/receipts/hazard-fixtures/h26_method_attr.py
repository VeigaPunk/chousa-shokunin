class Holder:
    def show(self):
        return "S"
    def run(self):
        return self.show()
if __name__ == "__main__":
    print(Holder().run())
