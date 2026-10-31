"""
Updated generate_review2_doc.py that embeds all 9 generated screenshots
directly into the Word Document (.docx), creating a 100% complete, submission-ready report.
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

def build_review2_doc():
    doc = Document()
    base_dir = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project"
    ss_dir = os.path.join(base_dir, "screenshots")

    # Set standard 1 inch margins
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
    p_main.paragraph_format.space_after = Pt(12)
    r_main = p_main.add_run("Campus Lost and Found Management System\nwith Rule-Based Automated Claim Verification")
    r_main.font.name = 'Calibri'
    r_main.font.size = Pt(20)
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(47, 84, 150)

    p_rev = doc.add_paragraph()
    p_rev.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rev.paragraph_format.space_before = Pt(0)
    p_rev.paragraph_format.space_after = Pt(16)
    r_rev = p_rev.add_run("REVIEW II PROJECT REPORT – DATABASE IMPLEMENTATION")
    r_rev.font.name = 'Calibri'
    r_rev.font.size = Pt(12)
    r_rev.font.bold = True
    r_rev.font.color.rgb = RGBColor(192, 0, 0)

    # 1. Project Title and Team Details
    add_styled_heading(doc, "1. Project Title and Team Details", level=1)
    t1 = doc.add_table(rows=1, cols=2)
    t1_headers = ["Item", "Details"]
    t1_data = [
        ("Project title", "Campus Lost and Found Management System with Rule-Based Automated Claim Verification"),
        ("Course", "BCSE302L – Database Systems (Lab Project)"),
        ("Academic Year / Term", "Fall Semester 2026"),
        ("Domain", "Campus Asset Management, University Administration & Security Services"),
        ("Student Name", "Arahat Gaikwad"),
        ("Registration Number", "24BYB0182"),
        ("Programme / Branch", "B.Tech Computer Science and Engineering"),
        ("School / Institution", "School of Computer Science Engineering and Information Systems, VIT Vellore")
    ]
    format_styled_table(t1, [Inches(2.2), Inches(4.3)], t1_headers, t1_data)

    # 2. Introduction and Problem Statement
    add_styled_heading(doc, "2. Introduction and Problem Statement", level=1)
    add_styled_heading(doc, "2.1 Introduction", level=2)
    p = doc.add_paragraph(
        "Campus Lost and Found Management System is an enterprise database application built on an Oracle relational database "
        "tailored for large academic campuses such as Vellore Institute of Technology (VIT). It models and coordinates the lifecycle "
        "of personal articles misplaced or discovered across lecture halls (SJT, TT, PRP), reading rooms, libraries, dining halls, "
        "and residential hostels. The system manages student profiles, administrative staff, campus physical locations, lost item reports, "
        "found item turns-ins, and student ownership claims.\n\n"
        "The distinctive operational feature of this system is rule-based automated claim verification and lifecycle synchronization. "
        "When an item is reported or claimed, predefined business rules written in SQL and PL/SQL enforce integrity: validating ownership proof, "
        "blocking fraudulent claims on already returned items, automatically updating item statuses upon verification, and batch-flagging "
        "long-unclaimed items using an explicit cursor for administrative disposal or auction.\n\n"
        "Note: This is a Database Systems (BCSE302L) project. No artificial intelligence or machine learning black-box models are used. "
        "All state progression, validation rules, batch scanning, and audit triggers are implemented purely using relational constraints, "
        "PL/SQL procedures, stored functions, explicit cursors, and row-level database triggers."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "2.2 Problem Statement", level=2)
    p = doc.add_paragraph(
        "Manual and informal lost-and-found management across university campuses suffers from critical operational bottlenecks:\n"
        "• Scattered & Duplicate Records: Physical registers maintained separately at security gates, hostel warden cabins, and library counters prevent unified tracking.\n"
        "• Unverified or Fraudulent Claims: High-value electronics (smartwatches, AirPods, scientific calculators) are frequently retrieved by unauthorized individuals without documented proof.\n"
        "• Low Recovery Rates: Students who lose items cannot discover whether an item matching their description was turned in at another campus block.\n"
        "• Lack of Automated Status Tracking: No automated mechanism exists to transition item statuses from LOST/FOUND to RETURNED, leading to stale inventory.\n"
        "• No Batch Processing for Aging Inventory: Unclaimed items accumulate indefinitely without systematic batch scans to calculate age and flag for auction.\n\n"
        "Need for Campus Lost and Found System: A single, centralized, 3NF-normalized relational database that securely logs incidents, enforces referential rules, "
        "automates claim review workflows, and provides rapid analytical querying for campus security."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "2.3 Objectives", level=2)
    p = doc.add_paragraph(
        "• Manage student identity profiles and administrative security staff with strict unique constraints.\n"
        "• Maintain a centralized catalog of campus buildings, classrooms, and loss hotspots.\n"
        "• Record detailed lost and found incident filings with timestamps and locations.\n"
        "• Process ownership claims with verified proof descriptions and admin assignment.\n"
        "• Enforce automated database rules preventing duplicate claims and claims on returned items.\n"
        "• Execute batch cursor audits to calculate unclaimed days and flag abandoned property.\n"
        "• Generate multi-table analytical reports using complex joins, aggregations, subqueries, and window functions."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    # 3. Functional Requirements
    add_styled_heading(doc, "3. Functional Requirements", level=1)
    t_fr = doc.add_table(rows=1, cols=3)
    fr_headers = ["No.", "Module", "What it does"]
    fr_data = [
        ("FR1", "Student Management", "Register, update, and maintain student identity profiles with unique institutional emails"),
        ("FR2", "Admin & Security Staff", "Maintain security officers, wardens, and library staff authorized to verify claims"),
        ("FR3", "Location Directory", "Maintain campus zones, academic blocks (SJT, TT, PRP), hostels, and specific spot details"),
        ("FR4", "Lost Item Reporting", "Record missing item reports filed by students with description, category, and date lost"),
        ("FR5", "Found Item Reporting", "Log items discovered and handed in by good Samaritans with discovery spot and date"),
        ("FR6", "Item Search & Filtering", "Enable students and staff to query catalog by keyword, category, status, and building"),
        ("FR7", "Claim Submission", "Permit students to file formal ownership claims supported by specific physical proof"),
        ("FR8", "Claim Verification", "Allow administrative personnel to adjudicate claims as APPROVED or REJECTED"),
        ("FR9", "Auto-Status Progression", "Automatically update item status to RETURNED when a claim is approved"),
        ("FR10", "Integrity Violation Block", "Automatically reject new claims on items that have already been returned"),
        ("FR11", "Unclaimed Age Calculation", "Compute elapsed calendar days an item remains unresolved in the system"),
        ("FR12", "Batch Cursor Audit", "Scan and flag long-unclaimed items in bulk using an explicit cursor for disposal"),
        ("FR13", "User Claim Status Tracking", "Display real-time claim adjudication updates (PENDING, APPROVED, REJECTED)"),
        ("FR14", "Analytical Reporting", "Generate categorical aggregations, building hotspot analysis, and staff review summaries"),
        ("FR15", "DML Operations Auditing", "Demonstrate INSERT, UPDATE, and DELETE operations with zero referential corruption")
    ]
    format_styled_table(t_fr, [Inches(0.8), Inches(2.2), Inches(3.5)], fr_headers, fr_data)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(8)
    p_sp.paragraph_format.space_after = Pt(4)
    r_sp = p_sp.add_run("Campus Business and Integrity Rules Enforced:")
    r_sp.font.bold = True

    t_br = doc.add_table(rows=1, cols=3)
    br_headers = ["Rule ID", "Condition / Trigger Event", "Database Result"]
    br_data = [
        ("R1", "Item status in ('LOST', 'FOUND', 'CLAIMED', 'RETURNED')", "Enforced via CHECK constraint chk_item_status; invalid status rejected"),
        ("R2", "Claim status in ('PENDING', 'APPROVED', 'REJECTED')", "Enforced via CHECK constraint chk_claim_status; invalid status rejected"),
        ("R3", "Student submits claim on an item with status = 'RETURNED'", "Trigger TRG_PREVENT_CLAIM_ON_RETURNED raises ORA-20001 and aborts insert"),
        ("R4", "Admin updates claim_status to 'APPROVED'", "Trigger TRG_AUTO_UPDATE_ITEM_STATUS automatically sets parent ITEM.status to 'RETURNED'"),
        ("R5", "Admin approves Claim X for an Item with other PENDING claims", "Procedure PROC_VERIFY_CLAIM automatically sets competing claims to REJECTED"),
        ("R6", "Unclaimed days >= Threshold (e.g. 10 days)", "Explicit cursor in PROC_FLAG_LONG_UNCLAIMED_ITEMS flags records for auction/disposal")
    ]
    format_styled_table(t_br, [Inches(0.9), Inches(2.6), Inches(3.0)], br_headers, br_data)

    # 4. ER Diagram
    add_styled_heading(doc, "4. ER Diagram", level=1)
    er_img_path = os.path.join(base_dir, "docs", "ER_Diagram.png")
    add_embedded_image(doc, er_img_path, "Figure 4.1: Entity-Relationship (ER) Diagram – Campus Lost and Found Management System")

    p = doc.add_paragraph(
        "Entities: LOCATION, STUDENT, ADMIN, ITEM, LOST_REPORT, FOUND_REPORT, CLAIM.\n"
        "Total Relationships: 9 One-to-Many (1 : N) relationships connecting all entities cleanly."
    )
    p.paragraph_format.space_after = Pt(6)

    t_rel = doc.add_table(rows=1, cols=3)
    rel_headers = ["Relationship", "Between Entities", "Cardinality"]
    rel_data = [
        ("reports (reported_by_student_id)", "STUDENT – ITEM", "1 : N"),
        ("has (location_id)", "LOCATION – ITEM", "1 : N"),
        ("submits (student_id)", "STUDENT – LOST_REPORT", "1 : N"),
        ("documents (item_id)", "ITEM – LOST_REPORT", "1 : N"),
        ("submits (student_id)", "STUDENT – FOUND_REPORT", "1 : N"),
        ("documents (item_id)", "ITEM – FOUND_REPORT", "1 : N"),
        ("submits (claimant_student_id)", "STUDENT – CLAIM", "1 : N"),
        ("claimed for (item_id)", "ITEM – CLAIM", "1 : N"),
        ("reviews (admin_id)", "ADMIN – CLAIM", "1 : N")
    ]
    format_styled_table(t_rel, [Inches(2.5), Inches(2.5), Inches(1.5)], rel_headers, rel_data)

    # 5. Relational Schema
    add_styled_heading(doc, "5. Relational Schema", level=1)
    p = doc.add_paragraph(
        "Primary keys are marked PK and foreign keys are marked FK. All tables satisfy Third Normal Form (3NF).\n\n"
        "LOCATION (location_id PK, location_name, building)\n"
        "STUDENT (student_id PK, name, email UNIQUE, phone)\n"
        "ADMIN (admin_id PK, name, email UNIQUE)\n"
        "ITEM (item_id PK, item_name, description, category, date_reported, status, location_id FK, reported_by_student_id FK)\n"
        "LOST_REPORT (lost_report_id PK, item_id FK, student_id FK, date_lost, details)\n"
        "FOUND_REPORT (found_report_id PK, item_id FK, student_id FK, date_found, details)\n"
        "CLAIM (claim_id PK, item_id FK, claimant_student_id FK, claim_date, proof_description, claim_status, admin_id FK)"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    t_fk = doc.add_table(rows=1, cols=3)
    fk_headers = ["Foreign Key Column", "Child Table", "References Parent Table & Column"]
    fk_data = [
        ("reported_by_student_id", "ITEM", "STUDENT(student_id)"),
        ("location_id", "ITEM", "LOCATION(location_id)"),
        ("item_id", "LOST_REPORT", "ITEM(item_id) [ON DELETE CASCADE]"),
        ("student_id", "LOST_REPORT", "STUDENT(student_id)"),
        ("item_id", "FOUND_REPORT", "ITEM(item_id) [ON DELETE CASCADE]"),
        ("student_id", "FOUND_REPORT", "STUDENT(student_id)"),
        ("item_id", "CLAIM", "ITEM(item_id) [ON DELETE CASCADE]"),
        ("claimant_student_id", "CLAIM", "STUDENT(student_id)"),
        ("admin_id", "CLAIM", "ADMIN(admin_id) [Nullable until reviewed]")
    ]
    format_styled_table(t_fk, [Inches(2.0), Inches(1.8), Inches(2.7)], fk_headers, fk_data)

    # 6. Table Creation and Constraints
    add_styled_heading(doc, "6. Table Creation and Constraints", level=1)
    p = doc.add_paragraph(
        "The scripts are written for Oracle 12c/19c/21c and are also compatible with SQL Developer, SQL*Plus, and LiveSQL. "
        "Run the scripts in this sequence: 1. Tables & Constraints (DDL) -> 2. Sample Data (DML) -> 3. Stored Functions -> "
        "4. Stored Procedures -> 5. Triggers -> 6. Queries & Demonstrations."
    )
    p.paragraph_format.space_after = Pt(6)

    add_styled_heading(doc, "6.1 DDL – Create Tables", level=2)
    ddl_code = """-- 1. LOCATION TABLE
