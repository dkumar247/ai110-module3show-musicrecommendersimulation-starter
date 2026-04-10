"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Default user profile: Pop / Happy listener
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    print(f"\nProfile: genre={user_prefs['favorite_genre']}  "
          f"mood={user_prefs['favorite_mood']}  "
          f"energy={user_prefs['target_energy']}")
    print("=" * 50)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop 5 Recommendations:\n")
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} — {song['artist']} [{song['genre']} / {song['mood']}]")
        print(f"     Score: {score:.2f}  |  Reasons: {', '.join(reasons)}")
        print()


if __name__ == "__main__":
    main()
