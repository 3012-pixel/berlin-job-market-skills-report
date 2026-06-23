import pandas as pd
import random
from datetime import datetime, timedelta

# use this if you want to run the analysis without hitting the live API
# e.g. for offline demos, testing changes to the taxonomy, etc.
# produces the same CSV schema as scraper.py so everything downstream works

random.seed(42)

COMPANIES = [
    ("Gorillas", "Berlin, Germany"),
    ("Tier Mobility", "Berlin, Germany"),
    ("N26", "Berlin, Germany"),
    ("Trade Republic", "Berlin, Germany"),
    ("Taxfix", "Berlin, Germany"),
    ("Enpal", "Berlin, Germany"),
    ("Moss", "Berlin, Germany"),
    ("Raisin", "Berlin, Germany"),
    ("HomeToGo", "Berlin, Germany"),
    ("Forto", "Berlin, Germany"),
    ("Grover", "Berlin, Germany"),
    ("Razor Group", "Berlin, Germany"),
    ("Spryker", "Berlin, Germany"),
    ("Zolar", "Berlin, Germany"),
    ("Finn", "Berlin, Germany"),
    ("Contentful", "Berlin, Germany"),
    ("Personio", "Berlin, Germany"),
    ("GetYourGuide", "Berlin, Germany"),
    ("HelloFresh", "Berlin, Germany"),
    ("Wefox", "Berlin, Germany"),
    ("Blinkist", "Berlin, Germany"),
    ("Foodspring", "Berlin, Germany"),
    ("FinLeap", "Berlin, Germany"),
    ("Pitch", "Berlin, Germany"),
    ("Remote First GmbH", "Remote"),
]