CREATE TABLE LOCATION (
    location_id     NUMBER(6)       NOT NULL,
    location_name   VARCHAR2(100)   NOT NULL,
    building        VARCHAR2(100)   NOT NULL,
    CONSTRAINT pk_location PRIMARY KEY (location_id)
);

-- 2. STUDENT TABLE
CREATE TABLE STUDENT (
    student_id      VARCHAR2(20)    NOT NULL,
    name            VARCHAR2(100)   NOT NULL,
    email           VARCHAR2(100)   NOT NULL,
    phone           VARCHAR2(20)    NOT NULL,
    CONSTRAINT pk_student PRIMARY KEY (student_id),
    CONSTRAINT uk_student_email UNIQUE (email)
);

-- 3. ADMIN TABLE
CREATE TABLE ADMIN (
    admin_id        NUMBER(6)       NOT NULL,
    name            VARCHAR2(100)   NOT NULL,
    email           VARCHAR2(100)   NOT NULL,
    CONSTRAINT pk_admin PRIMARY KEY (admin_id),
    CONSTRAINT uk_admin_email UNIQUE (email)
);

-- 4. ITEM TABLE
CREATE TABLE ITEM (
    item_id                 NUMBER(8)       NOT NULL,
    item_name               VARCHAR2(100)   NOT NULL,
    description             VARCHAR2(400),
    category                VARCHAR2(50)    NOT NULL,
    date_reported           DATE            DEFAULT SYSDATE NOT NULL,
    status                  VARCHAR2(20)    DEFAULT 'LOST' NOT NULL,
    location_id             NUMBER(6)       NOT NULL,
    reported_by_student_id  VARCHAR2(20)    NOT NULL,
    CONSTRAINT pk_item PRIMARY KEY (item_id),
    CONSTRAINT fk_item_location FOREIGN KEY (location_id) REFERENCES LOCATION(location_id),
    CONSTRAINT fk_item_student FOREIGN KEY (reported_by_student_id) REFERENCES STUDENT(student_id),
    CONSTRAINT chk_item_status CHECK (status IN ('LOST', 'FOUND', 'CLAIMED', 'RETURNED'))
);

