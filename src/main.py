"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

PROFILES = [
    {
        "label": "High-Energy Pop",
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
    },
    {
        "label": "Chill Lofi",
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.3,
    },
    {
        "label": "Deep Intense Rock",
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.8,
    },
    {
        "label": "Adversarial — High-Energy Sad R&B",
        "favorite_genre": "r&b",
        "favorite_mood": "sad",
        "target_energy": 0.9,
    },
]


def run_profile(songs, user_prefs, k=5):
    """Print top-k recommendations for a single profile."""
    label = user_prefs.get("label", "Unnamed Profile")
    print(f"\n{'=' * 54}")
    print(f"  Profile: {label}")
    print(f"  genre={user_prefs['favorite_genre']}  "
          f"mood={user_prefs['favorite_mood']}  "
          f"energy={user_prefs['target_energy']}")
    print(f"{'=' * 54}")

    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n  Top {k} Recommendations:\n")
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     [{song['genre']} / {song['mood']}]  Score: {score:.2f}")
        print(f"     Why: {', '.join(reasons)}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    for profile in PROFILES:
        run_profile(songs, profile, k=5)


if __name__ == "__main__":
    main()
