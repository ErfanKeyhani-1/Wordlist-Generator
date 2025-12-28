# Written by Erfan Keyhani (mr-3)
# Date: 12-12-2025

import itertools
import argparse
from datetime import datetime

BANNER = r"""
 #     #                                                #####                                                         
 #  #  #  ####  #####  #####  #      #  ####  #####    #     # ###### #    # ###### #####    ##   #####  ####  #####  
 #  #  # #    # #    # #    # #      # #        #      #       #      ##   # #      #    #  #  #    #   #    # #    # 
 #  #  # #    # #    # #    # #      #  ####    #      #  #### #####  # #  # #####  #    # #    #   #   #    # #    # 
 #  #  # #    # #####  #    # #      #      #   #      #     # #      #  # # #      #####  ######   #   #    # #####  
 #  #  # #    # #   #  #    # #      # #    #   #      #     # #      #   ## #      #   #  #    #   #   #    # #   #  
  ## ##   ####  #    # #####  ###### #  ####    #       #####  ###### #    # ###### #    # #    #   #    ####  #    # 
                                                                                                                                                                                                                                                                                    

Wordlist Generator Specifically for Authorised External Penetration testing
By Erfan Keyhani (mr-3)
https://www.github.com/erfankeyhani-1/
"""

def safe_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        raise SystemExit(130)
    except EOFError:
        print("\nNo input available.")
        raise SystemExit(1)

def ask_list(prompt, default=None):
    line = safe_input(prompt).strip()
    if not line and default is not None:
        return list(default)
    if not line:
        return []
    line = line.replace(";", ",")
    parts = [x.strip() for x in line.split(",")]
    return [p for p in parts if p]

def ask_yes(prompt, default=True):
    s = safe_input(prompt).strip().lower()
    if not s:
        return default
    return s in ("y", "yes", "1", "true", "t")

def casing_variants(token):
    s = set()
    s.add(token)
    s.add(token.lower())
    s.add(token.upper())
    if token:
        s.add(token[0].upper() + token[1:].lower())
    return s

def expand_tokens(tokens, squeeze_space=True):
    result = set()
    for t in tokens:
        if not t:
            continue
        result |= casing_variants(t)
        if squeeze_space and " " in t:
            t2 = t.replace(" ", "")
            result |= casing_variants(t2)
    return sorted(result)

def expand_years(years):
    result = set()
    for y in years:
        result.add(y)
        if y.isdigit() and len(y) == 4:
            result.add(y[2:])
    return sorted(result)

def gen_from_keys(data, keys):
    pools = []
    for k in keys:
        if k == "SPECIAL":
            pools.append(data.get("SPECIAL", []))
        else:
            pools.append(data.get(k, []))
    if not all(pools):
        return []
    for combo in itertools.product(*pools):
        yield "".join(combo)