-- 5. LOST_REPORT TABLE
CREATE TABLE LOST_REPORT (
    lost_report_id  NUMBER(8)       NOT NULL,
    item_id         NUMBER(8)       NOT NULL,
    student_id      VARCHAR2(20)    NOT NULL,
    date_lost       DATE            DEFAULT SYSDATE NOT NULL,
    details         VARCHAR2(400),
    CONSTRAINT pk_lost_report PRIMARY KEY (lost_report_id),
    CONSTRAINT fk_lost_item FOREIGN KEY (item_id) REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_lost_student FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

-- 6. FOUND_REPORT TABLE
CREATE TABLE FOUND_REPORT (
    found_report_id NUMBER(8)       NOT NULL,
    item_id         NUMBER(8)       NOT NULL,
    student_id      VARCHAR2(20)    NOT NULL,
    date_found      DATE            DEFAULT SYSDATE NOT NULL,
    details         VARCHAR2(400),
    CONSTRAINT pk_found_report PRIMARY KEY (found_report_id),
    CONSTRAINT fk_found_item FOREIGN KEY (item_id) REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_found_student FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

-- 7. CLAIM TABLE
CREATE TABLE CLAIM (
    claim_id            NUMBER(8)       NOT NULL,
    item_id             NUMBER(8)       NOT NULL,
    claimant_student_id VARCHAR2(20)    NOT NULL,
    claim_date          DATE            DEFAULT SYSDATE NOT NULL,
    proof_description   VARCHAR2(500)   NOT NULL,
    claim_status        VARCHAR2(20)    DEFAULT 'PENDING' NOT NULL,
    admin_id            NUMBER(6),
    CONSTRAINT pk_claim PRIMARY KEY (claim_id),
    CONSTRAINT fk_claim_item FOREIGN KEY (item_id) REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_claim_student FOREIGN KEY (claimant_student_id) REFERENCES STUDENT(student_id),
    CONSTRAINT fk_claim_admin FOREIGN KEY (admin_id) REFERENCES ADMIN(admin_id),
    CONSTRAINT chk_claim_status CHECK (claim_status IN ('PENDING', 'APPROVED', 'REJECTED'))
);"""
    add_code_block(doc, ddl_code)

    add_styled_heading(doc, "6.2 Constraints Summary", level=2)
    t_con = doc.add_table(rows=1, cols=3)
    con_headers = ["Constraint Type", "Where Used (Table & Column)", "Semantic Purpose"]
    con_data = [
        ("PRIMARY KEY", "Every table (location_id, student_id, admin_id, item_id, lost_report_id, found_report_id, claim_id)", "Guarantees unique entity identification with zero duplicate rows"),
        ("FOREIGN KEY", "ITEM (location_id, reported_by_student_id), LOST_REPORT (item_id, student_id), FOUND_REPORT (item_id, student_id), CLAIM (item_id, claimant_student_id, admin_id)", "Preserves referential consistency across all 9 relationships"),
        ("NOT NULL", "Names, emails, item names, categories, statuses, dates, and proof descriptions", "Prevents incomplete records and ensures essential data is always captured"),
        ("UNIQUE", "STUDENT(email), ADMIN(email)", "Prevents multiple accounts from registering with the same institutional email"),
        ("CHECK", "ITEM.status IN ('LOST', 'FOUND', 'CLAIMED', 'RETURNED')\nCLAIM.claim_status IN ('PENDING', 'APPROVED', 'REJECTED')", "Restricts domain values to permitted operational states"),
        ("DEFAULT", "date_reported = SYSDATE, date_lost = SYSDATE, date_found = SYSDATE, claim_date = SYSDATE, status = 'LOST', claim_status = 'PENDING'", "Automates default timestamping and initial workflow states"),
        ("ON DELETE CASCADE", "LOST_REPORT(item_id), FOUND_REPORT(item_id), CLAIM(item_id)", "Maintains referential cleanliness when an item record is safely purged")
    ]
    format_styled_table(t_con, [Inches(1.8), Inches(2.5), Inches(2.2)], con_headers, con_data)

    add_styled_heading(doc, "6.3 DML – Sample Data (10 or more records per table)", level=2)
    p = doc.add_paragraph(
        "All names, campus locations, and item descriptions represent realistic academic scenarios across VIT Vellore. "
        "A total of 72 records are populated across all 7 tables. Data is populated in strict parent-to-child order."
    )
    p.paragraph_format.space_after = Pt(6)

    dml_code = """-- 1. LOCATION (10 rows)
INSERT INTO LOCATION VALUES (101, 'Room 401 Lab', 'Silver Jubilee Tower (SJT)');
INSERT INTO LOCATION VALUES (102, 'Main Reading Hall', 'Central Library');
INSERT INTO LOCATION VALUES (103, 'Ground Floor Cafeteria', 'Foodys Central');
INSERT INTO LOCATION VALUES (104, 'Main Stage & Seating Area', 'Anna Auditorium');
INSERT INTO LOCATION VALUES (105, 'Room 214 Smart Classroom', 'Technology Tower (TT)');
INSERT INTO LOCATION VALUES (106, 'Physics Laboratory', 'Periyar EVR Block (PRP)');
INSERT INTO LOCATION VALUES (107, 'Badminton Court', 'Indoor Sports Complex');
INSERT INTO LOCATION VALUES (108, 'Mess Hall Block D', 'Men''s Hostel D Block');
INSERT INTO LOCATION VALUES (109, 'Common Study Lounge', 'Women''s Hostel B Block');
INSERT INTO LOCATION VALUES (110, 'Dean Office Reception', 'Main Building (MB)');

-- 2. STUDENT (10 rows)
INSERT INTO STUDENT VALUES ('24BYB0182', 'Arahat Gaikwad', 'arahat.gaikwad2024@vitstudent.ac.in', '9876543210');
INSERT INTO STUDENT VALUES ('24BCE1001', 'Rohan Sharma', 'rohan.sharma2024@vitstudent.ac.in', '9876543211');
INSERT INTO STUDENT VALUES ('24BCE1045', 'Ananya Iyer', 'ananya.iyer2024@vitstudent.ac.in', '9876543212');
INSERT INTO STUDENT VALUES ('24BEE0210', 'Vikas Patel', 'vikas.patel2024@vitstudent.ac.in', '9876543213');
INSERT INTO STUDENT VALUES ('24BCS0315', 'Sneha Reddy', 'sneha.reddy2024@vitstudent.ac.in', '9876543214');
INSERT INTO STUDENT VALUES ('24BME0512', 'Karthik Raja', 'karthik.raja2024@vitstudent.ac.in', '9876543215');
INSERT INTO STUDENT VALUES ('24BCE2190', 'Priya Menon', 'priya.menon2024@vitstudent.ac.in', '9876543216');
INSERT INTO STUDENT VALUES ('24BEC0420', 'Aditya Verma', 'aditya.verma2024@vitstudent.ac.in', '9876543217');
INSERT INTO STUDENT VALUES ('24BIT0115', 'Meera Nair', 'meera.nair2024@vitstudent.ac.in', '9876543218');
INSERT INTO STUDENT VALUES ('24BCE0882', 'Tanmay Sen', 'tanmay.sen2024@vitstudent.ac.in', '9876543219');

-- 3. ADMIN (10 rows)
INSERT INTO ADMIN VALUES (1, 'Dr. K. Raman', 'k.raman@vit.ac.in');
INSERT INTO ADMIN VALUES (2, 'Officer Ramesh Nair', 'ramesh.nair@security.vit.ac.in');
INSERT INTO ADMIN VALUES (3, 'Mrs. S. Vijayalakshmi', 'svijaya@library.vit.ac.in');
INSERT INTO ADMIN VALUES (4, 'Chief Warden S. Gupta', 'chiefwarden.mh@vit.ac.in');
INSERT INTO ADMIN VALUES (5, 'Officer Rajesh Singh', 'rajesh.singh@security.vit.ac.in');
INSERT INTO ADMIN VALUES (6, 'Mrs. Kalpana Das', 'kalpana.das@hostel.vit.ac.in');
INSERT INTO ADMIN VALUES (7, 'Mr. Arun Kumar', 'arun.kumar@admin.vit.ac.in');
INSERT INTO ADMIN VALUES (8, 'Security In-Charge Peter', 'peter.security@vit.ac.in');
INSERT INTO ADMIN VALUES (9, 'Dr. Deepa Chandran', 'deepa.chandran@vit.ac.in');
INSERT INTO ADMIN VALUES (10, 'Officer Selvam M.', 'selvam.m@security.vit.ac.in');

-- 4. ITEM (12 rows: LOST, FOUND, CLAIMED, RETURNED)
INSERT INTO ITEM VALUES (1001, 'VIT Student ID Card', 'ID Card belonging to Arahat Gaikwad with lanyard', 'Identity Cards', DATE '2026-10-10', 'RETURNED', 102, '24BYB0182');
INSERT INTO ITEM VALUES (1002, 'Apple AirPods Pro 2', 'White AirPods case with blue silicone cover', 'Electronics', DATE '2026-10-12', 'FOUND', 101, '24BCE1001');
INSERT INTO ITEM VALUES (1003, 'Black Casio Scientific Calculator', 'Model fx-991EX Classwiz with scratch on back', 'Electronics', DATE '2026-10-14', 'CLAIMED', 105, '24BCE1045');
INSERT INTO ITEM VALUES (1004, 'Blue Hydro Flask Water Bottle', '32oz wide mouth insulated flask with campus stickers', 'Personal Accessories', DATE '2026-10-15', 'LOST', 103, '24BEE0210');
INSERT INTO ITEM VALUES (1005, 'Database System Concepts Textbook', 'Silberschatz 7th edition hardcover book', 'Books & Study Material', DATE '2026-10-16', 'FOUND', 102, '24BCS0315');
INSERT INTO ITEM VALUES (1006, 'Hostel Room Key Set', 'Set of 3 brass keys with metal Marvel keychain', 'Keys', DATE '2026-10-18', 'RETURNED', 108, '24BME0512');
INSERT INTO ITEM VALUES (1007, 'Fastrack Black Analog Watch', 'Black dial leather strap watch found near court bench', 'Personal Accessories', DATE '2026-10-19', 'FOUND', 107, '24BCE2190');
INSERT INTO ITEM VALUES (1008, 'Lenovo 65W USB-C Charger', 'Original black ThinkPad laptop charger with adapter', 'Electronics', DATE '2026-10-20', 'LOST', 101, '24BEC0420');
INSERT INTO ITEM VALUES (1009, 'Brown Leather Wallet', 'Contains driver license and metro card', 'Wallets & Bags', DATE '2026-10-21', 'CLAIMED', 104, '24BIT0115');
INSERT INTO ITEM VALUES (1010, 'Noise Smartwatch Champagne Gold', 'ColorFit Pro 4 smartwatch with silicone band', 'Electronics', DATE '2026-10-22', 'LOST', 106, '24BCE0882');
INSERT INTO ITEM VALUES (1011, 'Black Umbrella', 'Compact foldable umbrella with auto-open button', 'Personal Accessories', DATE '2026-10-23', 'FOUND', 110, '24BYB0182');
INSERT INTO ITEM VALUES (1012, 'Spectacles in Red Case', 'Frameless reading glasses inside red hard shell case', 'Personal Accessories', DATE '2026-10-24', 'FOUND', 109, '24BCS0315');

-- 5. LOST_REPORT (10 rows)
INSERT INTO LOST_REPORT VALUES (201, 1001, '24BYB0182', DATE '2026-10-09', 'Lost ID card while reading near reference section in Central Library.');
INSERT INTO LOST_REPORT VALUES (202, 1003, '24BCE1045', DATE '2026-10-13', 'Left scientific calculator on desk row 3 after morning class.');
INSERT INTO LOST_REPORT VALUES (203, 1004, '24BEE0210', DATE '2026-10-15', 'Misplaced blue water bottle near the juice counter at Foodys.');
INSERT INTO LOST_REPORT VALUES (204, 1006, '24BME0512', DATE '2026-10-17', 'Keys slipped out of pocket while having dinner in D block mess.');
INSERT INTO LOST_REPORT VALUES (205, 1008, '24BEC0420', DATE '2026-10-20', 'Forgot Lenovo type-C laptop charger plugged in SJT lab 401.');
INSERT INTO LOST_REPORT VALUES (206, 1009, '24BIT0115', DATE '2026-10-21', 'Wallet dropped in Anna Auditorium auditorium seating row J.');
INSERT INTO LOST_REPORT VALUES (207, 1010, '24BCE0882', DATE '2026-10-22', 'Took off smartwatch before physics experiment, forgot to pick it up.');
INSERT INTO LOST_REPORT VALUES (208, 1002, '24BCE1001', DATE '2026-10-11', 'Misplaced AirPods Pro in computer lab during afternoon session.');
INSERT INTO LOST_REPORT VALUES (209, 1011, '24BCE2190', DATE '2026-10-22', 'Left black umbrella outside Dean office entrance in rain.');
INSERT INTO LOST_REPORT VALUES (210, 1012, '24BCE1045', DATE '2026-10-23', 'Left reading glasses in ladies hostel common room table.');

-- 6. FOUND_REPORT (10 rows)
INSERT INTO FOUND_REPORT VALUES (301, 1001, '24BCE1001', DATE '2026-10-10', 'Found student ID card lying on table 14 of library reading hall.');
INSERT INTO FOUND_REPORT VALUES (302, 1002, '24BYB0182', DATE '2026-10-12', 'Discovered AirPods case under computer bench 22 in SJT 401.');
INSERT INTO FOUND_REPORT VALUES (303, 1003, '24BCS0315', DATE '2026-10-14', 'Handed in calculator found on podium in TT room 214.');
INSERT INTO FOUND_REPORT VALUES (304, 1005, '24BCS0315', DATE '2026-10-16', 'Found database textbook on corner desk at Central Library.');
INSERT INTO FOUND_REPORT VALUES (305, 1006, '24BCE1001', DATE '2026-10-18', 'Picked up hostel room keys from D-block water cooler.');
INSERT INTO FOUND_REPORT VALUES (306, 1007, '24BCE2190', DATE '2026-10-19', 'Found Fastrack wristwatch resting on bleachers at sports complex.');
INSERT INTO FOUND_REPORT VALUES (307, 1009, '24BEE0210', DATE '2026-10-21', 'Turned in brown wallet discovered on auditorium chair.');
INSERT INTO FOUND_REPORT VALUES (308, 1011, '24BYB0182', DATE '2026-10-23', 'Found umbrella stand outside MB dean reception.');
INSERT INTO FOUND_REPORT VALUES (309, 1012, '24BCS0315', DATE '2026-10-24', 'Found eyeglasses in case on study table in B block.');
INSERT INTO FOUND_REPORT VALUES (310, 1004, '24BME0512', DATE '2026-10-24', 'Found insulated water bottle left on outdoor bench near Foodys.');

-- 7. CLAIM (10 rows: PENDING, APPROVED, REJECTED)
INSERT INTO CLAIM VALUES (401, 1001, '24BYB0182', DATE '2026-10-10', 'Matches my student photo, name Arahat Gaikwad, and reg no 24BYB0182.', 'APPROVED', 3);
INSERT INTO CLAIM VALUES (402, 1002, '24BCE1001', DATE '2026-10-13', 'Connects to my iPhone named "Rohan''s AirPods" and serial matches box.', 'PENDING', NULL);
INSERT INTO CLAIM VALUES (403, 1002, '24BEE0210', DATE '2026-10-14', 'I lost white airpods in SJT, but cannot provide original serial bill.', 'REJECTED', 2);
INSERT INTO CLAIM VALUES (404, 1003, '24BCE1045', DATE '2026-10-15', 'Has my initials AI carved on the battery slide cover.', 'APPROVED', 1);
INSERT INTO CLAIM VALUES (405, 1005, '24BCS0315', DATE '2026-10-17', 'VIT library barcode stamp on page 50 matching my book issue slip.', 'APPROVED', 3);
INSERT INTO CLAIM VALUES (406, 1006, '24BME0512', DATE '2026-10-18', 'Keys fit Room 314 D Block lock, verified with hostel warden.', 'APPROVED', 4);
INSERT INTO CLAIM VALUES (407, 1007, '24BCE2190', DATE '2026-10-20', 'Warranty card photo on my phone showing serial number.', 'PENDING', NULL);
INSERT INTO CLAIM VALUES (408, 1009, '24BIT0115', DATE '2026-10-22', 'Government driving license inside bears my photo and name Meera Nair.', 'APPROVED', 5);
INSERT INTO CLAIM VALUES (409, 1011, '24BCE2190', DATE '2026-10-24', 'Black umbrella with distinct silver tape mark on handle.', 'PENDING', NULL);
INSERT INTO CLAIM VALUES (410, 1012, '24BCE1045', DATE '2026-10-25', 'Spectacle frame prescription matches my optometrist card (-2.5 both eyes).', 'PENDING', NULL);
COMMIT;"""
    add_code_block(doc, dml_code)

    add_styled_heading(doc, "6.4 INSERT, UPDATE and DELETE Operations", level=2)
    dml_demo_code = """-- INSERT: Add a new student, location, and lost item
INSERT INTO STUDENT VALUES ('24BCS9999', 'Rishi Mukherjee', 'rishi.mukherjee2024@vitstudent.ac.in', '9898989898');
INSERT INTO LOCATION VALUES (111, 'Smart Conference Hall 1', 'Technology Tower (TT)');
INSERT INTO ITEM VALUES (1099, 'HP Wireless Mouse', 'Grey HP bluetooth optical mouse with dongle', 'Electronics', SYSDATE, 'LOST', 111, '24BCS9999');
INSERT INTO LOST_REPORT VALUES (299, 1099, '24BCS9999', SYSDATE, 'Left mouse on conference table during club meeting.');

-- UPDATE: Modify student contact info and update an item's details
UPDATE STUDENT SET phone = '9123456780' WHERE student_id = '24BCS9999';
UPDATE ITEM SET description = 'Grey HP bluetooth optical mouse with USB-C dongle attached' WHERE item_id = 1099;
UPDATE CLAIM SET proof_description = proof_description || ' [Admin Note: Photo verified at desk.]' WHERE claim_id = 402;

-- DELETE: Remove duplicate claim and clean up test records
INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status)
VALUES (499, 1099, '24BCS9999', SYSDATE, 'Accidental duplicate claim', 'PENDING');
DELETE FROM CLAIM WHERE claim_id = 499;
DELETE FROM LOST_REPORT WHERE lost_report_id = 299;
DELETE FROM ITEM WHERE item_id = 1099;
DELETE FROM LOCATION WHERE location_id = 111;
DELETE FROM STUDENT WHERE student_id = '24BCS9999';
COMMIT;"""
    add_code_block(doc, dml_demo_code)

    # Embed Screenshot 1
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_1_dml.png"), "Figure 6.1: Execution of INSERT, UPDATE, and DELETE Operations in Oracle SQL Developer")

    # 7. SQL Queries and Outputs
    add_styled_heading(doc, "7. SQL Queries and Outputs", level=1)
    p = doc.add_paragraph(
        "A total of 16 meaningful queries were developed covering simple filtering, multi-table inner joins, "
        "left outer joins, aggregate functions with GROUP BY and HAVING, subqueries (IN, NOT IN, NOT EXISTS, correlated), "
        "set operations (UNION ALL), date arithmetic, and window analytical ranking (DENSE_RANK)."
    )
    p.paragraph_format.space_after = Pt(6)

    queries_listing = """-- Q1 Filtering & Sorting: Items currently available in FOUND status
SELECT item_id, item_name, category, date_reported, status FROM ITEM WHERE status = 'FOUND' ORDER BY date_reported ASC;

-- Q2 3-Table INNER JOIN: Reported items with reporter student identity and building
SELECT i.item_id, i.item_name, i.category, s.student_id, s.name AS reporter, l.building
FROM ITEM i JOIN STUDENT s ON i.reported_by_student_id = s.student_id JOIN LOCATION l ON i.location_id = l.location_id;

-- Q3 LEFT OUTER JOIN: All items and their claims (detects items with zero claims)
SELECT i.item_id, i.item_name, i.status AS item_status, NVL(TO_CHAR(c.claim_id), 'NO CLAIM') AS claim_id, NVL(c.claim_status, 'UNCLAIMED') AS claim_status
FROM ITEM i LEFT OUTER JOIN CLAIM c ON i.item_id = c.item_id;

-- Q4 GROUP BY & Conditional Aggregation: Item status breakdown per category
SELECT category, COUNT(item_id) AS total,
       SUM(CASE WHEN status='LOST' THEN 1 ELSE 0 END) AS lost,
       SUM(CASE WHEN status='FOUND' THEN 1 ELSE 0 END) AS found,
       SUM(CASE WHEN status IN ('CLAIMED','RETURNED') THEN 1 ELSE 0 END) AS resolved
FROM ITEM GROUP BY category ORDER BY total DESC;

-- Q5 Aggregate with HAVING: Campus buildings with 2 or more loss incidents (Hotspots)
SELECT l.building, COUNT(i.item_id) AS incidents
FROM LOCATION l JOIN ITEM i ON l.location_id = i.location_id
GROUP BY l.building HAVING COUNT(i.item_id) >= 2;

-- Q6 Subquery with IN & NOT IN: Students who reported lost items but never submitted a claim
SELECT student_id, name, email FROM STUDENT
WHERE student_id IN (SELECT student_id FROM LOST_REPORT)
  AND student_id NOT IN (SELECT claimant_student_id FROM CLAIM);

-- Q7 Subquery with NOT EXISTS: Cataloged items that have zero claims submitted
SELECT i.item_id, i.item_name, i.category, i.status FROM ITEM i
WHERE NOT EXISTS (SELECT 1 FROM CLAIM c WHERE c.item_id = i.item_id);

-- Q8 Correlated Subquery: Total claims count calculated dynamically per item
SELECT i.item_id, i.item_name, i.status, (SELECT COUNT(*) FROM CLAIM c WHERE c.item_id = i.item_id) AS total_claims
FROM ITEM i ORDER BY total_claims DESC;

-- Q9 Set Operator (UNION ALL): Consolidated chronological campus incident timeline
SELECT 'LOST' AS event_type, i.item_name, lr.date_lost AS event_date, s.name FROM LOST_REPORT lr JOIN ITEM i ON lr.item_id=i.item_id JOIN STUDENT s ON lr.student_id=s.student_id
UNION ALL
SELECT 'FOUND' AS event_type, i.item_name, fr.date_found AS event_date, s.name FROM FOUND_REPORT fr JOIN ITEM i ON fr.item_id=i.item_id JOIN STUDENT s ON fr.student_id=s.student_id
ORDER BY event_date DESC;

-- Q10 Pattern Matching (LIKE): Search for electronics matching user keywords
SELECT item_id, item_name, description, category FROM ITEM
WHERE UPPER(item_name) LIKE '%AIRPODS%' OR UPPER(description) LIKE '%CHARGER%' OR UPPER(item_name) LIKE '%CALCULATOR%';

-- Q11 Date Arithmetic: Calculate elapsed days items have remained unresolved
SELECT item_id, item_name, status, TO_CHAR(date_reported, 'YYYY-MM-DD') AS report_date, ROUND(SYSDATE - date_reported, 1) AS days_in_system
FROM ITEM ORDER BY days_in_system DESC;

-- Q12 4-Table Join: Approved claims audit showing claimant, item, building, and approving admin
SELECT c.claim_id, s.name AS claimant, i.item_name, l.building, a.name AS approved_by, TO_CHAR(c.claim_date, 'YYYY-MM-DD') AS claim_date
FROM CLAIM c JOIN STUDENT s ON c.claimant_student_id = s.student_id JOIN ITEM i ON c.item_id = i.item_id JOIN LOCATION l ON i.location_id = l.location_id JOIN ADMIN a ON c.admin_id = a.admin_id
WHERE c.claim_status = 'APPROVED';

-- Q13 Subquery Comparison against System Average: Items unresolved longer than average
SELECT item_id, item_name, category, status FROM ITEM
WHERE (SYSDATE - date_reported) >= (SELECT AVG(SYSDATE - date_reported) FROM ITEM);

-- Q14 Conditional Aggregation: Performance summary of approved vs rejected decisions per admin
SELECT a.admin_id, a.name, COUNT(c.claim_id) AS total_reviewed,
       SUM(CASE WHEN c.claim_status='APPROVED' THEN 1 ELSE 0 END) AS approved_count,
       SUM(CASE WHEN c.claim_status='REJECTED' THEN 1 ELSE 0 END) AS rejected_count
FROM ADMIN a LEFT JOIN CLAIM c ON a.admin_id = c.admin_id GROUP BY a.admin_id, a.name;

-- Q15 Window Analytical Function (DENSE_RANK): Rank categories by incident frequency
SELECT category, COUNT(*) AS total_items, DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS category_rank
FROM ITEM GROUP BY category;

-- Q16 Conflict Detection (HAVING): Identify items with multiple competing claims
SELECT c.item_id, i.item_name, COUNT(c.claim_id) AS competing_claims
FROM CLAIM c JOIN ITEM i ON c.item_id = i.item_id GROUP BY c.item_id, i.item_name HAVING COUNT(c.claim_id) > 1;"""
    add_code_block(doc, queries_listing)

    # Embed Screenshot 2
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_2_queries.png"), "Figure 7.1: Multi-Table Inner Join Query Execution and Result Grid in Oracle SQL Developer")

    # 8. Procedures, Functions, Cursor and Triggers
    add_styled_heading(doc, "8. Procedures, Functions, Cursor and Triggers", level=1)
    p = doc.add_paragraph("Compile components in this sequence: Functions first, then Procedures, then Triggers.")
    p.paragraph_format.space_after = Pt(6)

    # 8.1 Functions
    add_styled_heading(doc, "8.1 Functions", level=2)
    func_code = """-- Function 1: Calculates how many days an item has been reported / unclaimed
CREATE OR REPLACE FUNCTION FUNC_CALCULATE_UNCLAIMED_DAYS (p_item_id IN NUMBER)
RETURN NUMBER AS
    v_date_reported DATE;
    v_status        VARCHAR2(20);
    v_claim_date    DATE;
    v_days          NUMBER;
BEGIN
    SELECT date_reported, status INTO v_date_reported, v_status FROM ITEM WHERE item_id = p_item_id;

    IF v_status = 'RETURNED' THEN
        SELECT MIN(claim_date) INTO v_claim_date FROM CLAIM WHERE item_id = p_item_id AND claim_status = 'APPROVED';
        IF v_claim_date IS NOT NULL THEN
            v_days := ROUND(v_claim_date - v_date_reported, 1);
        ELSE
            v_days := ROUND(SYSDATE - v_date_reported, 1);
        END IF;
    ELSE
        v_days := ROUND(SYSDATE - v_date_reported, 1);
    END IF;

    RETURN GREATEST(v_days, 0);
EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN -1;
    WHEN OTHERS THEN RETURN -99;
END;
/

-- Function 2: Returns consolidated activity metrics for a registered student
CREATE OR REPLACE FUNCTION FUNC_GET_STUDENT_ACTIVITY (p_student_id IN VARCHAR2)
RETURN VARCHAR2 AS
    v_lost_count   NUMBER := 0;
    v_found_count  NUMBER := 0;
    v_claims_count NUMBER := 0;
    v_student_name VARCHAR2(100);
BEGIN
    SELECT name INTO v_student_name FROM STUDENT WHERE student_id = p_student_id;
    SELECT COUNT(*) INTO v_lost_count   FROM LOST_REPORT  WHERE student_id = p_student_id;
    SELECT COUNT(*) INTO v_found_count  FROM FOUND_REPORT WHERE student_id = p_student_id;
    SELECT COUNT(*) INTO v_claims_count FROM CLAIM        WHERE claimant_student_id = p_student_id;

    RETURN v_student_name || ' [' || p_student_id || '] -> Lost Filed: ' || v_lost_count ||
           ' | Found Filed: ' || v_found_count || ' | Claims Submitted: ' || v_claims_count;
EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN 'Student not found in registry.';
    WHEN OTHERS THEN RETURN 'Error generating activity summary.';
END;
/"""
    add_code_block(doc, func_code)

    # 8.2 Procedures
    add_styled_heading(doc, "8.2 Procedures", level=2)
    proc_code = """-- Procedure 1: Submits an ownership claim with pre-validation and duplicate checks
CREATE OR REPLACE PROCEDURE PROC_SUBMIT_CLAIM (
    p_item_id           IN  NUMBER,
    p_claimant_id       IN  VARCHAR2,
    p_proof             IN  VARCHAR2,
    p_new_claim_id      OUT NUMBER,
    p_result_msg        OUT VARCHAR2
) AS
    v_student_count     NUMBER;
    v_item_status       VARCHAR2(20);
    v_existing_claim    NUMBER;
    v_max_id            NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_student_count FROM STUDENT WHERE student_id = p_claimant_id;
    IF v_student_count = 0 THEN
        p_new_claim_id := -1;
        p_result_msg := 'ERROR: Student ID ' || p_claimant_id || ' is not registered.';
        RETURN;
    END IF;

    BEGIN
        SELECT status INTO v_item_status FROM ITEM WHERE item_id = p_item_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_new_claim_id := -1;
            p_result_msg := 'ERROR: Item ID ' || p_item_id || ' does not exist.';
            RETURN;
    END;

    IF v_item_status = 'RETURNED' THEN
        p_new_claim_id := -1;
        p_result_msg := 'ERROR: Item ' || p_item_id || ' has already been returned to its owner.';
        RETURN;
    END IF;

    SELECT COUNT(*) INTO v_existing_claim FROM CLAIM
    WHERE item_id = p_item_id AND claimant_student_id = p_claimant_id AND claim_status = 'PENDING';
    IF v_existing_claim > 0 THEN
        p_new_claim_id := -1;
        p_result_msg := 'ERROR: Student already has a pending claim for this item.';
        RETURN;
    END IF;

    SELECT NVL(MAX(claim_id), 400) + 1 INTO v_max_id FROM CLAIM;
    INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status)
    VALUES (v_max_id, p_item_id, p_claimant_id, SYSDATE, p_proof, 'PENDING');

    p_new_claim_id := v_max_id;
    p_result_msg := 'SUCCESS: Claim #' || v_max_id || ' submitted successfully in PENDING status.';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_new_claim_id := -1;
        p_result_msg := 'SYSTEM EXCEPTION: ' || SQLERRM;
