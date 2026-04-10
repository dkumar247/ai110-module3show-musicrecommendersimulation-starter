from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Scoring mode strategies: each entry defines weights for genre, mood, energy
# ---------------------------------------------------------------------------
SCORING_MODES: Dict[str, Dict[str, float]] = {
    "genre-first":    {"genre_w": 2.0, "mood_w": 1.0, "energy_w": 1.0},
    "mood-first":     {"genre_w": 1.0, "mood_w": 2.0, "energy_w": 1.0},
    "energy-focused": {"genre_w": 1.0, "mood_w": 0.5, "energy_w": 2.0},
}


# ---------------------------------------------------------------------------
# Data classes (used by tests/test_recommender.py)
# ---------------------------------------------------------------------------

@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    # Advanced features (optional; have defaults for backward-compat with tests)
    popularity: int = 50
    release_decade: int = 2020
    mood_tags: str = ""


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Optional advanced preferences
    mode: str = "genre-first"
    target_popularity: Optional[int] = None
    preferred_decade: Optional[int] = None
    target_mood_tags: Optional[List[str]] = None


class Recommender:
    """OOP recommendation engine; required by tests/test_recommender.py."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score and rank all songs for the given user profile; return top k."""
        user_dict = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood":  user.favorite_mood,
            "target_energy":  user.target_energy,
        }
        if user.target_popularity is not None:
            user_dict["target_popularity"] = user.target_popularity
        if user.preferred_decade is not None:
            user_dict["preferred_decade"] = user.preferred_decade
        if user.target_mood_tags is not None:
            user_dict["target_mood_tags"] = user.target_mood_tags

        scored = []
        for song in self.songs:
            song_dict = {
                "id":             song.id,
                "genre":          song.genre,
                "mood":           song.mood,
                "energy":         song.energy,
                "popularity":     song.popularity,
                "release_decade": song.release_decade,
                "mood_tags":      song.mood_tags,
            }
            song_score, _ = score_song(user_dict, song_dict, mode=user.mode)
            scored.append((song, song_score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song was recommended."""
        user_dict = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood":  user.favorite_mood,
            "target_energy":  user.target_energy,
        }
        song_dict = {
            "id":             song.id,
            "genre":          song.genre,
            "mood":           song.mood,
            "energy":         song.energy,
            "popularity":     song.popularity,
            "release_decade": song.release_decade,
            "mood_tags":      song.mood_tags,
        }
        _, reasons = score_song(user_dict, song_dict, mode=user.mode)
        return ", ".join(reasons)


# ---------------------------------------------------------------------------
# Functional API (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting numeric fields to the correct types."""
    import csv

    int_fields   = {"id", "popularity", "release_decade"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field_name in int_fields:
                if field_name in row:
                    row[field_name] = int(row[field_name])
            for field_name in float_fields:
                if field_name in row:
                    row[field_name] = float(row[field_name])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(
    user_prefs: Dict,
    song: Dict,
    mode: str = "genre-first",
) -> Tuple[float, List[str]]:
    """Score a single song against user preferences using the chosen scoring mode.

    Returns (total_score, reasons_list).
    Base scoring (genre, mood, energy) uses weights from SCORING_MODES.
    Advanced features (popularity, decade, mood tags) add bonus points on top.
    """
    weights = SCORING_MODES.get(mode, SCORING_MODES["genre-first"])
    score   = 0.0
    reasons: List[str] = []

    # --- Core scoring ---------------------------------------------------------

    genre_w = weights["genre_w"]
    if song["genre"] == user_prefs["favorite_genre"]:
        score += genre_w
        reasons.append(f"genre match (+{genre_w:.1f})")

    mood_w = weights["mood_w"]
    if song["mood"] == user_prefs["favorite_mood"]:
        score += mood_w
        reasons.append(f"mood match (+{mood_w:.1f})")

    energy_w     = weights["energy_w"]
    energy_score = energy_w * (1.0 - abs(song["energy"] - user_prefs["target_energy"]))
    score        += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    # --- Advanced features (Challenge 1) --------------------------------------

    # Popularity proximity: rewards songs whose popularity is close to the target.
    # Max +0.5 when popularity matches exactly.
    if "target_popularity" in user_prefs and "popularity" in song:
        pop_score = 0.5 * (1.0 - abs(song["popularity"] / 100.0 - user_prefs["target_popularity"] / 100.0))
        score += pop_score
        reasons.append(f"popularity proximity (+{pop_score:.2f})")

    # Release decade match: +0.5 for an exact decade match.
    if "preferred_decade" in user_prefs and "release_decade" in song:
        if song["release_decade"] == user_prefs["preferred_decade"]:
            score += 0.5
            reasons.append("decade match (+0.50)")

    # Mood tag overlap: +0.5 per matching tag, capped at +1.5.
    if "target_mood_tags" in user_prefs and song.get("mood_tags"):
        song_tags   = set(song["mood_tags"].split("|"))
        target_tags = set(user_prefs["target_mood_tags"])
        matches     = song_tags & target_tags
        if matches:
            tag_score = min(len(matches) * 0.5, 1.5)
            score     += tag_score
            reasons.append(f"mood tags {sorted(matches)} (+{tag_score:.2f})")

    return (score, reasons)


def apply_diversity_penalty(
    scored_songs: List[Tuple[Dict, float, List[str]]],
    penalty: float = 0.5,
) -> List[Tuple[Dict, float, List[str]]]:
    """Re-rank a pre-scored list so repeated artist or genre incurs a penalty.

    Uses a greedy selection loop: pick the best available song, record its
    artist and genre as "seen," then subtract `penalty` from any future
    candidate whose artist or genre already appears in the selected set.
    """
    selected: List[Tuple[Dict, float, List[str]]] = []
    remaining = list(scored_songs)
    seen_artists: set = set()
    seen_genres:  set = set()

    while remaining:
        candidates = []
        for song, base_score, reasons in remaining:
            adj_score   = base_score
            adj_reasons = list(reasons)
            if song["artist"] in seen_artists:
                adj_score -= penalty
                adj_reasons.append(f"artist repeat (-{penalty:.1f})")
            if song["genre"] in seen_genres:
                adj_score -= penalty
                adj_reasons.append(f"genre repeat (-{penalty:.1f})")
            candidates.append((song, adj_score, adj_reasons))

        candidates.sort(key=lambda x: x[1], reverse=True)
        winner = candidates[0]
        selected.append(winner)

        # Remove winner from remaining by song id
        winner_id = winner[0]["id"]
        remaining = [r for r in remaining if r[0]["id"] != winner_id]

        seen_artists.add(winner[0]["artist"])
        seen_genres.add(winner[0]["genre"])

    return selected


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "genre-first",
    diversity: bool = False,
) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song, optionally re-rank with diversity penalty, return top k.

    Each result is a tuple of (song_dict, score, reasons_list).
    Set diversity=True to prevent the same artist or genre from dominating.
    Choose mode from: 'genre-first', 'mood-first', 'energy-focused'.
    """
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song, mode=mode)
        scored.append((song, song_score, reasons))

    scored.sort(key=lambda x: x[1], reverse=True)

    if diversity:
        scored = apply_diversity_penalty(scored)

    return scored[:k]
