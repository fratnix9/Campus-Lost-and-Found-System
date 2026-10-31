"""
Campus Lost and Found Management System
Interactive Terminal Application & Demonstration Suite
VIT - BCSE302L Database Systems Course Project
Author: Arahat Gaikwad (24BYB0182)
"""

import sys
import os
from datetime import datetime
from database import Database

db = Database(db_type="sqlite")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "=" * 75)
    print(f"  {title.center(71)}")
    print("=" * 75)

def print_table(headers, rows):
    if not rows:
        print("\n  [No records found.]\n")
        return

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            val_str = str(val) if val is not None else "NULL"
            if len(val_str) > widths[i]:
                widths[i] = min(len(val_str), 35)

    # Format header
    header_str = " | ".join(f"{h:<{widths[i]}}" for i, h in enumerate(headers))
    divider_str = "-+-".join("-" * widths[i] for i in range(len(headers)))
    
    print("\n" + header_str)
    print(divider_str)
    for row in rows:
        row_str = " | ".join(f"{(str(val) if val is not None else 'NULL')[:widths[i]]:<{widths[i]}}" for i, val in enumerate(row))
        print(row_str)
    print(f"\n  Total Records: {len(rows)}\n")

# =============================================================================
# STUDENT PORTAL FUNCTIONS
# =============================================================================

def student_report_lost():
    print_header("STUDENT PORTAL: REPORT A LOST ITEM")
    student_id = input("Enter your Student Reg No (e.g., 24BYB0182): ").strip().upper()
    
    # Check student
    res = db.execute_query("SELECT name FROM STUDENT WHERE student_id = ?", (student_id,))
    if not res:
        print(f"[!] Student ID '{student_id}' not found. Please register student first.")
        return

    student_name = res[0]['name']
    print(f"[+] Welcome, {student_name}!")
    
    item_name = input("Enter Item Name (e.g., Blue Fastrack Bottle): ").strip()
    category = input("Enter Category (Electronics/Identity Cards/Personal Accessories/Books & Study Material/Keys/Wallets & Bags): ").strip()
    description = input("Enter Description & Identifying marks: ").strip()
    
    # Show locations
    locations = db.execute_query("SELECT location_id, location_name, building FROM LOCATION")
    print("\nAvailable Campus Locations:")
    for loc in locations:
        print(f"  [{loc['location_id']}] {loc['location_name']} - {loc['building']}")
    
    try:
        location_id = int(input("Select Location ID where you lost it: ").strip())
    except ValueError:
        print("[!] Invalid location ID.")
        return

    # Execute User Operation -> SQL INSERT
    # Compute new IDs
    max_item = db.execute_query("SELECT COALESCE(MAX(item_id), 1000) + 1 AS next_id FROM ITEM")[0]['next_id']
    max_rep = db.execute_query("SELECT COALESCE(MAX(lost_report_id), 200) + 1 AS next_id FROM LOST_REPORT")[0]['next_id']
    
    today = datetime.now().strftime("%Y-%m-%d")
    db.execute_dml(
        "INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id) VALUES (?, ?, ?, ?, ?, 'LOST', ?, ?)",
        (max_item, item_name, description, category, today, location_id, student_id)
    )
    db.execute_dml(
        "INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details) VALUES (?, ?, ?, ?, ?)",
        (max_rep, max_item, student_id, today, description)
    )

    print("\n" + "-" * 75)
    print("  TRANSACTION SUMMARY (Interactive Database Flow)")
    print("-" * 75)
    print(f"  Operation:           Report Lost Belonging")
    print(f"  Tables Involved:     ITEM, LOST_REPORT")
    print(f"  Item Record Created: ID #{max_item} ('{item_name}') with Status 'LOST'")
    print(f"  Incident Filed:      Report #{max_rep} linked to Student {student_id}")
    print("-" * 75)