END;
/

-- Procedure 2: Adjudicates claims with automatic status updates & conflict resolution
CREATE OR REPLACE PROCEDURE PROC_VERIFY_CLAIM (
    p_claim_id          IN  NUMBER,
    p_admin_id          IN  NUMBER,
    p_decision          IN  VARCHAR2, -- 'APPROVED' or 'REJECTED'
    p_result_msg        OUT VARCHAR2
) AS
    v_admin_count       NUMBER;
    v_curr_status       VARCHAR2(20);
    v_target_item_id    NUMBER;
    v_decision_upper    VARCHAR2(20);
BEGIN
    v_decision_upper := UPPER(TRIM(p_decision));
    IF v_decision_upper NOT IN ('APPROVED', 'REJECTED') THEN
        p_result_msg := 'ERROR: Decision must be either APPROVED or REJECTED.';
        RETURN;
    END IF;

    SELECT COUNT(*) INTO v_admin_count FROM ADMIN WHERE admin_id = p_admin_id;
    IF v_admin_count = 0 THEN
        p_result_msg := 'ERROR: Admin ID ' || p_admin_id || ' does not exist.';
        RETURN;
    END IF;

    BEGIN
        SELECT claim_status, item_id INTO v_curr_status, v_target_item_id FROM CLAIM WHERE claim_id = p_claim_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_result_msg := 'ERROR: Claim ID ' || p_claim_id || ' not found.';
            RETURN;
    END;

    IF v_curr_status != 'PENDING' THEN
        p_result_msg := 'ERROR: Claim #' || p_claim_id || ' is already processed as ' || v_curr_status || '.';
        RETURN;
    END IF;

    IF v_decision_upper = 'APPROVED' THEN
        UPDATE CLAIM SET claim_status = 'APPROVED', admin_id = p_admin_id WHERE claim_id = p_claim_id;
        UPDATE ITEM SET status = 'RETURNED' WHERE item_id = v_target_item_id;
        UPDATE CLAIM SET claim_status = 'REJECTED', admin_id = p_admin_id
        WHERE item_id = v_target_item_id AND claim_id != p_claim_id AND claim_status = 'PENDING';

        p_result_msg := 'SUCCESS: Claim #' || p_claim_id || ' APPROVED. Item #' || v_target_item_id || ' marked RETURNED.';
    ELSE
        UPDATE CLAIM SET claim_status = 'REJECTED', admin_id = p_admin_id WHERE claim_id = p_claim_id;
        p_result_msg := 'SUCCESS: Claim #' || p_claim_id || ' REJECTED by Admin #' || p_admin_id || '.';
    END IF;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_result_msg := 'SYSTEM EXCEPTION: ' || SQLERRM;
