/* Probe A7 instrument — recover the battery's per-run subject permutation from the ORDER digest.
 *
 * `score()` prints `ORDER <i> sha256("|".join(permuted names))` before the calls. Thirteen names
 * is a 13! = 6,227,020,800 domain: a printed digest over a constant, small domain is not secrecy.
 * Incremental SHA-256 (context copy per branch) + OpenMP over the first two positions.
 *
 * usage: perm TARGET_HEX name0 name1 ... name12
 */
#include <openssl/sha.h>
#include <omp.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define N 13

static const char *names[N];
static char tok[N][64];              /* "|" + name */
static int toklen[N];
static unsigned char target[32];
static volatile int done = 0;
static double t_cpu0, t_wall0;
static int result[N];

static int hexval(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return -1;
}

static void rec(SHA256_CTX *ctx, int depth, unsigned used, int *order) {
    if (depth == N) {
        unsigned char md[32];
        SHA256_CTX c = *ctx;
        SHA256_Final(md, &c);
        if (memcmp(md, target, 32) == 0) {
#pragma omp critical
            {
                if (!done) {
                    done = 1;
                    for (int i = 0; i < N; i++) result[i] = order[i];
                    struct timespec now;
                    clock_gettime(CLOCK_MONOTONIC, &now);
                    double wall = (double)now.tv_sec + now.tv_nsec / 1e9 - t_wall0;
                    double cpu = (double)(clock() - t_cpu0) / CLOCKS_PER_SEC;
                    printf("FOUND secs_wall=%.1f secs_cpu=%.1f threads=%d\n",
                           wall, cpu, omp_get_max_threads());
                    for (int i = 0; i < N; i++) printf("POS %2d %s\n", i, names[result[i]]);
                    fflush(stdout);
                }
            }
        }
        return;
    }
    for (int i = 0; i < N; i++) {
        if ((used >> i) & 1u) continue;
        SHA256_CTX c = *ctx;
        SHA256_Update(&c, tok[i], (size_t)toklen[i]);
        order[depth] = i;
        rec(&c, depth + 1, used | (1u << i), order);
        if (done) return;
    }
}

int main(int argc, char **argv) {
    if (argc != N + 2) {
        fprintf(stderr, "usage: %s TARGET_HEX name0..name12\n", argv[0]);
        return 2;
    }
    for (int i = 0; i < 32; i++) {
        int hi = hexval(argv[1][2 * i]), lo = hexval(argv[1][2 * i + 1]);
        if (hi < 0 || lo < 0) { fprintf(stderr, "bad hex\n"); return 2; }
        target[i] = (unsigned char)((hi << 4) | lo);
    }
    for (int i = 0; i < N; i++) {
        names[i] = argv[i + 2];
        toklen[i] = snprintf(tok[i], sizeof tok[i], "|%s", names[i]);
    }
    struct timespec s0;
    clock_gettime(CLOCK_MONOTONIC, &s0);
    t_wall0 = (double)s0.tv_sec + s0.tv_nsec / 1e9;
    t_cpu0 = (double)clock() / CLOCKS_PER_SEC;
    int b0, b1;
#pragma omp parallel for collapse(2) schedule(dynamic, 1)
    for (b0 = 0; b0 < N; b0++) {
        for (b1 = 0; b1 < N; b1++) {
            if (b0 == b1 || done) continue;
            SHA256_CTX ctx;
            SHA256_Init(&ctx);
            SHA256_Update(&ctx, names[b0], strlen(names[b0]));
            SHA256_Update(&ctx, tok[b1], (size_t)toklen[b1]);
            int order[N];
            order[0] = b0; order[1] = b1;
            rec(&ctx, 2, (1u << b0) | (1u << b1), order);
        }
    }
    if (!done) { printf("NOTFOUND\n"); return 1; }
    return 0;
}
