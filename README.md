# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation systems like Spotify or YouTube use two main strategies to predict what you'll enjoy. **Collaborative filtering** looks at patterns across many users — if people with similar listening history to yours also loved a particular song, the system suggests it to you too. **Content-based filtering** ignores other users entirely and instead analyzes the properties of songs you've already liked (tempo, genre, mood) to find new tracks that share those same qualities. Most production systems blend both approaches, but collaborative filtering requires massive amounts of user behavior data that we don't have in a classroom simulation.

Our version uses **pure content-based filtering**: it compares a user's stated taste preferences directly against each song's attributes to compute a relevance score, then ranks all songs from highest to lowest score and returns the top results. This approach is transparent and explainable — every recommendation comes with a reason tied to specific features — which makes it ideal for understanding the core mechanics of how recommenders work.

**Features used by the `Song` object:**

| Feature | Type | Description |
|---|---|---|
| `genre` | string | Musical genre (e.g., pop, lofi, rock, jazz) |
| `mood` | string | Emotional tone (e.g., happy, chill, intense, moody) |
| `energy` | float (0.0–1.0) | Perceived intensity and activity level |
| `tempo_bpm` | float | Beats per minute — pace of the track |
| `valence` | float (0.0–1.0) | Musical positiveness; higher = more upbeat |
| `danceability` | float (0.0–1.0) | How suitable the track is for dancing |
| `acousticness` | float (0.0–1.0) | Confidence that the track is acoustic |

**Features used by the `UserProfile` object:**

| Preference | Type | Description |
|---|---|---|
| `favorite_genre` | string | The genre the user most wants to hear |
| `favorite_mood` | string | The mood that best matches the user's current vibe |
| `target_energy` | float (0.0–1.0) | The energy level the user is looking for |
| `likes_acoustic` | bool | Whether the user prefers acoustic over electronic sounds |

The scoring logic awards points for exact matches on genre and mood, and calculates a proximity score for numerical features like energy — so a song doesn't need to be a perfect match to appear in results, just the closest available fit.

### Algorithm Recipe

Every song in the catalog is judged by the same three rules, and the results are added together into a single relevance score:

| Rule | Points | Logic |
|---|---|---|
| Genre match | +2.0 | `song.genre == user.favorite_genre` |
| Mood match | +1.0 | `song.mood == user.favorite_mood` |
| Energy proximity | 0.0 – 1.0 | `1.0 - abs(song.energy - user.target_energy)` |

**Why these weights?** Genre is the strongest signal of taste — a country fan and a metal fan rarely want the same song regardless of energy. Mood is secondary; two songs can share a genre but feel completely different emotionally. Energy is scored continuously so that songs close to the user's target are rewarded even if they don't hit it exactly.

**Maximum possible score: 4.0** (genre match + mood match + perfect energy alignment)

### Data Flow

```mermaid
flowchart TD
    A([User Preferences\ngenre · mood · target_energy]) --> B[Load songs.csv\ninto list of dicts]
    B --> C{For each song\nin catalog}
    C --> D[Score: genre match?\n+2.0 pts]
    C --> E[Score: mood match?\n+1.0 pt]
    C --> F[Score: energy proximity\n1.0 − abs gap]
    D --> G[Sum all points\n→ final score + reasons list]
    E --> G
    F --> G
    G --> C
    C --> H[Sort all scored songs\nhighest → lowest]
    H --> I([Top K Recommendations\nwith scores and reasons])
```

### Known Biases and Limitations

- **Genre dominance:** A genre match is worth twice as much as a mood match. Songs that share the user's genre will almost always outrank songs from other genres, even if those songs are a far better match in mood and energy. This can create a "genre bubble" where the user never sees great tracks outside their stated preference.
- **Catalog imbalance:** If the dataset contains more songs of one genre than others, that genre will statistically appear in top results more often — not because those songs are better, but simply because there are more of them to match against.
- **Binary matching:** Genre and mood are treated as exact string matches. A user who likes "indie pop" gets zero credit for a "pop" song and vice versa, even though those genres heavily overlap.
- **Energy-only numerical scoring:** Tempo, valence, danceability, and acousticness are all ignored by the base recipe — a high-valence, highly danceable song gets the same energy-proximity score as a slow dirge, as long as both have the same energy value.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

