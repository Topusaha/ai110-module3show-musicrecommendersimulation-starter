"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "favorite_genre":      "pop",
        "favorite_mood":       "happy",
        "target_energy":       0.90,   # very high energy, pump-up feel
        "target_valence":      0.85,   # very positive, feel-good
        "target_danceability": 0.85,   # floor-ready danceability
        "target_acousticness": 0.10,   # heavily produced, not acoustic
        "target_tempo":        128,    # fast dance tempo
    },
    "Chill Lofi": {
        "favorite_genre":      "lofi",
        "favorite_mood":       "chill",
        "target_energy":       0.38,   # low energy, laid-back
        "target_valence":      0.58,   # mellow but not sad
        "target_danceability": 0.60,   # gentle groove
        "target_acousticness": 0.78,   # warm, organic texture
        "target_tempo":        76,     # slow, study-session pace
    },
    "Deep Intense Rock": {
        "favorite_genre":      "rock",
        "favorite_mood":       "intense",
        "target_energy":       0.92,   # maximum aggression
        "target_valence":      0.45,   # dark, serious tone
        "target_danceability": 0.65,   # headbang-friendly rhythm
        "target_acousticness": 0.08,   # distorted, electric
        "target_tempo":        150,    # fast, driving tempo
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        print(f"\n{'='*50}")
        print(f"Profile: {profile_name}")
        print(f"{'='*50}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
