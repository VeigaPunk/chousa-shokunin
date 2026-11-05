class C:
    @classmethod
    def make(cls, count=1):
        return count
if __name__ == "__main__":
    print(C.make(count=4))
