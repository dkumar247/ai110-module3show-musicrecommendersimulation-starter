# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

A content-based music recommender that matches songs to a user's stated genre, mood, and energy preferences using a simple weighted scoring formula.

---

## 2. Intended Use

VibeFinder 1.0 is designed for classroom exploration of how recommendation systems work. It takes a user profile (a preferred genre, mood, and energy level) and returns the top 5 most relevant songs from a small catalog. It is **not** intended for use in a real product or with real users. It makes no attempt to learn from listening behavior, skip history, or feedback. Every recommendation is based entirely on the labels and numbers stored in a CSV file — the system has no understanding of what a song actually sounds like.

**Not intended for:** deployment in any real application, making decisions about what music is "good," or representing the preferences of any real person.

---

## 3. How the Model Works

Think of VibeFinder like a very literal matchmaker. You tell it three things: what genre you like, what mood you are in, and how high-energy you want the music to feel. It then goes through every song in its catalog, one at a time, and gives each song a score based on how well it matches those three things.

- If the song's genre matches your favorite genre, it earns **2 bonus points**. Genre gets the most weight because it is the strongest signal of musical taste.
- If the song's mood matches your preferred mood, it earns **1 bonus point**.
- Every song also earns a **proximity score for energy**, between 0 and 1. A song whose energy perfectly matches your target scores 1.0. A song whose energy is completely opposite scores close to 0. This score is calculated by taking 1 minus the gap between the song's energy and your target energy.

The three scores are added together. The maximum a song can earn is 4.0 (genre match + mood match + perfect energy). All songs are then sorted from highest to lowest, and the top 5 are returned along with the specific reasons why each one ranked where it did.

Three optional advanced features can further adjust the score:

- **Popularity proximity** — rewards songs whose mainstream popularity score is close to the user's target (max +0.5).
- **Release decade match** — adds +0.5 if the song's decade matches the user's preferred decade.
- **Mood tag overlap** — awards +0.5 per matching detailed mood tag (e.g., "euphoric," "nostalgic," "aggressive"), capped at +1.5. This allows finer emotional matching beyond the broad mood category.

A **diversity penalty** is also available: when enabled, any song whose artist or genre already appears in the selected results loses 0.5 points, preventing one artist or genre from dominating the entire top-5 list.

---

## 4. Data

The catalog contains **18 songs** stored in `data/songs.csv`. The starter dataset had 10 songs; 8 more were added to broaden coverage. Each song has 13 attributes: `genre`, `mood`, `energy` (0.0–1.0), `tempo_bpm`, `valence` (0.0–1.0), `danceability` (0.0–1.0), `acousticness` (0.0–1.0), `popularity` (0–100), `release_decade`, and `mood_tags` (pipe-separated detailed descriptors such as "euphoric|upbeat|summery").

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, electronic, country, metal, hip-hop, blues.

**Moods represented:** happy, chill, intense, relaxed, focused, moody, sad, energetic, nostalgic, angry, romantic, uplifting, melancholic, groovy.

**Limitations of the data:** The catalog is tiny. Three lofi songs are included but only one rock song, which means lofi listeners get more tailored results than rock listeners. The songs are fictional and their attributes were assigned manually, not measured from real audio. The dataset likely reflects the taste assumptions of whoever created it — biased toward Western genres and English-language pop conventions.

---

## 5. Strengths

VibeFinder works best when the user's preferences are clearly represented in the catalog. In testing, the "perfect match" song (matching genre + mood + energy) ranked #1 for every profile tested, with a score well above the second-place result. This shows the scoring logic is functioning correctly and is easy to understand — each result comes with plain-language reasons that explain exactly why a song ranked where it did.

The system is also completely **transparent**. Unlike a neural network that produces a recommendation with no explanation, VibeFinder can always tell you the math behind every result. For a classroom context where the goal is to understand how recommenders work, that transparency is a genuine advantage. It is also fast: scoring all 18 songs takes a fraction of a second with no external dependencies.

---

## 6. Limitations and Bias

