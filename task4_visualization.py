
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load analysed data
df = pd.read_csv("data/trends_analysed.csv")
# Create outputs folder
os.makedirs("outputs", exist_ok=True)

# ---------------- Chart 1 ----------------
# Top 10 stories by score
top10 = df.nlargest(10, "score").copy()
# Shorten long titles
top10["short_title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)
plt.figure(figsize=(10, 6))
plt.barh(top10["short_title"],top10["score"])
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.show()
# ---------------- Chart 2 ----------------
# Number of stories in each category
category_counts = df["category"].value_counts()
colors = ["blue","green","orange","purple","red"]
plt.figure(figsize=(8, 5))
plt.bar(category_counts.index,category_counts.values,color=colors)
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.show()
# ---------------- Chart 3 ----------------
# Score vs comments
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]
plt.figure(figsize=(8, 5))
plt.scatter(popular["score"],popular["num_comments"],color="green",label="Popular")
plt.scatter(not_popular["score"],not_popular["num_comments"],color="red",label="Not Popular")
plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.show()
# ---------------- Bonus Dashboard ----------------
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
# Chart 1 in dashboard
axes[0].barh(top10["short_title"],top10["score"])
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
# Chart 2 in dashboard
axes[1].bar(category_counts.index,category_counts.values,color=colors)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(axis="x",rotation=45)
# Chart 3 in dashboard
axes[2].scatter(popular["score"],popular["num_comments"],color="green",label="Popular")
axes[2].scatter(not_popular["score"],not_popular["num_comments"],color="red",label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()
# Dashboard title
fig.suptitle("TrendPulse Dashboard",fontsize=18)
plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.show()

print("All charts saved in outputs/ folder.")
