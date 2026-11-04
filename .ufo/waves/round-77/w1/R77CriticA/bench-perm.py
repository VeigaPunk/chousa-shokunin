import hashlib, itertools, random, time
names = [f"n{i:02d}" for i in range(13)]
shuffled = names[:]; random.Random(1234).shuffle(shuffled)
target = hashlib.sha256("|".join(shuffled).encode()).digest()
t0 = time.perf_counter(); n = 0
for p in itertools.permutations(names):
    if hashlib.sha256("|".join(p).encode()).digest() == target:
        break
    n += 1
    if n >= 2_000_000:
        break
dt = time.perf_counter() - t0
rate = n / dt
print(f"hashed={n} secs={dt:.3f} per_sec={rate:,.0f}")
print(f"13!={6277020800:,} one_core_s={6277020800/rate:,.0f} cores32_s={6277020800/rate/32:,.0f}")