def student_report_found():
    print_header("STUDENT PORTAL: REPORT A FOUND ITEM")
    student_id = input("Enter your Student Reg No (e.g., 24BYB0182): ").strip().upper()
    
    res = db.execute_query("SELECT name FROM STUDENT WHERE student_id = ?", (student_id,))
    if not res:
        print(f"[!] Student ID '{student_id}' not found.")
        return

    student_name = res[0]['name']
    print(f"[+] Welcome, {student_name}!")
    
    item_name = input("Enter Item Name (e.g., Apple Pencil): ").strip()
    category = input("Enter Category (Electronics/Identity Cards/Personal Accessories/Books & Study Material/Keys/Wallets & Bags): ").strip()
    description = input("Enter Visual Description & Found State: ").strip()
    
    locations = db.execute_query("SELECT location_id, location_name, building FROM LOCATION")
    print("\nCampus Locations:")
    for loc in locations:
        print(f"  [{loc['location_id']}] {loc['location_name']} - {loc['building']}")
    
    try:
        location_id = int(input("Select Location ID where found: ").strip())
    except ValueError:
        print("[!] Invalid location ID.")
        return

    max_item = db.execute_query("SELECT COALESCE(MAX(item_id), 1000) + 1 AS next_id FROM ITEM")[0]['next_id']
    max_rep = db.execute_query("SELECT COALESCE(MAX(found_report_id), 300) + 1 AS next_id FROM FOUND_REPORT")[0]['next_id']
    today = datetime.now().strftime("%Y-%m-%d")

    db.execute_dml(
        "INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id) VALUES (?, ?, ?, ?, ?, 'FOUND', ?, ?)",
        (max_item, item_name, description, category, today, location_id, student_id)
    )
    db.execute_dml(
        "INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details) VALUES (?, ?, ?, ?, ?)",
        (max_rep, max_item, student_id, today, description)
    )

    print("\n" + "-" * 75)
    print("  TRANSACTION SUMMARY (Interactive Database Flow)")
    print("-" * 75)
    print(f"  Operation:           Report Discovered Item")
    print(f"  Tables Involved:     ITEM, FOUND_REPORT")
    print(f"  Item Record Created: ID #{max_item} ('{item_name}') with Status 'FOUND'")
    print(f"  Incident Filed:      Report #{max_rep} turned in by {student_id}")
    print("-" * 75)

def search_items():
    print_header("CAMPUS LOST & FOUND SEARCH ENGINE")
    keyword = input("Search by keyword (Item name or description) or [Enter] for all: ").strip()
    
    sql = """
    SELECT 
        i.item_id,
        i.item_name,
        i.category,
        i.status,
        i.date_reported,
        l.location_name || ' (' || l.building || ')' AS location,
        s.name AS reported_by
    FROM ITEM i
    JOIN LOCATION l ON i.location_id = l.location_id
    JOIN STUDENT s ON i.reported_by_student_id = s.student_id
    WHERE (LOWER(i.item_name) LIKE ? OR LOWER(i.description) LIKE ? OR LOWER(i.category) LIKE ?)
    ORDER BY i.date_reported DESC
    """
    param = f"%{keyword.lower()}%"
    rows = db.execute_query(sql, (param, param, param))
    headers = ["Item ID", "Item Name", "Category", "Status", "Date Reported", "Location", "Reported By"]
    print_table(headers, rows)

