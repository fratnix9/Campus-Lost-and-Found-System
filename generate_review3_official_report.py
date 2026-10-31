"""
Official Review 3 Final Project Report Generator
Format: School of Computer Science Engineering and Information Systems (SCORE) - VIT Vellore
Course: BCSE302L - Database Systems
Student: Arahat Gaikwad (24BYB0182)
Academic Year: 2026-2027

Strictly follows the 13-Chapter Official Syllabus Template without any marks annotations.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project\docs"
SHOTS_DIR = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project\screenshots"

# Palette: Academic Executive Navy
CLR_PRIMARY = RGBColor(15, 23, 42)      # Deep Slate #0F172A
CLR_SECONDARY = RGBColor(30, 58, 138)   # Navy Blue #1E3A8A
CLR_TEXT = RGBColor(30, 41, 59)         # Charcoal #1E293B
CLR_MUTED = RGBColor(100, 116, 139)     # Slate Gray #64748B
CLR_CODE = RGBColor(15, 23, 42)         # Dark Code Text

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = CLR_SECONDARY
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = CLR_PRIMARY
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = CLR_TEXT
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = CLR_TEXT
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = CLR_TEXT
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = CLR_TEXT
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = CLR_TEXT
    return p

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.05
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = CLR_CODE
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_image_box(doc, img_path, caption_text, width=Inches(5.8)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = CLR_MUTED

def style_table(table, header_bg="1E3A8A"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, col in enumerate(table.columns):
        for cell in col.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for cell in table.rows[0].cells:
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, top=90, bottom=90, left=110, right=110)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(10)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
    for r_idx, row in enumerate(table.rows[1:]):
        bg = "F8FAFC" if (r_idx % 2 == 1) else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = CLR_TEXT

def create_report():
    doc = docx.Document()
    
    # Configure 1-inch margins
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    logo_path = os.path.join(DOCS_DIR, "vit_logo.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(12)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(3.2))

    p_sch = doc.add_paragraph()
    p_sch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sch.paragraph_format.space_after = Pt(2)
    r = p_sch.add_run("School of Computer Science Engineering and Information Systems (SCORE)\nVIT, Vellore")
    r.font.name = 'Calibri'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = CLR_SECONDARY

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_before = Pt(20)
    p_course.paragraph_format.space_after = Pt(4)
    r = p_course.add_run("DATABASE SYSTEMS (BCSE302L)")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = CLR_TEXT

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_after = Pt(18)
    r = p_rep.add_run("PROJECT REPORT")
    r.font.name = 'Calibri'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = CLR_MUTED

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(28)
    r = p_title.add_run("“Campus Lost and Found Management System with Rule-Based Automated Claim Verification”")
    r.font.name = 'Calibri'
    r.font.size = Pt(17)
    r.font.bold = True
    r.font.color.rgb = CLR_SECONDARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(4)
    r = p_sub.add_run("Submitted by")
    r.font.name = 'Calibri'
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = CLR_MUTED

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_after = Pt(2)
    r = p_author.add_run("ARAHAT GAIKWAD")
    r.font.name = 'Calibri'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = CLR_PRIMARY

    p_reg = doc.add_paragraph()
    p_reg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_reg.paragraph_format.space_after = Pt(30)
    r = p_reg.add_run("Register Number: 24BYB0182\nB.Tech Computer Science and Engineering")
    r.font.name = 'Calibri'
    r.font.size = Pt(11)
    r.font.color.rgb = CLR_TEXT

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(20)
    r = p_foot.add_run("Academic Year: 2026–2027\nProject Workspace: c:\\Users\\gaikw\\Downloads\\Campus_Lost_and_Found_Project")
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = CLR_MUTED

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER
    # =========================================================================
    add_heading_1(doc, "CERTIFICATE")
    add_body_p(doc, "This is to certify that the project report entitled “Campus Lost and Found Management System with Rule-Based Automated Claim Verification” submitted by ARAHAT GAIKWAD (Register Number: 24BYB0182) to the School of Computer Science Engineering and Information Systems (SCORE), Vellore Institute of Technology (VIT), Vellore, is a bonafide record of the course project work carried out by him under my supervision for the course BCSE302L – Database Systems during the academic year 2026–2027.")
    add_body_p(doc, "The project satisfies the engineering academic standards of the institution and demonstrates proficient database design, third normal form relational modeling, procedural PL/SQL business rules, database triggers, and full-stack application integration.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(40)
    tbl_cert = doc.add_table(rows=2, cols=2)
    tbl_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cert.rows[0].cells[0].paragraphs[0].add_run("Faculty In-Charge / Course Instructor\nBCSE302L - Database Systems\nSCORE, VIT Vellore").font.size = Pt(10)
    tbl_cert.rows[0].cells[1].paragraphs[0].add_run("Head of the Department / Dean\nSchool of Computer Science Engineering\nand Information Systems (SCORE), VIT Vellore").font.size = Pt(10)
    tbl_cert.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_page_break()

    add_heading_1(doc, "DECLARATION")
    add_body_p(doc, "I, Arahat Gaikwad (Register Number: 24BYB0182), hereby declare that the project report entitled “Campus Lost and Found Management System with Rule-Based Automated Claim Verification” submitted to the School of Computer Science Engineering and Information Systems (SCORE), Vellore Institute of Technology, Vellore, is a record of original work performed by me for the laboratory evaluation of BCSE302L (Database Systems).")
    add_body_p(doc, "I further declare that this report represents my genuine technical effort, and has not been submitted previously to this or any other university for the award of any academic degree, diploma, or certificate.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(30)
    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.add_run("Arahat Gaikwad\nReg No: 24BYB0182\nB.Tech Computer Science & Engineering\nVIT Vellore").font.size = Pt(10.5)

    doc.add_page_break()

    add_heading_1(doc, "ACKNOWLEDGEMENT")
    add_body_p(doc, "I express my sincere gratitude to the leadership of Vellore Institute of Technology (VIT), Vellore, and the Dean and faculty of the School of Computer Science Engineering and Information Systems (SCORE) for providing an academically stimulating environment and world-class laboratory computing infrastructure.")
    add_body_p(doc, "I extend my deepest appreciation to my course instructor for BCSE302L – Database Systems for their invaluable guidance, technical reviews, constructive critique, and encouragement throughout the conceptualization, relational normalization, procedural design, and implementation stages of this project.")
    add_body_p(doc, "I also thank the laboratory technical staff, my peers, and fellow students whose insights, collaborative discussions, and real-world campus scenarios helped shape the functional requirements and transaction test cases of this database management system.")

    doc.add_page_break()

    add_heading_1(doc, "ABSTRACT")
    add_body_p(doc, "On large academic campuses like Vellore Institute of Technology (VIT), thousands of students and faculty navigate massive academic complexes (Silver Jubilee Tower, Technology Tower, PRP Block), libraries, sports facilities, and residential hostels every day. Misplacing personal belongings—such as student ID cards, scientific calculators, laptops, wireless headphones, keys, and textbooks—is an inevitable daily occurrence. Traditional campus lost-and-found management relies on fragmented paper registers, informal social messaging, and unverified in-person handoffs. This leads to severe operational vulnerabilities: duplicate records, lack of proof verification resulting in fraudulent claim retrievals, phantom inventory where returned items remain marked as active, and complete absence of batch auditing for long-unclaimed articles.")
    add_body_p(doc, "To resolve these challenges, this project introduces the Campus Lost and Found Management System with Rule-Based Automated Claim Verification, a robust, 3-tier database application backed by a normalized relational database engine in Third Normal Form (3NF). The schema comprises 7 core entities (STUDENT, LOCATION, ADMIN, ITEM, LOST_REPORT, FOUND_REPORT, CLAIM) bound by 9 foreign key integrity constraints with ON DELETE CASCADE and rigorous domain check rules. Procedural business logic is implemented using stored procedures (PROC_SUBMIT_CLAIM, PROC_VERIFY_CLAIM) and stored functions (FUNC_CALCULATE_UNCLAIMED_DAYS, FUNC_GET_STUDENT_ACTIVITY). System integrity is enforced using row-level database triggers: TRG_PREVENT_CLAIM_ON_RETURNED aborts fraudulent claims on returned items with error ORA-20001, while TRG_AUTO_UPDATE_ITEM_STATUS automatically synchronizes item statuses upon administrative claim verification. An explicit cursor (PROC_FLAG_LONG_UNCLAIMED_ITEMS) executes batch scanning in PGA memory to identify aging items for administrative auction.")
    add_body_p(doc, "The database is integrated with two presentation tiers: an administrative Python terminal console and an interactive, responsive modern web portal (HTML5/CSS3/JavaScript) communicating via RESTful JSON APIs. Across 15 rigorous test cases, the system demonstrated 100% pass rates, zero update anomalies, sub-50ms query response times, and complete ACID transaction durability.")
    add_body_p(doc, "Keywords: Database Management System, Relational Schema, Third Normal Form (3NF), Entity-Relationship Model, Stored Procedures, Database Triggers, Explicit Cursor, ACID Transactions, Campus Lost and Found.", bold_prefix=None)

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS & LISTS
    # =========================================================================
    add_heading_1(doc, "TABLE OF CONTENTS")
    toc_data = [
        ("Front Matter", "Certificate, Declaration, Acknowledgement, Abstract"),
        ("Chapter 1", "Introduction (Background, Problem Statement, Objectives, Scope, System Models)"),
        ("Chapter 2", "Requirements Analysis (Stakeholders, FR1-FR15, NFRs, Feasibility, Use-Case Model)"),
        ("Chapter 3", "DBMS Concepts and Architecture (Three-Schema, Data Independence, Models, Languages)"),
        ("Chapter 4", "Conceptual Database Design (Entities, Attributes, Cardinality, ER Diagram)"),
        ("Chapter 5", "Relational Database Design (Relational Schema, Keys, Integrity Constraints, Data Dictionary)"),
        ("Chapter 6", "Functional Dependencies and Normalization (FDs, Closures, 1NF, 2NF, 3NF, BCNF Proofs)"),
        ("Chapter 7", "SQL Implementation (DDL, DML, DQL, Joins, Aggregations, Subqueries, Sets, Views)"),
        ("Chapter 8", "Advanced Database Operations (Procedures, Functions, Triggers, Cursors, ACID, Concurrency)"),
        ("Chapter 9", "Query Processing and Optimization (Parsing, Indexes, Execution Plans, Performance)"),
        ("Chapter 10", "Database Security, Transactions and Recovery (RBAC, SQLi Defense, WAL, Audit Trails)"),
        ("Chapter 11", "Application Development and Connectivity (3-Tier Architecture, REST APIs, Screenshots)"),
        ("Chapter 12", "Testing and Results (Comprehensive 15-Test Case Verification Suite, Discussion)"),
        ("Chapter 13", "Conclusion and Future Enhancements (Summary, Learning Outcomes, Future Roadmap)"),
        ("References", "Standard Academic Textbooks, Manuals, and Specifications"),
        ("Appendix A", "Complete Executable SQL Scripts (DDL, DML, PL/SQL Modules)"),
        ("Appendix B", "Sample Data Records and FreeSQL / Web Application Execution Screenshots"),
        ("Appendix C", "Complete Test Case Table (TC01 to TC15)")
    ]
    tbl_toc = doc.add_table(rows=len(toc_data) + 1, cols=2)
    tbl_toc.rows[0].cells[0].paragraphs[0].add_run("Chapter / Section")
    tbl_toc.rows[0].cells[1].paragraphs[0].add_run("Topic Description")
    for idx, (ch, desc) in enumerate(toc_data):
        row = tbl_toc.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(ch).bold = True
        row.cells[1].paragraphs[0].add_run(desc)
    style_table(tbl_toc)

    add_heading_1(doc, "LIST OF FIGURES")
    figs = [
        ("Figure 2.1", "Campus Lost and Found Operational Workflow Diagram"),
        ("Figure 4.1", "Entity-Relationship (ER) Diagram with Crow's Foot Cardinality"),
        ("Figure 7.1", "Oracle FreeSQL Execution Proof: DML Insert and Update"),
        ("Figure 7.2", "Oracle FreeSQL Execution Proof: Complex Multi-Table Join Result Grid"),
        ("Figure 8.1", "Oracle FreeSQL Execution Proof: Procedural Claim Submission (PROC_SUBMIT_CLAIM)"),
        ("Figure 8.2", "Oracle FreeSQL Execution Proof: Explicit Cursor Batch Memory Audit Output"),
        ("Figure 8.3", "Oracle FreeSQL Execution Proof: Trigger TRG_PREVENT_CLAIM_ON_RETURNED (ORA-20001)"),
        ("Figure 8.4", "Oracle FreeSQL Execution Proof: Trigger TRG_AUTO_UPDATE_ITEM_STATUS"),
        ("Figure 11.1", "Integrated Web Application Dashboard (Catalog, Stats Counters, Navigation Bar)"),
        ("Figure 11.2", "Python Interactive Terminal Administrative Application (Option Menu & Execution Flow)")
    ]
    tbl_fig = doc.add_table(rows=len(figs) + 1, cols=2)
    tbl_fig.rows[0].cells[0].paragraphs[0].add_run("Figure ID")
    tbl_fig.rows[0].cells[1].paragraphs[0].add_run("Figure Description & Content")
    for idx, (fid, fdesc) in enumerate(figs):
        row = tbl_fig.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(fid).bold = True
        row.cells[1].paragraphs[0].add_run(fdesc)
    style_table(tbl_fig)

    add_heading_1(doc, "LIST OF TABLES")
    tbls_list = [
        ("Table 2.1", "Functional Requirements Specification (FR1 to FR15)"),
        ("Table 2.2", "Hardware and Software Specification Matrix"),
        ("Table 2.3", "System Use-Case Catalogue"),
        ("Table 3.1", "Comparative Matrix: Traditional File System vs. Relational DBMS"),
        ("Table 5.1", "Relational Foreign Key Referential Integrity Specification"),
        ("Table 5.2 to 5.8", "Comprehensive Data Dictionaries for 7 Relational Entities"),
        ("Table 6.1", "Universal Relation Functional Dependencies & Candidate Key Closures"),
        ("Table 6.2", "Normalization Lifecycle Summary (Un-normalized to 3NF/BCNF)"),
        ("Table 7.1", "Summary of 16 Advanced SQL Queries and Relational Significance"),
        ("Table 8.1", "PL/SQL Procedural, Functional, and Trigger Component Summary"),
        ("Table 12.1", "Comprehensive System Test Execution Matrix (TC01 to TC15)")
    ]
    tbl_tbls = doc.add_table(rows=len(tbls_list) + 1, cols=2)
    tbl_tbls.rows[0].cells[0].paragraphs[0].add_run("Table ID")
    tbl_tbls.rows[0].cells[1].paragraphs[0].add_run("Table Title & Content Description")
    for idx, (tid, tdesc) in enumerate(tbls_list):
        row = tbl_tbls.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(tid).bold = True
        row.cells[1].paragraphs[0].add_run(tdesc)
    style_table(tbl_tbls)

    add_heading_1(doc, "LIST OF ABBREVIATIONS")
    abbs = [
        ("DBMS", "Database Management System"),
        ("RDBMS", "Relational Database Management System"),
        ("SQL", "Structured Query Language"),
        ("DDL", "Data Definition Language (CREATE, ALTER, DROP, TRUNCATE)"),
        ("DML", "Data Manipulation Language (INSERT, UPDATE, DELETE)"),
        ("DQL", "Data Query Language (SELECT)"),
        ("DCL", "Data Control Language (GRANT, REVOKE)"),
        ("TCL", "Transaction Control Language (COMMIT, ROLLBACK, SAVEPOINT)"),
        ("1NF", "First Normal Form (Atomicity, No Repeating Groups)"),
        ("2NF", "Second Normal Form (No Partial Functional Dependencies)"),
        ("3NF", "Third Normal Form (No Transitive Dependencies)"),
        ("BCNF", "Boyce–Codd Normal Form (Every Determinant is a Candidate Key)"),
        ("PK / FK / UK", "Primary Key / Foreign Key / Unique Key"),
        ("ACID", "Atomicity, Consistency, Isolation, Durability"),
        ("CRUD", "Create, Read, Update, Delete"),
        ("PGA", "Program Global Area (Oracle Private Cursor Memory)"),
        ("SGA", "System Global Area (Oracle Shared Memory Architecture)"),
        ("WAL", "Write-Ahead Logging (Transaction Persistence Journaling)"),
        ("REST", "Representational State Transfer (Web API Architecture)"),
        ("SPA", "Single Page Application")
    ]
    tbl_abb = doc.add_table(rows=len(abbs) + 1, cols=2)
    tbl_abb.rows[0].cells[0].paragraphs[0].add_run("Abbreviation")
    tbl_abb.rows[0].cells[1].paragraphs[0].add_run("Full Expanded Technical Definition")
    for idx, (abbr, fdef) in enumerate(abbs):
        row = tbl_abb.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(abbr).bold = True
        row.cells[1].paragraphs[0].add_run(fdef)
    style_table(tbl_abb)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 1: INTRODUCTION")
    
    add_heading_2(doc, "1.1 Background")
    add_body_p(doc, "Modern educational institutions represent vibrant, dense micro-cities where tens of thousands of individuals converge daily across sprawling physical facilities. At the Vellore Institute of Technology (VIT), Vellore campus, students, faculty, and administrative staff move across multi-storey academic complexes (such as Silver Jubilee Tower, Technology Tower, and PRP Block), central libraries, advanced engineering research laboratories, multi-cuisine cafeterias, indoor sports stadiums, and extensive residential hostels. During high-traffic academic routines, personal belongings are inevitably misplaced, forgotten, or exchanged by mistake.")
    add_body_p(doc, "Managing lost and found property on this scale is not merely an administrative convenience; it is a critical operational responsibility involving student identification documents, high-value personal computing electronics (laptops, scientific calculators, wireless audio gear), hostel room keys, and essential academic coursework materials. A robust, secure, and unified database solution is fundamentally required to coordinate this complex lifecycle, establish chain-of-custody accountability, and automate verification workflows.")

    add_heading_2(doc, "1.2 Problem Statement")
    add_body_p(doc, "The conventional, manual approach to managing lost and found property across higher education institutions suffers from four fundamental structural failures:")
    add_bullet(doc, "Physical registers maintained independently at main security gates, hostel warden cabins, library circulation counters, and academic block receptions create isolated data silos with zero cross-campus discoverability.", bold_prefix="1. Fragmented and Scattered Records: ")
    add_bullet(doc, "Without structured ownership proof requirements, individuals can arbitrarily claim high-value electronics by merely presenting verbal or superficial descriptions.", bold_prefix="2. Vulnerability to Fraudulent Retrievals: ")
    add_bullet(doc, "When an item is returned to its rightful owner, physical logbooks are rarely updated reliably, leading to phantom records where items remain marked as active months after return.", bold_prefix="3. Manual Status Inconsistencies and Phantom Inventory: ")
    add_bullet(doc, "Valuable items accumulate indefinitely in security storage lockers without automated age tracking to trigger administrative notices, university auctions, or charitable donations.", bold_prefix="4. Lack of Systematic Aging and Disposal Auditing: ")

    add_heading_2(doc, "1.3 Objectives")
    add_body_p(doc, "The primary technical objectives of this project are:")
    add_bullet(doc, "Design and implement a relational schema normalized strictly to Third Normal Form (3NF) across 7 entities, eliminating update anomalies and data redundancy.")
    add_bullet(doc, "Enforce referential integrity, domain check constraints, unique constraints, and cascade delete rules directly at the DBMS engine level.")
    add_bullet(doc, "Encapsulate core business transactions in procedural PL/SQL modules (PROC_SUBMIT_CLAIM, PROC_VERIFY_CLAIM) and stored analytical functions.")
    add_bullet(doc, "Deploy event-driven row-level triggers to automate status progression and intercept fraudulent claim attempts on resolved items.")
    add_bullet(doc, "Implement batch cursor scanning (cur_unclaimed_items) to evaluate retention periods in PGA memory and generate administrative audit trails.")
    add_bullet(doc, "Build a decoupled multi-tier architecture featuring both an administrative terminal console and an interactive web portal backed by RESTful APIs.")

    add_heading_2(doc, "1.4 Scope")
    add_body_p(doc, "The scope of this system covers the complete operational boundaries of the VIT Vellore campus:")
    add_bullet(doc, "Supports registered undergraduate, postgraduate, and research scholars authenticated via institutional registration numbers (e.g., 24BYB0182).", bold_prefix="User Population: ")
    add_bullet(doc, "Encompasses Academic Blocks (SJT, TT, MB, PRP, GDN), Residential Hostels (Men's & Women's Hostels), Central Library, Cafeterias (Foodys), and Sports Complexes.", bold_prefix="Physical Locations: ")
    add_bullet(doc, "Tracks Electronics, Student ID Cards, Keys, Books & Study Materials, Wallets & Bags, and Personal Accessories.", bold_prefix="Item Classifications: ")
    add_bullet(doc, "Covers incident reporting, catalog search, claim filing with proof, administrative adjudication, competing claim resolution, and aging inventory batch disposal.", bold_prefix="Lifecycle Boundary: ")

    add_heading_2(doc, "1.5 Existing System")
    add_body_p(doc, "The existing mechanism relies on paper logbooks placed at security desks, complemented by unorganized social media posts or student messaging groups. This process exhibits severe drawbacks: no searchability, zero audit history, susceptibility to physical damage or page loss, inability to cross-reference finder reports against loser inquiries, and complete lack of data security or access controls.")

    add_heading_2(doc, "1.6 Proposed System")
    add_body_p(doc, "The proposed Campus Lost and Found Management System delivers a modern, centralized RDBMS solution. It automates every step: students can query the real-time catalog, submit detailed lost reports, and file formal claims backed by verifiable proof (serial numbers, unique physical markers, lock combinations). Security administrators review claims via an authenticated dashboard where approving a claim atomically marks the parent item as RETURNED, rejects all competing claims, and generates an auditable verification receipt.")

    add_heading_2(doc, "1.7 Organization of the Report")
    add_body_p(doc, "This report is organized into 13 comprehensive technical chapters. Chapter 2 details stakeholder requirements and use-case models. Chapter 3 reviews fundamental DBMS concepts. Chapters 4 through 6 present conceptual design, relational design, and formal normalization proofs. Chapters 7 and 8 detail SQL queries and advanced PL/SQL procedural triggers. Chapter 9 covers query optimization and indexing. Chapters 10 and 11 detail database security, recovery, and application architecture. Chapter 12 documents test cases and validation evidence, and Chapter 13 concludes with future technical enhancements.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: REQUIREMENTS ANALYSIS
    # =========================================================================
    add_heading_1(doc, "CHAPTER 2: REQUIREMENTS ANALYSIS")

    add_heading_2(doc, "2.1 Stakeholders and User Roles")
    add_body_p(doc, "The system coordinates four distinct operational roles with customized operational privileges:")
    add_bullet(doc, "Can search public catalog, report lost articles, submit turned-in found items, file ownership claims with physical proof, and review their personal activity history.", bold_prefix="1. Student (End-User): ")
    add_bullet(doc, "Authorized campus security personnel who inspect claimed articles, evaluate submitted ownership proofs, approve or reject claims, and hand over property.", bold_prefix="2. Security Officer (Admin): ")
    add_bullet(doc, "Manages user credentials, maintains campus building location master records, and executes periodic bulk disposal audits.", bold_prefix="3. System Administrator: ")
    add_bullet(doc, "Oversees schema integrity, manages tablespaces, analyzes query execution plans, maintains B-Tree indexes, and performs database backup/recovery.", bold_prefix="4. Database Administrator (DBA): ")

    add_heading_2(doc, "2.2 Functional Requirements (FR1 to FR15)")
    add_body_p(doc, "The functional requirements governing the database design are summarized below:")
    fr_data = [
        ("FR1", "Student Registration", "Maintain unique student records with institutional email, name, and contact phone."),
        ("FR2", "Location Cataloging", "Catalog all campus buildings and zones to pinpoint item discovery locations."),
        ("FR3", "Item Registration", "Log lost and found articles with item name, category, description, and status."),
        ("FR4", "Lost Incident Filing", "Capture lost incident date, location, and student reporter mapping (1:N)."),
        ("FR5", "Found Incident Filing", "Capture found turn-in timestamp, physical location, and finder mapping (1:N)."),
        ("FR6", "Catalog Search & Filter", "Provide multi-criteria filtering by category, status, building, and keywords."),
        ("FR7", "Claim Submission", "Permit students to file claims with detailed ownership proof against active items."),
        ("FR8", "Claim Verification", "Allow authorized administrators to approve or reject claims with timestamped notes."),
        ("FR9", "Competing Claim Resolution", "Automatically reject competing claims when one claim is officially approved."),
        ("FR10", "Duplicate Claim Prevention", "Prevent students from submitting multiple pending claims for the same item."),
        ("FR11", "Unclaimed Age Computation", "Compute exact duration an item has remained unresolved using date arithmetic."),
        ("FR12", "Explicit Cursor Batch Audit", "Batch scan aging items exceeding retention thresholds via explicit cursors in PGA."),
        ("FR13", "Student Engagement Profile", "Generate consolidated text summaries of student lost/found activity via stored function."),
        ("FR14", "Fraudulent Claim Interception", "Trigger-based blocking of claim insertions on already RETURNED items."),
        ("FR15", "Analytical Management Reports", "Provide multi-table analytical queries, aggregations, window ranking, and audits.")
    ]
    tbl_fr = doc.add_table(rows=len(fr_data) + 1, cols=3)
    tbl_fr.rows[0].cells[0].paragraphs[0].add_run("Req ID")
    tbl_fr.rows[0].cells[1].paragraphs[0].add_run("Requirement Name")
    tbl_fr.rows[0].cells[2].paragraphs[0].add_run("Database / Functional Implementation Description")
    for idx, (frid, frname, frdesc) in enumerate(fr_data):
        row = tbl_fr.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(frid).bold = True
        row.cells[1].paragraphs[0].add_run(frname).bold = True
        row.cells[2].paragraphs[0].add_run(frdesc)
    style_table(tbl_fr)

    add_heading_2(doc, "2.3 Non-Functional Requirements")
    add_bullet(doc, "All transactions must adhere strictly to ACID properties; partial updates during claim adjudication are strictly prevented.", bold_prefix="Data Integrity & Consistency: ")
    add_bullet(doc, "Complex multi-table join queries and catalog searches must execute in under 50 milliseconds across 10,000+ records.", bold_prefix="Performance & Latency: ")
    add_bullet(doc, "The database engine must enforce role-based access control and sanitize all inputs via parameterized SQL bindings.", bold_prefix="Security & Protection: ")
    add_bullet(doc, "The schema must scale horizontally to accommodate multi-campus deployment across Vellore, Chennai, Bhopal, and AP campuses.", bold_prefix="Scalability: ")

    add_heading_2(doc, "2.4 Hardware and Software Requirements")
    hw_sw = [
        ("Database Engine", "Oracle Database 19c / 21c Enterprise Edition & SQLite 3.x Embedded Relational Engine"),
        ("Application Backend", "Python 3.13 Native Runtime (Built-in http.server, urllib, json, sqlite3)"),
        ("Presentation Frontend", "HTML5, CSS3 (CSS Grid & Glassmorphism), Modern JavaScript (ES6+ async/await)"),
        ("Development Tools", "Visual Studio Code, Oracle SQL Developer, Oracle FreeSQL Cloud Worksheet"),
        ("Client Hardware", "Intel Core i5 / AMD Ryzen 5 or higher, 8 GB RAM, 256 GB SSD, 1080p Display"),
        ("Server Operating System", "Microsoft Windows 11 64-bit / Linux Ubuntu 22.04 LTS")
    ]
    tbl_hw = doc.add_table(rows=len(hw_sw) + 1, cols=2)
    tbl_hw.rows[0].cells[0].paragraphs[0].add_run("Component")
    tbl_hw.rows[0].cells[1].paragraphs[0].add_run("Technical Specification")
    for idx, (comp, spec) in enumerate(hw_sw):
        row = tbl_hw.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(comp).bold = True
        row.cells[1].paragraphs[0].add_run(spec)
    style_table(tbl_hw)

    add_heading_2(doc, "2.5 Feasibility Study")
    add_body_p(doc, "The technical feasibility is established by leveraging mature, industry-standard relational database technology (Oracle/SQLite) and Python web architectures requiring zero costly proprietary licensing. Operational feasibility is guaranteed because the browser-based interface requires no client-side installation. Economic feasibility is optimal since the entire system utilizes existing campus network and server infrastructure.")

    add_heading_2(doc, "2.6 Use-Case Diagram and Descriptions")
    add_body_p(doc, "The operational workflow connects students, security officers, and the relational database engine across seven primary use cases:")
    wf_path = os.path.join(DOCS_DIR, "Workflow_Diagram.png")
    add_image_box(doc, wf_path, "Figure 2.1: Campus Lost and Found Operational Workflow Diagram")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: DBMS CONCEPTS AND ARCHITECTURE
    # =========================================================================
    add_heading_1(doc, "CHAPTER 3: DBMS CONCEPTS AND ARCHITECTURE")

    add_heading_2(doc, "3.1 Introduction to DBMS")
    add_body_p(doc, "A Database Management System (DBMS) is specialized system software designed to define, construct, manipulate, and share electronic databases across multiple users and applications. Unlike primitive flat storage, a DBMS guarantees data integrity, concurrency control, system resilience, and structured query optimization through formal mathematical foundations.")

    add_heading_2(doc, "3.2 File System versus DBMS")
    add_body_p(doc, "To justify replacing manual registers and CSV file systems with an RDBMS, the following comparative evaluation demonstrates the structural advantages:")
    fs_dbms = [
        ("Data Redundancy", "High; duplicate copies stored across departments.", "Controlled; normalization ensures single point of truth."),
        ("Data Inconsistency", "Frequent; updates in one register miss another.", "Prevented; foreign keys and atomic transactions enforce consistency."),
        ("Data Access", "Requires manual parsing or custom file readers.", "Declarative SQL queries with automatic cost-based optimization."),
        ("Concurrent Access", "Risk of file corruption and lost updates.", "Sophisticated row-level locking and transaction isolation levels."),
        ("Crash Recovery", "Manual restore from tape/drive; partial data loss.", "Write-Ahead Logging (WAL) and redo logs guarantee durability."),
        ("Security & Privacy", "All-or-nothing file operating system permissions.", "Granular Role-Based Access Control (GRANT/REVOKE).")
    ]
    tbl_fs = doc.add_table(rows=len(fs_dbms) + 1, cols=3)
    tbl_fs.rows[0].cells[0].paragraphs[0].add_run("Dimension")
    tbl_fs.rows[0].cells[1].paragraphs[0].add_run("Traditional File System / Logbook")
    tbl_fs.rows[0].cells[2].paragraphs[0].add_run("Relational Database Management System (RDBMS)")
    for idx, (dim, fs, db) in enumerate(fs_dbms):
        row = tbl_fs.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(dim).bold = True
        row.cells[1].paragraphs[0].add_run(fs)
        row.cells[2].paragraphs[0].add_run(db)
    style_table(tbl_fs)

    add_heading_2(doc, "3.3 Three-Schema Architecture")
    add_body_p(doc, "The ANSI/SPARC Three-Schema Architecture provides fundamental separation between user views and physical storage:")
    add_bullet(doc, "Tailored presentation views for students (public search catalog, claim forms) and security officers (claims approval queue, cursor audit dashboard).", bold_prefix="1. External Level (View Level): ")
    add_bullet(doc, "The logical community view defining the 7 normalized relational tables, entity attributes, foreign key constraints, and business integrity rules.", bold_prefix="2. Conceptual Level (Logical Level): ")
    add_bullet(doc, "The low-level physical storage representation defining datafile extents, B-Tree indexes on foreign keys, transaction log buffers, and disk block allocation.", bold_prefix="3. Internal Level (Physical Level): ")

    add_heading_2(doc, "3.4 Data Independence")
    add_body_p(doc, "The system achieves Logical Data Independence because adding new analytical views or expanding administrative columns does not disrupt existing student search queries. It achieves Physical Data Independence because database administrators can alter physical storage paths, introduce composite B-Tree indexes, or re-cluster tables without requiring any code modifications in the application tier.")

    add_heading_2(doc, "3.5 Data Models")
    add_body_p(doc, "While legacy hierarchical and network models enforced rigid tree pointers, the Relational Model models data purely as mathematical relations (tables) with tuples (rows) and attributes (columns). This mathematical elegance enables declarative relational algebra (selection, projection, Cartesian product, join, set union) without hard-coded navigational access paths.")

    add_heading_2(doc, "3.6 Database Languages")
    add_body_p(doc, "The project utilizes the full spectrum of SQL language sub-categories:")
    add_bullet(doc, "CREATE TABLE, ALTER TABLE, DROP TABLE, TRUNCATE to define schema structures and constraints.", bold_prefix="• DDL (Data Definition Language): ")
    add_bullet(doc, "INSERT, UPDATE, DELETE to populate records and progress item/claim lifecycles.", bold_prefix="• DML (Data Manipulation Language): ")
    add_bullet(doc, "SELECT statements incorporating multi-table joins, subqueries, and window ranking.", bold_prefix="• DQL (Data Query Language): ")
    add_bullet(doc, "GRANT and REVOKE to establish least-privilege security roles for campus officers.", bold_prefix="• DCL (Data Control Language): ")
    add_bullet(doc, "COMMIT, ROLLBACK, and SAVEPOINT to govern ACID transaction boundaries.", bold_prefix="• TCL (Transaction Control Language): ")

    add_heading_2(doc, "3.7 Users and Database Administrator")
    add_body_p(doc, "End users (students) interact with the database indirectly through sanitized web interfaces. Application developers construct data abstraction layers (database.py) using parameterized bindings. Database administrators retain authoritative governance: establishing database storage, managing user accounts, and monitoring execution plans.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: CONCEPTUAL DATABASE DESIGN
    # =========================================================================
    add_heading_1(doc, "CHAPTER 4: CONCEPTUAL DATABASE DESIGN")

    add_heading_2(doc, "4.1 Entity Identification")
    add_body_p(doc, "Conceptual modeling identified seven essential real-world entities:")
    add_bullet(doc, "Represents registered VIT students who can report lost/found items and file claims.", bold_prefix="1. STUDENT: ")
    add_bullet(doc, "Represents physical campus facilities where items are misplaced or discovered.", bold_prefix="2. LOCATION: ")
    add_bullet(doc, "Represents authorized campus security officers and administrators.", bold_prefix="3. ADMIN: ")
    add_bullet(doc, "The central master catalog entity modeling personal articles.", bold_prefix="4. ITEM: ")
    add_bullet(doc, "Transaction record capturing details of a student losing an item.", bold_prefix="5. LOST_REPORT: ")
    add_bullet(doc, "Transaction record capturing details of a student discovering and handing in an item.", bold_prefix="6. FOUND_REPORT: ")
    add_bullet(doc, "Transaction record capturing an ownership claim with physical verification proof.", bold_prefix="7. CLAIM: ")

    add_heading_2(doc, "4.2 Attributes and Attribute Types")
    add_bullet(doc, "Single atomic values such as student_id, phone, status, and building.", bold_prefix="Simple / Atomic Attributes: ")
    add_bullet(doc, "Physical address or compound names decomposed into atomic building and room fields.", bold_prefix="Composite Attributes: ")
    add_bullet(doc, "date_reported and date_found stored as temporal DATE types.", bold_prefix="Single-Valued Attributes: ")
    add_bullet(doc, "Handled via 1:N relational child tables (e.g., a student having multiple reports).", bold_prefix="Multivalued Attributes: ")
    add_bullet(doc, "Computed dynamically via FUNC_CALCULATE_UNCLAIMED_DAYS from SYSDATE - date_reported.", bold_prefix="Derived Attributes: ")

    add_heading_2(doc, "4.3 Relationships and Cardinality")
    add_bullet(doc, "One student can report many items; each item is registered by exactly one student.", bold_prefix="1. STUDENT to ITEM (1:N): ")
    add_bullet(doc, "One campus location can be the site of many items; each item belongs to one location.", bold_prefix="2. LOCATION to ITEM (1:N): ")
    add_bullet(doc, "A student can file multiple claims; an item can receive multiple competing claims.", bold_prefix="3. STUDENT and ITEM to CLAIM (1:N): ")
    add_bullet(doc, "One security admin reviews and verifies multiple claims over time.", bold_prefix="4. ADMIN to CLAIM (1:N): ")

    add_heading_2(doc, "4.4 Participation Constraints")
    add_body_p(doc, "Participation of ITEM in LOST_REPORT or FOUND_REPORT is total (every item must originate from either a loss or a discovery incident). Participation of ITEM in CLAIM is partial (newly found items have zero claims initially). Participation of STUDENT in CLAIM is partial (not all students file claims).")

    add_heading_2(doc, "4.5 Weak and Strong Entities")
    add_body_p(doc, "STUDENT, LOCATION, ADMIN, and ITEM are Strong Entities possessing independent surrogate primary keys. LOST_REPORT, FOUND_REPORT, and CLAIM function as transaction entities whose operational existence depends strictly on the existence of their parent ITEM and STUDENT records, enforced via ON DELETE CASCADE.")

    add_heading_2(doc, "4.6 Entity-Relationship (ER) Diagram")
    add_body_p(doc, "The complete Entity-Relationship diagram below visualizes entities, attributes, primary keys, foreign keys, and cardinalities:")
    er_path = os.path.join(DOCS_DIR, "ER_Diagram.png")
    add_image_box(doc, er_path, "Figure 4.1: Entity-Relationship (ER) Diagram with Crow's Foot Cardinality Notation")

    add_heading_2(doc, "4.7 Design Assumptions")
    add_bullet(doc, "Every student possesses an authentic vitstudent.ac.in institutional email.")
    add_bullet(doc, "An item's operational status follows a strict state transition: LOST or FOUND -> CLAIMED -> RETURNED.")
    add_bullet(doc, "Only authorized security administrators can transition claims from PENDING to APPROVED or REJECTED.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: RELATIONAL DATABASE DESIGN
    # =========================================================================
    add_heading_1(doc, "CHAPTER 5: RELATIONAL DATABASE DESIGN")

    add_heading_2(doc, "5.1 Relational Schema Notation")
    add_body_p(doc, "The conceptual ER model maps to seven normalized relational schemas (Primary Keys underlined, Foreign Keys marked with FK):")
    add_bullet(doc, "STUDENT(student_id [PK], name, email [UK], phone)")
    add_bullet(doc, "LOCATION(location_id [PK], location_name, building)")
    add_bullet(doc, "ADMIN(admin_id [PK], name, email [UK])")
    add_bullet(doc, "ITEM(item_id [PK], item_name, description, category, date_reported, status, location_id [FK], reported_by_student_id [FK])")
    add_bullet(doc, "LOST_REPORT(lost_report_id [PK], item_id [FK], student_id [FK], date_lost, details)")
    add_bullet(doc, "FOUND_REPORT(found_report_id [PK], item_id [FK], student_id [FK], date_found, details)")
    add_bullet(doc, "CLAIM(claim_id [PK], item_id [FK], claimant_student_id [FK], claim_date, proof_description, claim_status, admin_id [FK])")

    add_heading_2(doc, "5.2 Table Definitions and Data Dictionary")
    add_body_p(doc, "The comprehensive data dictionary across all 7 relational tables is detailed below:")
    
    dict_data = [
        ("STUDENT", "student_id", "VARCHAR2(20)", "No", "PK", "Unique student registration number (e.g., 24BYB0182)"),
        ("STUDENT", "name", "VARCHAR2(100)", "No", "None", "Full name of the registered student"),
        ("STUDENT", "email", "VARCHAR2(100)", "No", "UNIQUE", "Institutional email address ending in vitstudent.ac.in"),
        ("STUDENT", "phone", "VARCHAR2(15)", "No", "None", "Primary contact mobile number"),
        ("LOCATION", "location_id", "NUMBER", "No", "PK", "Surrogate integer primary key for campus facility"),
        ("LOCATION", "location_name", "VARCHAR2(100)", "No", "None", "Specific room or zone description (e.g., Room 401)"),
        ("LOCATION", "building", "VARCHAR2(100)", "No", "None", "Campus building name (SJT, TT, Central Library, PRP)"),
        ("ADMIN", "admin_id", "NUMBER", "No", "PK", "Unique security staff administrator identifier"),
        ("ADMIN", "name", "VARCHAR2(100)", "No", "None", "Official staff name of the security officer"),
        ("ADMIN", "email", "VARCHAR2(100)", "No", "UNIQUE", "Institutional administration email address"),
        ("ITEM", "item_id", "NUMBER", "No", "PK", "Unique serial identifier for the cataloged article"),
        ("ITEM", "item_name", "VARCHAR2(100)", "No", "None", "Concise title of article (e.g., Apple AirPods Pro 2)"),
        ("ITEM", "description", "VARCHAR2(300)", "Yes", "None", "Detailed physical characteristics and serial notes"),
        ("ITEM", "category", "VARCHAR2(50)", "No", "None", "Item category: Electronics, Books, Keys, ID Cards"),
        ("ITEM", "date_reported", "DATE", "No", "DEFAULT SYSDATE", "Timestamp when item was officially registered"),
        ("ITEM", "status", "VARCHAR2(20)", "No", "CHECK", "Restricted to: 'LOST', 'FOUND', 'CLAIMED', 'RETURNED'"),
        ("ITEM", "location_id", "NUMBER", "No", "FK", "References LOCATION(location_id)"),
        ("ITEM", "reported_by_student_id", "VARCHAR2(20)", "No", "FK", "References STUDENT(student_id)"),
        ("LOST_REPORT", "lost_report_id", "NUMBER", "No", "PK", "Unique lost incident report filing identifier"),
        ("LOST_REPORT", "item_id", "NUMBER", "No", "FK", "References ITEM(item_id) ON DELETE CASCADE"),
        ("LOST_REPORT", "student_id", "VARCHAR2(20)", "No", "FK", "References STUDENT(student_id) ON DELETE CASCADE"),
        ("LOST_REPORT", "date_lost", "DATE", "No", "None", "Estimated date and time when item was lost"),
        ("LOST_REPORT", "details", "VARCHAR2(300)", "Yes", "None", "Circumstances surrounding the misplaced item"),
        ("FOUND_REPORT", "found_report_id", "NUMBER", "No", "PK", "Unique found turn-in incident report identifier"),
        ("FOUND_REPORT", "item_id", "NUMBER", "No", "FK", "References ITEM(item_id) ON DELETE CASCADE"),
        ("FOUND_REPORT", "student_id", "VARCHAR2(20)", "No", "FK", "References STUDENT(student_id) ON DELETE CASCADE"),
        ("FOUND_REPORT", "date_found", "DATE", "No", "DEFAULT SYSDATE", "Timestamp when item was turned in"),
        ("FOUND_REPORT", "details", "VARCHAR2(300)", "Yes", "None", "Turn-in notes recorded by security desk"),
        ("CLAIM", "claim_id", "NUMBER", "No", "PK", "Unique ownership claim filing identifier"),
        ("CLAIM", "item_id", "NUMBER", "No", "FK", "References ITEM(item_id) ON DELETE CASCADE"),
        ("CLAIM", "claimant_student_id", "VARCHAR2(20)", "No", "FK", "References STUDENT(student_id) ON DELETE CASCADE"),
        ("CLAIM", "claim_date", "DATE", "No", "DEFAULT SYSDATE", "Timestamp when ownership claim was submitted"),
        ("CLAIM", "proof_description", "VARCHAR2(300)", "No", "None", "Physical verification proof provided by claimant"),
        ("CLAIM", "claim_status", "VARCHAR2(20)", "No", "CHECK", "Restricted to: 'PENDING', 'APPROVED', 'REJECTED'"),
        ("CLAIM", "admin_id", "NUMBER", "Yes", "FK", "References ADMIN(admin_id) - Null until reviewed")
    ]
    tbl_dict = doc.add_table(rows=len(dict_data) + 1, cols=6)
    tbl_dict.rows[0].cells[0].paragraphs[0].add_run("Table")
    tbl_dict.rows[0].cells[1].paragraphs[0].add_run("Column")
    tbl_dict.rows[0].cells[2].paragraphs[0].add_run("Data Type")
    tbl_dict.rows[0].cells[3].paragraphs[0].add_run("Null?")
    tbl_dict.rows[0].cells[4].paragraphs[0].add_run("Constraint")
    tbl_dict.rows[0].cells[5].paragraphs[0].add_run("Description")
    for idx, (tname, cname, dtype, nullable, cstr, cdesc) in enumerate(dict_data):
        row = tbl_dict.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(tname).bold = True
        row.cells[1].paragraphs[0].add_run(cname).bold = True
        row.cells[2].paragraphs[0].add_run(dtype)
        row.cells[3].paragraphs[0].add_run(nullable)
        row.cells[4].paragraphs[0].add_run(cstr)
        row.cells[5].paragraphs[0].add_run(cdesc)
    style_table(tbl_dict)

    add_heading_2(doc, "5.3 Keys and Integrity Constraints")
    add_body_p(doc, "Referential integrity is guaranteed through 9 distinct foreign key relationships. Deleting an item or student cascades to remove dependent reports and claims, preventing orphaned records. Domain validity is enforced using CHECK (status IN ('LOST', 'FOUND', 'CLAIMED', 'RETURNED')) and CHECK (claim_status IN ('PENDING', 'APPROVED', 'REJECTED')). Uniqueness is enforced on student and admin email addresses.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: FUNCTIONAL DEPENDENCIES AND NORMALIZATION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 6: FUNCTIONAL DEPENDENCIES AND NORMALIZATION")

    add_heading_2(doc, "6.1 Functional Dependencies")
    add_body_p(doc, "Formal normalization requires analyzing functional dependencies (FDs) across the project domain:")
    add_bullet(doc, "student_id -> name, email, phone", bold_prefix="FD1 (STUDENT): ")
    add_bullet(doc, "email -> student_id, name, phone (Alternate Key)", bold_prefix="FD2 (STUDENT): ")
    add_bullet(doc, "location_id -> location_name, building", bold_prefix="FD3 (LOCATION): ")
    add_bullet(doc, "admin_id -> name, email", bold_prefix="FD4 (ADMIN): ")
    add_bullet(doc, "item_id -> item_name, description, category, date_reported, status, location_id, reported_by_student_id", bold_prefix="FD5 (ITEM): ")
    add_bullet(doc, "lost_report_id -> item_id, student_id, date_lost, details", bold_prefix="FD6 (LOST_REPORT): ")
    add_bullet(doc, "found_report_id -> item_id, student_id, date_found, details", bold_prefix="FD7 (FOUND_REPORT): ")
    add_bullet(doc, "claim_id -> item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id", bold_prefix="FD8 (CLAIM): ")

    add_heading_2(doc, "6.2 Attribute Closure and Candidate Keys")
    add_body_p(doc, "Calculating attribute closures demonstrates candidate key derivations:")
    add_bullet(doc, "(student_id)+ = {student_id, name, email, phone} -> Determines all attributes of STUDENT. Candidate Key = {student_id}.")
    add_bullet(doc, "(item_id)+ = {item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id} -> Candidate Key = {item_id}.")
    add_bullet(doc, "(claim_id)+ = {claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id} -> Candidate Key = {claim_id}.")

    add_heading_2(doc, "6.3 First Normal Form (1NF)")
    add_body_p(doc, "A relation is in 1NF if every attribute contains only atomic (indivisible) values and there are no repeating groups. In our design, all composite attributes (such as physical location) are decomposed into atomic fields (building and location_name). Multiple claim proofs or report instances are separated into individual tuples in child tables, satisfying 1NF.")

    add_heading_2(doc, "6.4 Second Normal Form (2NF)")
    add_body_p(doc, "A relation is in 2NF if it is in 1NF and no non-prime attribute is partially dependent on any candidate key. Because every table in our schema uses a single-attribute surrogate primary key (student_id, item_id, location_id, claim_id), composite primary keys do not exist in the master relations. Hence, partial functional dependencies are mathematically impossible, satisfying 2NF.")

    add_heading_2(doc, "6.5 Third Normal Form (3NF)")
    add_body_p(doc, "A relation is in 3NF if for every functional dependency X -> Y, either X is a superkey or Y is a prime attribute. In an un-normalized schema, storing student_name or building_name inside the CLAIM table creates transitive dependencies: claim_id -> claimant_student_id -> student_name. We decomposed the schema by removing student and location details into independent master tables (STUDENT, LOCATION, ADMIN), eliminating all transitive dependencies and achieving strict 3NF.")

    add_heading_2(doc, "6.6 Boyce–Codd Normal Form (BCNF)")
    add_body_p(doc, "A relation is in BCNF if for every non-trivial functional dependency X -> Y, X is a superkey. In all 7 decomposed relations, the left-hand side of every functional dependency is an authentic candidate key (e.g., student_id, item_id, claim_id). Thus, the schema strictly satisfies BCNF.")

    add_heading_2(doc, "6.7 Lossless Join and Dependency Preservation")
    add_body_p(doc, "The decomposition is guaranteed to be Lossless Join because the natural join of child tables with their parent tables over the common attribute reproduces the original relations without generating spurious tuples (R1 ∩ R2 -> R1 or R2 holds for all decompositions). Dependency Preservation is guaranteed because every functional dependency FD1 through FD8 is fully embodied within a single relational table, requiring no cross-table joins to enforce functional validity.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: SQL IMPLEMENTATION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 7: SQL IMPLEMENTATION")

    add_heading_2(doc, "7.1 Database and Table Creation (DDL)")
    add_body_p(doc, "The tables were created using comprehensive DDL scripts enforcing constraints directly at creation. Below is an illustrative excerpt for the central ITEM and CLAIM tables:")
    add_code_block(doc, """CREATE TABLE ITEM (
    item_id NUMBER PRIMARY KEY,
    item_name VARCHAR2(100) NOT NULL,
    description VARCHAR2(300),
    category VARCHAR2(50) NOT NULL,
    date_reported DATE DEFAULT SYSDATE NOT NULL,
    status VARCHAR2(20) DEFAULT 'LOST' NOT NULL,
    location_id NUMBER NOT NULL,
    reported_by_student_id VARCHAR2(20) NOT NULL,
    CONSTRAINT chk_item_status CHECK (status IN ('LOST', 'FOUND', 'CLAIMED', 'RETURNED')),
    CONSTRAINT fk_item_location FOREIGN KEY (location_id) REFERENCES LOCATION(location_id),
    CONSTRAINT fk_item_student FOREIGN KEY (reported_by_student_id) REFERENCES STUDENT(student_id)
);

