
import pandas as pd
import numpy as np

df = pd.read_csv("data/trends_clean.csv")
print(f"Loaded data: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

average_score = df["score"].mean()
average_comments = df["num_comments"].mean()
print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")

scores = df["score"].to_numpy()
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)
print("\n NumPy Stats")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

category_counts = df["category"].value_counts()
most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print(f"\nMost stories in: "f"{most_common_category} ({most_common_count} stories)")
most_commented_index = df["num_comments"].idxmax()
most_commented_title = df.loc[most_commented_index, "title"]
most_commented_count = df.loc[most_commented_index, "num_comments"]
print(f'\nMost commented story: "{most_commented_title}" 'f"— {most_commented_count} comments")

df["engagement"] = (df["num_comments"] / (df["score"] + 1))
df["is_popular"] = df["score"] > average_score
output_file = "data/trends_analysed.csv"
df.to_csv(output_file,index=False)
print(f"\nSaved to {output_file}")
