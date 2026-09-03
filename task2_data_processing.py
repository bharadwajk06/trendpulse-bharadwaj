import os
import glob
import pandas as pd

# Step 1: Find the latest JSON file
json_files = glob.glob("data/trends_*.json")

if len(json_files) == 0:
    print("No JSON file found.")
    raise SystemExit
latest_file = max(json_files, key=os.path.getmtime)

# Step 2: Load JSON data into DataFrame
df = pd.read_json(latest_file)
print("Rows loaded:", len(df))

# Step 3: Remove duplicate post IDs
df.drop_duplicates(subset=["post_id"], inplace=True)
print("After removing duplicates:", len(df))

# Step 4: Convert score and comments to numbers
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"],errors="coerce")

# Step 5: Remove rows with important missing values
df.dropna(subset=["post_id", "title", "score"],inplace=Tru)
print("After removing missing values:", len(df))

# Step 6: Replace missing comments with 0
df["num_comments"] = df["num_comments"].fillna(0)

# Step 7: Convert score and comments to integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Step 8: Remove extra spaces from titles
df["title"] = df["title"].str.strip()

# Step 9: Keep stories with score 5 or more
df = df[df["score"] >= 5]
print("After removing low score stories:", len(df))

# Step 10: Save cleaned data
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)
print()
print("Saved", len(df), "rows to", output_file)

# Step 11: Show number of stories in each category
print()
print("Stories per category:")
category_counts = df["category"].value_counts()
for category, count in category_counts.items():
    print(category, ":", count)
