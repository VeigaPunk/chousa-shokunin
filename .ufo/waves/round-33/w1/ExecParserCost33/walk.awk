# Same C1-style walk in gawk, for throughput comparison. Reads JSONL from a file.
# Prints one line per record: size members dup id line sha256
{
  s = $0
  n = length(s)
  st = 0; depth = 0; wantkey = 0; iskey = 0; tok = 0
  members = 0; dupflag = 0; expect_val = 0
  rid = ""; rline = ""; rsha = ""; lastkey = ""; key = ""
  delete dupcnt
  for (i = 1; i <= n; i++) {
    c = substr(s, i, 1)
    if (st == 1) {
      if (c == "\\") { st = 2 }
      else if (c == "\"") {
        if (iskey) {
          if (depth == 1) {
            key = substr(s, tok, i - tok)
            lastkey = key
            if (key == "id" || key == "source" || key == "span" || key == "expect" ||
                key == "marker" || key == "line" || key == "sha256") {
              dupcnt[key]++
              if (dupcnt[key] > 1) dupflag = 1
            }
          }
          wantkey = 0
        } else if (expect_val == 1 && depth == 1) {
          val = substr(s, tok, i - tok)
          members++
          expect_val = 0
          if (lastkey == "id") rid = val
          else if (lastkey == "line") rline = val
          else if (lastkey == "sha256") rsha = val
        }
        iskey = 0; tok = 0; st = 0
      }
    } else if (st == 2) {
      st = 1
    } else if (c == "\"") {
      tok = i + 1; iskey = wantkey; st = 1
    } else if (c == "{" || c == "[") {
      if (depth == 0) { depth = 1; wantkey = 1 }
      else {
        if (depth == 1 && expect_val == 1) { members++; expect_val = 0 }
        depth++
      }
    } else if (c == "}" || c == "]") {
      if (depth > 0) depth--
      if (depth == 1) expect_val = 0
    } else if (c == ":") {
      if (depth == 1) expect_val = 1
    } else if (c == ",") {
      if (depth == 1) { expect_val = 0; wantkey = 1 }
    } else if (depth == 1 && expect_val == 1) {
      members++; expect_val = 0
    }
  }
  print n, members, dupflag, rid, rline, rsha
}
