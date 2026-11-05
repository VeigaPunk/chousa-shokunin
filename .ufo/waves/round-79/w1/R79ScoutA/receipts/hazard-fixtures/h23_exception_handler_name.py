try:
    raise ValueError("x")
except ValueError as exc:
    print(type(exc).__name__)