def student_submit_claim():
    print_header("STUDENT PORTAL: SUBMIT A CLAIM FOR A FOUND ITEM")
    student_id = input("Enter your Student Reg No: ").strip().upper()
    
    res = db.execute_query("SELECT name FROM STUDENT WHERE student_id = ?", (student_id,))
    if not res:
        print("[!] Student ID not registered.")
        return

    # Show found items
    sql = """
    SELECT i.item_id, i.item_name, i.category, i.status, l.building
    FROM ITEM i
    JOIN LOCATION l ON i.location_id = l.location_id
    WHERE i.status IN ('FOUND', 'LOST')
    """
    rows = db.execute_query(sql)
    print("\nAvailable Items Eligible for Verification:")
    print_table(["Item ID", "Item Name", "Category", "Status", "Building"], rows)
    
    try:
        item_id = int(input("Enter the Item ID you wish to claim: ").strip())
    except ValueError:
        print("[!] Invalid Item ID.")
        return

    proof = input("Describe your proof of ownership (e.g. serial number, unique marks, lock combination): ").strip()
    if not proof:
        print("[!] Proof description is mandatory.")
        return

    # Simulated Procedure: PROC_SUBMIT_CLAIM
    item_rows = db.execute_query("SELECT item_name, status FROM ITEM WHERE item_id = ?", (item_id,))
    if not item_rows:
        print(f"[!] Item ID {item_id} does not exist.")
        return

    item_status = item_rows[0]['status']
    
    # Check trigger / business rule: Cannot claim returned items
    if item_status == 'RETURNED':
        print(f"\n[TRIGGER BLOCKED]: Integrity Rule Violation! Item #{item_id} is already RETURNED to owner.")
        return

    # Check for duplicate claim
    dup = db.execute_query("SELECT claim_id FROM CLAIM WHERE item_id = ? AND claimant_student_id = ? AND claim_status = 'PENDING'", (item_id, student_id))
    if dup:
        print(f"\n[!] Duplicate Claim: You already have a PENDING claim (Claim #{dup[0]['claim_id']}) for this item.")
        return

    max_claim = db.execute_query("SELECT COALESCE(MAX(claim_id), 400) + 1 AS next_id FROM CLAIM")[0]['next_id']
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        db.execute_dml(
            "INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status) VALUES (?, ?, ?, ?, ?, 'PENDING')",
            (max_claim, item_id, student_id, today, proof)
        )
        print("\n" + "-" * 75)
        print("  TRANSACTION SUMMARY (Interactive Database Flow)")
        print("-" * 75)
        print(f"  Operation:           PROC_SUBMIT_CLAIM Execution")
        print(f"  Table Affected:      CLAIM")
        print(f"  Claim Created:       Claim ID #{max_claim}")
        print(f"  Item Claimed:        Item #{item_id} ('{item_rows[0]['item_name']}')")
        print(f"  Status:              PENDING (Awaiting Campus Security/Admin Review)")
        print("-" * 75)
    except Exception as e:
        print(f"[DATABASE ERROR / TRIGGER TRIGGERED]: {e}")

def view_my_activity():
    print_header("STUDENT PROFILE & ACTIVITY HISTORY")
    student_id = input("Enter your Student Reg No: ").strip().upper()
    
    res = db.execute_query("SELECT * FROM STUDENT WHERE student_id = ?", (student_id,))
    if not res:
        print("[!] Student not found.")
        return

    st = res[0]
    print(f"\nStudent Details: {st['name']} ({st['student_id']}) | Email: {st['email']} | Phone: {st['phone']}")
    
    # Function 2 Demonstration: FUNC_GET_STUDENT_ACTIVITY
    lost_c = db.execute_query("SELECT COUNT(*) AS c FROM LOST_REPORT WHERE student_id = ?", (student_id,))[0]['c']
    found_c = db.execute_query("SELECT COUNT(*) AS c FROM FOUND_REPORT WHERE student_id = ?", (student_id,))[0]['c']
    claim_c = db.execute_query("SELECT COUNT(*) AS c FROM CLAIM WHERE claimant_student_id = ?", (student_id,))[0]['c']
    appr_c = db.execute_query("SELECT COUNT(*) AS c FROM CLAIM WHERE claimant_student_id = ? AND claim_status = 'APPROVED'", (student_id,))[0]['c']
    
    print(f"\n[PL/SQL FUNCTION RESULT: FUNC_GET_STUDENT_ACTIVITY]")
    print(f"  -> Lost Reports Filed:     {lost_c}")
    print(f"  -> Found Reports Handed:   {found_c}")
    print(f"  -> Claims Submitted:       {claim_c} (Approved: {appr_c})")

    # My Claims
    claims = db.execute_query("""
    SELECT c.claim_id, i.item_name, c.claim_date, c.claim_status, COALESCE(a.name, 'Under Review') AS reviewed_by
    FROM CLAIM c
    JOIN ITEM i ON c.item_id = i.item_id
    LEFT JOIN ADMIN a ON c.admin_id = a.admin_id
    WHERE c.claimant_student_id = ?
    """, (student_id,))
    print("\nMy Claims History:")
    print_table(["Claim ID", "Item Name", "Date Filed", "Status", "Reviewed By"], claims)

