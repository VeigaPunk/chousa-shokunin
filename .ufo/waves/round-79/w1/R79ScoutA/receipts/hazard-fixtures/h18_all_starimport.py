def foo():
    return 1
def bar():
    return 2
__all__ = ["foo", "bar"]
if __name__ == "__main__":
    print(foo(), bar(), __all__)
