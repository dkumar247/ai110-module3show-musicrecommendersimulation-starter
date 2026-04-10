# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The most significant bias in this system is **genre dominance**: a genre match is worth +2.0 points while a mood match is only worth +1.0, meaning a song that shares the user's genre but has a completely wrong mood or mismatched energy will almost always outrank a song from a different genre that is a far better emotional fit. This creates a "genre bubble" — the user never encounters great songs outside their stated preference, even if those songs would feel identical to listen to. A second limitation is **catalog imbalance**: the dataset has 3 lofi songs and only 1 rock song, so a lofi listener gets more varied top results than a rock listener purely because the genre is better represented. Third, genre and mood are matched as **exact strings**, meaning "indie pop" gets zero credit toward a "pop" preference even though these genres heavily overlap — a subtlety the system cannot express. Finally, numerically rich fields like `valence`, `danceability`, `acousticness`, and `tempo_bpm` are **completely ignored** by the scoring formula, so a high-valence, danceable track scores identically to a slow, somber one as long as their energy values are the same.

---

## 7. Evaluation  

Four user profiles were tested: **High-Energy Pop** (genre=pop, mood=happy, energy=0.9), **Chill Lofi** (genre=lofi, mood=chill, energy=0.3), **Deep Intense Rock** (genre=rock, mood=intense, energy=0.8), and an **Adversarial profile** (genre=r&b, mood=sad, energy=0.9) designed to expose contradictions between genre and mood. In every case the correct "perfect match" song ranked #1 with a score near 4.0, which confirmed the scoring logic works as intended. The most interesting surprise was in the **Adversarial profile**: even though "sad" and "energy=0.9" feel like contradictory preferences (sad songs are usually slow and low-energy), the system still produced a reasonable #1 result — "Rainy Days & Neon Signs" (r&b/sad) — because genre and mood matched despite the energy gap penalty. A **weight experiment** was also run that doubled the energy weight and halved the genre weight: this caused "Spacewalk Thoughts" (ambient/chill, energy=0.28) to jump past "Focus Flow" (lofi/focused) in the Chill Lofi list, which arguably felt more accurate for a vibe-based listener. The experiment confirmed that the current genre-heavy weights favour genre loyalty over emotional fit, and that re-weighting can surface better results for users who define their taste by feeling rather than category.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
