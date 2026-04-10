# Reflection: Profile Comparisons and Evaluation Notes

---

## Profile 1 vs Profile 2 — High-Energy Pop vs Chill Lofi

These two profiles produced completely different top-5 lists, which is reassuring: the system isn't just recycling the same songs for everyone. The High-Energy Pop listener gets songs with fast tempos and high energy scores (0.82–0.93), while the Chill Lofi listener gets songs with slow tempos and very low energy scores (0.28–0.42). What's interesting is *why* the third result differs. For Chill Lofi, "Spacewalk Thoughts" (ambient, energy=0.28) ranked #4 behind two lofi songs — even though its energy is nearly a perfect match for the target of 0.3. It lost ground purely because it's not labeled "lofi." This shows the genre weight acting like a gate: no matter how well a song fits the vibe, wrong genre label = knocked down the list. For a non-programmer, think of it like a librarian who will only recommend books from the exact shelf you asked for, even if the book next door is a better fit.

---

## Profile 1 vs Profile 3 — High-Energy Pop vs Deep Intense Rock

Both profiles target high energy (0.9 and 0.8), so several of the same songs appear in both lists — notably "Gym Hero" (pop/intense) and "Sunrise City" (pop/happy). But the *order* flips. For High-Energy Pop, "Sunrise City" is #1 because it matches genre AND mood AND energy. For Deep Intense Rock, "Sunrise City" drops to #3 because it only scores on energy proximity — no genre match, no mood match. "Storm Runner" (rock/intense) takes #1 for the Rock listener for the same reason "Sunrise City" led the Pop listener: all three criteria line up. This comparison illustrates that the recommender is doing its job correctly — the same song earns very different scores depending on who is asking. It also reveals that "Gym Hero" keeps showing up near the top of high-energy lists regardless of genre. The reason is simple: "Gym Hero" has an energy of 0.93, which is close to the target for any high-energy user, so it collects a large energy-similarity bonus even without a genre or mood match.

---

## Profile 2 vs Profile 3 — Chill Lofi vs Deep Intense Rock

These are the most different profiles and produce the most different results — almost no overlap in the top 5. The Chill Lofi list is dominated by very quiet, acoustic-leaning tracks. The Deep Intense Rock list is dominated by high-energy, distortion-heavy tracks. What's worth noting is that the Rock listener's list feels slightly "thin" — after "Storm Runner" at #1, the next results are pop and synthwave songs that just happen to have similar energy values (0.75–0.82). There is only one rock song in the entire dataset, so once that slot is filled, the system has nothing else to offer the rock fan from their own genre. This is a direct consequence of catalog imbalance: more songs in a genre means more tailored recommendations. A rock fan using this system would likely feel underserved compared to a lofi fan who has three genre-matched songs to draw from.

---

## Profile 3 vs Profile 4 — Deep Intense Rock vs Adversarial (High-Energy Sad R&B)

The adversarial profile was designed to test a contradiction: can you really want high-energy *and* sad music at the same time? Most sad songs are slow and quiet — so a "sad + energy=0.9" listener is asking for something rare. The system found "Rainy Days & Neon Signs" as the #1 result because it matches both genre (r&b) and mood (sad), even though its energy (0.48) is far from the target (0.9). The genre+mood bonus outweighed the energy penalty. The remaining slots were filled by high-energy songs from completely different genres — rock, electronic, pop — because those scored well on energy alone. The result feels strange to a human listener: slots 3–5 are energetic songs that don't match the sadness vibe at all. This is the adversarial experiment doing its job: it revealed that conflicting preferences cause the system to split the list between "matches the emotion" and "matches the intensity," with no single song satisfying both. A real platform would likely resolve this by learning from the user's actual skip behavior, but our content-based system has no way to know which preference matters more.

---

## Weight Experiment Notes (Phase 4, Step 3)

Doubling the energy weight and halving the genre weight changed the rankings in subtle but meaningful ways. The biggest move was "Spacewalk Thoughts" jumping from #4 to #3 in the Chill Lofi list, leapfrogging "Focus Flow." With standard weights, "Focus Flow" ranked higher because it's a lofi song (genre bonus). With the adjusted weights, "Spacewalk Thoughts" won because its energy (0.28) is almost identical to the user's target (0.3). Neither result is objectively "wrong" — it depends on whether this listener cares more about the genre label or the actual feel of the music. The experiment confirmed that weight choices encode a hidden assumption about what users value most. The default weights assume genre is the most reliable proxy for taste; the experimental weights assume energy/mood is. Both are simplifications of the much more complex reality of how people actually experience music.
