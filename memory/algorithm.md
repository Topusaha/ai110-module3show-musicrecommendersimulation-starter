# Scoring Algorithm

This document defines the exact scoring rule used to rank songs for a given user profile.

---

## Core Idea: Gaussian Proximity Scoring

For each numerical feature, a song is scored based on how **close** its value is to the user's preference — not whether it is higher or lower. The score is always between 0.0 and 1.0, where 1.0 is a perfect match.

### Proximity Formula

```
proximity(song_value, user_pref, σ) = exp( -( (song_value - user_pref)² / (2σ²) ) )
```

- Peaks at **1.0** when `song_value == user_pref`
- Falls off symmetrically on both sides
- `σ` (sigma) controls tolerance — larger σ = more forgiving

---

## Feature Weights and Sigma Values

| Feature | Type | Weight | Sigma (σ) | Notes |
|---|---|---|---|---|
| `genre` | categorical | 3.0 | — | Binary match (1 or 0) |
| `mood` | categorical | 2.5 | — | Binary match (1 or 0) |
| `energy` | numeric | 2.0 | 0.15 | Strong driver of listening experience |
| `valence` | numeric | 1.8 | 0.20 | Emotional tone is core to indie/chill feel; bumped up |
| `danceability` | numeric | 0.7 | 0.20 | Secondary context signal for chill listening; reduced |
| `acousticness` | numeric | 1.0 | 0.15 | Tighter tolerance — texture preference is deliberate |
| `tempo_bpm` | numeric | 0.5 | 15.0 | Scale is 60–160 BPM; σ is in BPM units |

**Total weight = 11.5**

---

## Per-Feature Score Definitions

### Genre (weight = 3.0)
```
genre_score = 1.0   if song.genre == user.favorite_genre
            = 0.0   otherwise
```

### Mood (weight = 2.5)
```
mood_score = 1.0   if song.mood == user.favorite_mood
           = 0.0   otherwise
```

### Energy (weight = 2.0, σ = 0.15)
```
energy_score = exp( -( (song.energy - user.target_energy)² / (2 × 0.15²) ) )
             = exp( -( (song.energy - user.target_energy)² / 0.045 ) )
```

### Valence (weight = 1.8, σ = 0.20)
```
valence_score = exp( -( (song.valence - user.target_valence)² / (2 × 0.20²) ) )
              = exp( -( (song.valence - user.target_valence)² / 0.08 ) )
```

### Danceability (weight = 0.7, σ = 0.20)
```
danceability_score = exp( -( (song.danceability - user.target_danceability)² / 0.08 ) )
```

### Acousticness (weight = 1.0, σ = 0.15)
```
acousticness_score = exp( -( (song.acousticness - user.target_acousticness)² / (2 × 0.15²) ) )
                   = exp( -( (song.acousticness - user.target_acousticness)² / 0.045 ) )
```

### Tempo (weight = 0.5, σ = 15.0)
```
tempo_score = exp( -( (song.tempo_bpm - user.target_tempo)² / (2 × 15²) ) )
            = exp( -( (song.tempo_bpm - user.target_tempo)² / 450 ) )
```

---

## Total Score Formula

```
raw_score = (3.0 × genre_score)
          + (2.5 × mood_score)
          + (2.0 × energy_score)
          + (1.8 × valence_score)
          + (0.7 × danceability_score)
          + (1.0 × acousticness_score)
          + (0.5 × tempo_score)

final_score = raw_score / 11.5
```

`final_score` is always in the range **[0.0, 1.0]**.

---

## Worked Example

**User profile:**
- `favorite_genre` = "lofi"
- `favorite_mood` = "chill"
- `target_energy` = 0.40
- `target_valence` = 0.58
- `target_danceability` = 0.60
- `target_acousticness` = 0.75
- `target_tempo` = 76

**Song: "Library Rain" (id=4)**
```
genre        = "lofi"   → genre_score        = 1.0
mood         = "chill"  → mood_score         = 1.0
energy       = 0.35     → energy_score       = exp(-(0.05² / 0.045))  = exp(-0.0556) ≈ 0.946
valence      = 0.60     → valence_score      = exp(-(0.02² / 0.08))   = exp(-0.005)  ≈ 0.995
danceability = 0.58     → danceability_score = exp(-(0.02² / 0.08))   = exp(-0.005)  ≈ 0.995
acousticness = 0.86     → acousticness_score = exp(-(0.11² / 0.045))  = exp(-0.2689) ≈ 0.764
tempo_bpm    = 72       → tempo_score        = exp(-(4² / 450))       = exp(-0.0356) ≈ 0.965
```

```
raw_score = (3.0 × 1.0) + (2.5 × 1.0) + (2.0 × 0.946) + (1.8 × 0.995)
          + (0.7 × 0.995) + (1.0 × 0.764) + (0.5 × 0.965)

          = 3.0 + 2.5 + 1.892 + 1.791 + 0.697 + 0.764 + 0.483
          = 11.127

final_score = 11.127 / 11.5 ≈ 0.968
```

"Library Rain" scores **0.968** — still excellent. The small drop vs. before reflects the tighter acousticness tolerance (σ=0.15) penalizing the 0.11 gap more sharply.

---

## Design Decisions

**Why Gaussian over linear distance?**
Linear scoring (`1 - |x - pref|`) creates a sharp, uniform penalty at all distances. The Gaussian creates a natural "comfort zone" around the user's preference — songs slightly off still score very high, while distant songs fall off rapidly. This better reflects how human preferences actually work.

**Why are genre and mood weighted highest?**
They are the user's most deliberate, declared preferences. Getting these wrong overrides any numerical similarity — a jazz track that perfectly matches energy still shouldn't top a lofi playlist.

**Why is tempo weighted lowest?**
Tempo is a secondary signal. Users rarely think "I want exactly 120 BPM" — they think "I want high energy" (which correlates with tempo). Including it lightly adds precision without over-indexing on a single rhythmic dimension.
