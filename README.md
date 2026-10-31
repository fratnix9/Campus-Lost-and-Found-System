Campus Lost and Found Management System
BCSE302L - Database Systems 
**Student:** Arahat Gaikwad (Reg No: 24BYB0182)  
**School:**  SCORE  
**Institution:** Vellore Institute of Technology (VIT), Vellore  
**Academic Year:** 2026–2027  
**Repository Link:** [https://github.com/fratnix9/Campus-Lost-and-Found-System](https://github.com/fratnix9/Campus-Lost-and-Found-System)

---

 🚀 Quick Start Guide: How to Open and Run the Project

> **Prerequisites:** Python 3.8 or higher installed.  
> **Zero Dependencies:** No external `pip` packages needed! The entire system is built using Python's native standard library (`http.server`, `sqlite3`, `json`, `urllib`).

---

 Step 1: Download or Clone the Repository
* **Option A:** Click the green **`<> Code`** button at the top of this GitHub page $\rightarrow$ select **`Download ZIP`**, then extract the ZIP on your PC.  
* **Option B:** Or clone via terminal:
  ```bash
  git clone https://github.com/fratnix9/Campus-Lost-and-Found-System.git
  cd Campus-Lost-and-Found-System
  ```

---

Step 2: Run the Web Application (This is the demonstration for Review III )

 🟢 Method A: The 1-Click Way (Windows)
* Simply **double-click `run_web_app.bat`** in the project folder.  
* This automatically starts the backend server and immediately opens **`http://127.0.0.1:5000`** in your default web browser!

🔵 Method B: Via Terminal / Command Prompt / VS Code
Open your terminal in the project directory and run:
```bash
python run_web_app.py
```
Then open your web browser and navigate to:  
👉 **`http://127.0.0.1:5000`** *(or `http://localhost:5000`)*

---

Step 3: Run the Interactive Terminal Console (This is the demonstration of Review II CLI)
If evaluating via command-line menu:
```bash
cd app
python app.py
```
* **Options 1–3:** Catalog search and incident filing.
* **Option 4:** Submit claim with procedural validation (`PROC_SUBMIT_CLAIM`).
* **Option 6:** Review pending claims queue and auto-update item status (`PROC_VERIFY_CLAIM`).
* **Option 7:** Explicit cursor batch scan of aging inventory.
* **Option 8:** Interactive runner for all 16 analytical queries.
* **Option 9:** Automated 5-step transaction walkthrough mode.

---

Step 4: Execute in Oracle Database (FreeSQL / SQL Developer / SQL*Plus) [I used FreeSQL] 
All relational SQL scripts are pre-packaged in the **`sql/`** directory:
1. Connect to your Oracle database schema.
2. Run the master script:
   ```sql
   @sql/06_master_run_all.sql
   ```
   Or execute individual scripts in sequence:
   * `sql/01_create_tables.sql` (DDL & 3NF Schema Constraints)
   * `sql/02_insert_sample_data.sql` (72+ Records across 7 tables)
   * `sql/04_plsql_components.sql` (Stored Procedures, Functions, Triggers & Cursors)
   * `sql/03_queries.sql` (16 Analytical SQL Queries)
   * `sql/05_dml_demonstration.sql` (DML Verification & Transaction Rollback tests)

---
📁 Project Directory Structure

```
Campus_Lost_and_Found_System/
├── sql/
│   ├── 01_create_tables.sql      # DDL: 7 Tables in 3NF, PKs, FKs (CASCADE), CHECK, UNIQUE
│   ├── 02_insert_sample_data.sql # DML: 72+ Realistic campus records (10+ per table)
│   ├── 03_queries.sql            # 16 Meaningful SQL queries (Joins, Aggregations, Subqueries)
│   ├── 04_plsql_components.sql   # PL/SQL: Stored Procedures, Functions, Cursors & Triggers
│   ├── 05_dml_demonstration.sql  # DML Transaction Tests: INSERT, UPDATE, DELETE verification
│   └── 06_master_run_all.sql     # Single master runner for Oracle FreeSQL / SQL Developer
├── app/
│   ├── web_app.py                # Zero-dependency Python Web Application Server (REST APIs)
│   ├── database.py               # Data Access Layer (SQLite Engine + Oracle Connector)
│   ├── app.py                    # Interactive Terminal Console Menu System
│   ├── campus_lost_found.db      # Pre-populated Relational Database
│   └── requirements.txt          # Python dependencies
├── docs/
│   ├── ER_Diagram.png            # Complete Entity-Relationship Diagram (Crow's Foot)
│   └── Workflow_Diagram.png      # Campus Operational Lifecycle Model
├── screenshots/                  # Authentic Execution Proofs & Interface Captures
├── run_web_app.bat               # Windows 1-Click Application Launcher
├── run_web_app.py                # Python Web Server & Auto-Browser Launcher
├── .gitignore                    # Standard clean Git ignore rules
└── README.md                     # Project Documentation & Evaluation Guide
```

---

📊 Summary of Syllabus & Evaluation Compliance

| Evaluation Component | Implementation in Project | File Reference |
| :--- | :--- | :--- |
| **7 Normalized Tables (3NF)** | Exactly 7 tables (`STUDENT`, `LOCATION`, `ADMIN`, `ITEM`, `LOST_REPORT`, `FOUND_REPORT`, `CLAIM`) | `sql/01_create_tables.sql` |
| **Integrity Constraints** | 9 Foreign Keys (`ON DELETE CASCADE`), `CHECK (status IN ...)`, `UNIQUE` on emails | `sql/01_create_tables.sql` |
| **Realistic Dataset** | 72+ records populated across 7 tables (10+ records/table) | `sql/02_insert_sample_data.sql` |
| **16 Analytical Queries** | 3-Table & 4-Table Joins, `GROUP BY`, `HAVING`, `NOT EXISTS`, `DENSE_RANK()` | `sql/03_queries.sql` |
| **Procedural Transactions** | `PROC_SUBMIT_CLAIM`, `PROC_VERIFY_CLAIM`, `FUNC_CALCULATE_UNCLAIMED_DAYS` | `sql/04_plsql_components.sql` |
| **Database Triggers** | `TRG_PREVENT_CLAIM_ON_RETURNED` (Abort `ORA-20001`), `TRG_AUTO_UPDATE_ITEM_STATUS` | `sql/04_plsql_components.sql` |
| **Explicit Cursor** | `cur_unclaimed_items` in `PROC_FLAG_LONG_UNCLAIMED_ITEMS` (5-stage lifecycle) | `sql/04_plsql_components.sql` |
| **Integrated Multi-Tier App** | Dual frontends: Web Portal (`web_app.py`) & Terminal Console (`app.py`) | `app/web_app.py`, `app/app.py` |