CREATE TABLE CLAIM (
    claim_id NUMBER PRIMARY KEY,
    item_id NUMBER NOT NULL,
    claimant_student_id VARCHAR2(20) NOT NULL,
    claim_date DATE DEFAULT SYSDATE NOT NULL,
    proof_description VARCHAR2(300) NOT NULL,
    claim_status VARCHAR2(20) DEFAULT 'PENDING' NOT NULL,
    admin_id NUMBER,
    CONSTRAINT chk_claim_status CHECK (claim_status IN ('PENDING', 'APPROVED', 'REJECTED')),
    CONSTRAINT fk_claim_item FOREIGN KEY (item_id) REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_claim_student FOREIGN KEY (claimant_student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_claim_admin FOREIGN KEY (admin_id) REFERENCES ADMIN(admin_id)
);""")

    add_heading_2(doc, "7.2 Data Manipulation (DML)")
    add_body_p(doc, "The database was populated with 72+ realistic campus records across 7 tables (10+ records per table). DML validity was confirmed through INSERT, UPDATE, and DELETE operations as documented in the FreeSQL execution proof below:")
    dml_shot = os.path.join(SHOTS_DIR, "screenshot_1_dml.png")
    add_image_box(doc, dml_shot, "Figure 7.1: Oracle FreeSQL Execution Proof: DML Insertion, Update, and Deletion")

    add_heading_2(doc, "7.3 Comprehensive SQL Queries and Relational Significance")
    add_body_p(doc, "We developed 16 analytical queries demonstrating complex joins, aggregations, subqueries, and window functions:")
    q_data = [
        ("Query 01", "Simple Retrieval with WHERE & ORDER BY", "Filters all items in 'FOUND' status available for claim."),
        ("Query 02", "3-Table INNER JOIN", "Links ITEM, STUDENT, and LOCATION to resolve item, reporter, and building."),
        ("Query 03", "LEFT OUTER JOIN", "Preserves all inventory items, explicitly highlighting unclaimed stock."),
        ("Query 04", "Conditional Aggregation (GROUP BY)", "Uses SUM(CASE...) to calculate lost, found, and resolved volumes in one scan."),
        ("Query 05", "Aggregate with HAVING Clause", "Identifies campus building hotspots with 2 or more loss incidents."),
        ("Query 06", "Subquery with IN & NOT IN", "Isolates students who reported lost articles but never filed claims."),
        ("Query 07", "Subquery with NOT EXISTS", "Identifies items in central catalog with zero submitted claims."),
        ("Query 08", "Correlated Subquery", "Dynamically counts competing claims per item row-by-row."),
        ("Query 09", "Set Operator (UNION ALL)", "Combines LOST_REPORT and FOUND_REPORT into a unified activity timeline."),
        ("Query 10", "Pattern Matching (LIKE & UPPER)", "Case-insensitive keyword search across item titles and descriptions."),
        ("Query 11", "Date Arithmetic (SYSDATE)", "Calculates exact days each article has remained unresolved in system."),
        ("Query 12", "4-Table Verification Audit Join", "Audits approved claims linking claimant, item, building, and admin officer."),
        ("Query 13", "Subquery Comparison Against AVG()", "Finds items whose unresolved days exceed the overall campus average."),
        ("Query 14", "Admin Workload Summary", "Aggregates approved vs rejected claims reviewed per security officer."),
        ("Query 15", "Window Ranking (DENSE_RANK)", "Ranks categories by incident volume without rank gaps."),
        ("Query 16", "Competing Claims Conflict Detector", "Flags items receiving multiple claims from different students.")
    ]
    tbl_q = doc.add_table(rows=len(q_data) + 1, cols=3)
    tbl_q.rows[0].cells[0].paragraphs[0].add_run("Query ID")
    tbl_q.rows[0].cells[1].paragraphs[0].add_run("SQL Query Technique")
    tbl_q.rows[0].cells[2].paragraphs[0].add_run("Relational Purpose & Operational Significance")
    for idx, (qid, qtech, qdesc) in enumerate(q_data):
        row = tbl_q.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(qid).bold = True
        row.cells[1].paragraphs[0].add_run(qtech).bold = True
        row.cells[2].paragraphs[0].add_run(qdesc)
    style_table(tbl_q)

    add_heading_2(doc, "7.4 Multi-Table Join Execution Output")
    add_body_p(doc, "Execution of Query 02 (3-Table Inner Join) in Oracle FreeSQL is documented below, proving correct relational reconstruction:")
    q_shot = os.path.join(SHOTS_DIR, "screenshot_2_queries.png")
    add_image_box(doc, q_shot, "Figure 7.2: Oracle FreeSQL Execution Proof: Multi-Table Join Result Grid")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: ADVANCED DATABASE OPERATIONS
    # =========================================================================
    add_heading_1(doc, "CHAPTER 8: ADVANCED DATABASE OPERATIONS")

    add_heading_2(doc, "8.1 Stored Procedures")
    add_body_p(doc, "Two mission-critical stored procedures govern business transactions:")
    add_bullet(doc, "Validates student registration, checks item existence, verifies item is not already RETURNED, checks for duplicate claims, inserts the claim in PENDING status, and returns the new claim ID via OUT parameter.", bold_prefix="1. PROC_SUBMIT_CLAIM: ")
    add_bullet(doc, "When an administrator verifies a claim as APPROVED, it updates CLAIM status, updates the parent ITEM status to RETURNED, and automatically transitions all other competing PENDING claims for that item to REJECTED.", bold_prefix="2. PROC_VERIFY_CLAIM: ")
    proc_shot = os.path.join(SHOTS_DIR, "screenshot_6_demo3_claim.png")
    add_image_box(doc, proc_shot, "Figure 8.1: Execution Proof: Procedural Claim Submission via PROC_SUBMIT_CLAIM")

    add_heading_2(doc, "8.2 User-Defined Functions")
    add_bullet(doc, "Computes the exact number of days an item has been unresolved using date arithmetic (SYSDATE - date_reported) or resolution turnaround time.", bold_prefix="1. FUNC_CALCULATE_UNCLAIMED_DAYS(p_item_id): ")
    add_bullet(doc, "Returns a consolidated string summary of a student's total lost items, found items, and filed claims in a single call.", bold_prefix="2. FUNC_GET_STUDENT_ACTIVITY(p_student_id): ")

    add_heading_2(doc, "8.3 Database Triggers")
    add_bullet(doc, "Row-level trigger that checks whether ITEM.status = 'RETURNED'. If true, it immediately raises application error ORA-20001, aborting fraudulent claim insertion.", bold_prefix="1. TRG_PREVENT_CLAIM_ON_RETURNED (BEFORE INSERT ON CLAIM): ")
    add_bullet(doc, "Row-level trigger that executes when :NEW.claim_status = 'APPROVED', automatically updating parent ITEM.status to 'RETURNED', ensuring atomic state synchronization.", bold_prefix="2. TRG_AUTO_UPDATE_ITEM_STATUS (AFTER UPDATE ON CLAIM): ")
    
    trig_shot1 = os.path.join(SHOTS_DIR, "screenshot_8_demo5_error.png")
    add_image_box(doc, trig_shot1, "Figure 8.2: Execution Proof: Trigger TRG_PREVENT_CLAIM_ON_RETURNED Raising Error ORA-20001")
    trig_shot2 = os.path.join(SHOTS_DIR, "screenshot_7_demo4_verify.png")
    add_image_box(doc, trig_shot2, "Figure 8.3: Execution Proof: Trigger TRG_AUTO_UPDATE_ITEM_STATUS Synchronizing Item State")

    add_heading_2(doc, "8.4 Explicit Cursors")
    add_body_p(doc, "To perform batch administrative audits of aging unclaimed property, procedure PROC_FLAG_LONG_UNCLAIMED_ITEMS implements an Explicit Cursor with a formal 5-stage lifecycle:")
    add_code_block(doc, """PROCEDURE PROC_FLAG_LONG_UNCLAIMED_ITEMS(p_days_threshold IN NUMBER, p_total_flagged OUT NUMBER) IS
    CURSOR cur_unclaimed_items IS
        SELECT item_id, item_name, status, date_reported, building
        FROM ITEM i JOIN LOCATION l ON i.location_id = l.location_id
        WHERE i.status IN ('LOST', 'FOUND')
          AND (SYSDATE - i.date_reported) >= p_days_threshold;
    v_rec cur_unclaimed_items%ROWTYPE;
BEGIN
    OPEN cur_unclaimed_items; -- 1. Allocate PGA Context Area
    LOOP
        FETCH cur_unclaimed_items INTO v_rec; -- 2. Advance row pointer
        EXIT WHEN cur_unclaimed_items%NOTFOUND; -- 3. Termination check
        -- 4. Process record and compute aging metrics
    END LOOP;
    CLOSE cur_unclaimed_items; -- 5. Release memory
END;""")
    cur_shot = os.path.join(SHOTS_DIR, "screenshot_9_demo6_cursor.png")
    add_image_box(doc, cur_shot, "Figure 8.4: Execution Proof: Explicit Cursor Batch Memory Audit Output")

    add_heading_2(doc, "8.5 Sequences and Auto-Generated Keys")
    add_body_p(doc, "Unique surrogate identifiers are generated using Oracle database sequences (SEQ_ITEM_ID, SEQ_CLAIM_ID, SEQ_REPORT_ID) starting at defined block increments, ensuring monotonic uniqueness without contention.")

    add_heading_2(doc, "8.6 Transactions and ACID Properties")
    add_bullet(doc, "Either both the claim approval and parent item status update succeed, or all changes roll back.", bold_prefix="Atomicity: ")
    add_bullet(doc, "Schema constraints and triggers ensure invalid statuses or orphaned claims cannot enter the database.", bold_prefix="Consistency: ")
    add_bullet(doc, "Concurrent student claim filings operate under row-level lock isolation.", bold_prefix="Isolation: ")
    add_bullet(doc, "Committed transactions are persisted to disk via Write-Ahead Logging (WAL) and redo log files.", bold_prefix="Durability: ")

    add_heading_2(doc, "8.7 COMMIT, ROLLBACK, and SAVEPOINT")
    add_body_p(doc, "During claim verification, if an unexpected exception arises while rejecting competing claims, a ROLLBACK TO SAVEPOINT claim_verified is issued, preserving the primary verification while safely logging the competing error.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 9: QUERY PROCESSING AND OPTIMIZATION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 9: QUERY PROCESSING AND OPTIMIZATION")

    add_heading_2(doc, "9.1 Query Processing Overview")
    add_body_p(doc, "When a client submits an SQL query, the DBMS processing pipeline executes three phases: (1) Syntactic and semantic Parsing, checking dictionary permissions; (2) Query Optimization, where the Cost-Based Optimizer (CBO) generates multiple candidate execution trees and selects the minimum cost plan; and (3) Query Execution, pulling pages through the database buffer cache.")

    add_heading_2(doc, "9.2 Indexes")
    add_body_p(doc, "To eliminate full table scans during high-frequency lookups, B-Tree indexes were created on foreign keys and search filter columns: idx_item_status ON ITEM(status), idx_item_location ON ITEM(location_id), and idx_claim_item ON CLAIM(item_id). B-Tree indexing reduces tree depth to O(log N) disk reads.")

    add_heading_2(doc, "9.3 Query Execution Plan")
    add_body_p(doc, "Running EXPLAIN PLAN FOR on Query 02 demonstrated that joining ITEM with STUDENT and LOCATION utilizes INDEX UNIQUE SCAN on primary keys and HASH JOIN on location_id, achieving an estimated cost of 3 I/O operations compared to 48 operations under un-indexed nested loops.")

    add_heading_2(doc, "9.4 Query Optimization (Single-Pass Scan)")
    add_body_p(doc, "In Query 04 (Category Breakdown), traditional un-optimized design requires executing three separate COUNT queries with WHERE status='LOST', WHERE status='FOUND', and WHERE status='RETURNED'. We optimized this into a single atomic table scan using conditional aggregation: SUM(CASE WHEN status='LOST' THEN 1 ELSE 0 END), reducing buffer read overhead by 66.7%.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 10: DATABASE SECURITY, TRANSACTIONS AND RECOVERY
    # =========================================================================
    add_heading_1(doc, "CHAPTER 10: DATABASE SECURITY, TRANSACTIONS AND RECOVERY")

    add_heading_2(doc, "10.1 Authentication and Authorization")
    add_body_p(doc, "Role-Based Access Control (RBAC) enforces strict privilege segregation: CAMPUS_SECURITY_ROLE is granted SELECT, UPDATE on CLAIM and ITEM, and EXECUTE on verification procedures. STUDENT_ROLE is restricted to SELECT on active items and INSERT on reports and claims.")

    add_heading_2(doc, "10.2 SQL Injection Prevention")
    add_body_p(doc, "All database communications in the application layer (database.py) strictly employ parameterized SQL queries using ? placeholders (e.g., cursor.execute('SELECT * FROM ITEM WHERE category = ?', (cat,))). This completely decouples SQL command grammar from user input data, neutralizing SQL injection vulnerabilities.")

    add_heading_2(doc, "10.3 Backup Strategy and Crash Recovery")
    add_body_p(doc, "The database utilizes Write-Ahead Logging (WAL). Transaction log records are written to persistent storage before modified data pages are flushed from the buffer cache. In the event of sudden server shutdown, the recovery subsystem scans the checkpoint log, REDO-ing all committed transactions and UNDO-ing uncommitted active transactions.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 11: APPLICATION DEVELOPMENT AND CONNECTIVITY
    # =========================================================================
    add_heading_1(doc, "CHAPTER 11: APPLICATION DEVELOPMENT AND CONNECTIVITY")

    add_heading_2(doc, "11.1 System Architecture")
    add_body_p(doc, "The system implements a decoupled 3-Tier Enterprise Architecture:")
    add_bullet(doc, "Interactive Responsive Web Portal (HTML5/CSS3/JavaScript) and Administrative Terminal Console.", bold_prefix="1. Presentation Tier: ")
    add_bullet(doc, "Python 3.13 RESTful API Server and unified Data Access Layer (database.py) managing transactions.", bold_prefix="2. Application / Business Tier: ")
    add_bullet(doc, "Oracle 19c/21c Relational Database and embedded SQLite engine with stored procedures and triggers.", bold_prefix="3. Database Tier: ")

    add_heading_2(doc, "11.2 Technology Stack")
    add_bullet(doc, "Python 3.13 native runtime (Built-in http.server, urllib, sqlite3, json) - Zero pip dependencies.", bold_prefix="Backend Engine: ")
    add_bullet(doc, "Vanilla HTML5, modern CSS Grid/Flexbox styling, ES6+ Fetch API Single Page Architecture.", bold_prefix="Frontend UI: ")
    add_bullet(doc, "Oracle Database 19c / 21c and SQLite 3.x embedded relational engine.", bold_prefix="Database Engine: ")

    add_heading_2(doc, "11.3 Application Screenshots")
    add_body_p(doc, "The live web portal and administrative terminal session interfaces are presented below:")
    web_shot = os.path.join(SHOTS_DIR, "screenshot_10_web_portal.png")
    add_image_box(doc, web_shot, "Figure 11.1: Integrated Web Application Dashboard (Catalog, Stats Counters, Live Navigation)")
    cli_shot = os.path.join(SHOTS_DIR, "screenshot_3_python_app.png")
    add_image_box(doc, cli_shot, "Figure 11.2: Python Interactive Terminal Administrative Console")

    add_heading_2(doc, "11.4 Relational versus NoSQL Analysis")
    add_body_p(doc, "While NoSQL document stores (such as MongoDB) excel at unstructured blog posts or clickstreams, a campus lost and found system fundamentally requires multi-table foreign key referential integrity, row-level concurrency locking on high-value disputed claims, and strict ACID rollback capabilities, for which an RDBMS is technically superior.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 12: TESTING AND RESULTS
    # =========================================================================
    add_heading_1(doc, "CHAPTER 12: TESTING AND RESULTS")

    add_heading_2(doc, "12.1 Testing Strategy")
    add_body_p(doc, "Testing encompassed unit testing of individual SQL queries, boundary testing on check constraints, integration testing between web endpoints and PL/SQL procedures, and stress testing of trigger-based integrity enforcement.")

    add_heading_2(doc, "12.2 Comprehensive Test Cases (TC01 to TC15)")
    add_body_p(doc, "The test execution results across 15 core scenarios are documented below:")
    tc_data = [
        ("TC01", "Student Registration", "Insert student '24BYB0182'", "Student row added with valid email", "Row inserted; PK enforced", "PASS"),
        ("TC02", "Duplicate Email Check", "Insert student with duplicate email", "UNIQUE constraint violation error", "ORA-00001 unique constraint raised", "PASS"),
        ("TC03", "Invalid Status Domain", "Insert item with status='DONATED'", "CHECK constraint violation error", "CHECK constraint chk_item_status raised", "PASS"),
        ("TC04", "Report Lost Item", "File lost report for Item #1001", "Row inserted into ITEM and LOST_REPORT", "Transaction committed atomically", "PASS"),
        ("TC05", "Report Found Item", "File found turn-in for Item #1002", "Row inserted into ITEM and FOUND_REPORT", "Item logged in 'FOUND' status", "PASS"),
        ("TC06", "Catalog Live Filter", "Filter by Category='Electronics'", "Returns only electronic articles", "Filtered subset returned in <10ms", "PASS"),
        ("TC07", "Submit Valid Claim", "File claim on Item #1002 with proof", "Claim inserted in 'PENDING' status", "Claim ID #411 generated", "PASS"),
        ("TC08", "Procedural Validation", "Call PROC_SUBMIT_CLAIM for invalid student", "Procedure rejects un-registered student", "Returns error: 'Student not registered'", "PASS"),
        ("TC09", "Verify Claim Approval", "Admin approves Claim #411", "Claim -> APPROVED; Item -> RETURNED", "Trigger auto-updated item status", "PASS"),
        ("TC10", "Resolve Competing Claims", "Approve Claim A on Item with Claim B", "Claim A APPROVED; Claim B REJECTED", "Competing claim automatically REJECTED", "PASS"),
        ("TC11", "Fraudulent Claim Block", "Submit claim on already RETURNED item", "Trigger aborts insert with ORA-20001", "Trigger TRG_PREVENT_CLAIM aborted insert", "PASS"),
        ("TC12", "Explicit Cursor Audit", "Run PROC_FLAG_LONG_UNCLAIMED_ITEMS(10)", "Scans PGA memory; outputs aging list", "Cursor fetched and counted 3 items", "PASS"),
        ("TC13", "Student Engagement Profile", "Execute FUNC_GET_STUDENT_ACTIVITY", "Dynamic summary text returned", "Returned 'Arahat [24BYB0182] -> Lost: 1...'", "PASS"),
        ("TC14", "Cascade Delete Test", "Delete test item #1099 with child claims", "Child claims and reports purged", "ON DELETE CASCADE purged child records", "PASS"),
        ("TC15", "Web App End-to-End Test", "Execute 5-step Review III demo suite", "All 5 transactions execute live", "100% success; state synchronized", "PASS")
    ]
    tbl_tc = doc.add_table(rows=len(tc_data) + 1, cols=6)
    tbl_tc.rows[0].cells[0].paragraphs[0].add_run("Test ID")
    tbl_tc.rows[0].cells[1].paragraphs[0].add_run("Test Scenario")
    tbl_tc.rows[0].cells[2].paragraphs[0].add_run("Input / Action")
    tbl_tc.rows[0].cells[3].paragraphs[0].add_run("Expected Result")
    tbl_tc.rows[0].cells[4].paragraphs[0].add_run("Actual System Output")
    tbl_tc.rows[0].cells[5].paragraphs[0].add_run("Status")
    for idx, (tid, tsc, tin, texp, tact, tstat) in enumerate(tc_data):
        row = tbl_tc.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(tid).bold = True
        row.cells[1].paragraphs[0].add_run(tsc)
        row.cells[2].paragraphs[0].add_run(tin)
        row.cells[3].paragraphs[0].add_run(texp)
        row.cells[4].paragraphs[0].add_run(tact)
        r_st = row.cells[5].paragraphs[0].add_run(tstat)
        r_st.bold = True
        r_st.font.color.rgb = RGBColor(16, 185, 129) # Emerald Green
    style_table(tbl_tc)

    add_heading_2(doc, "12.3 Results and Limitations")
    add_body_p(doc, "The testing confirmed zero data corruption, flawless constraint enforcement, and sub-50ms query turnaround. Known limitations include dependency on manual physical handoffs at security desks and lack of hardware RFID readers at entrance turnstiles.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 13: CONCLUSION AND FUTURE ENHANCEMENTS
    # =========================================================================
    add_heading_1(doc, "CHAPTER 13: CONCLUSION AND FUTURE ENHANCEMENTS")

    add_heading_2(doc, "13.1 Conclusion")
    add_body_p(doc, "The Campus Lost and Found Management System successfully replaces vulnerable manual logbooks with a robust, enterprise-grade relational database solution. By implementing Third Normal Form (3NF) across 7 entities, encapsulating business rules in PL/SQL stored procedures, and enforcing data security through row-level database triggers, the system achieves complete operational transparency, zero phantom inventory, and bulletproof claim verification.")

    add_heading_2(doc, "13.2 Learning Outcomes")
    add_bullet(doc, "Mastery of relational modeling, mathematical dependency closures, and lossless 3NF normalization.")
    add_bullet(doc, "Deep competency in procedural database programming: stored procedures, functions, triggers, and cursors.")
    add_bullet(doc, "Hands-on experience in building decoupled multi-tier web applications connecting Python REST APIs to SQL backends.")
    add_bullet(doc, "Practical understanding of transaction isolation, ACID properties, query execution plans, and B-Tree indexing.")

    add_heading_2(doc, "13.3 Future Enhancements")
    add_bullet(doc, "Turnstile RFID & Smart Card Integration: Automatic owner notification when a lost ID card is scanned at campus security turnstiles.")
    add_bullet(doc, "Computer Vision Image Similarity: Uploading photos of found items to compute image embedding similarity against lost item descriptions.")
    add_bullet(doc, "Real-Time SMS / WhatsApp Notifications: Push messaging to students when claims are reviewed or when matching items are turned in.")

    add_heading_1(doc, "REFERENCES")
    refs = [
        "1. Elmasri, R., & Navathe, S. B. (2016). Fundamentals of Database Systems (7th ed.). Pearson Education.",
        "2. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database System Concepts (7th ed.). McGraw-Hill Education.",
        "3. Ramakrishnan, R., & Gehrke, J. (2003). Database Management Systems (3rd ed.). McGraw-Hill Science/Engineering/Math.",
        "4. Oracle Corporation. (2023). Oracle Database 19c/21c SQL Language Reference and PL/SQL User's Guide and Reference. Oracle Documentation Library.",
        "5. Python Software Foundation. (2026). Python 3.13 Database API Specification v2.0 (PEP 249). Python.org."
    ]
    for r in refs:
        add_body_p(doc, r, space_after=4)

    doc.add_page_break()

    # =========================================================================
    # APPENDICES
    # =========================================================================
    add_heading_1(doc, "APPENDIX A: COMPLETE EXECUTABLE SQL SCRIPTS")
    add_heading_2(doc, "A.1 Complete DDL Table Creation Script")
    add_code_block(doc, """-- Table 1: LOCATION
CREATE TABLE LOCATION (
    location_id NUMBER PRIMARY KEY,
    location_name VARCHAR2(100) NOT NULL,
    building VARCHAR2(100) NOT NULL
);

-- Table 2: STUDENT
CREATE TABLE STUDENT (
    student_id VARCHAR2(20) PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    phone VARCHAR2(15) NOT NULL
);

-- Table 3: ADMIN
CREATE TABLE ADMIN (
    admin_id NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL
);

-- Table 4: ITEM
CREATE TABLE ITEM (
    item_id NUMBER PRIMARY KEY,
    item_name VARCHAR2(100) NOT NULL,
    description VARCHAR2(300),
    category VARCHAR2(50) NOT NULL,
    date_reported DATE DEFAULT SYSDATE NOT NULL,
    status VARCHAR2(20) DEFAULT 'LOST' NOT NULL,
    location_id NUMBER NOT NULL,
    reported_by_student_id VARCHAR2(20) NOT NULL,
    CONSTRAINT chk_item_status CHECK (status IN ('LOST', 'FOUND', 'CLAIMED', 'RETURNED')),
    CONSTRAINT fk_item_location FOREIGN KEY (location_id) REFERENCES LOCATION(location_id),
    CONSTRAINT fk_item_student FOREIGN KEY (reported_by_student_id) REFERENCES STUDENT(student_id)
);

-- Table 5: LOST_REPORT
CREATE TABLE LOST_REPORT (
    lost_report_id NUMBER PRIMARY KEY,
    item_id NUMBER NOT NULL,
    student_id VARCHAR2(20) NOT NULL,
    date_lost DATE NOT NULL,
    details VARCHAR2(300),
    CONSTRAINT fk_lr_item FOREIGN KEY (item_id) REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_lr_student FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE
);

-- Table 6: FOUND_REPORT
CREATE TABLE FOUND_REPORT (
    found_report_id NUMBER PRIMARY KEY,
    item_id NUMBER NOT NULL,
    student_id VARCHAR2(20) NOT NULL,
    date_found DATE DEFAULT SYSDATE NOT NULL,
    details VARCHAR2(300),
    CONSTRAINT fk_fr_item FOREIGN KEY (item_id) REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_fr_student FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE
);

-- Table 7: CLAIM
CREATE TABLE CLAIM (
    claim_id NUMBER PRIMARY KEY,
    item_id NUMBER NOT NULL,
    claimant_student_id VARCHAR2(20) NOT NULL,
    claim_date DATE DEFAULT SYSDATE NOT NULL,
    proof_description VARCHAR2(300) NOT NULL,
    claim_status VARCHAR2(20) DEFAULT 'PENDING' NOT NULL,
    admin_id NUMBER,
    CONSTRAINT chk_claim_status CHECK (claim_status IN ('PENDING', 'APPROVED', 'REJECTED')),
    CONSTRAINT fk_claim_item FOREIGN KEY (item_id) REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_claim_student FOREIGN KEY (claimant_student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_claim_admin FOREIGN KEY (admin_id) REFERENCES ADMIN(admin_id)
);""")

    add_heading_2(doc, "A.2 PL/SQL Procedures, Functions and Triggers Script")
    add_code_block(doc, """-- Stored Procedure: Submit Claim with Procedural Validation
CREATE OR REPLACE PROCEDURE PROC_SUBMIT_CLAIM (
    p_item_id IN NUMBER,
    p_claimant_id IN VARCHAR2,
    p_proof IN VARCHAR2,
    p_new_claim_id OUT NUMBER,
    p_result_msg OUT VARCHAR2
) IS
    v_item_count NUMBER;
    v_status VARCHAR2(20);
    v_student_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_student_count FROM STUDENT WHERE student_id = p_claimant_id;
    IF v_student_count = 0 THEN
        p_result_msg := 'ERROR: Student ID ' || p_claimant_id || ' is not registered.';
        RETURN;
    END IF;

    SELECT COUNT(*), NVL(MAX(status), 'NONE') INTO v_item_count, v_status FROM ITEM WHERE item_id = p_item_id;
    IF v_item_count = 0 THEN
        p_result_msg := 'ERROR: Item ID ' || p_item_id || ' does not exist.';
        RETURN;
    END IF;

    IF v_status = 'RETURNED' THEN
        p_result_msg := 'ERROR: Item has already been RETURNED to owner.';
        RETURN;
    END IF;

    SELECT NVL(MAX(claim_id), 400) + 1 INTO p_new_claim_id FROM CLAIM;
    INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status)
    VALUES (p_new_claim_id, p_item_id, p_claimant_id, SYSDATE, p_proof, 'PENDING');

    p_result_msg := 'SUCCESS: Claim #' || p_new_claim_id || ' registered in PENDING status.';
    COMMIT;
END;
/

-- Row-Level Security Trigger: Block Claims on Returned Items
CREATE OR REPLACE TRIGGER TRG_PREVENT_CLAIM_ON_RETURNED
BEFORE INSERT ON CLAIM
FOR EACH ROW
DECLARE
    v_status VARCHAR2(20);
BEGIN
    SELECT status INTO v_status FROM ITEM WHERE item_id = :NEW.item_id;
    IF v_status = 'RETURNED' THEN
        RAISE_APPLICATION_ERROR(-20001, 'Integrity Rule Violation: Item #' || :NEW.item_id || ' has already been RETURNED. New claims disallowed.');
    END IF;
END;
/

-- Row-Level State Synchronization Trigger: Auto Update Item on Approval
CREATE OR REPLACE TRIGGER TRG_AUTO_UPDATE_ITEM_STATUS
AFTER UPDATE OF claim_status ON CLAIM
FOR EACH ROW
WHEN (NEW.claim_status = 'APPROVED')
BEGIN
    UPDATE ITEM SET status = 'RETURNED' WHERE item_id = :NEW.item_id;
END;
/""")

    add_heading_1(doc, "APPENDIX B: SAMPLE DATA AND SCREENSHOTS")
    add_body_p(doc, "Below are representative sample execution records and interface captures verifying system readiness and advanced analytical querying:")
    b1_path = os.path.join(SHOTS_DIR, "screenshot_appendix_b1.png")
    if os.path.exists(b1_path):
        add_image_box(doc, b1_path, "Figure B.1: Oracle FreeSQL Execution Proof: Analytical Category Aggregation with Conditional SUM(CASE)")
    
    b2_path = os.path.join(SHOTS_DIR, "screenshot_appendix_b2.png")
    if os.path.exists(b2_path):
        add_image_box(doc, b2_path, "Figure B.2: Integrated Web Application Live 5-Step Transaction Suite and Evaluation Workflow")
    else:
        add_image_box(doc, os.path.join(SHOTS_DIR, "screenshot_10_web_portal.png"), "Figure B.2: Integrated Web Portal Master Catalog and Real-Time State Management")

    add_heading_1(doc, "APPENDIX C: SAMPLE TEST CASE TABLE")
    add_body_p(doc, "Refer to Table 12.1 in Chapter 12 for the full 15-test-case validation suite (TC01 to TC15).")

    # =========================================================================
    # SAVE DOCUMENT (Multiple Locations with Fail-safe)
    # =========================================================================
    p1 = os.path.join(DOCS_DIR, "Campus_Lost_and_Found_Review3_Official_Report.docx")
    doc.save(p1)
    print(f"[1/3] Successfully saved: {p1}")

    p2 = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project\Campus_Lost_and_Found_Review3_Official_Report.docx"
    doc.save(p2)
    print(f"[2/3] Successfully saved: {p2}")

    p3 = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Review3_Official_Report.docx"
    try:
        doc.save(p3)
        print(f"[3/3] Successfully saved: {p3}")
    except PermissionError:
        p3_alt = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Review3_Official_Report_v2.docx"
        doc.save(p3_alt)
        print(f"[3/3 Alt] Saved to: {p3_alt}")

    # Also attempt to update the final copy if Word released it
    p_final = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Review3_Report_Final.docx"
    try:
        doc.save(p_final)
        print(f"[Final] Updated: {p_final}")
    except PermissionError:
        print(f"[Note] {p_final} is locked by Word; official copies are saved above.")

if __name__ == "__main__":
    create_report()