The most significant bias in this system is **genre dominance**: a genre match is worth +2.0 points while a mood match is only worth +1.0, meaning a song that shares the user's genre but has a completely wrong mood or mismatched energy will almost always outrank a song from a different genre that is a far better emotional fit. This creates a "genre bubble" — the user never encounters great songs outside their stated preference, even if those songs would feel identical to listen to. A second limitation is **catalog imbalance**: the dataset has 3 lofi songs and only 1 rock song, so a lofi listener gets more varied top results than a rock listener purely because the genre is better represented. Third, genre and mood are matched as **exact strings**, meaning "indie pop" gets zero credit toward a "pop" preference even though these genres heavily overlap — a subtlety the system cannot express. Finally, numerically rich fields like `valence`, `danceability`, `acousticness`, and `tempo_bpm` are **completely ignored** by the scoring formula, so a high-valence, danceable track scores identically to a slow, somber one as long as their energy values are the same.

---

## 7. Evaluation

Four user profiles were tested: **High-Energy Pop** (genre=pop, mood=happy, energy=0.9), **Chill Lofi** (genre=lofi, mood=chill, energy=0.3), **Deep Intense Rock** (genre=rock, mood=intense, energy=0.8), and an **Adversarial profile** (genre=r&b, mood=sad, energy=0.9) designed to expose contradictions between genre and mood. In every case the correct "perfect match" song ranked #1 with a score near 4.0, which confirmed the scoring logic works as intended. The most interesting surprise was in the **Adversarial profile**: even though "sad" and "energy=0.9" feel like contradictory preferences (sad songs are usually slow and low-energy), the system still produced a reasonable #1 result — "Rainy Days & Neon Signs" (r&b/sad) — because genre and mood matched despite the energy gap penalty. A **weight experiment** was also run that doubled the energy weight and halved the genre weight: this caused "Spacewalk Thoughts" (ambient/chill, energy=0.28) to jump past "Focus Flow" (lofi/focused) in the Chill Lofi list, which arguably felt more accurate for a vibe-based listener. The experiment confirmed that the current genre-heavy weights favour genre loyalty over emotional fit, and that re-weighting can surface better results for users who define their taste by feeling rather than category.

---

## 8. Future Work

**1. Score valence, danceability, and acousticness.** These fields are already in the CSV but the base scoring formula ignores them. Adding proximity scoring for valence (musical positiveness) would make "happy" vs "sad" preferences far more precise — right now two songs with the same energy score identically even if one is bright and uplifting and the other is dark and heavy.

**2. Replace exact string matching with fuzzy or hierarchical genre matching.** Right now, "indie pop" and "pop" are treated as completely different genres. A simple lookup table that groups related genres together (e.g., pop, indie pop, and synth-pop all belong to the "pop family") would dramatically reduce the binary-matching problem and surface more relevant results for edge-case genre preferences.

**3. Simulate collaborative filtering alongside content-based scoring.** The current system is entirely blind to what other users enjoy. Building a second recommender that says "users who liked X also liked Y" — even with synthetic data — would allow direct comparison of the two approaches and show how collaborative filtering surfaces songs that content-based scoring can never find on its own.

---

## 9. Personal Reflection

The biggest learning moment in this project was realizing how much a single design decision — the genre weight being 2.0 instead of 1.0 — shapes every result the system produces. It feels like a small number, but it means genre is twice as powerful as mood in every scoring calculation. That's a value judgment baked into the math, and the system never tells the user that it's there. Real recommendation engines have hundreds of weights like this, tuned through experimentation and sometimes reinforcing biases that nobody intended.

What surprised me most was how convincing the results felt even with such simple logic. When the High-Energy Pop profile returned "Sunrise City" at #1 with a score of 3.92, it genuinely seemed like a smart recommendation — and in a sense it was, because the scoring logic was doing exactly what it was designed to do. But there was no understanding behind it. The system doesn't know what pop music sounds like. It just pattern-matched three labels and added up some numbers. That gap between "feels right" and "actually understands" is probably the most important thing I'll take away from this project when I think about real AI systems.

I'd want to try collaborative filtering next — specifically, simulating what happens when two users with overlapping but not identical profiles share data. The content-based approach here is entirely blind to what other listeners enjoy. A hybrid system that says "users who liked X also liked Y" could surface songs the content-based model would never consider, and comparing the two outputs would be a much more interesting experiment.