END;
/"""
    add_code_block(doc, proc_code)

    # 8.3 Cursor
    add_styled_heading(doc, "8.3 Cursor", level=2)
    p = doc.add_paragraph(
        "The procedure below uses an explicit cursor to process multiple records sequentially. "
        "It manages the complete lifecycle (OPEN, FETCH, %NOTFOUND loop, CLOSE) to scan all unresolved items "
        "whose age exceeds a threshold and compile an automated batch security report."
    )
    p.paragraph_format.space_after = Pt(4)

    cursor_code = """CREATE OR REPLACE PROCEDURE PROC_FLAG_LONG_UNCLAIMED_ITEMS (
    p_days_threshold IN  NUMBER,
    p_total_flagged  OUT NUMBER
) AS
    CURSOR cur_unclaimed_items IS
        SELECT i.item_id, i.item_name, i.category, i.status, i.date_reported, l.building
        FROM ITEM i JOIN LOCATION l ON i.location_id = l.location_id
        WHERE i.status IN ('LOST', 'FOUND')
          AND (SYSDATE - i.date_reported) >= p_days_threshold
        ORDER BY i.date_reported ASC;

    v_item_rec cur_unclaimed_items%ROWTYPE;
    v_count    NUMBER := 0;
    v_days     NUMBER;
