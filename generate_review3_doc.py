"""
Script to generate the Review 3 Project Report Word Document (.docx)
Strictly adheres to the official BCSE302L Review III guidelines:
- Integrated Database Operation (2 Marks)
- Real-World Transactions (3 Marks)
- SQL/PLSQL Interaction (2 Marks)
- Output & Reports (1 Mark)
- Project Report & Documentation (1 Mark)
- Viva / Project Understanding (1 Mark)
Total: 10 Marks
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    run = h.runs[0]
    run.font.name = 'Calibri'
    if level == 1:
        run.font.size = Pt(15.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(31, 78, 121) # Deep Navy
    elif level == 2:
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(47, 84, 150) # Slate Blue
    elif level == 3:
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(38, 38, 38)
    return h

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F2F4F7")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="18" w:space="0" w:color="2F5597"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.0)
    run.font.color.rgb = RGBColor(33, 37, 41)
    
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

def add_embedded_image(doc, img_path, caption_text, width=Inches(6.2)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=width)

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9.0)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 100, 100)

def format_styled_table(table, col_widths, headers, data, header_bg="2F5597"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.runs[0]
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        bg_color = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=140, right=140)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            if p.runs:
                run = p.runs[0]
                run.font.name = 'Calibri'
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(40, 40, 40)

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

def build_review3_doc():
    doc = Document()
    base_dir = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project"
    ss_dir = os.path.join(base_dir, "screenshots")
    docs_dir = os.path.join(base_dir, "docs")

    # Set standard 1-inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Document Header
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_before = Pt(0)
    p_top.paragraph_format.space_after = Pt(2)
    r_top = p_top.add_run("VELLORE INSTITUTE OF TECHNOLOGY")
    r_top.font.name = 'Calibri'
    r_top.font.size = Pt(15)
    r_top.font.bold = True
    r_top.font.color.rgb = RGBColor(31, 78, 121)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run("School of Computer Science Engineering and Information Systems (SCORE)\nBCSE302L – Database Systems | Laboratory Course Project")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(80, 80, 80)

    p_main = doc.add_paragraph()
    p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_main.paragraph_format.space_before = Pt(8)
    p_main.paragraph_format.space_after = Pt(8)
    r_main = p_main.add_run("Campus Lost and Found Management System\nIntegrated Database Application with Real-World Transaction Processing")
    r_main.font.name = 'Calibri'
    r_main.font.size = Pt(18)
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(47, 84, 150)

    p_rev = doc.add_paragraph()
    p_rev.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rev.paragraph_format.space_before = Pt(0)
    p_rev.paragraph_format.space_after = Pt(14)
    r_rev = p_rev.add_run("REVIEW III FINAL PROJECT REPORT – INTEGRATED SYSTEM & DEMONSTRATION")
    r_rev.font.name = 'Calibri'
    r_rev.font.size = Pt(12)
    r_rev.font.bold = True
    r_rev.font.color.rgb = RGBColor(192, 0, 0)

    # 1. Project Title and Team Details
    add_styled_heading(doc, "1. Project Title and Candidate Details", level=1)
    t1 = doc.add_table(rows=1, cols=2)
    t1_headers = ["Project Item", "Specification Details"]
    t1_data = [
        ("Project Title", "Campus Lost and Found Management System (Integrated Web Application & Database)"),
        ("Course Code & Title", "BCSE302L – Database Systems (Integrated Laboratory Project)"),
        ("Academic Year / Term", "Fall Semester 2026"),
        ("Theme / Domain", "Campus Asset Tracking, Student Welfare & Security Administration"),
        ("Student Name", "Arahat Gaikwad"),
        ("Registration Number", "24BYB0182"),
        ("Programme / Branch", "B.Tech Computer Science and Engineering"),
        ("School & Campus", "School of Computer Science Engineering and Information Systems (SCORE), VIT Vellore")
    ]
    format_styled_table(t1, [Inches(2.2), Inches(4.3)], t1_headers, t1_data)

    # Review III Evaluation Rubric Mapping Table
    add_styled_heading(doc, "Review III Official Evaluation Rubric Mapping (10 Marks)", level=2)
    t_rubric = doc.add_table(rows=1, cols=4)
    rub_headers = ["Evaluation Component", "Official Evaluation Criteria", "Weightage", "How Covered in This Report"]
    rub_data = [
        ("Integrated Database Operation", "Database components work together to support the proposed application", "2 Marks", "3-tier architecture: Interactive Web Portal (localhost:5000), Terminal App, and Relational Database Engine. (Section 6)"),
        ("Real-World Transactions", "Demonstration of at least 5 meaningful transactions/operations", "3 Marks", "6 comprehensive transactions demonstrating the entire lifecycle: lost filing, turn-in, claim, approval, and security tests. (Section 7)"),
        ("SQL/PLSQL Interaction", "Appropriate use of queries, procedures, functions, cursors and triggers during transactions", "2 Marks", "PROC_SUBMIT_CLAIM, PROC_VERIFY_CLAIM, FUNC_CALCULATE_UNCLAIMED_DAYS, cur_unclaimed_items, and 2 triggers. (Section 8)"),
        ("Output & Reports", "Correct and meaningful results/reports generated from the database", "1 Mark", "Hotspot identification, Category ranking (DENSE_RANK), Officer audit matrix, and Batch cursor disposal reports. (Section 9)"),
        ("Project Report & Documentation", "Completeness, clarity and technical documentation", "1 Mark", "Complete 10-section formal report with 3NF schema, 9 foreign keys, ER diagram, workflow model, and embedded screenshots. (Sections 1-5, 9)"),
        ("Viva / Project Understanding", "Ability to explain the complete database workflow and justify design choices", "1 Mark", "Architectural justification of 3NF, trigger event timing rationale, cursor lifecycle, and ACID transaction proof. (Section 10)")
    ]
    format_styled_table(t_rubric, [Inches(1.6), Inches(2.2), Inches(0.9), Inches(2.3)], rub_headers, rub_data, header_bg="1F4E79")

    # 2. Introduction, Problem Statement and System Overview
    add_styled_heading(doc, "2. Introduction, Problem Statement and System Overview", level=1)
    add_styled_heading(doc, "2.1 Introduction", level=2)
    p = doc.add_paragraph(
        "The Campus Lost and Found Management System is a fully integrated, multi-tier database application designed to resolve "
        "the daily challenge of lost and misplaced personal articles across the Vellore Institute of Technology (VIT) campus. "
        "Every day, thousands of students and faculty navigate academic complexes (Silver Jubilee Tower, Technology Tower, PRP Block), "
        "central libraries, auditoriums, cafeterias, and residential hostels, resulting in misplaced ID cards, laptops, scientific calculators, "
        "headphones, wallets, and keys.\n\n"
        "In Review III, the application demonstrates full integrated operation: connecting an interactive user interface (both a modern Web Portal "
        "and a Terminal Application) with a robust, normalized relational backend. Real-world transactions follow the complete data lifecycle: "
        "an item is reported lost, discovered and turned in, searched by the rightful owner, claimed with physical proof, and verified by "
        "administrative authorities. Underneath, automated triggers, stored procedures, functions, and explicit cursors ensure data integrity, "
        "synchronize item statuses, and resolve competing claims atomically."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "2.2 Problem Statement", level=2)
    p = doc.add_paragraph(
        "Traditional campus lost-and-found management relies on manual registers and ad-hoc communication, leading to:\n"
        "1. Fragmented Records: Physical logbooks scattered across security gates, library reception, and hostel wardens.\n"
        "2. Fraudulent Retrievals: Lack of verified proof of ownership enables false claims on high-value electronics.\n"
        "3. Manual Status Inconsistencies: Items returned to owners remain marked as active in logbooks, causing phantom inventory.\n"
        "4. Stale Unclaimed Belongings: No batch mechanism exists to scan aged items exceeding retention periods for administrative auction.\n\n"
        "The Integrated Solution: A unified database system where every student action triggers immediate procedural checks and "
        "event-driven database triggers, providing complete transparency and end-to-end accountability."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "2.3 Objectives & Review III System Deliverables", level=2)
    p = doc.add_paragraph(
        "• Demonstrate integrated database operation where frontend user actions directly execute backend SQL/PL-SQL logic.\n"
        "• Validate at least 5 meaningful end-to-end real-world transactions answering all 5 evaluation questions.\n"
        "• Demonstrate procedural business logic (PROC_SUBMIT_CLAIM, PROC_VERIFY_CLAIM) and functions (FUNC_CALCULATE_UNCLAIMED_DAYS).\n"
        "• Verify automated trigger execution: auto-updating item status upon approval and blocking claims on returned items.\n"
        "• Demonstrate batch processing of multiple records using an explicit cursor (PROC_FLAG_LONG_UNCLAIMED_ITEMS).\n"
        "• Generate multi-table analytical management reports and audit summaries directly from the database."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    # 3. Functional Requirements & Workflow Model
    add_styled_heading(doc, "3. Functional Requirements & Workflow Model", level=1)
    
    # Embed Workflow Diagram
    wf_img_path = os.path.join(docs_dir, "Workflow_Diagram.png")
    add_embedded_image(doc, wf_img_path, "Figure 3.1: Campus Lost and Found Lifecycle Workflow (From Lost to Found & Return)")

    t_fr = doc.add_table(rows=1, cols=3)
    fr_headers = ["FR ID", "Functional Module", "Operational Role in Integrated System"]
    fr_data = [
        ("FR1", "Student Management", "Maintains authenticated student profiles (e.g. Arahat Gaikwad, 24BYB0182) with unique institutional emails."),
        ("FR2", "Admin & Security Staff", "Authorizes campus security officers, wardens, and library staff to adjudicate claims."),
        ("FR3", "Location Directory", "Catalogs campus buildings (SJT, TT, PRP, Library, Hostels) for incident origin mapping."),
        ("FR4", "Lost Item Reporting", "Allows students to register lost articles with timestamps and location references."),
        ("FR5", "Found Item Turn-in", "Enables discoverers to submit turned-in items, automatically updating catalog status to 'FOUND'."),
        ("FR6", "Interactive Search", "Provides multi-criteria search by keyword, category, status, and campus building."),
        ("FR7", "Ownership Claim Filing", "Executes PROC_SUBMIT_CLAIM to register ownership claims with mandatory proof descriptions."),
        ("FR8", "Administrative Verification", "Executes PROC_VERIFY_CLAIM enabling staff to formally APPROVE or REJECT claims."),
        ("FR9", "Auto-Status Progression", "Fires Trigger TRG_AUTO_UPDATE_ITEM_STATUS to set parent item to 'RETURNED' upon approval."),
        ("FR10", "Integrity Violation Block", "Fires Trigger TRG_PREVENT_CLAIM_ON_RETURNED to block claims on already returned items."),
        ("FR11", "Aging Unclaimed Calculation", "Executes FUNC_CALCULATE_UNCLAIMED_DAYS to compute unresolved days using date arithmetic."),
        ("FR12", "Bulk Explicit Cursor Audit", "Executes PROC_FLAG_LONG_UNCLAIMED_ITEMS using an explicit cursor to flag aged items for disposal."),
        ("FR13", "Status Tracking", "Displays real-time claim progress feedback (PENDING -> APPROVED/REJECTED) to student claimants."),
        ("FR14", "Analytical Reporting", "Generates categorical summaries, campus building hotspots, and officer decision matrices."),
        ("FR15", "DML Integrity Auditing", "Executes transactional INSERT, UPDATE, and DELETE operations with zero referential corruption.")
    ]
    format_styled_table(t_fr, [Inches(0.9), Inches(2.2), Inches(3.4)], fr_headers, fr_data)

    # 4. Entity-Relationship (ER) Diagram & Schema Mapping
    add_styled_heading(doc, "4. Entity-Relationship (ER) Diagram & Cardinality Mapping", level=1)
    er_img_path = os.path.join(docs_dir, "ER_Diagram.png")
    add_embedded_image(doc, er_img_path, "Figure 4.1: Entity-Relationship (ER) Diagram – 7 Entities with 9 One-to-Many Relationships")

    p = doc.add_paragraph(
        "The system architecture consists of 7 normalized entities linked by 9 One-to-Many (1 : N) relationships, "
        "ensuring strict referential integrity with ON DELETE CASCADE enabled on all child incident filings."
    )
    p.paragraph_format.space_after = Pt(6)

    t_rel = doc.add_table(rows=1, cols=4)
    rel_headers = ["Relationship", "Parent Table (1)", "Child Table (N)", "Foreign Key Column"]
    rel_data = [
        ("reports", "STUDENT", "ITEM", "reported_by_student_id"),
        ("has", "LOCATION", "ITEM", "location_id"),
        ("submits", "STUDENT", "LOST_REPORT", "student_id"),
        ("documents", "ITEM", "LOST_REPORT", "item_id"),
        ("submits", "STUDENT", "FOUND_REPORT", "student_id"),
        ("documents", "ITEM", "FOUND_REPORT", "item_id"),
        ("submits", "STUDENT", "CLAIM", "claimant_student_id"),
        ("claimed for", "ITEM", "CLAIM", "item_id"),
        ("reviews", "ADMIN", "CLAIM", "admin_id (Nullable until reviewed)")
    ]
    format_styled_table(t_rel, [Inches(1.5), Inches(1.6), Inches(1.6), Inches(1.8)], rel_headers, rel_data)

    # 5. Relational Schema & 3NF Normalization
    add_styled_heading(doc, "5. Relational Schema & 3NF Normalization", level=1)
    p = doc.add_paragraph(
        "The database strictly conforms to Third Normal Form (3NF):\n"
        "• 1NF: All attributes contain atomic values; no multi-valued attributes or repeating groups exist.\n"
        "• 2NF: All non-key attributes are fully functionally dependent on the complete primary key; no partial dependencies exist.\n"
        "• 3NF: No transitive functional dependencies exist (i.e. Non-key -> Non-key). Reports and claims are separated into "
        "independent relation schemas to avoid null bloat.\n\n"
        "Formal Relational Schema:\n"
        "• LOCATION (location_id PK, location_name, building)\n"
        "• STUDENT (student_id PK, name, email UNIQUE, phone)\n"
        "• ADMIN (admin_id PK, name, email UNIQUE)\n"
        "• ITEM (item_id PK, item_name, description, category, date_reported, status, location_id FK, reported_by_student_id FK)\n"
        "• LOST_REPORT (lost_report_id PK, item_id FK, student_id FK, date_lost, details)\n"
        "• FOUND_REPORT (found_report_id PK, item_id FK, student_id FK, date_found, details)\n"
        "• CLAIM (claim_id PK, item_id FK, claimant_student_id FK, claim_date, proof_description, claim_status, admin_id FK)"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    # 6. Integrated Database Operation & Multi-Tier Architecture (2 Marks)
    add_styled_heading(doc, "6. Integrated Database Operation & Architecture (2 Marks)", level=1)
    p = doc.add_paragraph(
        "To fulfill the Review III requirement for 'Integrated Database Operation (2 Marks)', the application implements "
        "a multi-tier architecture connecting interactive client interfaces with a unified relational backend:\n\n"
        "1. Presentation Tier (Dual Client Flexibility):\n"
        "   • Modern Web Application Portal (web_app.py): A zero-dependency, browser-based single-page application running locally "
        "on http://localhost:5000 with dedicated portals for student self-service, admin claims review, and live Review III demonstrations.\n"
        "   • Interactive Terminal Application (app.py): A console interface allowing instant keyboard-driven execution and debugging.\n"
        "2. Application & Data Access Tier (database.py):\n"
        "   • Unified database abstraction managing connection pooling, parameterized query execution, transactional commits, "
        "and exception trapping.\n"
        "3. Database Engine Tier (Oracle Database 19c/21c & SQLite 3NF Schema):\n"
        "   • 7 normalized tables enforcing primary/foreign keys, domain CHECK constraints, unique institutional emails, "
        "event-driven triggers, stored procedures, and explicit cursors."
    )
    p.paragraph_format.space_after = Pt(6)

    # Embed Screenshot of Web Portal
    web_ss_path = os.path.join(ss_dir, "screenshot_10_web_portal.png")
    add_embedded_image(doc, web_ss_path, "Figure 6.1: Integrated Web Application Portal (Interactive Browser Interface on http://localhost:5000)")

    # Embed Screenshot of Python CLI
    cli_ss_path = os.path.join(ss_dir, "screenshot_3_python_app.png")
    add_embedded_image(doc, cli_ss_path, "Figure 6.2: Integrated Python Application Terminal Session (Live Transaction Flow)")

    p_conn = doc.add_paragraph(
        "Core Database Connectivity & Transaction Processing Routine (app/database.py):"
    )
    p_conn.paragraph_format.space_after = Pt(4)

    conn_code = """class Database:
    def __init__(self, db_type="sqlite", oracle_config=None):
        self.db_type = db_type
        self.oracle_config = oracle_config
        self.connect()

    def connect(self):
        if self.db_type == "oracle":
            import oracledb
            cfg = self.oracle_config or {}
            self.conn = oracledb.connect(user=cfg.get("user"), password=cfg.get("password"), dsn="localhost:1521/XEPDB1")
        else:
            self.conn = sqlite3.connect("campus_lost_found.db", check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON;")

    def execute_dml(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params or ())
        self.conn.commit()
        return cursor.rowcount"""
    add_code_block(doc, conn_code)

    # 7. Real-World Transaction Demonstrations (3 Marks)
    add_styled_heading(doc, "7. Real-World Transaction Demonstrations (3 Marks)", level=1)
    p = doc.add_paragraph(
        "In accordance with Section 4 and the Review III rubric ('Demonstration of at least 5 meaningful transactions/operations - 3 Marks'), "
        "every transaction is evaluated against the complete operational flow:\n"
        "User Operation → SQL/PL/SQL → Database Processing → Database Update/Retrieval → Result\n\n"
        "For each transaction, the five standard evaluation questions are answered and supported by live execution proofs:"
    )
    p.paragraph_format.space_after = Pt(8)

    # Tx 1
    add_styled_heading(doc, "Transaction 1: Student Files Lost Belonging Incident Report (FR4)", level=2)
    t_tx1 = doc.add_table(rows=1, cols=2)
    format_styled_table(t_tx1, [Inches(2.2), Inches(4.3)], ["Evaluation Question", "System Demonstration Answer"], [
        ("What operation is performed?", "Student Arahat Gaikwad (24BYB0182) registers a report for an ID card lost in Central Library."),
        ("Which tables are involved?", "STUDENT, LOCATION, ITEM, LOST_REPORT"),
        ("Which SQL/PL/SQL component runs?", "INSERT INTO ITEM (...) and INSERT INTO LOST_REPORT (...)"),
        ("How is the database affected?", "New ITEM row (ID 1001, status 'LOST') and linked LOST_REPORT row (ID 201) are inserted with foreign key references."),
        ("What result is generated?", "Item cataloged and indexed under Central Library; reference report ID 201 generated for student.")
    ])
    tx1_sql = """INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1001, 'VIT Student ID Card', 'ID Card belonging to Arahat Gaikwad with lanyard', 'Identity Cards', DATE '2026-10-10', 'LOST', 102, '24BYB0182');
INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (201, 1001, '24BYB0182', DATE '2026-10-09', 'Lost near library reference hall.');
SELECT item_id, item_name, status, reported_by_student_id FROM ITEM WHERE item_id = 1001;"""
    add_code_block(doc, tx1_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_4_demo1_lost.png"), "Figure 7.1: Transaction 1 – Filing Lost Belonging and Item Table Record Creation")

    # Tx 2
    add_styled_heading(doc, "Transaction 2: Good Samaritan Turns in Found Item & Updates Status (FR5)", level=2)
    t_tx2 = doc.add_table(rows=1, cols=2)
    format_styled_table(t_tx2, [Inches(2.2), Inches(4.3)], ["Evaluation Question", "System Demonstration Answer"], [
        ("What operation is performed?", "Another student (Rohan Sharma) discovers the misplaced ID card on library table 14 and turns it in."),
        ("Which tables are involved?", "ITEM, FOUND_REPORT, STUDENT"),
        ("Which SQL/PL/SQL component runs?", "INSERT INTO FOUND_REPORT (...) and UPDATE ITEM SET status = 'FOUND'"),
        ("How is the database affected?", "FOUND_REPORT row (ID 301) is created; ITEM 1001 status transitions from 'LOST' to 'FOUND'."),
        ("What result is generated?", "Item is cataloged as recovered and becomes discoverable in search for claimant filing.")
    ])
    tx2_sql = """INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (301, 1001, '24BCE1001', DATE '2026-10-10', 'Found lying on reading table 14 in library.');
