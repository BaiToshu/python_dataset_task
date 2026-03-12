# statistics to show the correlation between lifestyle, productivity and final grades for students

import pandas as pd

df=pd.read_csv("student_productivity.csv")

# sleep score calc: 7-9 hours is ideal
# too little or too much sleep is penalized in score cal
# max score is 25

def sleep_score(hours):
    if hours < 7:
        return max(0,(hours-3)/(7-3))*25
    elif hours <= 9:
        return 25
    else:
        return max(0,(10-hours) / (10-9)) * 25

df["sleep_score"] = df["sleep_hours"].apply(sleep_score).round(2)

# exercise score calc is base on minutes per day
# max score is 25

df["exercise_score"] = ((df["exercise_minutes"]/120)*25).round(2)

# stress score is based of the scale in the dataset wwich is between 1-10
# max score is 25

df["stress_score"] = (((10 - df["stress_level"]) / (10-1)) * 25).round(2)

# phone score is baased of the scale in the dataset which is between 0.5-12 hours
#max score is 25

df["phone_score"] = (((12 - df["phone_usage_hours"]) / (12-0.5)) * 25).round(2)

# balanced lifestyle score is the combined score of the 4 scores above
# max score 100

df["balanced_lifestyle_score"] = (
    df["sleep_score"]
    + df["exercise_score"]
    + df["stress_score"]
    + df["phone_score"]
).round(2)

# tiers based on balanced lifestyle score

def lifestyle_tier(score):
    if score >= 75:
        return "Great"
    elif score >= 50:
        return "Balanced"
    elif score >= 25:
        return "Poor"
    else:
        return "At risk"

df["lifestyle_tier"] = df["balanced_lifestyle_score"].apply(lifestyle_tier)

print("  Balanced lifestyle score - summery stats")

print("Score distribution")
print(df["balanced_lifestyle_score"].describe().round(2))

print("Tier breakdown")
tier_counts = df["lifestyle_tier"].value_counts()
tier_pct = df["lifestyle_tier"].value_counts(normalize=True) * 100
tier_summery = pd.DataFrame({"Count": tier_counts, "Percent": tier_pct.round(1)})
print(tier_summery)

print("Average aacademic outcome based on lifestyle tier")
tier_order = ["Great","Balanced","Poor","At risk"]
outcomes = (df.groupby("lifestyle_tier")[["final_grade","productivity_score","focus_score"]].mean().round(2).reindex(tier_order))
print(outcomes)

print("Sub-score averages by tier")
sub_scores = (df.groupby("lifestyle_tier")[['sleep_score','exercise_score','stress_score','phone_score']].mean().round(2).reindex(tier_order))
print(sub_scores)

output_cols = ["student_id","age","gender","sleep_hours","exercise_minutes","stress_level","phone_usage_hours","sleep_score","exercise_score","stress_score","phone_score","balanced_lifestyle_score","lifestyle_tier","final_grade","productivity_score","focus_score"]
df[output_cols].to_csv("student_productivity-lifestyle.csv",index=False)