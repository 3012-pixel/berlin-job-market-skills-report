from scraper import scrape_jobs
from analyzer import analyze
from visualizer import visualize

# runs the full pipeline in one go
# step 1 -> raw_jobs.csv
# step 2 -> skills_report.xlsx
# step 3 -> chart_top20.png, chart_categories.png, chart_wordcloud.png

print("--- step 1: scraping jobs ---")
scrape_jobs()

print("\n--- step 2: analyzing skills ---")
analyze()

print("\n--- step 3: generating charts ---")
visualize()

print("\nall done. check the folder for outputs.")