UPDATE ITEM SET status = 'FOUND' WHERE item_id = 1001;
SELECT item_id, item_name, status, location_id FROM ITEM WHERE item_id = 1001;"""
    add_code_block(doc, tx2_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_5_demo2_found.png"), "Figure 7.2: Transaction 2 – Found Report Filing and Item Status Transition to 'FOUND'")

    # Tx 3
    add_styled_heading(doc, "Transaction 3: Owner Files Ownership Claim with Proof via Procedure (FR7)", level=2)
    t_tx3 = doc.add_table(rows=1, cols=2)
    format_styled_table(t_tx3, [Inches(2.2), Inches(4.3)], ["Evaluation Question", "System Demonstration Answer"], [
        ("What operation is performed?", "Owner Arahat Gaikwad discovers his card in the found list and submits a claim with proof of ownership."),
        ("Which tables are involved?", "CLAIM, ITEM, STUDENT"),
        ("Which SQL/PL/SQL component runs?", "PROC_SUBMIT_CLAIM(1001, '24BYB0182', 'Matches my photo and reg no 24BYB0182', v_id, v_msg)"),
        ("How is the database affected?", "Procedure validates student and item; checks status != 'RETURNED'; inserts Claim #401 in 'PENDING' status."),
        ("What result is generated?", "Claim ID #401 generated and placed into campus security review queue; success message returned.")
    ])
    tx3_sql = """VARIABLE v_claim_id NUMBER;
