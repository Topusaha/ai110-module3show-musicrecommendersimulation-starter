---
name: Experiment Log — Multi-Profile Recommender Run
description: Summary of the multi-profile recommender experiment: profiles added, edge cases identified, and observed terminal results
type: project
---

# Experiment Log — Multi-Profile Recommender Run
**Date:** 2026-03-31

---

## What We Did

### 1. Added Three Distinct User Profiles to `src/main.py`

Replaced the single hardcoded `user_prefs` dict with a `PROFILES` dictionary containing three named profiles, and updated `main()` to iterate over all of them.

| Profile | Genre | Mood | Energy | Valence | Danceability | Acousticness | Tempo |
|---|---|---|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.90 | 0.85 | 0.85 | 0.10 | 128 BPM |
| Chill Lofi | lofi | chill | 0.38 | 0.58 | 0.60 | 0.78 | 76 BPM |
| Deep Intense Rock | rock | intense | 0.92 | 0.45 | 0.65 | 0.08 | 150 BPM |

---

### 2. Ran an Edge-Case Analysis Agent

An Explore agent read the scoring logic in `recommender.py`, the song catalog in `data/songs.csv`, and the profiles in `main.py`, then produced a comprehensive vulnerability analysis.

**Key findings:**

- **Binary cliff effect** — Genre + mood combined = 47.8% of total possible score (5.5 / 11.5). A wrong-genre song with perfect numeric features can never beat a correct-genre song with mediocre numerics.
- **Extreme targets act as hard filters** — Setting `target_acousticness=1.0` with sigma=0.20 silently eliminates most of the catalog (anything below 0.8 scores near-zero on that feature).
- **Contradictory profiles expose categorical vs. numeric tension** — A "jazz/relaxed" user with `target_energy=0.9` will receive non-jazz recommendations because the numeric preferences override the genre preference.
- **Tempo is implicitly stricter** — sigma=15 BPM covers only ~7.5% of the BPM range, while energy sigma=0.15 covers 15% of [0,1]. Tempo mismatches are proportionally more penalizing.
- **No input validation** — Missing or wrongly-typed preference keys (e.g., `None`, string instead of float) will crash the scorer at runtime.
- **Tie-breaking is insertion-order dependent** — Songs with identical scores are returned in CSV file order; reordering the CSV changes results.
- **Reasons string can be empty** — If all features score near-zero, the explanation output is "Because: " with nothing after it.

**Five adversarial profiles designed:**
1. `target_acousticness=1.0` (acoustic maximum trap)
2. `target_tempo=200` (extreme tempo outlier with no matching songs)
3. `target_energy=0.0` (zero-energy seeker, creates hard filter)
4. Jazz/relaxed genre with contradictory high-energy, fast-tempo numerics
5. All features at extremes (0.0, 1.0, 1.0, 0.0, 180 BPM) — numeric alignment beats categorical match

---

### 3. Ran a Planning Agent

A Plan agent determined the correct shell command to execute the script:
- Must run from **project root** so `"data/songs.csv"` resolves correctly
- Python auto-adds `src/` to `sys.path` when running `python src/main.py`, so no PYTHONPATH changes needed

**Exact command:** `python src/main.py` (from project root)

---

### 4. Observed Terminal Output — Top 5 per Profile

**High-Energy Pop**
| Rank | Song | Score |
|---|---|---|
| 1 | Sunrise City | 0.96 |
| 2 | Gym Hero | 0.76 |
| 3 | Rooftop Lights | 0.63 |
| 4 | Storm Runner | 0.35 |
| 5 | Night Drive Loop | 0.30 |

Sunrise City dominated with genre + mood + near-perfect numerics. Gym Hero ranked 2nd despite no mood match — its energy/danceability alignment was strong.

**Chill Lofi**
| Rank | Song | Score |
|---|---|---|
| 1 | Midnight Coding | 0.99 |
| 2 | Library Rain | 0.99 |
| 3 | Focus Flow | 0.78 |
| 4 | Spacewalk Thoughts | 0.63 |
| 5 | Coffee Shop Stories | 0.47 |

Effectively a tie at the top. Focus Flow (lofi but "focused" mood, not "chill") ranked 3rd, showing genre weight pulling it up despite mood mismatch.

**Deep Intense Rock**
| Rank | Song | Score |
|---|---|---|
| 1 | Storm Runner | 1.00 |
| 2 | Gym Hero | 0.58 |
| 3 | Night Drive Loop | 0.37 |
| 4 | Sunrise City | 0.31 |
| 5 | Rooftop Lights | 0.23 |

Storm Runner scored a perfect 1.00 — only one rock/intense song in the catalog and it matched on every numeric dimension too. The cliff to #2 (0.58) was dramatic, confirming the binary cliff effect.

---

## What to Explore Next

- Add adversarial profiles to `main.py` and observe whether the predicted "tricks" hold
- Introduce a fallback/genre-diversity mechanism to prevent single-song dominance
- Add input validation to `score_song` for out-of-range or missing preference keys
- Expand the song catalog so underrepresented genres (rock, synthwave, ambient) have more candidates
