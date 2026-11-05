def foo():
    return 1
__all__ = ["foo"]
if __name__ == "__main__":
    print(foo(), __all__)