# =============================================================================
# ADMIN PORTAL FUNCTIONS
# =============================================================================

def admin_review_claims():
    print_header("ADMINISTRATIVE PORTAL: CLAIM VERIFICATION QUEUE")
    
    sql = """
    SELECT 
        c.claim_id,
        c.item_id,
        i.item_name,
        i.category,
        s.student_id AS claimant_id,
        s.name AS claimant_name,
        c.proof_description,
        c.claim_date
    FROM CLAIM c
    JOIN ITEM i ON c.item_id = i.item_id
    JOIN STUDENT s ON c.claimant_student_id = s.student_id
    WHERE c.claim_status = 'PENDING'
    ORDER BY c.claim_date ASC
    """
    pending = db.execute_query(sql)
    if not pending:
        print("\n  [+] All claims are up to date! No pending claims to review.\n")
        return

    print_table(["Claim ID", "Item ID", "Item Name", "Category", "Claimant ID", "Claimant Name", "Proof", "Date"], pending)

    try:
        claim_id = int(input("Enter Claim ID to verify (or 0 to cancel): ").strip())
        if claim_id == 0:
            return
    except ValueError:
        print("[!] Invalid Claim ID.")
        return

    claim_match = [r for r in pending if r['claim_id'] == claim_id]
    if not claim_match:
        print(f"[!] Claim #{claim_id} is not in the pending queue.")
        return

    target = claim_match[0]
    print(f"\nReviewing Claim #{claim_id} for '{target['item_name']}' filed by {target['claimant_name']}.")
    print(f"Claimant's Proof: \"{target['proof_description']}\"")
    
    # Select Admin
    admins = db.execute_query("SELECT admin_id, name FROM ADMIN")
    print("\nCampus Security / Admin Reviewers:")
    for a in admins:
        print(f"  [{a['admin_id']}] {a['name']}")
    try:
        admin_id = int(input("Select your Admin ID: ").strip())
    except ValueError:
        print("[!] Invalid Admin ID.")
        return

    decision = input("Enter Decision (APPROVE / REJECT): ").strip().upper()
    if decision not in ('APPROVE', 'REJECT'):
        print("[!] Decision must be APPROVE or REJECT.")
        return

    # Simulated Procedure: PROC_VERIFY_CLAIM
    if decision == 'APPROVE':
        # Update Claim to APPROVED
        db.execute_dml("UPDATE CLAIM SET claim_status = 'APPROVED', admin_id = ? WHERE claim_id = ?", (admin_id, claim_id))
        # Trigger 2 Fires automatically / Item update:
        db.execute_dml("UPDATE ITEM SET status = 'RETURNED' WHERE item_id = ?", (target['item_id'],))
        # Reject any other pending claims for this item
        db.execute_dml("UPDATE CLAIM SET claim_status = 'REJECTED', admin_id = ? WHERE item_id = ? AND claim_id != ? AND claim_status = 'PENDING'", (admin_id, target['item_id'], claim_id))
        
        print("\n" + "-" * 75)
        print("  TRANSACTION SUMMARY (Interactive Database Flow)")
        print("-" * 75)
        print(f"  Operation:           PROC_VERIFY_CLAIM [APPROVED]")
        print(f"  Trigger Fired:       TRG_AUTO_UPDATE_ITEM_STATUS")
        print(f"  Claim Table:         Claim #{claim_id} updated to 'APPROVED'")
        print(f"  Item Table:          Item #{target['item_id']} ('{target['item_name']}') status automatically set to 'RETURNED'")
        print(f"  Conflict Resolution: Other pending claims for Item #{target['item_id']} automatically REJECTED")
        print("-" * 75)
    else:
        db.execute_dml("UPDATE CLAIM SET claim_status = 'REJECTED', admin_id = ? WHERE claim_id = ?", (admin_id, claim_id))
        print("\n" + "-" * 75)
        print("  TRANSACTION SUMMARY (Interactive Database Flow)")
        print("-" * 75)
        print(f"  Operation:           PROC_VERIFY_CLAIM [REJECTED]")
        print(f"  Claim Table:         Claim #{claim_id} updated to 'REJECTED' by Admin #{admin_id}")
        print(f"  Item Status:         Remains '{target['item_name']}' for other potential claimants")
        print("-" * 75)

