import os
import glob
import pandas as pd

json_files = glob.glob("data/trends_*.json")
if len(json_files) == 0:
    print("No JSON file found in data folder.")
    raise SystemExit
latest_json = max(json_files, key=os.path.getmtime)
df = pd.read_json(latest_json)
print(f"Loaded {len(df)} stories from {latest_json}")
df.drop_duplicates(subset=["post_id"], inplace=True)
print(f"After removing duplicates: {len(df)}")
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"],errors="coerce")
df.dropna(subset=["post_id", "title", "score"],inplace=True)
print(f"After removing nulls: {len(df)}")
df["num_comments"] = df["num_comments"].fillna(0)
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)
df["title"] = df["title"].str.strip()
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")
output_path = "data/trends_clean.csv"
df.to_csv(output_path,index=False)
print(f"\nSaved {len(df)} rows to {output_path}")
print("\nStories per category:")
counts = df.groupby("category").size()
for category, count in counts.items():
    print(f"  {category:<18} {count}")
