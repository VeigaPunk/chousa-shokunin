from dataclasses import dataclass
@dataclass
class R:
    count: int = 1
if __name__ == "__main__":
    print(R().count)