VARIABLE v_msg VARCHAR2(250);
EXEC PROC_SUBMIT_CLAIM(1001, '24BYB0182', 'Matches my student photo and reg no 24BYB0182', :v_claim_id, :v_msg);
PRINT v_msg;
SELECT claim_id, item_id, claimant_student_id, claim_status, claim_date FROM CLAIM WHERE claim_id = 401;"""
    add_code_block(doc, tx3_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_6_demo3_claim.png"), "Figure 7.3: Transaction 3 – Execution of Stored Procedure PROC_SUBMIT_CLAIM Generating Claim #401")

    # Tx 4
    add_styled_heading(doc, "Transaction 4: Administrative Review, Claim Approval & Trigger Execution (FR8, FR9)", level=2)
    t_tx4 = doc.add_table(rows=1, cols=2)
    format_styled_table(t_tx4, [Inches(2.2), Inches(4.3)], ["Evaluation Question", "System Demonstration Answer"], [
        ("What operation is performed?", "Library In-Charge Mrs. Vijayalakshmi (Admin 3) verifies proof against student registry and approves Claim #401."),
        ("Which tables are involved?", "CLAIM, ITEM, ADMIN"),
        ("Which SQL/PL/SQL component runs?", "PROC_VERIFY_CLAIM(401, 3, 'APPROVED', v_msg) and Trigger TRG_AUTO_UPDATE_ITEM_STATUS"),
        ("How is the database affected?", "Claim #401 status updated to 'APPROVED'; Trigger fires AFTER UPDATE and automatically sets ITEM #1001 status to 'RETURNED'."),
        ("What result is generated?", "Item returned to owner; competing pending claims auto-rejected; audit record permanently preserved.")
    ])
    tx4_sql = """VARIABLE v_msg VARCHAR2(250);