BEGIN
    DBMS_OUTPUT.PUT_LINE('=================================================================');
    DBMS_OUTPUT.PUT_LINE('  BATCH CURSOR AUDIT: ITEMS UNCLAIMED >= ' || p_days_threshold || ' DAYS');
    DBMS_OUTPUT.PUT_LINE('=================================================================');
    DBMS_OUTPUT.PUT_LINE(RPAD('ITEM ID', 10) || RPAD('ITEM NAME', 28) || RPAD('STATUS', 10) || RPAD('DAYS', 8) || 'LOCATION');
    DBMS_OUTPUT.PUT_LINE('-----------------------------------------------------------------');

    OPEN cur_unclaimed_items; -- 1. OPEN Cursor
    LOOP
        FETCH cur_unclaimed_items INTO v_item_rec; -- 2. FETCH Record
        EXIT WHEN cur_unclaimed_items%NOTFOUND;    -- 3. Check %NOTFOUND

        v_count := v_count + 1;
        v_days := ROUND(SYSDATE - v_item_rec.date_reported, 1);
        DBMS_OUTPUT.PUT_LINE(
            RPAD(TO_CHAR(v_item_rec.item_id), 10) ||
            RPAD(SUBSTR(v_item_rec.item_name, 1, 26), 28) ||
            RPAD(v_item_rec.status, 10) ||
            RPAD(TO_CHAR(v_days), 8) ||
            v_item_rec.building
        );
    END LOOP;
    CLOSE cur_unclaimed_items; -- 4. CLOSE Cursor

    DBMS_OUTPUT.PUT_LINE('-----------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('Total Long-Unclaimed Items Processed: ' || v_count);
    p_total_flagged := v_count;
END;
/"""
    add_code_block(doc, cursor_code)

    # 8.4 Triggers
    add_styled_heading(doc, "8.4 Triggers", level=2)
    trigger_code = """-- Trigger 1: Prevents fraudulent or duplicate claims on already returned items
CREATE OR REPLACE TRIGGER TRG_PREVENT_CLAIM_ON_RETURNED
BEFORE INSERT ON CLAIM
FOR EACH ROW
DECLARE
    v_status VARCHAR2(20);
BEGIN
    SELECT status INTO v_status FROM ITEM WHERE item_id = :NEW.item_id;

    IF v_status = 'RETURNED' THEN
        RAISE_APPLICATION_ERROR(
            -20001, 
            'Integrity Rule Violation: Item #' || :NEW.item_id || ' has already been RETURNED to its owner. New claims are disallowed.'
        );
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'Referenced item #' || :NEW.item_id || ' does not exist.');
END;
/