def admin_cursor_audit():
    print_header("ADMIN BATCH AUDIT: EXPLICIT CURSOR SIMULATION")
    print("Requirement: At least 1 Cursor for processing multiple records (FR12)")
    
    try:
        threshold = int(input("Enter minimum days threshold to flag unclaimed items (e.g., 0, 5, 10): ").strip())
    except ValueError:
        threshold = 0

    # PL/SQL Cursor Simulation
    sql = """
    SELECT 
        i.item_id,
        i.item_name,
        i.category,
        i.status,
        i.date_reported,
        l.location_name,
        l.building
    FROM ITEM i
    JOIN LOCATION l ON i.location_id = l.location_id
    WHERE i.status IN ('LOST', 'FOUND')
    ORDER BY i.date_reported ASC
    """
    items = db.execute_query(sql)
    
    print("\n" + "=" * 75)
    print(f"  BATCH CURSOR AUDIT: ITEMS UNRESOLVED >= {threshold} DAYS")
    print("=" * 75)
    
    flagged = []
    today = datetime.now()
    
    # Cursor loop
    for item in items:
        rep_date = datetime.strptime(item['date_reported'], "%Y-%m-%d")
        days = (today - rep_date).days
        if days >= threshold:
            flagged.append((item['item_id'], item['item_name'], item['category'], item['status'], f"{days} days", item['building']))

    print_table(["Item ID", "Item Name", "Category", "Status", "Age", "Building"], flagged)
    print(f"[+] Total items flagged by cursor scan: {len(flagged)}")

# =============================================================================
# 15 PREDEFINED SQL QUERIES RUNNER
# =============================================================================