def build_wordlist(data):
    words = set()
    base_keys = ["SEASON_CURRENT", "SEASON_PAST", "YEAR_CURRENT", "YEAR_PAST",
                 "TEAM", "ADDRESS", "COLLEGE", "USER", "COMPANY"]

    for k in base_keys:
        for v in data.get(k, []):
            words.add(v)

    for k in base_keys:
        for w in gen_from_keys(data, [k, "SPECIAL"]):
            words.add(w)
        for w in gen_from_keys(data, [k, "SPECIAL", "SPECIAL"]):
            words.add(w)

    for s_key in ["SEASON_CURRENT", "SEASON_PAST"]:
        for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
            for base in ([s_key, y_key], [y_key, s_key]):
                for extra in ([], ["SPECIAL"], ["SPECIAL", "SPECIAL"]):
                    keys = base + extra
                    for w in gen_from_keys(data, keys):
                        words.add(w)

    for k in ["SEASON_CURRENT", "SEASON_PAST", "YEAR_CURRENT", "YEAR_PAST"]:
        for w in gen_from_keys(data, [k, "SPECIAL"]):
            words.add(w)
        for w in gen_from_keys(data, ["SPECIAL", k]):
            words.add(w)

    for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
        for w in gen_from_keys(data, ["TEAM", y_key]):
            words.add(w)
        for w in gen_from_keys(data, ["TEAM", y_key, "SPECIAL"]):
            words.add(w)
        for w in gen_from_keys(data, ["TEAM", y_key, "SPECIAL", "SPECIAL"]):
            words.add(w)

    for s_key in ["SEASON_CURRENT", "SEASON_PAST"]:
        for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
            for w in gen_from_keys(data, ["TEAM", s_key, y_key]):
                words.add(w)
            for w in gen_from_keys(data, ["TEAM", s_key, y_key, "SPECIAL"]):
                words.add(w)

    for addr_key in ["ADDRESS"]:
        for w in gen_from_keys(data, [addr_key]):
            words.add(w)
        for w in gen_from_keys(data, [addr_key, "SPECIAL"]):
            words.add(w)
        for w in gen_from_keys(data, [addr_key, "SPECIAL", "SPECIAL"]):
            words.add(w)
        for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
            for pattern in ([addr_key, y_key],
                            [addr_key, y_key, "SPECIAL"]):
                for w in gen_from_keys(data, pattern):
                    words.add(w)
        for s_key in ["SEASON_CURRENT", "SEASON_PAST"]:
            for pattern in ([addr_key, s_key],
                            [addr_key, s_key, "YEAR_CURRENT"],
                            [addr_key, s_key, "YEAR_CURRENT", "SPECIAL"]):
                for w in gen_from_keys(data, pattern):
                    words.add(w)

    for col_key in ["COLLEGE"]:
        for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
            for w in gen_from_keys(data, [col_key, y_key]):
                words.add(w)
            for w in gen_from_keys(data, [col_key, y_key, "SPECIAL"]):
                words.add(w)
        for w in gen_from_keys(data, [col_key, "SPECIAL"]):
            words.add(w)
        for s_key in ["SEASON_CURRENT", "SEASON_PAST"]:
            for w in gen_from_keys(data, [col_key, s_key, "YEAR_CURRENT", "SPECIAL"]):
                words.add(w)

    for user_key in ["USER"]:
        for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
            for w in gen_from_keys(data, [user_key, y_key]):
                words.add(w)
            for w in gen_from_keys(data, [user_key, y_key, "SPECIAL"]):
                words.add(w)
        for w in gen_from_keys(data, [user_key, "SPECIAL"]):
            words.add(w)
        for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
            for w in gen_from_keys(data, [y_key, user_key, "SPECIAL"]):
                words.add(w)
        for s_key in ["SEASON_CURRENT", "SEASON_PAST"]:
            for w in gen_from_keys(data, [s_key, user_key, "SPECIAL"]):
                words.add(w)

    for comp_key in ["COMPANY"]:
        for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
            for w in gen_from_keys(data, [comp_key, y_key]):
                words.add(w)
            for w in gen_from_keys(data, [comp_key, y_key, "SPECIAL"]):
                words.add(w)
        for w in gen_from_keys(data, [comp_key, "SPECIAL"]):
            words.add(w)
        for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
            for w in gen_from_keys(data, [y_key, comp_key, "SPECIAL"]):
                words.add(w)
        for s_key in ["SEASON_CURRENT", "SEASON_PAST"]:
            for w in gen_from_keys(data, [s_key, comp_key, "YEAR_CURRENT", "SPECIAL"]):
                words.add(w)
            for w in gen_from_keys(data, [comp_key, s_key, "YEAR_CURRENT", "SPECIAL"]):
                words.add(w)

    strong_keys = ["SEASON_CURRENT", "SEASON_PAST", "YEAR_CURRENT", "YEAR_PAST",
                   "TEAM", "ADDRESS", "COLLEGE", "USER", "COMPANY"]
    for i, a in enumerate(strong_keys):
        for j, b in enumerate(strong_keys):
            if i == j:
                continue
            for pattern in ([a, b], [a, b, "SPECIAL"], [a, b, "YEAR_CURRENT"], [a, b, "YEAR_CURRENT", "SPECIAL"]):
                for w in gen_from_keys(data, pattern):
                    words.add(w)

    extra_keys = ["TEAM", "ADDRESS", "COLLEGE", "USER", "COMPANY"]
    for x in extra_keys:
        for pattern in ([x, "SEASON_CURRENT", "YEAR_CURRENT"],
                        [x, "SEASON_CURRENT", "YEAR_CURRENT", "SPECIAL"],
                        ["SEASON_CURRENT", "YEAR_CURRENT", x],
                        ["SEASON_CURRENT", "YEAR_CURRENT", x, "SPECIAL"],
                        [x, "SEASON_PAST", "YEAR_PAST", "SPECIAL"],
                        ["SEASON_CURRENT", x, "YEAR_CURRENT", "SPECIAL"],
                        ["SEASON_PAST", x, "YEAR_CURRENT", "SPECIAL"],
                        ["SEASON_CURRENT", x, "YEAR_PAST", "SPECIAL"],
                        ["SEASON_PAST", x, "YEAR_PAST", "SPECIAL"]):
            for w in gen_from_keys(data, pattern):
                words.add(w)

    for x in extra_keys:
        for pattern in ([x, "SEASON_CURRENT", "YEAR_CURRENT", "SPECIAL"],
                        [x, "SEASON_PAST", "YEAR_CURRENT", "SPECIAL"],
                        [x, "SEASON_CURRENT", "YEAR_PAST", "SPECIAL"],
                        [x, "SEASON_PAST", "YEAR_PAST", "SPECIAL"]):
            for w in gen_from_keys(data, pattern):
                words.add(w)

    for i, x in enumerate(extra_keys):
        for j, y in enumerate(extra_keys):
            if i == j:
                continue
            for pattern in ([x, y, "YEAR_CURRENT", "SPECIAL"],
                            [x, y, "YEAR_PAST", "SPECIAL"],
                            ["SEASON_CURRENT", x, y, "YEAR_CURRENT", "SPECIAL"],
                            ["SEASON_PAST", x, y, "YEAR_CURRENT", "SPECIAL"]):
                for w in gen_from_keys(data, pattern):
                    words.add(w)

    seps = ["", "_", ".", "-"]
    base_for_seps = []
    for s_key in ["SEASON_CURRENT", "SEASON_PAST"]:
        for y_key in ["YEAR_CURRENT", "YEAR_PAST"]:
            base_for_seps.append((s_key, y_key))
    for s_key, y_key in base_for_seps:
        for sep in seps:
            for w in gen_from_keys(data, [s_key, y_key]):
                for sp in data.get("SPECIAL", [""]):
                    words.add(w + sep + sp)

    return words

