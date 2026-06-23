import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from wordcloud import WordCloud
import warnings
warnings.filterwarnings("ignore")

# color choices: wanted each category to be visually distinct but not look like
# a default matplotlib palette. Blues for technical, greens for strategy, etc.
CATEGORY_COLORS = {
    "Technical Tools":                "#1A56A0",
    "Data & Analytics":               "#2E86C1",
    "Strategy & Business":            "#1B7A4B",
    "Marketing & Growth":             "#E67E22",
    "Operations & Project Management":"#8E44AD",
    "Soft Skills":                    "#C0392B",
    "Languages":                      "#2C3E50",
    "Startup / VC Context":           "#16A085",
}

BG = "#F8F9FA"
GRID = "#E0E0E0"


def chart_top20(top25_df, output="chart_top20.png"):
    top20 = top25_df.head(20).copy()
    colors = [CATEGORY_COLORS.get(c, "#1A56A0") for c in top20["Category"]]

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    bars = ax.barh(
        top20["Skill"][::-1],
        top20["% of Job Postings"][::-1],
        color=colors[::-1],
        edgecolor="white",
        linewidth=0.6,
        height=0.65,
    )

    for bar, val in zip(bars, top20["% of Job Postings"][::-1]):
        ax.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.0f}%",
            va="center", ha="left", fontsize=9, color="#444444", fontweight="bold"
        )

    legend_handles = [
        mpatches.Patch(color=c, label=cat)
        for cat, c in CATEGORY_COLORS.items()
        if cat in top20["Category"].values
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=8,
              framealpha=0.85, title="Category", title_fontsize=8)

    ax.set_xlabel("% of Job Postings", fontsize=10, labelpad=10)
    ax.set_title(
        "Top 20 Skills — Berlin Startup Roles (Werkstudent / Intern / Junior)",
        fontsize=13, fontweight="bold", pad=14, color="#1A1A2E"
    )
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=100, decimals=0))
    ax.set_xlim(0, top20["% of Job Postings"].max() * 1.18)
    ax.axvline(x=50, color="#BBBBBB", linestyle="--", linewidth=0.8, alpha=0.7)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", labelsize=10)

    fig.text(0.99, 0.01, "Source: Arbeitnow API", ha="right", fontsize=7, color="#AAAAAA")
    plt.tight_layout()
    plt.savefig(output, dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"  saved: {output}")


def chart_categories(category_df, output="chart_categories.png"):
    df = category_df.sort_values("Total_Mentions", ascending=True)
    colors = [CATEGORY_COLORS.get(c, "#1A56A0") for c in df["Category"]]

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    bars = ax.barh(df["Category"], df["Total_Mentions"], color=colors,
                   edgecolor="white", linewidth=0.6, height=0.6)

    for bar, row in zip(bars, df.itertuples()):
        ax.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(row.Total_Mentions)} mentions  |  top skill: {row.Top_Skill}",
            va="center", ha="left", fontsize=8.5, color="#333333"
        )

    ax.set_xlabel("Total Mentions Across All Postings", fontsize=10, labelpad=10)
    ax.set_title("Skill Categories — Which clusters appear most in Berlin startup JDs?",
                 fontsize=12, fontweight="bold", pad=14, color="#1A1A2E")
    ax.set_xlim(0, df["Total_Mentions"].max() * 1.45)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", labelsize=9.5)

    fig.text(0.99, 0.01, "Source: Arbeitnow API", ha="right", fontsize=7, color="#AAAAAA")
    plt.tight_layout()
    plt.savefig(output, dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"  saved: {output}")


def chart_wordcloud(all_skills_df, output="chart_wordcloud.png"):
    freq = dict(zip(all_skills_df["Skill"], all_skills_df["Total Mentions"]))

    wc = WordCloud(
        width=1400, height=700,
        background_color="white",
        colormap="Blues",
        max_words=120,
        prefer_horizontal=0.85,
        min_font_size=10,
        max_font_size=120,
        collocations=False,
    ).generate_from_frequencies(freq)

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor(BG)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Berlin Startup Jobs — Skills Word Cloud (size = frequency)",
                 fontsize=13, fontweight="bold", pad=14, color="#1A1A2E")

    fig.text(0.99, 0.01, "Source: Arbeitnow API", ha="right", fontsize=7, color="#AAAAAA")
    plt.tight_layout()
    plt.savefig(output, dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"  saved: {output}")


def visualize(report_file="skills_report.xlsx"):
    try:
        top25_df      = pd.read_excel(report_file, sheet_name="Top 25 Skills", index_col=0)
        all_skills_df = pd.read_excel(report_file, sheet_name="All Skills")
        category_df   = pd.read_excel(report_file, sheet_name="Category Summary")
    except FileNotFoundError:
        print(f"'{report_file}' not found - run analyzer.py first")
        return

    print("generating charts...")
    chart_top20(top25_df)
    chart_categories(category_df)
    chart_wordcloud(all_skills_df)
    print("done")


if __name__ == "__main__":
    visualize()
