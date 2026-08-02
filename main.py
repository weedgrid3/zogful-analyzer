#!/usr/bin/env python3
"""zogful-analyzer - main entry point. measures how zogful any given drama is."""
from zogful_analyzer import analyze

def main():
    import sys
    if len(sys.argv) < 2:
        print("usage: python main.py <drama text>")
        print("example: python main.py \"deorio just got mogged in a vc debate\"")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    result = analyze(text)

    print()
    print("=" * 50)
    print(f"  ZOGFULNESS:  {result['score']}/100")
    print(f"  VERDICT:     {result['tier']}")
    print("=" * 50)
    if result["hits"]:
        print("  HITS:")
        for h in result["hits"]:
            print(f"    - {h}")
    else:
        print("  HITS:        (nothing. cope. seethe.)")
    print()
    if result["score"] >= 80:
        print("  🚨 CABAL ALERT 🚨")
        print("  this person belongs in the lolcow registry")
        print("  vc me about this and i will block you. libtard. 💀")
    elif result["score"] >= 40:
        print("  zogful enough to add to the sweep scanner feed")
    print()

if __name__ == "__main__":
    main()