QUERIES = [
    ("Query 1: Items Available in 'FOUND' Status", "SELECT item_id, item_name, category, date_reported, status FROM ITEM WHERE status = 'FOUND' ORDER BY date_reported ASC"),
    ("Query 2: Multi-Table Inner Join (Item + Reporter + Location)", """SELECT i.item_id, i.item_name, i.category, i.status, s.student_id, s.name AS reporter, l.building 
      FROM ITEM i JOIN STUDENT s ON i.reported_by_student_id = s.student_id JOIN LOCATION l ON i.location_id = l.location_id"""),
    ("Query 3: Left Outer Join (Items and their Claims)", """SELECT i.item_id, i.item_name, i.status, COALESCE(c.claim_id, 'NO CLAIM') AS claim_id, COALESCE(c.claim_status, 'UNCLAIMED') AS status 
      FROM ITEM i LEFT JOIN CLAIM c ON i.item_id = c.item_id"""),
    ("Query 4: Category Aggregation & Breakdown", """SELECT category, COUNT(item_id) AS total, 
      SUM(CASE WHEN status='LOST' THEN 1 ELSE 0 END) AS lost, 
      SUM(CASE WHEN status='FOUND' THEN 1 ELSE 0 END) AS found, 
      SUM(CASE WHEN status IN ('CLAIMED', 'RETURNED') THEN 1 ELSE 0 END) AS resolved 
      FROM ITEM GROUP BY category ORDER BY total DESC"""),
    ("Query 5: Campus Locations with Multiple Incidents (HAVING)", """SELECT l.building, COUNT(i.item_id) AS incidents 
      FROM LOCATION l JOIN ITEM i ON l.location_id = i.location_id GROUP BY l.building HAVING COUNT(i.item_id) >= 2"""),
    ("Query 6: Students who Reported Lost Items but Never Claimed (IN)", """SELECT student_id, name, email FROM STUDENT 
      WHERE student_id IN (SELECT student_id FROM LOST_REPORT) AND student_id NOT IN (SELECT claimant_student_id FROM CLAIM)"""),
    ("Query 7: Unclaimed Items (NOT EXISTS)", """SELECT i.item_id, i.item_name, i.category, i.status FROM ITEM i 
      WHERE NOT EXISTS (SELECT 1 FROM CLAIM c WHERE c.item_id = i.item_id)"""),
    ("Query 8: Correlated Subquery (Claims Count per Item)", """SELECT i.item_id, i.item_name, i.status, 
      (SELECT COUNT(*) FROM CLAIM c WHERE c.item_id = i.item_id) AS total_claims FROM ITEM i ORDER BY total_claims DESC"""),
    ("Query 9: Unified Activity Feed (UNION ALL)", """SELECT 'LOST' AS type, i.item_name, lr.date_lost AS event_date, s.name FROM LOST_REPORT lr JOIN ITEM i ON lr.item_id = i.item_id JOIN STUDENT s ON lr.student_id = s.student_id 
      UNION ALL 
      SELECT 'FOUND' AS type, i.item_name, fr.date_found AS event_date, s.name FROM FOUND_REPORT fr JOIN ITEM i ON fr.item_id = i.item_id JOIN STUDENT s ON fr.student_id = s.student_id 
      ORDER BY event_date DESC"""),
    ("Query 10: Pattern Matching Search (LIKE)", """SELECT item_id, item_name, description, category FROM ITEM 
      WHERE LOWER(item_name) LIKE '%airpods%' OR LOWER(description) LIKE '%charger%' OR LOWER(item_name) LIKE '%calculator%'"""),
    ("Query 11: Date Arithmetic (Days in System)", """SELECT item_id, item_name, status, date_reported, 
      CAST((julianday('now') - julianday(date_reported)) AS INTEGER) AS days_in_system FROM ITEM ORDER BY days_in_system DESC"""),
    ("Query 12: 4-Table Join (Approved Claims Audit)", """SELECT c.claim_id, s.name AS claimant, i.item_name, l.building, a.name AS approved_by, c.claim_date 
      FROM CLAIM c JOIN STUDENT s ON c.claimant_student_id = s.student_id JOIN ITEM i ON c.item_id = i.item_id JOIN LOCATION l ON i.location_id = l.location_id JOIN ADMIN a ON c.admin_id = a.admin_id 
      WHERE c.claim_status = 'APPROVED'"""),
    ("Query 13: Subquery Comparison Against System Average", """SELECT item_id, item_name, category, status FROM ITEM 
      WHERE (julianday('now') - julianday(date_reported)) >= (SELECT AVG(julianday('now') - julianday(date_reported)) FROM ITEM)"""),
    ("Query 14: Admin Performance Breakdown (Conditional Aggregation)", """SELECT a.admin_id, a.name, COUNT(c.claim_id) AS total_reviewed, 
      SUM(CASE WHEN c.claim_status = 'APPROVED' THEN 1 ELSE 0 END) AS approved, 
      SUM(CASE WHEN c.claim_status = 'REJECTED' THEN 1 ELSE 0 END) AS rejected 
      FROM ADMIN a LEFT JOIN CLAIM c ON a.admin_id = c.admin_id GROUP BY a.admin_id, a.name"""),
    ("Query 15: Incident Frequency Ranking per Category", """SELECT category, COUNT(*) AS total_items, 
      DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS category_rank FROM ITEM GROUP BY category"""),
    ("Query 16: Competing Claims Detection (HAVING)", """SELECT c.item_id, i.item_name, COUNT(c.claim_id) AS claims_count 
      FROM CLAIM c JOIN ITEM i ON c.item_id = i.item_id GROUP BY c.item_id, i.item_name HAVING COUNT(c.claim_id) > 1""")
]

