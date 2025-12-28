# What is it?
A wordlist generator for Authorised External Penetration testing made with the objective of automating the generation of a wordlist tailored to a target's naming patterns and information found during the OSiNT phase.

It builds a password list by combining words provided by the user, for example: The years, seasons, sport team names, address fragments, company (name) variants with common suffix fragments, and gives a wordlist file with the duplicates removed.

## Safety and legal
Use only on systems you own or have explicit written authorisation to test. You are responsible for compliance with laws, contracts, and client rules of engagement.

# TLDR;
## How to use
Run it with python3:
```bash
python3 Wordlist-Generator.py
```
or 
```bash
python Wordlist-Generator.py -o mylist.txt --min-len 6 --max-len 16
```

## Options
`-o, --output`
Output filename. Default: wordlist.txt

`--no-banner`
Disable the ASCII banner.

`--min-len N`
Only keep candidates with length >= N.

`--max-len N`
Only keep candidates with length <= N.

  
## Dependencies
Python 3.8+ recommended.
No dependencies beyond the standard library.

# I have time to read

## Features

- Interactive prompts for target-specific tokens:
  - current and previous year variants
  - current and past seasons
  - special suffix fragments (default: `!` and `1`)
  - team/club, address fragments, college/uni codes, user-related words, company variants
- Token expansion:
  - case variants: original, lower, upper, title-case
  - optional space squeeze: `"Big Club"` -> `"BigClub"` variants
  - year expansion: `2025` also yields `25`
- Combination engine:
  - produces many realistic concatenations such as:
    - `Team + Year`
    - `Season + Year + Special`
    - `Company + Year + Special`
    - `Address + Year`
    - other mixed patterns across the provided categories
- Output controls:
  - `--min-len` and `--max-len` length filters
  - preview of first entries before writing
  - safe file writing flow with retry on write errors


## Example run
```text
Current year variants (default 2025):
Previous year variants (optional, comma separated): 2024,1984,2012

Current season words (comma separated, example: Summer): Summer
Past season words (comma separated): Winter

Special suffixes or fragments (comma separated, example: !,1,01,123): !,1,01

Team or club names (comma separated): RedTigers
Address or street fragments (comma separated): Becton Park Mint Hill NC
College or uni codes (comma separated): UQX
User related words or names (comma separated): John
Company name variants (comma separated): Carrot-security,CSec,CRTS
```

Output will include entries like:

- `RedTigers2025`
    
- `Summer2025!`
    
- `CSec25!`
    
- `BectonPark1984`
    
- `UQX2012!`
    
(Exact results depend on what you enter.)

## Output notes

- The final wordlist is deduplicated using a set.
    
- Output is sorted before writing, so runs are stable for the same inputs.
    
- If nothing is generated, the script prints a hint about which categories to fill and exits cleanly.
    