def apply_len_filters(words, min_len=None, max_len=None):
    if min_len is None and max_len is None:
        return words
    out = set()
    for w in words:
        lw = len(w)
        if min_len is not None and lw < min_len:
            continue
        if max_len is not None and lw > max_len:
            continue
        out.add(w)
    return out

def validate_lengths(min_len, max_len):
    if min_len is not None and min_len < 0:
        print("min length must be 0 or higher.")
        raise SystemExit(2)
    if max_len is not None and max_len < 0:
        print("max length must be 0 or higher.")
        raise SystemExit(2)
    if min_len is not None and max_len is not None and min_len > max_len:
        print("min length cannot be greater than max length.")
        raise SystemExit(2)

def write_wordlist(path, ordered):
    while True:
        try:
            with open(path, "w", encoding="utf8") as f:
                for w in ordered:
                    f.write(w + "\n")
            return path
        except OSError as e:
            print(f"Could not write file: {e}")
            if not ask_yes("Try a different output filename? [Y/n]: ", default=True):
                raise SystemExit(1)
            path = safe_input("Output filename [wordlist.txt]: ").strip() or "wordlist.txt"

def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("-o", "--output", default="wordlist.txt")
    ap.add_argument("--no-banner", action="store_true")
    ap.add_argument("--min-len", type=int, default=None)
    ap.add_argument("--max-len", type=int, default=None)
    args = ap.parse_args()

    validate_lengths(args.min_len, args.max_len)

    if not args.no_banner:
        print(BANNER.strip("\n"))

    print("Smart wordlist generator for authorised testing only.")
    print()

    data = {}

    current_year = str(datetime.now().year)
    yc = ask_list(f"Current year variants (default {current_year}): ", default=[current_year])
    yp = ask_list("Previous year variants (optional, comma separated): ")
    data["YEAR_CURRENT"] = expand_years(yc)
    data["YEAR_PAST"] = expand_years(yp)

    print()
    sc = ask_list("Current season words (comma separated, example: Summer): ")
    sp = ask_list("Past season words (comma separated): ")
    data["SEASON_CURRENT"] = expand_tokens(sc)
    data["SEASON_PAST"] = expand_tokens(sp)

    print()
    specials = ask_list("Special suffixes or fragments (comma separated, example: !,1,01,123): ")
    if not specials:
        specials = ["!", "1"]
    data["SPECIAL"] = specials

    print()
    team = ask_list("Team or club names (comma separated): ")
    address = ask_list("Address or street fragments (comma separated): ")
    college = ask_list("College or uni codes (comma separated): ")
    user = ask_list("User related words or names (comma separated): ")
    company = ask_list("Company name variants (comma separated): ")

    data["TEAM"] = expand_tokens(team)
    data["ADDRESS"] = expand_tokens(address)
    data["COLLEGE"] = expand_tokens(college)
    data["USER"] = expand_tokens(user)
    data["COMPANY"] = expand_tokens(company)

    words = build_wordlist(data)
    words = apply_len_filters(words, args.min_len, args.max_len)
    ordered = sorted(words)

    print()
    print(f"Candidates: {len(ordered)}")
    if not ordered:
        print("Nothing generated. Fill at least one of these: team, address, college, user, company, seasons, years.")
        raise SystemExit(0)

    n = min(12, len(ordered))
    print(f"Preview (first {n}):")
    for w in ordered[:n]:
        print(w)
    print()

    if not ask_yes(f"Write to file '{args.output}'? [Y/n]: ", default=True):
        print("Cancelled.")
        return

    out_path = write_wordlist(args.output, ordered)
    print(f"Saved {len(ordered)} entries into {out_path}")

if __name__ == "__main__":
    main()
