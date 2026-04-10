"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main

Demonstrates all optional extensions:
  Challenge 1 — Advanced song features (popularity, decade, mood tags)
  Challenge 2 — Multiple scoring modes (genre-first | mood-first | energy-focused)
  Challenge 3 — Diversity penalty (artist / genre repeat = −0.5)
  Challenge 4 — Formatted table output via tabulate
"""

from tabulate import tabulate
from src.recommender import SCORING_MODES, load_songs, recommend_songs

# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

PROFILES = [
    {
        "label":            "High-Energy Pop",
        "favorite_genre":   "pop",
        "favorite_mood":    "happy",
        "target_energy":    0.9,
        "target_popularity": 75,
        "preferred_decade":  2020,
        "target_mood_tags":  ["euphoric", "upbeat", "pumped"],
    },
    {
        "label":            "Chill Lofi",
        "favorite_genre":   "lofi",
        "favorite_mood":    "chill",
        "target_energy":    0.3,
        "target_popularity": 60,
        "preferred_decade":  2020,
        "target_mood_tags":  ["mellow", "dreamy", "peaceful"],
    },
    {
        "label":            "Deep Intense Rock",
        "favorite_genre":   "rock",
        "favorite_mood":    "intense",
        "target_energy":    0.8,
        "target_popularity": 50,
        "preferred_decade":  2010,
        "target_mood_tags":  ["aggressive", "pumped", "driving"],
    },
    {
        "label":            "Adversarial — High-Energy Sad R&B",
        "favorite_genre":   "r&b",
        "favorite_mood":    "sad",
        "target_energy":    0.9,
        "target_popularity": 65,
        "preferred_decade":  2010,
        "target_mood_tags":  ["melancholic", "longing", "heartfelt"],
    },
]

# ---------------------------------------------------------------------------
# Display helper (Challenge 4)
# ---------------------------------------------------------------------------

def display_table(
    recommendations: list,
    mode: str = "genre-first",
    diversity: bool = False,
) -> None:
    """Print recommendations as a formatted table using tabulate."""
    mode_weights = SCORING_MODES.get(mode, SCORING_MODES["genre-first"])
    mode_label   = (
        f"{mode}  "
        f"(genre ×{mode_weights['genre_w']:.1f} | "
        f"mood ×{mode_weights['mood_w']:.1f} | "
        f"energy ×{mode_weights['energy_w']:.1f})"
    )
    diversity_label = "diversity ON  (repeat penalty −0.5)" if diversity else "diversity OFF"
    print(f"  Mode: {mode_label}   |   {diversity_label}\n")

    rows = []
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        reason_lines = "\n".join(f"• {r}" for r in reasons)
        rows.append([
            rank,
            song["title"],
            song["artist"],
            f"{song['genre']}\n{song['mood']}",
            f"{score:.2f}",
            reason_lines,
        ])

    headers = ["#", "Title", "Artist", "Genre / Mood", "Score", "Reasons"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print()


# ---------------------------------------------------------------------------
# Section printers
# ---------------------------------------------------------------------------

def section(title: str) -> None:
    """Print a visual section separator."""
    bar = "═" * 62
    print(f"\n{bar}")
    print(f"  {title}")
    print(f"{bar}\n")


def demo_scoring_modes(songs: list, profile: dict) -> None:
    """Challenge 2: run one profile through all three scoring modes."""
    section(f"SCORING MODE DEMO  ·  {profile['label']}")
    # Use a base profile without advanced features so mode differences are clear
    base = {k: v for k, v in profile.items() if k not in
            ("target_popularity", "preferred_decade", "target_mood_tags", "label")}
    for mode in SCORING_MODES:
        recs = recommend_songs(base, songs, k=5, mode=mode, diversity=False)
        display_table(recs, mode=mode, diversity=False)


def demo_diversity(songs: list, profile: dict) -> None:
    """Challenge 3: show the same profile with and without the diversity penalty."""
    section(f"DIVERSITY DEMO  ·  {profile['label']}  (genre-first)")
    base = {k: v for k, v in profile.items() if k not in ("label",)}

    print("  ── Without diversity penalty ──\n")
    recs_plain = recommend_songs(base, songs, k=5, mode="genre-first", diversity=False)
    display_table(recs_plain, mode="genre-first", diversity=False)

    print("  ── With diversity penalty ──\n")
    recs_div = recommend_songs(base, songs, k=5, mode="genre-first", diversity=True)
    display_table(recs_div, mode="genre-first", diversity=True)


def full_run(songs: list) -> None:
    """Run all 4 profiles with genre-first mode, diversity ON, and all advanced features."""
    section("FULL PROFILE RUNS  (genre-first | diversity ON | all features active)")
    for profile in PROFILES:
        label = profile["label"]
        prefs = {k: v for k, v in profile.items() if k != "label"}
        print(f"  ▶  {label}\n")
        recs = recommend_songs(prefs, songs, k=5, mode="genre-first", diversity=True)
        display_table(recs, mode="genre-first", diversity=True)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")

    # Challenge 2: scoring mode comparison (High-Energy Pop, no advanced features)
    demo_scoring_modes(songs, PROFILES[0])

    # Challenge 3: diversity effect (High-Energy Pop, all features)
    demo_diversity(songs, PROFILES[0])

    # Full run: all 4 profiles with every enhancement active
    full_run(songs)


if __name__ == "__main__":
    main()
