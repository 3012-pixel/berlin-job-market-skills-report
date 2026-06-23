# Running the project

## Before you start

You need Python 3.8 or higher. Check with:
```bash
python --version
```

If you don't have it, download from [python.org](https://www.python.org/downloads/). On Windows, make sure you tick **"Add Python to PATH"** during installation — easy to miss and causes confusing errors later.

You also need Git to clone the repo. Check with `git --version`. If not installed: [git-scm.com/downloads](https://git-scm.com/downloads).

---

## Setup

Clone the repo and install dependencies:

```bash
git clone https://github.com/YOUR-USERNAME/berlin-job-market-skills-report.git
cd berlin-job-market-skills-report
pip install -r requirements.txt
```

If `pip` isn't found, try `pip3`. On Windows, try `py -m pip install -r requirements.txt`.

---

## Running it

**Option 1 — full pipeline (recommended)**
```bash
python run_all.py
```
Scrapes live jobs, analyzes skills, generates charts. Takes about 1–2 minutes.

**Option 2 — step by step**
```bash
python scraper.py          # -> raw_jobs.csv
python analyzer.py         # -> skills_report.xlsx
python visualizer.py       # -> three .png charts
```
Useful if you want to inspect the data between steps.

**Option 3 — offline/demo mode**
```bash
python generate_sample_data.py
python analyzer.py
python visualizer.py
```
Creates a synthetic dataset of 120 Berlin startup job postings — same schema as the live scraper, so everything downstream works the same. Use this if the API is blocked on your network or you just want to test changes to the taxonomy.

---

## Outputs

After running you'll have:

| File | What it is |
|---|---|
| `raw_jobs.csv` | raw job postings from the scraper |
| `skills_report.xlsx` | frequency analysis (4 sheets) |
| `chart_top20.png` | top 20 skills bar chart |
| `chart_categories.png` | skills by category |
| `chart_wordcloud.png` | word cloud weighted by frequency |

---

## Customizing

**Targeting different roles** — edit `TARGET_TITLES` in `scraper.py`:
```python
TARGET_TITLES = [
    "werkstudent", "working student", "intern",
    "your role here",
]
```

**More data** — increase `MAX_PAGES` in `scraper.py` (default is 10, each page is ~10–15 jobs):
```python
MAX_PAGES = 20
```

**Adding skills** — extend any category in `SKILLS_TAXONOMY` in `analyzer.py`:
```python
"Technical Tools": [
    "python", "sql", "excel", ...,
    "new skill here",
],
```

---

## Troubleshooting

`python: command not found` → try `python3`

`ModuleNotFoundError` → run `pip install -r requirements.txt` again

`403 Forbidden` from the API → your network is blocking the Arbeitnow API. Run Option 3 (offline mode) instead.

`FileNotFoundError: raw_jobs.csv` → run `scraper.py` (or `generate_sample_data.py`) before `analyzer.py`

`FileNotFoundError: skills_report.xlsx` → run `analyzer.py` before `visualizer.py`

Charts are blank → check wordcloud and matplotlib installed: `pip show wordcloud matplotlib`

Windows: terminal closes immediately → run from inside a terminal window, don't double-click the `.py` file