def run_query_viewer():
    print_header("15+ MEANINGFUL SQL QUERIES VIEWER")
    for idx, (title, _) in enumerate(QUERIES, 1):
        print(f"  [{idx:2d}] {title}")
    print("  [ 0] Return to Main Menu")
    
    try:
        choice = int(input("\nSelect Query Number to Execute (0-16): ").strip())
        if choice == 0:
            return
        if 1 <= choice <= len(QUERIES):
            title, sql = QUERIES[choice - 1]
            print_header(title)
            print(f"Executed SQL:\n{sql}\n")
            cursor = db.conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]
            print_table(headers, rows)
        else:
            print("[!] Invalid selection.")
    except ValueError:
        print("[!] Invalid number.")

# =============================================================================
# REVIEW 3 DEMONSTRATION WALKTHROUGH (5 REAL-WORLD TRANSACTIONS)
# =============================================================================

def run_review3_walkthrough():
    print_header("REVIEW III: 5 REAL-WORLD TRANSACTION FLOW DEMONSTRATION")
    print("Demonstrating: User Operation -> SQL/PL/SQL -> Database Processing -> Database Update -> Result")
    
    transactions = [
        {
            "num": 1,
            "title": "Student Files a Lost Report for Misplaced ID Card",
            "operation": "INSERT into ITEM and LOST_REPORT",
            "tables": "ITEM, LOST_REPORT, LOCATION, STUDENT",
            "component": "INSERT INTO ITEM (...) and INSERT INTO LOST_REPORT (...)",
            "effect": "Creates item ID with status 'LOST' and logs student contact information.",
            "action": lambda: db.execute_dml(
                "INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id) VALUES (1088, 'Titan Blue Backpack', 'Contains notebook and geometry box', 'Personal Accessories', DATE('now'), 'LOST', 105, '24BYB0182')"
            )
        },
        {
            "num": 2,
            "title": "Good Samaritan Discovers Backpack and Files Found Report",
            "operation": "INSERT into FOUND_REPORT and UPDATE ITEM",
            "tables": "ITEM, FOUND_REPORT, STUDENT",
            "component": "INSERT INTO FOUND_REPORT (...) and UPDATE ITEM status to 'FOUND'",
            "effect": "Flags backpack as FOUND at TT Room 214 and notifies campus system.",
            "action": lambda: db.execute_dml("UPDATE ITEM SET status = 'FOUND' WHERE item_id = 1088")
        },
        {
            "num": 3,
            "title": "Owner Discovers Match and Files Claim with Proof",
            "operation": "PROC_SUBMIT_CLAIM (Procedure)",
            "tables": "CLAIM, ITEM, STUDENT",
            "component": "PROC_SUBMIT_CLAIM validates student & creates claim with status 'PENDING'",
            "effect": "Inserts Claim #488 with proof description: 'Notebook has my name Arahat Gaikwad'.",
            "action": lambda: db.execute_dml(
                "INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status) VALUES (488, 1088, '24BYB0182', DATE('now'), 'Notebook inside has my name Arahat Gaikwad', 'PENDING')"
            )
        },
        {
            "num": 4,
            "title": "Security Officer Verifies Proof and Approves Claim",
            "operation": "PROC_VERIFY_CLAIM (Procedure) & TRG_AUTO_UPDATE_ITEM_STATUS (Trigger)",
            "tables": "CLAIM, ITEM, ADMIN",
            "component": "PROC_VERIFY_CLAIM updates CLAIM to 'APPROVED', Trigger automatically updates ITEM to 'RETURNED'",
            "effect": "Claim #488 approved by Admin #2; Backpack marked 'RETURNED' in ITEM table.",
            "action": lambda: (
                db.execute_dml("UPDATE CLAIM SET claim_status = 'APPROVED', admin_id = 2 WHERE claim_id = 488"),
                db.execute_dml("UPDATE ITEM SET status = 'RETURNED' WHERE item_id = 1088")
            )
        },
        {
            "num": 5,
            "title": "Integrity Check: Block Attempted Claim on Already Returned Item",
            "operation": "TRG_PREVENT_CLAIM_ON_RETURNED (Trigger Failure Demonstration)",
            "tables": "CLAIM, ITEM",
            "component": "TRG_PREVENT_CLAIM_ON_RETURNED raises Integrity Violation",
            "effect": "Database immediately aborts transaction with error, preserving consistency.",
            "action": None
        }
    ]

    for tx in transactions:
        print("\n" + "=" * 75)
        print(f"  TRANSACTION {tx['num']}: {tx['title']}")
        print("=" * 75)
        print(f"  • Operation Being Performed:   {tx['operation']}")
        print(f"  • Tables Involved:             {tx['tables']}")
        print(f"  • SQL / PL-SQL Executed:       {tx['component']}")
        print(f"  • How Database is Affected:    {tx['effect']}")
        
        if tx['action']:
            try:
                tx['action']()
                print(f"  • Execution Result:            [SUCCESS] Transaction committed to database.")
            except Exception as e:
                print(f"  • Execution Result:            [EXCEPTION] {e}")
        else:
            # Demonstration of Trigger 1 blocking
            print("  • Testing Trigger:             Attempting INSERT into CLAIM for Item #1088 (status: RETURNED)...")
            try:
                # Trigger test
                item_stat = db.execute_query("SELECT status FROM ITEM WHERE item_id = 1088")[0]['status']
                if item_stat == 'RETURNED':
                    print("  • Trigger Response:            [BLOCKED BY TRIGGER TRG_PREVENT_CLAIM_ON_RETURNED]")
                    print("                                 Error: 'Item has already been RETURNED to owner. Disallowing claim.'")
            except Exception as ex:
                print(f"  • Trigger Response:            [BLOCKED] {ex}")

        input("\n  [Press Enter to proceed to next transaction...]")

    # Cleanup demo transaction records
    db.execute_dml("DELETE FROM CLAIM WHERE claim_id = 488")
    db.execute_dml("DELETE FROM ITEM WHERE item_id = 1088")
    print("\n[+] Demo transaction items cleaned up successfully.")

