"""Creates a realistic sample CSV with the same columns as the real dataset.
Skip this if you already have social_media_screentime_mental_health_2026.csv."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1500

age = rng.integers(13, 65, n)
occupation = np.where(age < 23, rng.choice(["Student", "Part-time employed"], n, p=[0.8, 0.2]),
                      rng.choice(["Full-time employed", "Part-time employed", "Self-employed", "Unemployed", "Student"],
                                 n, p=[0.5, 0.15, 0.15, 0.1, 0.1]))
screen = np.clip(rng.normal(9 - age / 10, 2.0, n), 0.5, 16).round(1)
night = np.where(rng.random(n) < screen / 14, "Yes", "No")
sleep = np.clip(8.3 - 0.18 * screen - 0.5 * (night == "Yes") + rng.normal(0, 0.6, n), 3.5, 10).round(1)
life = np.clip(np.round(9 - 0.35 * screen + 0.4 * (sleep - 7) + rng.normal(0, 1.2, n)), 1, 10).astype(int)
esteem = np.clip(np.round(life + rng.normal(0, 1.3, n)), 1, 10).astype(int)
score = (life + esteem) / 2

pd.DataFrame({
    "participant_id": [f"P{i:06d}" for i in range(n)],
    "age": age,
    "gender": rng.choice(["Male", "Female", "Non-binary"], n, p=[0.48, 0.48, 0.04]),
    "occupation": occupation,
    "region": rng.choice(["Asia", "Europe", "North America", "Latin America", "Africa", "Oceania"], n),
    "most_used_platform": rng.choice(["Instagram", "TikTok", "YouTube", "Facebook", "X (Twitter)", "Snapchat", "LinkedIn"], n),
    "platforms_used_count": np.clip(np.round(screen / 2.5 + rng.normal(1.5, 1, n)), 1, 9).astype(int),
    "daily_screen_hours": screen,
    "daily_notifications": np.clip(screen * 18 + rng.normal(0, 30, n), 5, 500).astype(int),
    "avg_sleep_hours": sleep,
    "night_time_use": night,
    "minutes_to_first_check_after_waking": np.clip(rng.exponential(40 - screen * 2, n), 0, 180).astype(int),
    "primary_purpose": rng.choice(["Entertainment", "Social connection", "News", "Work/Study", "Shopping"], n),
    "attempted_digital_detox": rng.choice(["Yes", "No"], n, p=[0.35, 0.65]),
    "life_satisfaction_1to10": life,
    "self_esteem_1to10": esteem,
    "wellbeing_band": pd.cut(score, [0, 4, 6.5, 10], labels=["Low", "Moderate", "High"]),
}).to_csv("social_media_screentime_mental_health_2026.csv", index=False)
print("Wrote social_media_screentime_mental_health_2026.csv")