EXEC PROC_VERIFY_CLAIM(401, 3, 'APPROVED', :v_msg);
PRINT v_msg;
SELECT c.claim_id, c.claim_status, c.admin_id, i.item_id, i.status AS item_status
FROM CLAIM c JOIN ITEM i ON c.item_id = i.item_id WHERE c.claim_id = 401;"""
    add_code_block(doc, tx4_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_7_demo4_verify.png"), "Figure 7.4: Transaction 4 – Claim Approval and Trigger TRG_AUTO_UPDATE_ITEM_STATUS Execution")

    # Tx 5
    add_styled_heading(doc, "Transaction 5: Negative Security Test: Trigger Blocks Claim on Returned Item (FR10)", level=2)
    t_tx5 = doc.add_table(rows=1, cols=2)
    format_styled_table(t_tx5, [Inches(2.2), Inches(4.3)], ["Evaluation Question", "System Demonstration Answer"], [
        ("What operation is performed?", "Another student (24BEE0210) attempts to file a fraudulent claim on Item #1001 which has already been returned."),
        ("Which tables are involved?", "CLAIM, ITEM"),
        ("Which SQL/PL/SQL component runs?", "Trigger TRG_PREVENT_CLAIM_ON_RETURNED (BEFORE INSERT ON CLAIM)"),
        ("How is the database affected?", "Trigger detects status = 'RETURNED' and immediately calls RAISE_APPLICATION_ERROR(-20001, ...)."),
        ("What result is generated?", "Oracle error raised; insertion is immediately rolled back; zero dirty or conflicting records are inserted.")
    ])
    tx5_sql = """-- Negative Test: Attempting invalid claim on already returned item
INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status)
VALUES (999, 1001, '24BEE0210', SYSDATE, 'Attempting claim on already returned ID card', 'PENDING');
-- Output: ORA-20001: Integrity Rule Violation: Item has already been RETURNED to its owner."""
    add_code_block(doc, tx5_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_8_demo5_error.png"), "Figure 7.5: Transaction 5 – Trigger TRG_PREVENT_CLAIM_ON_RETURNED Aborting Invalid Transaction")

    # Tx 6
    add_styled_heading(doc, "Transaction 6: Bulk Explicit Cursor Scans Long-Unclaimed Items for Auction (FR11, FR12)", level=2)
    t_tx6 = doc.add_table(rows=1, cols=2)
    format_styled_table(t_tx6, [Inches(2.2), Inches(4.3)], ["Evaluation Question", "System Demonstration Answer"], [
        ("What operation is performed?", "Campus security runs periodic batch audit scanning items unclaimed for >= 10 days."),
        ("Which tables are involved?", "ITEM, LOCATION"),
        ("Which SQL/PL/SQL component runs?", "PROC_FLAG_LONG_UNCLAIMED_ITEMS(10, v_total) using explicit cursor cur_unclaimed_items"),
        ("How is the database affected?", "Cursor fetches rows iteratively into memory record, computing days unresolved and building location."),
        ("What result is generated?", "Tabular batch report generated via DBMS_OUTPUT with count of aged items flagged for campus auction.")
    ])
    tx6_sql = """SET SERVEROUTPUT ON;