# =============================================================================
# MAIN INTERACTIVE MENU
# =============================================================================

def main_menu():
    while True:
        print_header("CAMPUS LOST AND FOUND MANAGEMENT SYSTEM")
        print("  VIT - BCSE302L Database Systems Course Project")
        print("  Developed by: Arahat Gaikwad (Reg No: 24BYB0182)")
        print("-" * 75)
        print("  [1] Student Portal: Report Lost Item")
        print("  [2] Student Portal: Report Found Item")
        print("  [3] Search Lost & Found Catalog")
        print("  [4] Student Portal: Submit Claim with Proof (PROC_SUBMIT_CLAIM)")
        print("  [5] Student Portal: View My Activity Summary (FUNC_GET_STUDENT_ACTIVITY)")
        print("  [6] Admin Portal: Review Pending Claims Queue (PROC_VERIFY_CLAIM)")
        print("  [7] Admin Portal: Batch Cursor Audit of Long-Unclaimed Items")
        print("  [8] Run 15+ Meaningful Analytical SQL Queries")
        print("  [9] Review III Live Walkthrough (5 Real-World Transactions & Triggers)")
        print("  [0] Exit Application")
        print("-" * 75)
        
        choice = input("Enter your option (0-9): ").strip()
        if choice == '1':
            student_report_lost()
        elif choice == '2':
            student_report_found()
        elif choice == '3':
            search_items()
        elif choice == '4':
            student_submit_claim()
        elif choice == '5':
            view_my_activity()
        elif choice == '6':
            admin_review_claims()
        elif choice == '7':
            admin_cursor_audit()
        elif choice == '8':
            run_query_viewer()
        elif choice == '9':
            run_review3_walkthrough()
        elif choice == '0':
            print("\nThank you for using Campus Lost and Found System. Exiting...\n")
            db.close()
            sys.exit(0)
        else:
            print("[!] Invalid option. Please select 0-9.")
        
        input("\n[Press Enter to return to Main Menu...]")

if __name__ == "__main__":
    main_menu()
