from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(dict(row))
    return songs

import math

WEIGHTS = {
    "genre":        3.0,
    "mood":         2.5,
    "energy":       2.0,
    "valence":      1.5,
    "danceability": 1.0,
    "acousticness": 1.0,
    "tempo_bpm":    0.5,
}
SIGMAS = {
    "energy":       0.15,
    "valence":      0.20,
    "danceability": 0.20,
    "acousticness": 0.20,
    "tempo_bpm":    15.0,
}
TOTAL_WEIGHT = 11.5


def _gaussian(x: float, mu: float, sigma: float) -> float:
    return math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song against the user's preferences.
    Returns (normalized_score, reasons) where each reason shows a feature's weighted contribution.
    """
    contributions: List[Tuple[str, float]] = []

    genre_match = 1.0 if song.get("genre") == user_prefs.get("favorite_genre") else 0.0
    contributions.append(("genre match" if genre_match else "genre mismatch",
                           WEIGHTS["genre"] * genre_match))

    mood_match = 1.0 if song.get("mood") == user_prefs.get("favorite_mood") else 0.0
    contributions.append(("mood match" if mood_match else "mood mismatch",
                           WEIGHTS["mood"] * mood_match))

    for feature, pref_key, label in [
        ("energy",       "target_energy",       "energy"),
        ("valence",      "target_valence",      "valence"),
        ("danceability", "target_danceability", "danceability"),
        ("acousticness", "target_acousticness", "acousticness"),
        ("tempo_bpm",    "target_tempo",        "tempo"),
    ]:
        g = _gaussian(song[feature], user_prefs[pref_key], SIGMAS[feature])
        contributions.append((label, WEIGHTS[feature] * g))

    raw = sum(points for _, points in contributions)
    score = raw / TOTAL_WEIGHT
    reasons = [f"{label} (+{points:.2f})" for label, points in contributions if points > 0]
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Score every song using score_song, sort by score, and return the top k results.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    top_k = scored[:k]
    return [(song, score, ", ".join(reasons)) for song, score, reasons in top_k]
