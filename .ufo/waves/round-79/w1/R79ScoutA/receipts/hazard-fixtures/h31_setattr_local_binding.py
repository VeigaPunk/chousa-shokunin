def helper():
    return 1
class O: pass
o = O()
setattr(o, "helper", helper())
if __name__ == "__main__":
    print(getattr(o, "helper"))