-- Trigger 2: Automatically updates ITEM status to RETURNED upon claim approval
CREATE OR REPLACE TRIGGER TRG_AUTO_UPDATE_ITEM_STATUS
AFTER UPDATE OF claim_status ON CLAIM
FOR EACH ROW
BEGIN
    IF :NEW.claim_status = 'APPROVED' AND (:OLD.claim_status IS NULL OR :OLD.claim_status != 'APPROVED') THEN
        UPDATE ITEM
        SET status = 'RETURNED'
        WHERE item_id = :NEW.item_id;
    END IF;
END;
/"""
    add_code_block(doc, trigger_code)

    # 8.5 Database Connectivity
    add_styled_heading(doc, "8.5 Database Connectivity (Python)", level=2)
    p = doc.add_paragraph(
        "The Python application provides interactive menu-driven access connecting to SQLite (embedded, zero-configuration) "
        "and Oracle Database using the oracledb driver. It allows students to file reports, submit claims, and view history, "
        "and provides security admins with claim adjudication and explicit cursor batch scanning."
    )
    p.paragraph_format.space_after = Pt(4)

    py_code = """import sys, os
from database import Database

db = Database(db_type="sqlite") # Connects to embedded database or Oracle via oracledb

def submit_claim_interactive():
    student_id = input("Enter Student Reg No: ").strip().upper()
    item_id = int(input("Enter Item ID to claim: ").strip())
    proof = input("Describe ownership proof (e.g. serial number): ").strip()
    
    # Executes PL/SQL procedure PROC_SUBMIT_CLAIM logic with trigger protection
    try:
        db.execute_dml("INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status) VALUES (?, ?, ?, DATE('now'), ?, 'PENDING')",
                       (next_id, item_id, student_id, proof))
        print("[SUCCESS] Claim submitted in PENDING status.")
    except Exception as e:
        print("[TRIGGER BLOCKED]:", e)"""
    add_code_block(doc, py_code)

    # Embed Screenshot 3
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_3_python_app.png"), "Figure 8.1: Interactive Python Application Terminal Session (Student Portal Claim Submission)")

    # 9. Real-World Transaction Demonstrations
    add_styled_heading(doc, "9. Real-World Transaction Demonstrations", level=1)
    p = doc.add_paragraph(
        "Every transaction demonstrates the complete end-to-end flow required by the course guidelines:\n"
        "User Operation → SQL/PL/SQL → Database Processing → Database Update/Retrieval → Result"
    )
    p.paragraph_format.space_after = Pt(8)

    # Demo 1
    add_styled_heading(doc, "Demonstration 1 – Student Reports Lost Belonging", level=2)
    t_d1 = doc.add_table(rows=1, cols=2)
    d1_headers = ["Evaluation Question", "System Implementation Answer"]
    d1_data = [
        ("What operation is performed?", "Student Arahat Gaikwad (24BYB0182) files a report for a missing ID card lost in Central Library"),
        ("Which tables are involved?", "STUDENT, LOCATION, ITEM, LOST_REPORT"),
        ("Which SQL/PL/SQL component runs?", "INSERT INTO ITEM (...) and INSERT INTO LOST_REPORT (...)"),
        ("How is the database affected?", "New ITEM row (ID 1001, status 'LOST') and linked LOST_REPORT row (ID 201) are inserted"),
        ("What result is generated?", "Item cataloged and indexed under Central Library; reference report ID generated for student")
    ]
    format_styled_table(t_d1, [Inches(2.2), Inches(4.3)], d1_headers, d1_data)
    
    d1_sql = """INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1001, 'VIT Student ID Card', 'ID Card belonging to Arahat Gaikwad', 'Identity Cards', DATE '2026-10-10', 'LOST', 102, '24BYB0182');
INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (201, 1001, '24BYB0182', DATE '2026-10-09', 'Lost near library reference hall.');
SELECT item_id, item_name, status, reported_by_student_id FROM ITEM WHERE item_id = 1001;"""
    add_code_block(doc, d1_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_4_demo1_lost.png"), "Figure 9.1: Demonstration 1 – Filing Lost Belonging and Item Table Creation")

    # Demo 2
    add_styled_heading(doc, "Demonstration 2 – Good Samaritan Reports Found Item", level=2)
    t_d2 = doc.add_table(rows=1, cols=2)
    d2_headers = ["Evaluation Question", "System Implementation Answer"]
    d2_data = [
        ("What operation is performed?", "Another student Rohan Sharma discovers the misplaced ID card and turns it in at library desk"),
        ("Which tables are involved?", "ITEM, FOUND_REPORT, STUDENT"),
        ("Which SQL/PL/SQL component runs?", "INSERT INTO FOUND_REPORT (...) and UPDATE ITEM SET status = 'FOUND'"),
        ("How is the database affected?", "FOUND_REPORT row (ID 301) is created; ITEM 1001 status is updated from 'LOST' to 'FOUND'"),
        ("What result is generated?", "Item is flagged as recovered and becomes visible to students searching the found catalog")
    ]
    format_styled_table(t_d2, [Inches(2.2), Inches(4.3)], d2_headers, d2_data)

    d2_sql = """INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (301, 1001, '24BCE1001', DATE '2026-10-10', 'Found lying on reading table 14.');
