import re, json, hashlib
BASE="/fast/scratch/hyaku/chousa-r99/R99ExecC2Repro"
def norm(s):
    return " ".join(s.replace("\u2018","'").replace("\u2019","'").replace("\u201c",'"').replace("\u201d",'"').split())
plos=open(BASE+"/live/plos.txt",encoding="utf-8",errors="ignore").read()
epmc=open(BASE+"/live/epmc.json",encoding="utf-8",errors="ignore").read()
rec=json.loads(epmc)["resultList"]["result"][0]
tests={
 "G4":"a major content error was a cited assertion in which the referenced source either failed to substantiate, was unrelated to, or contradicted the assertion.",
 "G10":"I estimate that 14.5% (10.5% to 18.6% at a 95% confidence interval) of cited assertions in original research articles in medical journals are inaccurate.",
 "G11":"the distribution of content errors (64.8% major to 35.2% minor errors) is particularly concerning.",
 "J2":"and estimated major, minor and total quotation error rates of 11,9%, 95% CI [8.4, 16.6] 11.5% [8.3, 15.7], and 25.4% [19.5, 32.4].",
 "J3":"While heterogeneity was substantial, even the lowest estimate of total quotation errors was considerable (6.7%).",
}
for k,q in tests.items():
    hay = norm(plos) if k.startswith("G") else norm(rec.get("abstractText",""))
    print(k, norm(q) in hay)
# G6 typo check: capture has "an informative or factual inaccuracies" (grammatically wrong) - verify live too
print("G6 live:", "an informative or" in norm(plos))
print("G6 live exact:", "as an informative or" in norm(plos))
