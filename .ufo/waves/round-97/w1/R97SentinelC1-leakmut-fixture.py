import sys

# Fixture-only mutant: a self-test that writes a file relative to the cwd and then fails (a "killed" mutant that leaks).
def _leak():
    open("leak-r97.txt", "w", encoding="utf-8").write("x\n")
    print("SEARCH_RERUN_SELFTEST: FAIL cases=0/47")
    return 1


if __name__ == "__main__":
    sys.exit(_leak() if "--selftest" in sys.argv else 2)
