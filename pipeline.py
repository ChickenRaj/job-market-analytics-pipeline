
import sqlite3

def setup_database():
    # 1. Connect to a database file named 'job_market.db'
    # (If the file doesn't exist, SQLite will create it automatically)
    connection = sqlite3.connect("job_market.db")
    
    # 2. Create a cursor object to execute SQL commands
    cursor = connection.cursor()
    
    # 3. Write your SQL query string to create the table 'raw_jobs'
    # Hint: Use CREATE TABLE IF NOT EXISTS raw_jobs (...)
    create_table_query = "create table if not exists raw_jobs(id INTEGER PRIMARY KEY, title TEXT, company TEXT, description TEXT)"
    
    # 4. Execute the query using the cursor
    cursor.execute(create_table_query)
    # 5. Commit the changes and close the connection
    connection.commit()
    connection.close()
    print("Database and raw_jobs table setup successfully!")

# Run the function

    

def fetch_raw_jobs():
    print("Fetching raw job postings...")
    
    # Create a list of 3 mock job dictionaries
    raw_data = [
        {
            "title": "Junior Data Analyst",
            "company": "DataCorp",
            "description": "Looking for an analyst comfortable with spreadsheets and data cleaning."
        },
        {
            "title": "Backend Software Engineer",
            "company": "TechSolutions",
            "description": "Building scalable web services. Experience with databases is required."
        },
        {
            "title": "Cloud Solutions Architect",
            "company": "Cloudify",
            "description": "Must have experience with AWS or Azure, and proficiency in python or java."
            
        }
    ]
    
    return raw_data

# Test the function

    

def store_raw_jobs(job_list):
    # 1. Connect to our existing database
    connection = sqlite3.connect("job_market.db")
    cursor = connection.cursor()
    
    # 2. Define the parameterized insert query
    # We don't insert 'id' because it autoincrements on its own!
    insert_query = """
    INSERT INTO raw_jobs (title, company, description) 
    VALUES (?, ?, ?);
    """
    
    # 3. Loop through each job dictionary and save it
    for job in job_list:
        # Extract values from the current job dictionary
        job_title = job["title"]
        job_company = job["company"]
        # YOUR TURN: Extract the description from the dictionary
        job_desc = job["description"]
        
        # 4. Execute the insert query
        # Hint: Pass a tuple of variables (job_title, job_company, job_desc) as the second argument
        cursor.execute(insert_query, (job_title, job_company, job_desc))
        
    # 5. Commit and close
    connection.commit()
    connection.close()
    print(f"Successfully saved {len(job_list)} raw jobs to the database!")



def process_job_skills():
    connection = sqlite3.connect("job_market.db")
    cursor = connection.cursor()
    
    # 1. Fetch all rows from the raw_jobs table
    cursor.execute("SELECT title, description FROM raw_jobs;")
    all_jobs = cursor.fetchall() # Returns a list of tuples: [(title, desc), (title, desc)...]
    
    # Define the list of technical skills we want to monitor
    target_skills = ["python", "sql", "java"]
    
    print("\n--- Processing Job Skills ---")
    
    for job in all_jobs:
        title = job[0]
        # Convert description to lowercase for easier matching
        description_lower = job[1].lower() 
        
        found_skills = []
        
        # 2. Loop through each skill in our target list and check the description
        for skill in target_skills:
            if skill in description_lower:
                found_skills.append(skill)
            # Hint: In Python, you can use the 'in' keyword!
            
            # # IF SKILL IS IN DESCRIPTION LOWER:
            #     found_skills.append(skill)
                
        print(f"Job: {title} | Skills Found: {found_skills}")
        
    connection.close()


    




def process_and_store_skills():
    connection = sqlite3.connect("job_market.db")
    cursor = connection.cursor()
    
    # 1. Create the new clean table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_skills (
        job_title TEXT,
        skill_found TEXT
    );
    """)
    
    # Fetch all data from raw_jobs
    cursor.execute("SELECT title, description FROM raw_jobs;")
    all_jobs = cursor.fetchall()
    
    target_skills = ["python", "sql", "java"]
    
    for job in all_jobs:
        title = job[0]
        description_lower = job[1].lower()
        
        for skill in target_skills:
            # Using your perfect fix from earlier!
            if skill in description_lower:
                
                # 2. YOUR TURN: Write the SQL query string to insert data 
                # into your new 'job_skills' table.
                # Hint: Use INSERT INTO job_skills (job_title, skill_found) VALUES (?, ?)
                insert_skill_query = """
                insert into job_skills(job_title, skill_found) values(?, ?)
                """
                
                # Execute the insertion passing a tuple of our variables
                cursor.execute(insert_skill_query, (title, skill))
                
    connection.commit()
    
    # 3. Aggregation Step: Count how many times each skill appears!
    print("\n--- FINAL JOB MARKET INSIGHTS ---")
    cursor.execute("""
    SELECT skill_found, COUNT(*) FROM job_skills GROUP BY skill_found;
    """)
    insights = cursor.fetchall()
    
    for row in insights:
        print(f"Skill: {row[0].upper()} | Total Demand: {row[1]} postings")
        
    connection.close()

if __name__ == "__main__":
    # Step 1: Initialize the database tables
    setup_database()
    
    # Step 2: Fetch the mock job listings into a variable
    jobs = fetch_raw_jobs()
    
    # Step 3: Insert those fetched jobs into the raw_jobs table
    store_raw_jobs(jobs)
    
    # Step 4: Extract the skills, save them, and print the final insights
    process_and_store_skills()