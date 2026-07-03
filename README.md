# 📊 Automated Job Market Intelligence Pipeline

**A lightweight ETL (Extract, Transform, Load) pipeline designed to programmatically analyze real-time market demand for core programming languages.**

This tool automates the ingestion of unstructured job description texts, filters them for targeted developer skill sets (e.g., Python, SQL, Java), and aggregates the findings into an optimized database to expose hiring trends.

---

## 🛠️ Tech Stack & Architecture Breakdown

- **Core Language:** Python 3.x (Modular function design and control flow logic)
- **Database Layer:** SQLite3 (Relational database management, structural schema design)
- **SQL Techniques Engine:** Data definition (`CREATE TABLE`), parameterized manipulation (`INSERT INTO`), and metrics aggregation (`COUNT`, `GROUP BY`)

---

## 🏗️ Key Engineering Challenges Solved

### Overcoming Data Pipeline Deserialization & Execution Order
- **The Challenge:** During initial testing, the data aggregation layer executed flawlessly but yielded empty tables and zero market insights.
- **The Root Cause:** The script suffered from an execution order bug where data reading and text processing functions were triggered before the database ingestion engine could populate the tables.
- **The Solution:** I refactored the execution engine to enforce strict chronological orchestration. By sequencing the pipeline into isolated phases (Setup ➡️ Ingest ➡️ Store ➡️ Process), I eliminated data races and ensured clean state management.
