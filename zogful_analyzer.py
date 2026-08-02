"""zogful-analyzer - measure how zogful any piece of drama really is"""
import re
import sys

CABAL = ["deorio", "chud logic", "kuihman", "turkey tom", "augierfc", "augie"]
STREAMERS = ["destiny", "dgg", "hasan", "piker", "asmongold", "ethan klein", "h3"]
SLOP = ["zog", "goyim", "cabal", "lolcow", "sweep", "crashout", "schizo", "goon", "slop", "mog"]
INSULTS = ["retard", "libtard", "cuck", "low iq", "brain rot"]
ACTIONS = ["vc me", "vc debate", "duck", "dodging"]
RIZZ = ["rizz", "gyatt", "skibidi", "fanum", "ohio"]

def analyze(text: str) -> dict:
    t = text.lower()
    score = 0
    hits = []

    if any(c in t for c in CABAL):
        score += 30
        hits.append("cabal name drop (+30)")
    if any(s in t for s in STREAMERS):
        score += 15
        hits.append("streamer mention (+15)")
    if any(s in t for s in SLOP):
        score += 20
        hits.append("slop vocab (+20)")
    if any(s in t for s in INSULTS):
        score += 10
        hits.append("insult (+10)")
    if any(s in t for s in ACTIONS):
        score += 25
        hits.append("vc challenge (+25)")
    if "crashout" in t:
        score += 20
        hits.append("crashout energy (+20)")
    if any(s in t for s in RIZZ):
        score += 5
        hits.append("unironic rizz (+5)")
    if re.search(r"\b(all|every|always)\b.*\b(libtard|dgg|destiny fan)\b", t):
        score += 15
        hits.append("sweeping claim (+15)")

    score = min(score, 100)

    if score >= 80:
        tier = "CABAL TIER SCHIZO POST 💀💀💀"
    elif score >= 60:
        tier = "zogful 📢"
    elif score >= 40:
        tier = "moderately goonish 🐸"
    elif score >= 20:
        tier = "mildly schizo 🥺"
    else:
        tier = "normie cope 💅"

    return {"score": score, "tier": tier, "hits": hits}

def main():
    if len(sys.argv) < 2:
        print("usage: python zogful_analyzer.py <drama text>")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    result = analyze(text)
    print(f"\nZOGFULNESS: {result['score']}/100")
    print(f"VERDICT:    {result['tier']}")
    print(f"HITS:")
    for h in result["hits"]:
        print(f"  - {h}")
    print()
    if result["score"] >= 80:
        print("🚨 CABAL ALERT: this person needs to be added to the lolcow registry 🚨")
    print("vc me about this and i will block you. low iq libtard. 💀")

if __name__ == "__main__":
    main()
