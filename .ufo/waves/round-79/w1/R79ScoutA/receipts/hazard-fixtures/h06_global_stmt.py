counter = 0
def bump():
    global counter
    counter += 1
    return counter
if __name__ == "__main__":
    print(bump(), bump(), counter)
