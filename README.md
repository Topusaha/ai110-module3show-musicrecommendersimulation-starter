# 🎵 Music Recommender Simulation

## Project Summary

The music reccomender sysem  provides a numerical fearture to score how close a song is to what the users preference is. In this small demo the users preference is defined and we score each song using different statistical techniques. 

---

## How The System Works

Each **Song** has 7 scored features: `genre`, `mood`, `energy`, `valence`, `danceability`, `acousticness`, and `tempo_bpm`. Each **UserProfile** stores a preferred genre, mood, and target numeric values for those same features.

The **Recommender** scores every song by comparing it to the user's profile. Categorical features (`genre`, `mood`) score 1.0 on an exact match or 0.0 otherwise. Numeric features are scored with a Gaussian bell curve — 1.0 when the song exactly hits the target, decaying smoothly as it drifts away. Each feature's score is multiplied by a weight (genre is most important at 3.0; tempo least at 0.5), summed, and divided by 11.5 to produce a final 0–1 score. The top-k songs by score are returned as recommendations.


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

See [experiment-log.md](memory/experiment-log.md) for a full log of experiments.

---

## Limitations and Risks

### Binary Cliff Effect

Genre + mood together control 47.8% of the total possible score (5.5 / 11.5). This creates a hard cliff: any genre-matched song with even mediocre numerics will beat a numerically perfect wrong-genre song.

**Example — High-Energy Pop user** (`genre=pop, mood=happy, energy=0.90, valence=0.85, danceability=0.85, acousticness=0.10, tempo=128 BPM`)

**Song A — correct genre/mood, mediocre numerics** → score **0.68**

| Feature | Value | Gaussian | × Weight | Points |
|---|---|---|---|---|
| genre (pop ✓) | — | 1.0 | × 3.0 | 3.000 |
| mood (happy ✓) | — | 1.0 | × 2.5 | 2.500 |
| energy | 0.60 vs 0.90, σ=0.15 | 0.135 | × 2.0 | 0.270 |
| valence | 0.60 vs 0.85, σ=0.20 | 0.458 | × 1.5 | 0.687 |
| danceability | 0.65 vs 0.85, σ=0.20 | 0.607 | × 1.0 | 0.607 |
| acousticness | 0.30 vs 0.10, σ=0.20 | 0.607 | × 1.0 | 0.607 |
| tempo | 105 vs 128, σ=15 | 0.308 | × 0.5 | 0.154 |
| **Total** | | | | **7.825 / 11.5 = 0.68** |

**Song B — wrong genre/mood, perfect numerics** → score **0.52**

| Feature | Value | Gaussian | × Weight | Points |
|---|---|---|---|---|
| genre (rock ✗) | — | 0.0 | × 3.0 | 0.000 |
| mood (intense ✗) | — | 0.0 | × 2.5 | 0.000 |
| energy | 0.90 vs 0.90 | 1.0 | × 2.0 | 2.000 |
| valence | 0.85 vs 0.85 | 1.0 | × 1.5 | 1.500 |
| danceability | 0.85 vs 0.85 | 1.0 | × 1.0 | 1.000 |
| acousticness | 0.10 vs 0.10 | 1.0 | × 1.0 | 1.000 |
| tempo | 128 vs 128 | 1.0 | × 0.5 | 0.500 |
| **Total** | | | | **6.000 / 11.5 = 0.52** |

The absolute ceiling for a wrong-genre song is 0.522. Genre + mood alone contribute 0.478 — so a matching song needs only a tiny numeric contribution to win, regardless of how well the wrong-genre song fits everywhere else.



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