VARIABLE v_total NUMBER;
EXEC PROC_FLAG_LONG_UNCLAIMED_ITEMS(10, :v_total);
PRINT v_total;"""
    add_code_block(doc, tx6_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_9_demo6_cursor.png"), "Figure 7.6: Transaction 6 – Explicit Cursor Batch Processing and DBMS_OUTPUT Report")

    # 8. SQL & PL/SQL Interaction Matrix (2 Marks)
    add_styled_heading(doc, "8. SQL & PL/SQL Interaction Matrix during Transactions (2 Marks)", level=1)
    p = doc.add_paragraph(
        "To fulfill the Review III requirement for 'SQL/PLSQL Interaction (2 Marks)', the matrix below maps each real-world "
        "transaction to the exact queries, stored procedures, functions, explicit cursor, and database triggers that execute:"
    )
    p.paragraph_format.space_after = Pt(6)

    t_mat = doc.add_table(rows=1, cols=4)
    mat_headers = ["Transaction", "Primary Operation", "SQL / PL-SQL Component Executed", "Event Timing & Role"]
    mat_data = [
        ("Tx 1: Report Lost", "INSERT", "INSERT INTO ITEM, INSERT INTO LOST_REPORT", "Initial state generation; status set to 'LOST'"),
        ("Tx 2: Report Found", "INSERT & UPDATE", "INSERT INTO FOUND_REPORT, UPDATE ITEM", "Status transition from 'LOST' to 'FOUND'"),
        ("Tx 3: Submit Claim", "PROCEDURE", "PROC_SUBMIT_CLAIM", "Pre-validates student/item; checks status; creates Claim in 'PENDING'"),
        ("Tx 4: Claim Approval", "PROCEDURE & TRIGGER", "PROC_VERIFY_CLAIM & Trigger TRG_AUTO_UPDATE_ITEM_STATUS", "AFTER UPDATE trigger sets ITEM status to 'RETURNED'; rejects competitors"),
        ("Tx 5: Fraud Block", "TRIGGER", "Trigger TRG_PREVENT_CLAIM_ON_RETURNED", "BEFORE INSERT trigger aborts claim if item status = 'RETURNED' (ORA-20001)"),
        ("Tx 6: Bulk Audit", "EXPLICIT CURSOR", "PROC_FLAG_LONG_UNCLAIMED_ITEMS (cur_unclaimed_items)", "OPEN, FETCH, %NOTFOUND, CLOSE lifecycle for batch processing"),
        ("Tx 7: Profile Analytics", "FUNCTION", "FUNC_GET_STUDENT_ACTIVITY & FUNC_CALCULATE_UNCLAIMED_DAYS", "Dynamic aggregation returning activity strings and aging days")
    ]
    format_styled_table(t_mat, [Inches(1.5), Inches(1.3), Inches(2.2), Inches(1.8)], mat_headers, mat_data)

    # 9. Output & Reports (Administrative Reporting & Hotspots) (1 Mark)
    add_styled_heading(doc, "9. Output & Reports (Administrative Decision Support) (1 Mark)", level=1)
    p = doc.add_paragraph(
        "In accordance with Review III 'Output & Reports (1 Mark)', the database generates meaningful analytical management "
        "reports directly through complex queries utilizing multi-table joins, GROUP BY, HAVING, and window functions:"
    )
    p.paragraph_format.space_after = Pt(6)

    # Embed Screenshot 2 (Queries output)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_2_queries.png"), "Figure 9.1: Multi-Table Join Query Result Grid – Item, Student Reporter & Campus Building Details")

    t_rep = doc.add_table(rows=1, cols=3)
    rep_headers = ["Report Title", "Analytical SQL Query Logic", "Administrative Purpose"]
    rep_data = [
        ("Campus Building Loss Hotspots", "SELECT l.building, COUNT(i.item_id) FROM LOCATION l JOIN ITEM i ON l.location_id=i.location_id GROUP BY l.building HAVING COUNT(i.item_id) >= 2;", "Pinpoints buildings with recurring losses (e.g. SJT, Library) for security patrol allocation."),
        ("Category Incident Summary", "SELECT category, COUNT(*), SUM(CASE WHEN status='LOST' THEN 1 ELSE 0 END), SUM(CASE WHEN status='FOUND' THEN 1 ELSE 0 END) FROM ITEM GROUP BY category;", "Identifies which categories (Electronics, Accessories, Keys) are most frequently misplaced."),
        ("Admin Verification Matrix", "SELECT a.name, COUNT(c.claim_id), SUM(CASE WHEN c.claim_status='APPROVED' THEN 1 ELSE 0 END) FROM ADMIN a LEFT JOIN CLAIM c ON a.admin_id=c.admin_id GROUP BY a.name;", "Evaluates review performance and decision breakdown across campus security officers."),
        ("Aged Item Retention Audit", "Explicit Cursor in PROC_FLAG_LONG_UNCLAIMED_ITEMS filtering items unresolved >= 10 days.", "Generates an inventory list of abandoned goods eligible for university auction or recycling.")
    ]
    format_styled_table(t_rep, [Inches(1.8), Inches(2.7), Inches(2.3)], rep_headers, rep_data)

    # DML Verification Image
    add_styled_heading(doc, "DML Operations Integrity Verification (INSERT, UPDATE, DELETE)", level=2)
    p_dml = doc.add_paragraph(
        "In compliance with Section 3 and FR15, the project verified that all three DML operations execute cleanly with zero "
        "referential integrity violations across foreign key cascades and triggers:"
    )
    p_dml.paragraph_format.space_after = Pt(4)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_1_dml.png"), "Figure 9.2: DML Execution Verification in Oracle Database (INSERT, UPDATE, DELETE with Cascading Integrity)")

    # 10. Conclusion and Viva Technical Defense (1 Mark)
    add_styled_heading(doc, "10. Conclusion and Viva Technical Defense (1 Mark)", level=1)
    p = doc.add_paragraph(
        "10.1 Key Accomplishments:\n"
        "• Successfully implemented an end-to-end relational database application adhering to Third Normal Form (3NF).\n"
        "• Integrated frontend user operations with backend SQL and PL/SQL procedures, functions, explicit cursors, and triggers.\n"
        "• Demonstrated all 6 major real-world transactions answering the 5 standard evaluation questions.\n"
        "• Enforced strict database integrity: blocking fraudulent claims on returned items and synchronizing parent-child states.\n\n"
        "10.2 Review III Viva Defense Highlights:\n"
        "• Schema Justification: Separating LOST_REPORT and FOUND_REPORT preserves independent incident timelines and satisfies 3NF without NULL bloat.\n"
        "• Trigger Mechanics: TRG_PREVENT_CLAIM_ON_RETURNED acts as a BEFORE INSERT gatekeeper; TRG_AUTO_UPDATE_ITEM_STATUS acts as an AFTER UPDATE state synchronizer.\n"
        "• Conflict Resolution: When multiple students claim the same item, PROC_VERIFY_CLAIM approves one and automatically rejects all competing claims within the same atomic transaction.\n"
        "• Multi-Record Processing: The explicit cursor manages memory safely using the OPEN -> FETCH -> CLOSE lifecycle without risk of cursor exhaustion."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(12)

    # Save Review 3 Documents
    out_dir = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project\docs"
    out_file = os.path.join(out_dir, "Campus_Lost_and_Found_Review3_Report.docx")
    doc.save(out_file)
    print(f"Review 3 Document successfully created at: {out_file}")

    root_file = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Review3_Report_Final.docx"
    try:
        doc.save(root_file)
        print(f"Final Copy saved at: {root_file}")
    except PermissionError:
        alt_file = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Review3_Report_SCORE.docx"
        doc.save(alt_file)
        print(f"File locked by Word. Saved fresh copy to: {alt_file}")

    project_copy = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project\Campus_Lost_and_Found_Review3_Report_Final.docx"
    doc.save(project_copy)
    print(f"Project Folder Copy saved at: {project_copy}")

if __name__ == "__main__":
    build_review3_doc()
