#!/usr/bin/env python3
"""zogful-analyzer — score takes on the zogfulness scale 0-420."""

import re
import sys
import random
from dataclasses import dataclass, field

# curated from too many hours of the commentary cabal
CABAL_LEXICON = {
    # core zogful triggers
    "zogful": 69,
    "zog": 42,
    "goyim": 33,
    "goy": 33,
    "cuking": 100,
    "retvrn": 50,
    "based": 25,
    "redpilled": 40,
    "blackpilled": 60,
    "schizo": 30,
    "schizopill": 70,
    # commentary cabal
    "deorio": 25,
    "de orio": 25,
    "chud logic": 35,
    "chudlogic": 35,
    "kuihman": 20,
    "turkey tom": 20,
    "augierfc": 20,
    "augie": 15,
    # streaming politics
    "destiny": 5,
    "dgg": 10,
    "dgger": 15,
    "hasan": 5,
    "piker": 10,
    "asmongold": 5,
    "asmongold": 5,
    "ethan klein": 5,
    "ethan": 5,
    "hila": 10,
    # drama moves
    "sweeping": 35,
    "crashout": 40,
    "crashing out": 40,
    "vc me": 50,
    "come vc": 50,
    "debate me": 45,
    "ducking": 30,
    "dodging": 30,
    "mogging": 35,
    "mog": 30,
    "swept": 25,
    "lolcow": 40,
    "lolcowed": 60,
    # misc slop
    "slop": 25,
    "slop farming": 45,
    "slopfarming": 45,
    "gooning": 30,
    "goon": 25,
    "goon cave": 45,
    "rizz": 20,
    "no rizz": 35,
    "cuck": 25,
    "cucked": 45,
    "libtard": 30,
    "retard": 30,
    "low iq": 35,
    "lowiq": 35,
    "dunce": 20,
    "brainrot": 25,
    "brain rot": 25,
    "full retard": 60,
    "podcast": 5,
    "stream": 5,
    "twitch": 5,
    "twitter": 5,
    "tweet": 10,
    "poast": 20,
    "post": 5,
    "based and redpilled": 80,
    "cope": 25,
    "seethe": 30,
    "cope and seethe": 70,
}

CABAL_QUADRANTS = [
    "dgg quadrant (destiny-aligned, priors locked)",
    "hasan quadrant (the dems are persecuting me)",
    "asmongold quadrant (the devs are lazy and entitled)",
    "ethan quadrant (hila look at this meme)",
    "turkey tom quadrant (anti-dgg, pro-chaos)",
    "kuihman quadrant (sweeping the basement as we speak)",
    "augierfc quadrant (whitford monologues)",
    "deorio quadrant (operant conditioning arc)",
    "chud logic quadrant (full retard confirmed)",
    "schizo quadrant (no priors, terminally based)",
    "true neutral (you barely post, suspicious)",
]

LOLCOW_RISK_THRESHOLDS = [
    (0, 100, "low — you are safe for now"),
    (100, 250, "moderate — one bad clip away from a sweep"),
    (250, 380, "HIGH — kuihman is already typing"),
    (380, 420, "TERMINAL — you will be turned into a lolcow by morning"),
]


@dataclass
class ZogSnapshot:
    raw: str
    zogfulness: int
    quadrant: str
    lolcow_risk: str
    slop_probability: float
    rizz_rating: int
    gooning_detected: bool
    matched_tokens: list = field(default_factory=list)


def normalize(text: str) -> str:
    return text.lower().strip()


def score_text(text: str) -> ZogSnapshot:
    norm = normalize(text)
    tokens = re.findall(r"[a-zA-Z][a-zA-Z\s\-]*", norm)
    matched = []
    score = 0

    # bigram-aware matching for multi-word tokens like "turkey tom"
    for phrase, weight in CABAL_LEXICON.items():
        if phrase in norm:
            score += weight
            matched.append((phrase, weight))

    # bonus for length and terminally online cadence
    if len(text) > 280:
        score += 10
    if text.count("!") > 2:
        score += 15
    if text.count("🚨") + text.count("💀") + text.count("😭") > 0:
        score += 20

    # clamp 0–420
    score = max(0, min(420, score))

    quadrant = random.choice(CABAL_QUADRANTS)

    lolcow_risk = "unknown"
    for lo, hi, label in LOLCOW_RISK_THRESHOLDS:
        if lo <= score < hi:
            lolcow_risk = f"{label} (score {lo}-{hi})"
            break
    if score >= 420:
        lolcow_risk = "TERMINAL — you will be turned into a lolcow by morning (420 club)"

    slop_prob = round(min(1.0, score / 420 + random.uniform(-0.05, 0.05)), 3)
    rizz = random.randint(-50, 50) - (score // 12)
    gooning = any(t in norm for t in ["goon", "gooning", "goon cave"])

    return ZogSnapshot(
        raw=text,
        zogfulness=score,
        quadrant=quadrant,
        lolcow_risk=lolcow_risk,
        slop_probability=slop_prob,
        rizz_rating=rizz,
        gooning_detected=gooning,
        matched_tokens=matched,
    )


def render(snap: ZogSnapshot) -> str:
    bars = "█" * (snap.zogfulness // 20) + "░" * (21 - (snap.zogfulness // 20))
    crown = " 👑 ZOG MAX" if snap.zogfulness >= 400 else ""
    return f"""zogfulness:       {snap.zogfulness:>3} / 420 [{bars}]{crown}
cabal alignment:  {snap.quadrant}
lolcow risk:      {snap.lolcow_risk}
slop probability: {snap.slop_probability * 100:.1f}%  💅
rizz rating:       {snap.rizz_rating:+d} ({"net positive, mogging" if snap.rizz_rating > 0 else "net negative, get off chat"})
gooning detected: {"YES — put the phone down 🚨" if snap.gooning_detected else "no (suspicious, verified human?)"}
tokens hit:       {len(snap.matched_tokens)} (top: {", ".join(t for t,_ in snap.matched_tokens[:5]) or "none"})
"""


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: python main.py <take-to-rate>")
        print('try: python main.py "turkey tom would mog destiny in a vc its not even close"')
        return 1

    take = " ".join(argv[1:])
    snap = score_text(take)
    print(render(snap))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
