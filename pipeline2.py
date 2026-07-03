import sqlite3
import requests
from bs4 import BeautifulSoup

# --- MILESTONE 1: DATABASE SETUP ---
def setup_database():
    connection = sqlite3.connect("job_market.db")
    cursor = connection.cursor()
    
    # Setup our raw ingestion table
    create_table_query = "CREATE TABLE IF NOT EXISTS raw_jobs(id INTEGER PRIMARY KEY, title TEXT, company TEXT, description TEXT)"
    cursor.execute(create_table_query)
    
    connection.commit()
    connection.close()
    print("Database initialization successful!")


# --- MILESTONE 5: LIVE DATA INGESTION (WEB SCRAPING) ---
def fetch_live_jobs():
    print("Sending HTTP request to live job board...")
    url = "https://realpython.github.io/fake-jobs/"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    job_cards = soup.find_all("div", class_="card-content")
    
    live_data = []
    print(f"Discovered {len(job_cards)} live postings. Scraping text data...")
    
    for card in job_cards:
        title_element = card.find("h2", class_="title")
        company_element = card.find("h3", class_="company")
        desc_element = card.find("p", class_="content")

        # Defensive Coding: Only call .text if the element is NOT None
        job_title = title_element.text.strip() if title_element else "Unknown Title"
        job_company = company_element.text.strip() if company_element else "Unknown Company"
        
        # This line safely protects against the NoneType crash!
        job_desc = desc_element.text.strip() if desc_element else "No description provided."

        live_data.append({
            "title": job_title,
            "company": job_company,
            "description": job_desc
        })
        
    return live_data

def store_raw_jobs(job_list):
    connection = sqlite3.connect("job_market.db")
    cursor = connection.cursor()
    
    # Clean out the table so we don't double up on re-runs
    cursor.execute("DELETE FROM raw_jobs;")
    
    insert_query = "INSERT INTO raw_jobs (title, company, description) VALUES (?, ?, ?);"
    
    for job in job_list:
        cursor.execute(insert_query, (job["title"], job["company"], job["description"]))
        
    connection.commit()
    connection.close()
    print(f"Successfully cached {len(job_list)} live listings into local database.")


# --- MILESTONE 4: PRODUCTION PROCESSING & METRICS ---
def process_and_store_skills():
    connection = sqlite3.connect("job_market.db")
    cursor = connection.cursor()
    
    # Re-initialize clean skills tracking table
    cursor.execute("DROP TABLE IF EXISTS job_skills;")
    cursor.execute("""
    CREATE TABLE job_skills (
        job_title TEXT,
        skill_found TEXT
    );
    """)
    
    cursor.execute("SELECT title, description FROM raw_jobs;")
    all_jobs = cursor.fetchall()
    
    target_skills = ["python", "sql", "java"]
    
    print("\n--- Scanning Live Data for Tech Competencies ---")
    
    for job in all_jobs:
        title = job[0]
        description_lower = job[1].lower()
        
        # ADD THIS LINE: Convert the job title to lowercase too!
        title_lower = title.lower()
        
        for skill in target_skills:
            # REFRACTOR THIS IF STATEMENT: Check if the skill is in the title OR the description!
            if skill in title_lower or skill in description_lower:
                insert_skill_query = "INSERT INTO job_skills(job_title, skill_found) VALUES(?, ?)"
                cursor.execute(insert_skill_query, (title, skill))
                
    connection.commit()
    
    # Print our actual findings from the live web data
    print("\n--- LIVE MARKET ANALYSIS RESULTS ---")
    cursor.execute("SELECT skill_found, COUNT(*) FROM job_skills GROUP BY skill_found ORDER BY COUNT(*) DESC;")
    insights = cursor.fetchall()
    
    if not insights:
        print("Pipeline processed successfully, but no target keywords were matched in these specific postings.")
    for row in insights:
        print(f"Skill: {row[0].upper()} | Found in {row[1]} live postings")
        
    connection.close()


# --- THE MAIN ORCHESTRATION ENGINE ---
if __name__ == "__main__":
    setup_database()
    
    # Data moves seamlessly from the web -> memory -> local SQL engine
    live_jobs_list = fetch_live_jobs()
    store_raw_jobs(live_jobs_list)
    
    process_and_store_skills()
