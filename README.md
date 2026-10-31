# Campus Lost and Found Management System
### BCSE302L - Database Systems | Course Project Implementation
**Student:** Arahat Gaikwad (Reg No: 24BYB0182)  
**Institution:** Vellore Institute of Technology (VIT), Vellore

---

## 📁 Project Structure

```
Campus_Lost_and_Found_Project/
├── sql/
│   ├── 01_create_tables.sql      # DDL: 7 Tables, PKs, FKs, CHECK, UNIQUE, NOT NULL, DEFAULT
│   ├── 02_insert_sample_data.sql # DML: Realistic dataset (10+ records per table)
│   ├── 03_queries.sql            # 16 Meaningful SQL queries (Joins, Aggregation, Subqueries, Sets)
│   ├── 04_plsql_components.sql   # PL/SQL: 2 Procedures, 2 Functions, 1 Explicit Cursor, 2 Triggers
│   ├── 05_dml_demonstration.sql  # DML Demonstration: INSERT, UPDATE, DELETE with before/after checks
│   └── 06_master_run_all.sql     # Single script runner for Oracle SQL Developer / SQL*Plus / APEX
├── app/
│   ├── database.py               # Database layer (SQLite embedded engine + Oracle connector)
│   ├── app.py                    # Interactive Python Terminal Demonstration System
│   └── requirements.txt          # Python dependencies (Optional: oracledb for live Oracle connection)
└── docs/
    ├── Campus_Lost_and_Found_Project_Report.md  # Complete 10-section project report
    ├── ER_Diagram.png                           # Visual ER Diagram
    └── Workflow_Diagram.png                     # Campus Workflow Diagram
```

---

## 🚀 Quick Start Guide

### Option 1: Run the Interactive Python Demonstration System (Recommended for Viva)
No database installation or server setup is required. The embedded engine is pre-loaded with the entire schema, constraints, triggers, and sample data.

```bash
cd "Campus_Lost_and_Found_Project/app"
python app.py
```

#### Application Features:
* **Option 1 & 2:** Student Portal (Report Lost / Found Items)
* **Option 3:** Search Catalog by keyword, category, or location
* **Option 4:** Submit Claim with Proof (`PROC_SUBMIT_CLAIM`)
* **Option 5:** Student Activity Summary (`FUNC_GET_STUDENT_ACTIVITY`)
* **Option 6:** Admin Claim Verification (`PROC_VERIFY_CLAIM` & Trigger)
* **Option 7:** Batch Cursor Audit of Long-Unclaimed Items (`PROC_FLAG_LONG_UNCLAIMED_ITEMS`)
* **Option 8:** Interactive Viewer for all 16 SQL Queries with formatted tables
* **Option 9:** **Review III Walkthrough Mode:** Step-by-step demonstration of the 5 Real-World Transactions answering all viva questions!

---

### Option 2: Execute in Oracle SQL Developer / SQL*Plus / Oracle APEX
To run the full suite in Oracle Database (19c/21c/XE/LiveSQL):

1. Open **Oracle SQL Developer** or launch `sqlplus`.
2. Connect to your schema.
3. Run the master script:
   ```sql
   @Campus_Lost_and_Found_Project/sql/06_master_run_all.sql
   ```
   Or execute individual scripts in order:
   * `01_create_tables.sql`
   * `02_insert_sample_data.sql`
   * `04_plsql_components.sql`
   * `03_queries.sql`
   * `05_dml_demonstration.sql`

---

## 📊 Summary of Guideline Compliance

| Guideline Requirement | Project Implementation | File Reference |
| :--- | :--- | :--- |
| **6–8 Related Tables** | Exactly **7 Normalized Tables** (`LOCATION`, `STUDENT`, `ADMIN`, `ITEM`, `LOST_REPORT`, `FOUND_REPORT`, `CLAIM`) | `sql/01_create_tables.sql` |
| **Constraints** | PK, FK (9 links), `NOT NULL`, `UNIQUE` (emails), `CHECK` (statuses), `DEFAULT` (`SYSDATE`, `'PENDING'`) | `sql/01_create_tables.sql` |
| **10+ Records per Table** | Complete seed data with 10–12 records per table (70+ total rows) | `sql/02_insert_sample_data.sql` |
| **15+ Meaningful Queries** | 16 queries covering Inner/Left Joins, Group By, Having, Subqueries (`IN`, `NOT EXISTS`, Correlated), `UNION ALL`, `LIKE`, `DENSE_RANK()` | `sql/03_queries.sql` |
| **2 Procedures & 2 Functions** | • `PROC_SUBMIT_CLAIM`<br>• `PROC_VERIFY_CLAIM`<br>• `FUNC_CALCULATE_UNCLAIMED_DAYS`<br>• `FUNC_GET_STUDENT_ACTIVITY` | `sql/04_plsql_components.sql` |
| **1 Explicit Cursor** | `cur_unclaimed_items` in `PROC_FLAG_LONG_UNCLAIMED_ITEMS` with `OPEN`, `FETCH`, `CLOSE` loop | `sql/04_plsql_components.sql` |
| **2 Triggers** | • `TRG_PREVENT_CLAIM_ON_RETURNED` (BEFORE INSERT)<br>• `TRG_AUTO_UPDATE_ITEM_STATUS` (AFTER UPDATE) | `sql/04_plsql_components.sql` |
| **DML Demonstration** | Clear INSERT, UPDATE, and DELETE operations with before/after state verification | `sql/05_dml_demonstration.sql` |
| **Database Connectivity** | Python 3 application connecting via SQLite & Oracle Database (`oracledb`) | `app/app.py`, `app/database.py` |
| **Project Report** | Full 10-section formal report with diagrams, relational schema, queries, and transaction demonstrations | `docs/Campus_Lost_and_Found_Project_Report.md` |
