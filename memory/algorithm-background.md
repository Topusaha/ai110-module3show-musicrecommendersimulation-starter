# Algorithm Background

This document explains the mathematical concepts behind the scoring rule used in the music recommender. No prior math background is assumed.

---

## 1. The Problem With "Higher Is Better"

Many features in the dataset — `energy`, `valence`, `danceability`, `acousticness` — are continuous numbers between 0.0 and 1.0. A naive approach might simply reward higher values (or lower ones), but that misses the point: a user who wants chill, low-energy music (energy ~0.3) should NOT be recommended a high-energy track just because it has a high number.

What we actually want is **proximity**: songs that are *close* to the user's preference should score high, and songs that are far away should score low — regardless of which direction.

---

## 2. Absolute Distance: The Simplest Proximity Measure

The most straightforward way to measure closeness between two numbers is **absolute distance**:

```
distance = |song_value - user_preference|
```

If the user wants energy = 0.8 and a song has energy = 0.75, the distance is 0.05 (very close). If another song has energy = 0.2, the distance is 0.6 (far away).

To turn this into a score (higher = better), we subtract from 1:

```
linear_score = 1 - |song_value - user_preference|
```

This is simple but has a flaw: the penalty for being off is the same whether you're a little off or a lot off. A song that misses by 0.1 is penalized the same amount relative to one that misses by 0.4 — the relationship is perfectly linear, with no sense of a "comfort zone."

---

## 3. The Gaussian Function: A Natural Proximity Curve

A better model for preference matching is the **Gaussian function** (also called the bell curve or normal distribution shape). It looks like this:

```
               ___
              /   \
             /     \
____________/       \____________
     far    close   close    far
```

The formula is:

```
proximity(x) = exp( -( (x - μ)² / (2σ²) ) )
```

Where:
- `x` is the song's feature value
- `μ` (mu) is the user's preferred value (the center of the bell)
- `σ` (sigma) controls the **width** of the bell — how strict or forgiving the match is
- `exp(...)` is the exponential function (e raised to the power of...)

### Properties that make this ideal for scoring:

| Property | Meaning |
|---|---|
| Output is always between 0 and 1 | Perfect for a score |
| Output = 1 when song exactly matches user preference | Maximum reward for a perfect match |
| Output decays smoothly as values diverge | No harsh cliffs or cutoffs |
| Symmetric | Being 0.2 above OR below the preference is penalized equally |
| σ controls tolerance | Large σ = forgiving; small σ = strict |

---

## 4. Understanding Sigma (σ)

Sigma is the most important parameter to tune. Think of it as "how far off can a song be before I stop caring about it?"

For features on a 0–1 scale:

| σ value | Behavior |
|---|---|
| σ = 0.05 | Very strict — only near-perfect matches score well |
| σ = 0.15 | Moderate — songs within ~0.15 units still score above 0.6 |
| σ = 0.30 | Lenient — songs quite far away still get decent scores |

For `tempo_bpm` (range ~60–160 BPM), the scale is different, so σ is set in BPM units (e.g., σ = 15 means songs within ~15 BPM still score well).

---

## 5. Categorical Features: Hard Match

Features like `genre` and `mood` are not numbers — they are categories. You cannot be "a little pop" or "halfway between happy and intense." For these, we use a **binary match**:

```
categorical_score = 1   if song value == user preference
categorical_score = 0   otherwise
```

These matches are weighted heavily because genre and mood are the most intentional, user-declared preferences.

---

## 6. Weighted Feature Combination

Not all features matter equally. We combine individual feature scores using a **weighted sum**:

```
total_score = Σ (weight_i × feature_score_i)
```

Then divide by the total weight to keep the final score between 0 and 1:

```
normalized_score = total_score / sum_of_all_weights
```

Weights reflect feature importance:
- Genre and mood (categorical) get the highest weights — they represent explicit user intent
- Energy and valence get high weights — they have the strongest correlation with listening experience
- Danceability, acousticness, and tempo get moderate weights — they refine but don't define recommendations

---

## 7. Why This Is Called an RBF Kernel

In machine learning, the Gaussian proximity function is known as the **Radial Basis Function (RBF) kernel** or **Gaussian kernel**. It is widely used in:
- Support Vector Machines (SVMs)
- Gaussian Processes
- K-Nearest Neighbor similarity metrics

Using it here is mathematically equivalent to measuring how similar two points are in a high-dimensional feature space — exactly the kind of similarity a content-based recommender needs.

---

## 8. Summary

| Concept | What it does |
|---|---|
| Absolute distance | Measures how far a song is from user preference |
| Gaussian proximity | Converts distance into a smooth 0–1 score, peaked at the preference |
| Sigma (σ) | Controls how strictly the proximity is enforced |
| Categorical match | Binary 0/1 score for genre, mood |
| Weighted sum | Combines all feature scores with importance weights |
| Normalization | Keeps the final score between 0 and 1 |
