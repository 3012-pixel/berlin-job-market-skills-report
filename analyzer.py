import pandas as pd
import re
from collections import Counter

# I built this taxonomy manually after going through ~30 job postings by hand.
# Took about an hour but it made the output way more meaningful than a generic
# NLP approach would have. The categories reflect how I actually think about
# skill groupings when reading JDs.

SKILLS_TAXONOMY = {
    "Technical Tools": [
        "python", "sql", "excel", "power bi", "powerbi", "tableau",
        "r studio", "google analytics", "google sheets", "looker",
        "salesforce", "hubspot", "notion", "jira", "confluence",
        "airtable", "zapier", "figma", "powerpoint", "vba", "alteryx",
    ],
    "Data & Analytics": [
        "data analysis", "data analytics", "data visualization",
        "dashboard", "kpi", "reporting", "machine learning", "statistics",
        "pandas", "numpy", "matplotlib", "a/b testing",
        "market research", "competitive analysis", "financial modeling",
    ],
    "Strategy & Business": [
        "business development", "strategy", "consulting", "go-to-market",
        "market entry", "competitive intelligence", "okr", "roadmap",
        "business model", "swot", "pestle", "stakeholder management",
        "pitch deck", "investor relations", "due diligence", "fundraising",
    ],
    "Marketing & Growth": [
        "seo", "sem", "google ads", "social media", "content marketing",
        "email marketing", "crm", "lead generation", "growth hacking",
        "brand strategy", "campaign management", "performance marketing",
        "copywriting", "inbound", "outbound",
    ],
    "Operations & Project Management": [
        "project management", "operations", "process optimization",
        "agile", "scrum", "kanban", "lean", "product management",
        "product owner", "sprint", "backlog", "supply chain",
    ],
    "Soft Skills": [
        "communication", "analytical", "problem solving", "teamwork",
        "leadership", "presentation", "negotiation", "critical thinking",
        "self-starter", "proactive", "cross-functional",
    ],
    "Languages": [
        "german", "english", "french", "spanish",
        "c1", "c2", "b2", "fluent", "native",
    ],
    "Startup / VC Context": [
        "startup", "series a", "series b", "series c", "seed",
        "venture capital", "vc", "scale-up", "early-stage",
        "growth stage", "product-market fit",
    ],
}


def extract_skills(text, taxonomy):
    text_lower = text.lower()
    found = {}
    for category, skills in taxonomy.items():
        for skill in skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            count = len(re.findall(pattern, text_lower))
            if count > 0:
                found[skill] = found.get(skill, 0) + count
    return found


def analyze(input_file="raw_jobs.csv", output_file="skills_report.xlsx"):
    try:
        df = pd.read_csv(input_file, encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"'{input_file}' not found - run scraper.py first")
        return None

    print(f"loaded {len(df)} job postings")

    # combine title + description + tags for better signal
    df["full_text"] = (
        df["title"].fillna("") + " " +
        df["description"].fillna("") + " " +
        df["tags"].fillna("")
    )

    global_counter = Counter()
    job_presence = Counter()

    for _, row in df.iterrows():
        found = extract_skills(row["full_text"], SKILLS_TAXONOMY)
        global_counter.update(found)
        job_presence.update({k: 1 for k in found})

    skill_rows = []
    for category, skills in SKILLS_TAXONOMY.items():
        for skill in skills:
            total = global_counter.get(skill, 0)
            jobs_with = job_presence.get(skill, 0)
            pct = round(jobs_with / len(df) * 100, 1) if len(df) > 0 else 0
            if total > 0:
                skill_rows.append({
                    "Category":          category,
                    "Skill":             skill.title(),
                    "Total Mentions":    total,
                    "Jobs Mentioning":   jobs_with,
                    "% of Job Postings": pct,
                })

    results_df = pd.DataFrame(skill_rows).sort_values(
        ["Category", "% of Job Postings"], ascending=[True, False]
    )

    category_summary = (
        results_df.groupby("Category")
        .agg(
            Unique_Skills_Found=("Skill", "count"),
            Total_Mentions=("Total Mentions", "sum"),
            Top_Skill=("Skill", "first"),
        )
        .sort_values("Total_Mentions", ascending=False)
        .reset_index()
    )

    top25 = results_df.nlargest(25, "% of Job Postings").reset_index(drop=True)
    top25.index += 1

    print("\ntop 25 skills by % of postings:\n")
    print(top25[["Skill", "Category", "% of Job Postings", "Jobs Mentioning"]].to_string())

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        top25.to_excel(writer, sheet_name="Top 25 Skills", index=True)
        results_df.to_excel(writer, sheet_name="All Skills", index=False)
        category_summary.to_excel(writer, sheet_name="Category Summary", index=False)
        df[["title", "company", "location", "remote", "tags", "url"]].to_excel(
            writer, sheet_name="Raw Jobs", index=False
        )

    print(f"\nsaved to {output_file}")
    return results_df, top25, category_summary


if __name__ == "__main__":
    analyze()