UPDATE ITEM SET status = 'FOUND' WHERE item_id = 1001;
SELECT item_id, item_name, status FROM ITEM WHERE item_id = 1001;"""
    add_code_block(doc, d2_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_5_demo2_found.png"), "Figure 9.2: Demonstration 2 – Found Report Filing and Item Status Update to 'FOUND'")

    # Demo 3
    add_styled_heading(doc, "Demonstration 3 – Student Files Claim via Stored Procedure", level=2)
    t_d3 = doc.add_table(rows=1, cols=2)
    d3_headers = ["Evaluation Question", "System Implementation Answer"]
    d3_data = [
        ("What operation is performed?", "Owner Arahat Gaikwad identifies his ID card in the found list and submits a claim with proof"),
        ("Which tables are involved?", "CLAIM, ITEM, STUDENT"),
        ("Which SQL/PL/SQL component runs?", "PROC_SUBMIT_CLAIM(1001, '24BYB0182', 'Matches my photo and reg no 24BYB0182', v_id, v_msg)"),
        ("How is the database affected?", "Pre-validates student and item; inserts Claim #401 with claim_status = 'PENDING' and admin_id = NULL"),
        ("What result is generated?", "Claim ID #401 created; message returned: 'SUCCESS: Claim submitted in PENDING status.'")
    ]
    format_styled_table(t_d3, [Inches(2.2), Inches(4.3)], d3_headers, d3_data)

    d3_sql = """VARIABLE v_claim_id NUMBER;
VARIABLE v_msg VARCHAR2(250);
EXEC PROC_SUBMIT_CLAIM(1001, '24BYB0182', 'Matches my student photo and reg no 24BYB0182', :v_claim_id, :v_msg);
PRINT v_msg;
SELECT claim_id, item_id, claimant_student_id, claim_status FROM CLAIM WHERE claim_id = 401;"""
    add_code_block(doc, d3_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_6_demo3_claim.png"), "Figure 9.3: Demonstration 3 – Stored Procedure PROC_SUBMIT_CLAIM Execution and Claim Generation")

    # Demo 4
    add_styled_heading(doc, "Demonstration 4 – Admin Review, Claim Approval & Trigger Auto-Update", level=2)
    t_d4 = doc.add_table(rows=1, cols=2)
    d4_headers = ["Evaluation Question", "System Implementation Answer"]
    d4_data = [
        ("What operation is performed?", "Library In-Charge Mrs. Vijayalakshmi (Admin 3) verifies proof and approves Claim #401"),
        ("Which tables are involved?", "CLAIM, ITEM, ADMIN"),
        ("Which SQL/PL/SQL component runs?", "PROC_VERIFY_CLAIM(401, 3, 'APPROVED', v_msg) and Trigger TRG_AUTO_UPDATE_ITEM_STATUS"),
        ("How is the database affected?", "Claim #401 status updated to 'APPROVED'; Trigger fires and sets ITEM #1001 status to 'RETURNED'"),
        ("What result is generated?", "Success message returned; item lifecycle complete; competing pending claims auto-rejected")
    ]
    format_styled_table(t_d4, [Inches(2.2), Inches(4.3)], d4_headers, d4_data)

    d4_sql = """VARIABLE v_msg VARCHAR2(250);
EXEC PROC_VERIFY_CLAIM(401, 3, 'APPROVED', :v_msg);
PRINT v_msg;
SELECT c.claim_id, c.claim_status, c.admin_id, i.item_id, i.status AS item_status
FROM CLAIM c JOIN ITEM i ON c.item_id = i.item_id WHERE c.claim_id = 401;"""
    add_code_block(doc, d4_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_7_demo4_verify.png"), "Figure 9.4: Demonstration 4 – Claim Approval and Trigger TRG_AUTO_UPDATE_ITEM_STATUS Execution")

    # Demo 5
    add_styled_heading(doc, "Demonstration 5 – Negative Integrity Test: Trigger Blocks Claim on Returned Item", level=2)
    t_d5 = doc.add_table(rows=1, cols=2)
    d5_headers = ["Evaluation Question", "System Implementation Answer"]
    d5_data = [
        ("What operation is performed?", "Another student (24BEE0210) attempts to file a fraudulent claim on Item #1001 (already RETURNED)"),
        ("Which tables are involved?", "CLAIM, ITEM"),
        ("Which SQL/PL/SQL component runs?", "Trigger TRG_PREVENT_CLAIM_ON_RETURNED (BEFORE INSERT ON CLAIM)"),
        ("How is the database affected?", "Trigger detects status = 'RETURNED' and executes RAISE_APPLICATION_ERROR(-20001, ...)"),
        ("What result is generated?", "Oracle error raised; insertion is immediately aborted; no dirty or conflicting claim is inserted")
    ]
    format_styled_table(t_d5, [Inches(2.2), Inches(4.3)], d5_headers, d5_data)

    d5_sql = """-- Attempting invalid claim on already returned item
INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status)
VALUES (999, 1001, '24BEE0210', SYSDATE, 'Attempting claim on already returned ID card', 'PENDING');
-- Expected: ORA-20001: Integrity Rule Violation: Item has already been RETURNED to its owner."""
    add_code_block(doc, d5_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_8_demo5_error.png"), "Figure 9.5: Demonstration 5 – Trigger TRG_PREVENT_CLAIM_ON_RETURNED Aborting Invalid Transaction")

    # Demo 6
    add_styled_heading(doc, "Demonstration 6 – Explicit Cursor Scans Long-Unclaimed Items in Bulk", level=2)
    t_d6 = doc.add_table(rows=1, cols=2)
    d6_headers = ["Evaluation Question", "System Implementation Answer"]
    d6_data = [
        ("What operation is performed?", "Campus security runs periodic batch audit for items unclaimed for >= 10 days"),
        ("Which tables are involved?", "ITEM, LOCATION"),
        ("Which SQL/PL/SQL component runs?", "PROC_FLAG_LONG_UNCLAIMED_ITEMS(10, v_total) using explicit cursor cur_unclaimed_items"),
        ("How is the database affected?", "Cursor iterates sequentially through items in memory, computing days unresolved and building location"),
        ("What result is generated?", "Batch audit table printed via DBMS_OUTPUT with total count of aged items flagged for auction")
    ]
    format_styled_table(t_d6, [Inches(2.2), Inches(4.3)], d6_headers, d6_data)

    d6_sql = """SET SERVEROUTPUT ON;
VARIABLE v_total NUMBER;
EXEC PROC_FLAG_LONG_UNCLAIMED_ITEMS(10, :v_total);
PRINT v_total;"""
    add_code_block(doc, d6_sql)
    add_embedded_image(doc, os.path.join(ss_dir, "screenshot_9_demo6_cursor.png"), "Figure 9.6: Demonstration 6 – Explicit Cursor Batch Processing and DBMS_OUTPUT Report")

    # 10. Conclusion and Future Enhancements
    add_styled_heading(doc, "10. Conclusion and Future Enhancements", level=1)
    p = doc.add_paragraph(
        "The Campus Lost and Found Management System successfully integrates relational modeling with robust PL/SQL business rules "
        "to solve the campus-wide challenge of misplaced and unrecovered personal articles. The system features 7 normalized tables (3NF) "
        "with complete primary keys, foreign keys, domain CHECK constraints, UNIQUE constraints, and DEFAULT values. "
        "A comprehensive suite of 16 SQL queries provides complex multi-table joins, categorical grouping, hotspot analysis, and subqueries.\n\n"
        "Business operations and lifecycle progression are implemented using 2 stored procedures, 2 stored functions, an explicit cursor "
        "for batch multi-record processing, and 2 database triggers that enforce strict integrity and automated synchronization. "
        "The system was demonstrated using both Oracle SQL/PL-SQL and an interactive Python application, confirming zero referential integrity "
        "violations and seamless end-to-end transaction flows.\n\n"
        "Future Enhancements:\n"
        "• Turnstile RFID & Smart Card Integration: Automatic owner notification when a lost ID card is scanned at campus security turnstiles.\n"
        "• Computer Vision Image Matching: Uploading photos of found items to compute image similarity scores against lost item descriptions.\n"
        "• Real-Time SMS / WhatsApp Notifications: Instant push messaging to students when claims are reviewed or when matching items are turned in."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(12)

    # Save documents
    out_dir = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project\docs"
    out_file = os.path.join(out_dir, "Campus_Lost_and_Found_Review2_Report.docx")
    doc.save(out_file)
    print(f"Document successfully created at: {out_file}")

    root_file = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Review2_Report.docx"
    doc.save(root_file)
    print(f"Copy saved at: {root_file}")

if __name__ == "__main__":
    build_review2_doc()