JOB_TEMPLATES = [
    {
        "title": "Werkstudent Business Development (m/f/d)",
        "tags": ["business-development", "startup", "berlin"],
        "description": """
We are looking for a Werkstudent Business Development to join our growing team in Berlin.
You will support our business development and strategy team in identifying new market opportunities.
Requirements: Strong analytical skills, proficiency in Excel and PowerPoint, experience with market research.
Nice to have: Python, SQL, Tableau or Power BI for data analysis and reporting.
You will work on go-to-market strategy, competitive analysis, and stakeholder management.
Fluent English required; German is a plus. Agile working environment with OKR-driven goals.
You will collaborate cross-functionally with marketing, product, and operations teams.
Experience with CRM tools like Salesforce or HubSpot is beneficial.
        """
    },
    {
        "title": "Working Student Strategy & Operations (m/f/d)",
        "tags": ["strategy", "operations", "working-student"],
        "description": """
Join our strategy and operations team as a Working Student in Berlin.
You will support senior consultants on key projects including process optimization and financial modeling.
Strong Excel and PowerPoint skills are mandatory. SQL knowledge is a big plus.
You will conduct market research, competitive intelligence, and SWOT analysis.
Stakeholder management and communication skills are essential.
Experience with project management tools like Notion, Jira or Confluence preferred.
Knowledge of agile and scrum methodologies is advantageous.
We use data analytics and Power BI dashboards for reporting and KPI tracking.
English C1 level required; German B2 or above strongly preferred.
        """
    },
    {
        "title": "Intern Marketing & Growth (m/f/d)",
        "tags": ["marketing", "growth", "intern"],
        "description": """
We are looking for a Marketing and Growth Intern to support our performance marketing team.
You will work on SEO, SEM, and Google Ads campaigns targeting European markets.
Proficiency in Google Analytics, Excel, and social media platforms required.
Experience with email marketing, HubSpot, or Salesforce CRM is a plus.
You will own campaign management from briefing to reporting, tracking KPIs and ROI.
Content marketing, copywriting, and basic data visualization skills appreciated.
You will run A/B testing and support lead generation initiatives.
Fluent English required; German C1 preferred.
        """
    },
    {
        "title": "Werkstudent Data & Analytics (m/f/d)",
        "tags": ["data", "analytics", "python"],
        "description": """
Our analytics team is hiring a Werkstudent to support data-driven decision making.
You will work with Python (Pandas, NumPy, Matplotlib) and SQL for data extraction and analysis.
Experience with Power BI, Tableau, or Looker for dashboard creation is required.
You will build KPI reporting frameworks and automate Excel-based workflows.
Knowledge of statistics and A/B testing is a strong plus.
Familiarity with Google Analytics and data visualization best practices appreciated.
We work in an agile environment using Jira, Confluence, and Notion.
English fluency required; German skills are advantageous.
        """
    },
    {
        "title": "Junior Consultant / Working Student Strategy (m/f/d)",
        "tags": ["consulting", "strategy", "junior"],
        "description": """
We are a Berlin-based strategy consultancy seeking a Junior Consultant or Working Student.
You will support client-facing strategy projects including business model analysis and due diligence.
Strong analytical and problem solving skills are essential, along with excellent PowerPoint skills.
You will apply frameworks including SWOT, PESTLE, and Business Model Canvas.
Financial modeling in Excel and stakeholder management experience are highly valued.
Project management experience and proficiency in tools like Notion or Asana preferred.
German C1 and English C1 required for client communication.
Experience in market research, competitive analysis, and pitch deck creation is a plus.
        """
    },
    {
        "title": "Werkstudent Product & Operations (m/f/d)",
        "tags": ["product", "operations", "startup"],
        "description": """
Join our product and operations team as a Werkstudent at a Series B startup in Berlin.
You will support product owners in backlog management, sprint planning, and roadmap development.
Experience with agile, scrum, and kanban frameworks is required.
Strong analytical skills and proficiency in Excel, Notion, and Jira preferred.
Cross-functional collaboration with engineering, marketing, and business development teams.
Python or SQL for data analysis is a significant advantage.
English fluency required. German language skills are a plus.
        """
    },
    {
        "title": "Werkstudent Venture & Investment Analysis (m/f/d)",
        "tags": ["venture-capital", "investment", "analysis"],
        "description": """
Our venture capital team is looking for an analytical Werkstudent.
You will support deal sourcing, due diligence, and competitive intelligence for Series A and B investments.
Strong Excel and financial modeling skills are mandatory.
Experience with market research, investor relations, and pitch deck analysis is valued.
Familiarity with startup ecosystems and go-to-market strategy.
Python or R for data analysis is a strong plus. Tableau or Power BI experience preferred.
Fluent English and German (B2+) required.
        """
    },
    {
        "title": "Intern Business Intelligence & Reporting (m/f/d)",
        "tags": ["business-intelligence", "reporting", "data"],
        "description": """
We are looking for a Business Intelligence Intern to join our data team in Berlin.
You will create and maintain Power BI and Tableau dashboards for leadership reporting.
SQL proficiency is required for data extraction and transformation.
Strong Excel skills including pivot tables and VLOOKUP are valued.
Python (Pandas, NumPy) experience for data automation is a significant plus.
You will define and track KPIs and build reporting frameworks.
English and German communication skills essential.
        """
    },
    {
        "title": "Werkstudent SEO & Content Strategy (m/f/d)",
        "tags": ["seo", "content", "marketing"],
        "description": """
Our digital marketing team is hiring a Werkstudent for SEO and Content Strategy.
You will conduct SEO audits, keyword research, and competitive analysis for European markets.
Proficiency in Google Search Console, Ahrefs, Semrush, or Ubersuggest is required.
Experience with Google Analytics, Google Ads, and SEM campaigns is a strong plus.
Content marketing and copywriting skills appreciated.
Excel for reporting and HubSpot CRM familiarity preferred.
Fluent English required; German C1 is a strong advantage.
        """
    },
    {
        "title": "Working Student Founder's Associate (m/f/d)",
        "tags": ["founders-associate", "chief-of-staff", "startup"],
        "description": """
Work directly with our founders at this fast-growing Berlin startup.
You will own strategic projects spanning business development, operations, and fundraising.
Strong analytical, problem solving, and communication skills are non-negotiable.
You will prepare investor materials, pitch decks, and due diligence reports.
Market research, competitive intelligence, and financial modeling in Excel are core responsibilities.
Proficiency in Notion, Confluence, and project management tools preferred.
Python or SQL skills for data analysis are advantageous.
English and German (C1) required.
        """
    },
]


def random_date(days_back=60):
    d = datetime.now() - timedelta(days=random.randint(0, days_back))
    return d.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def generate_dataset(n_jobs=120, output="raw_jobs.csv"):
    rows = []
    for i in range(n_jobs):
        template = random.choice(JOB_TEMPLATES)
        company, location = random.choice(COMPANIES)
        rows.append({
            "title":       template["title"],
            "company":     company,
            "location":    location,
            "remote":      "Remote" in location,
            "url":         f"https://www.arbeitnow.com/jobs/sample-{i+1}",
            "created_at":  random_date(),
            "tags":        ", ".join(template["tags"]),
            "description": template["description"].strip(),
        })

    df = pd.DataFrame(rows)
    df.to_csv(output, index=False, encoding="utf-8-sig")
    print(f"generated {len(df)} sample job postings -> {output}")
    return df


if __name__ == "__main__":
    generate_dataset()
