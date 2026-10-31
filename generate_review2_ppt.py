"""
Script to generate the Review 2 PowerPoint Presentation for VIT BCSE302L.
Matches the dark modern tech aesthetic of Review 1 with rich content for all Review 2 evaluation criteria.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_DARK = RGBColor(15, 23, 42)        # #0F172A (Deep Slate Navy)
    CARD_BG = RGBColor(30, 41, 59)        # #1E293B (Card Fill)
    CARD_BORDER = RGBColor(51, 65, 85)    # #334155 (Subtle Border)
    TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC (White Text)
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8 (Muted Gray Text)
    ACCENT_CYAN = RGBColor(56, 189, 248)  # #38BDF8 (Tech Cyan Accent)
    ACCENT_BLUE = RGBColor(96, 165, 250)  # #60A5FA (Soft Blue Accent)
    ACCENT_GREEN = RGBColor(52, 211, 153) # #34D399 (Emerald Green Accent)
    ACCENT_AMBER = RGBColor(251, 191, 36) # #FBBF24 (Amber Accent)
    CODE_BG = RGBColor(24, 33, 47)         # #18212F (Code block background)

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="REVIEW II: DATABASE IMPLEMENTATION"):
        # Category / Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN
        p_cat.font.name = "Segoe UI"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.font.name = "Segoe UI"

    def add_card(slide, left, top, width, height, title="", title_color=ACCENT_CYAN, fill_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.font.name = "Segoe UI"

        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # University Badge / Tag
    tag_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11.0), Inches(0.4))
    tf_tag = tag_box.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "VELLORE INSTITUTE OF TECHNOLOGY | BCSE302L - DATABASE SYSTEMS"
    p_tag.font.size = Pt(12)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_CYAN
    p_tag.font.name = "Segoe UI"

    # Main Project Title
    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(1.8))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Campus Lost and Found\nManagement System"
    p_t.font.size = Pt(40)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE
    p_t.font.name = "Segoe UI"

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(1.2), Inches(3.7), Inches(11.0), Inches(0.6))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "REVIEW II: DATABASE IMPLEMENTATION & TECHNICAL DEFENSE"
    p_sub.font.size = Pt(16)
    p_sub.font.bold = True
    p_sub.font.color.rgb = ACCENT_BLUE
    p_sub.font.name = "Segoe UI"

    # Student Card Box
    add_card(s1, Inches(1.2), Inches(4.5), Inches(10.9), Inches(1.8), title="", fill_color=CARD_BG)
    info_box = s1.shapes.add_textbox(Inches(1.5), Inches(4.7), Inches(10.3), Inches(1.4))
    tf_info = info_box.text_frame
    tf_info.word_wrap = True

    lines = [
        ("Student Name:", " Arahat Gaikwad"),
        ("Registration Number:", " 24BYB0182"),
        ("Programme / Branch:", " B.Tech Computer Science & Engineering"),
        ("School:", " School of Computer Science Engineering and Information Systems (SCORE)")
    ]
    for idx, (label, val) in enumerate(lines):
        p = tf_info.paragraphs[0] if idx == 0 else tf_info.add_paragraph()
        run1 = p.add_run()
        run1.text = label
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = ACCENT_CYAN
        run1.font.name = "Segoe UI"
        run2 = p.add_run()
        run2.text = val
        run2.font.size = Pt(13)
        run2.font.color.rgb = TEXT_WHITE
        run2.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 2: REVIEW II AGENDA & EVALUATION MAPPING
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Review II Evaluation Agenda & Deliverables Mapping", "OFFICIAL EVALUATION CRITERIA")

    agenda_items = [
        ("1. DDL & Constraints", "2 Marks", "Creation of 7 normalized tables with PK, FK, CHECK, UNIQUE, NOT NULL & DEFAULT constraints.", ACCENT_CYAN),
        ("2. DML & Population", "1 Mark", "Meaningful dataset with 10+ records per table (70+ total rows) and INSERT/UPDATE/DELETE tests.", ACCENT_BLUE),
        ("3. SQL Queries", "2 Marks", "16 comprehensive queries covering multi-table joins, aggregations, subqueries, set ops & ranking.", ACCENT_GREEN),
        ("4. Procedures & Functions", "2 Marks", "Business operations: PROC_SUBMIT_CLAIM, PROC_VERIFY_CLAIM, and 2 analytical stored functions.", ACCENT_AMBER),
        ("5. Cursor & Triggers", "2 Marks", "Explicit Cursor batch scan for aging items + 2 automated triggers for status sync & error blocking.", ACCENT_CYAN),
        ("6. Technical Viva", "1 Mark", "Execution demonstration, schema rationale, atomic transactions, and relational defense.", ACCENT_BLUE)
    ]

    for idx, (title, marks, desc, col) in enumerate(agenda_items):
        col_idx = idx % 3
        row_idx = idx // 3
        c_left = Inches(0.8 + col_idx * 3.95)
        c_top = Inches(1.65 + row_idx * 2.65)
        c_w = Inches(3.75)
        c_h = Inches(2.45)

        add_card(s2, c_left, c_top, c_w, c_h, title="", fill_color=CARD_BG)

        tb = s2.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.2), c_w - Inches(0.4), c_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.font.name = "Segoe UI"

        p_m = tf.add_paragraph()
        p_m.text = f"Weightage: {marks}"
        p_m.font.size = Pt(12)
        p_m.font.bold = True
        p_m.font.color.rgb = ACCENT_AMBER
        p_m.font.name = "Segoe UI"

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 3: RELATIONAL ARCHITECTURE & 3NF RECAP
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Normalized Relational Architecture (3NF)", "SYSTEM SCHEMA ARCHITECTURE")

    # Left: 7 Tables Summary Card
    add_card(s3, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.2), "7 Core Normalized Entities (3NF)", ACCENT_CYAN)
    tb_left = s3.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.5))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True

    tables_info = [
        ("LOCATION", "location_id (PK), location_name, building"),
        ("STUDENT", "student_id (PK), name, email (UK), phone"),
        ("ADMIN", "admin_id (PK), name, email (UK)"),
        ("ITEM", "item_id (PK), item_name, description, category, date_reported, status, location_id (FK), reported_by_student_id (FK)"),
        ("LOST_REPORT", "lost_report_id (PK), item_id (FK), student_id (FK), date_lost, details"),
        ("FOUND_REPORT", "found_report_id (PK), item_id (FK), student_id (FK), date_found, details"),
        ("CLAIM", "claim_id (PK), item_id (FK), claimant_student_id (FK), claim_date, proof_description, claim_status, admin_id (FK)")
    ]
    for idx, (tname, tcols) in enumerate(tables_info):
        p = tf_l.paragraphs[0] if idx == 0 else tf_l.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {tname}: "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_GREEN
        r1.font.name = "Segoe UI"
        r2 = p.add_run()
        r2.text = tcols
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED
        r2.font.name = "Segoe UI"

    # Right: Relationships & Normalization Rationale
    add_card(s3, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2), "9 Relational Foreign Key Mappings (1:N)", ACCENT_BLUE)
    tb_right = s3.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.5))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True

    rel_info = [
        "1. STUDENT -> ITEM (1:N via reported_by_student_id)",
        "2. LOCATION -> ITEM (1:N via location_id)",
        "3. STUDENT -> LOST_REPORT (1:N via student_id)",
        "4. ITEM -> LOST_REPORT (1:N via item_id)",
        "5. STUDENT -> FOUND_REPORT (1:N via student_id)",
        "6. ITEM -> FOUND_REPORT (1:N via item_id)",
        "7. STUDENT -> CLAIM (1:N via claimant_student_id)",
        "8. ITEM -> CLAIM (1:N via item_id)",
        "9. ADMIN -> CLAIM (1:N via admin_id)",
        "",
        "Normalization Justification (3NF):",
        "• 1NF: Atomic attributes, no repeating groups.",
        "• 2NF: No partial key dependencies; non-keys fully dependent on PK.",
        "• 3NF: No transitive dependencies; reports separated from claims."
    ]
    for idx, rtext in enumerate(rel_info):
        p = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        p.text = rtext
        p.font.size = Pt(11)
        if "Normalization" in rtext:
            p.font.bold = True
            p.font.color.rgb = ACCENT_AMBER
        elif rtext.startswith("•"):
            p.font.color.rgb = TEXT_WHITE
        else:
            p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 4: DDL IMPLEMENTATION & INTEGRITY CONSTRAINTS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "DDL Implementation & Integrity Constraints (2 Marks)", "DATA DEFINITION LANGUAGE")

    constraints = [
        ("Primary Keys (PK)", "Guarantees entity uniqueness across all 7 tables:\n• pk_location on location_id\n• pk_student on student_id\n• pk_admin on admin_id\n• pk_item on item_id\n• pk_lost_report on lost_report_id\n• pk_found_report on found_report_id\n• pk_claim on claim_id", ACCENT_CYAN),
        ("Foreign Keys (FK)", "9 Referential integrity relationships:\n• Restricts orphan records\n• ON DELETE CASCADE enabled on ITEM reports and claims to maintain referential cleanliness when items are removed\n• All child tables strictly map to parent PKs", ACCENT_BLUE),
        ("Domain CHECK Rules", "Strict allowable values enforcement:\n• chk_item_status:\n  CHECK (status IN ('LOST', 'FOUND', 'CLAIMED', 'RETURNED'))\n• chk_claim_status:\n  CHECK (claim_status IN ('PENDING', 'APPROVED', 'REJECTED'))", ACCENT_AMBER),
        ("UNIQUE, NOT NULL & DEFAULT", "Field-level validity & automation:\n• UNIQUE (email) on STUDENT and ADMIN\n• NOT NULL on critical identifying attributes\n• DEFAULT SYSDATE on dates\n• DEFAULT 'PENDING' on claim status\n• DEFAULT 'LOST' on item status", ACCENT_GREEN)
    ]

    for idx, (title, desc, col) in enumerate(constraints):
        col_idx = idx % 2
        row_idx = idx // 2
        c_left = Inches(0.8 + col_idx * 5.95)
        c_top = Inches(1.65 + row_idx * 2.65)
        c_w = Inches(5.75)
        c_h = Inches(2.45)

        add_card(s4, c_left, c_top, c_w, c_h, title, col)
        tb = s4.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.65), c_w - Inches(0.4), c_h - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 5: DML & DATA POPULATION
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "DML & Data Population: 10+ Records/Table (1 Mark)", "DATA MANIPULATION LANGUAGE")

    # Card 1: Population Overview
    add_card(s5, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.2), "Meaningful Campus Data Population", ACCENT_CYAN)
    tb_pop = s5.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.5))
    tf_pop = tb_pop.text_frame
    tf_pop.word_wrap = True

    pop_pts = [
        "• Minimum Requirement Satisfied: At least 10 meaningful records per table.",
        "• Total Records Populated: 72+ records across 7 tables.",
        "",
        "Table Breakdown:",
        "  1. LOCATION: 10 Campus buildings (SJT, TT, Library, PRP, Foodys, MB, Hostels).",
        "  2. STUDENT: 10 Registered students with valid VIT emails & phones.",
        "  3. ADMIN: 10 Campus security officers and library administrators.",
        "  4. ITEM: 12 Cataloged items (Electronics, IDs, Keys, Books, Accessories).",
        "  5. LOST_REPORT: 10 Detailed missing item incident filings.",
        "  6. FOUND_REPORT: 10 Turned-in item discoveries.",
        "  7. CLAIM: 10 Ownership verification claims (PENDING, APPROVED, REJECTED)."
    ]
    for idx, pt in enumerate(pop_pts):
        p = tf_pop.paragraphs[0] if idx == 0 else tf_pop.add_paragraph()
        p.text = pt
        p.font.size = Pt(11)
        p.font.color.rgb = ACCENT_AMBER if "Table Breakdown" in pt else (TEXT_WHITE if pt.startswith("•") else TEXT_MUTED)
        p.font.name = "Segoe UI"

    # Card 2: DML Demonstration (INSERT, UPDATE, DELETE)
    add_card(s5, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2), "DML Operations Demonstration (FR15)", ACCENT_GREEN)
    tb_dml = s5.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.5))
    tf_dml = tb_dml.text_frame
    tf_dml.word_wrap = True

    dml_pts = [
        "1. INSERT Demonstration:",
        "   • Registration of student '24BCS9999' (Rishi Mukherjee)",
        "   • Creation of Location #111 ('Smart Conference Hall 1')",
        "   • Filing of Lost Item #1099 with linked Lost Report #299",
        "",
        "2. UPDATE Demonstration:",
        "   • Student contact update: changing phone number",
        "   • Item specification refinement: adding dongle detail",
        "   • Administrative review note appended to Claim #402",
        "",
        "3. DELETE Demonstration:",
        "   • Deletion of duplicate/withdrawn Claim #499",
        "   • Safe cleanup of temporary demo item and report",
        "   • Verification query before & after confirming zero orphan rows"
    ]
    for idx, pt in enumerate(dml_pts):
        p = tf_dml.paragraphs[0] if idx == 0 else tf_dml.add_paragraph()
        p.text = pt
        p.font.size = Pt(11)
        if any(h in pt for h in ["1. INSERT", "2. UPDATE", "3. DELETE"]):
            p.font.bold = True
            p.font.color.rgb = ACCENT_CYAN
        else:
            p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 6: SQL QUERIES - JOINS & RETRIEVAL
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "SQL Queries: Complex Joins & Retrieval (2 Marks)", "QUERYING & REPORTING - PART 1")

    queries_part1 = [
        ("Query 01: Simple Retrieval with WHERE & ORDER BY",
         "SELECT item_id, item_name, category, date_reported, status\nFROM ITEM WHERE status = 'FOUND'\nORDER BY date_reported ASC;",
         "Lists all items currently ready to be claimed, sorted chronologically."),
        ("Query 02: 3-Table INNER JOIN (Full Context)",
         "SELECT i.item_name, s.name AS reporter, l.building\nFROM ITEM i\nJOIN STUDENT s ON i.reported_by_student_id = s.student_id\nJOIN LOCATION l ON i.location_id = l.location_id;",
         "Combines item, reporter identity, and exact campus building."),
        ("Query 03: LEFT OUTER JOIN (Unclaimed Detection)",
         "SELECT i.item_name, NVL(c.claim_status, 'UNCLAIMED') AS status\nFROM ITEM i\nLEFT OUTER JOIN CLAIM c ON i.item_id = c.item_id;",
         "Preserves all items, highlighting items with zero submitted claims."),
        ("Query 12: 4-Table Join (Approved Claims Audit)",
         "SELECT c.claim_id, s.name, i.item_name, l.building, a.name AS admin\nFROM CLAIM c\nJOIN STUDENT s ON c.claimant_student_id = s.student_id\nJOIN ITEM i ON c.item_id = i.item_id\nJOIN LOCATION l ON i.location_id = l.location_id\nJOIN ADMIN a ON c.admin_id = a.admin_id\nWHERE c.claim_status = 'APPROVED';",
         "Audits verified claims linking claimant, item, location & approving admin.")
    ]

    for idx, (title, sql_text, desc) in enumerate(queries_part1):
        col_idx = idx % 2
        row_idx = idx // 2
        c_left = Inches(0.8 + col_idx * 5.95)
        c_top = Inches(1.65 + row_idx * 2.65)
        c_w = Inches(5.75)
        c_h = Inches(2.45)

        add_card(s6, c_left, c_top, c_w, c_h, title, ACCENT_CYAN)

        # SQL box
        sql_box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), c_top + Inches(0.6), c_w - Inches(0.4), Inches(1.15))
        sql_box.fill.solid()
        sql_box.fill.fore_color.rgb = CODE_BG
        sql_box.line.color.rgb = CARD_BORDER
        tf_s = sql_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = Inches(0.08)
        p_s = tf_s.paragraphs[0]
        p_s.text = sql_text
        p_s.font.size = Pt(9.5)
        p_s.font.color.rgb = ACCENT_GREEN
        p_s.font.name = "Consolas"

        # Desc box
        d_box = s6.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(1.8), c_w - Inches(0.4), Inches(0.55))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = f"Purpose: {desc}"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 7: SQL QUERIES - AGGREGATIONS & GROUPING
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "SQL Queries: Aggregations & Grouping (2 Marks)", "QUERYING & REPORTING - PART 2")

    queries_part2 = [
        ("Query 04: Group By with Conditional Aggregation",
         "SELECT category, COUNT(item_id) AS total,\n       SUM(CASE WHEN status='LOST' THEN 1 ELSE 0 END) AS lost,\n       SUM(CASE WHEN status='FOUND' THEN 1 ELSE 0 END) AS found\nFROM ITEM GROUP BY category ORDER BY total DESC;",
         "Breaks down total item volume into lost vs found counts per category."),
        ("Query 05: Aggregate with HAVING Clause",
         "SELECT l.building, COUNT(i.item_id) AS incidents\nFROM LOCATION l\nJOIN ITEM i ON l.location_id = i.location_id\nGROUP BY l.building\nHAVING COUNT(i.item_id) >= 2;",
         "Detects high-loss hotspot zones on campus with 2 or more incidents."),
        ("Query 14: Conditional Aggregation (Admin Decision Breakdown)",
         "SELECT a.name, COUNT(c.claim_id) AS reviewed,\n       SUM(CASE WHEN c.claim_status='APPROVED' THEN 1 ELSE 0 END) AS approved,\n       SUM(CASE WHEN c.claim_status='REJECTED' THEN 1 ELSE 0 END) AS rejected\nFROM ADMIN a LEFT JOIN CLAIM c ON a.admin_id = c.admin_id GROUP BY a.name;",
         "Generates performance accountability report for campus security staff."),
        ("Query 15: Window Analytical Function (DENSE_RANK)",
         "SELECT category, COUNT(*) AS total_items,\n       DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS cat_rank\nFROM ITEM GROUP BY category;",
         "Ranks item categories based on total reported incident frequency.")
    ]

    for idx, (title, sql_text, desc) in enumerate(queries_part2):
        col_idx = idx % 2
        row_idx = idx // 2
        c_left = Inches(0.8 + col_idx * 5.95)
        c_top = Inches(1.65 + row_idx * 2.65)
        c_w = Inches(5.75)
        c_h = Inches(2.45)

        add_card(s7, c_left, c_top, c_w, c_h, title, ACCENT_BLUE)

        sql_box = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), c_top + Inches(0.6), c_w - Inches(0.4), Inches(1.15))
        sql_box.fill.solid()
        sql_box.fill.fore_color.rgb = CODE_BG
        sql_box.line.color.rgb = CARD_BORDER
        tf_s = sql_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = Inches(0.08)
        p_s = tf_s.paragraphs[0]
        p_s.text = sql_text
        p_s.font.size = Pt(9.5)
        p_s.font.color.rgb = ACCENT_GREEN
        p_s.font.name = "Consolas"

        d_box = s7.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(1.8), c_w - Inches(0.4), Inches(0.55))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = f"Purpose: {desc}"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 8: SQL QUERIES - SUBQUERIES & SET OPERATIONS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "SQL Queries: Subqueries & Set Operators (2 Marks)", "QUERYING & REPORTING - PART 3")

    queries_part3 = [
        ("Query 06: Nested Subquery with IN & NOT IN",
         "SELECT student_id, name, email FROM STUDENT\nWHERE student_id IN (SELECT student_id FROM LOST_REPORT)\n  AND student_id NOT IN (SELECT claimant_student_id FROM CLAIM);",
         "Finds students who filed lost reports but have never submitted any claim."),
        ("Query 07: Subquery with NOT EXISTS",
         "SELECT item_id, item_name, category, status\nFROM ITEM i\nWHERE NOT EXISTS (SELECT 1 FROM CLAIM c WHERE c.item_id = i.item_id);",
         "Identifies cataloged items that have zero claims filed against them."),
        ("Query 08: Correlated Subquery",
         "SELECT i.item_id, i.item_name, i.status,\n       (SELECT COUNT(*) FROM CLAIM c WHERE c.item_id = i.item_id) AS total_claims\nFROM ITEM i ORDER BY total_claims DESC;",
         "Calculates competing claims volume per item dynamically."),
        ("Query 09: Set Operator (UNION ALL)",
         "SELECT 'LOST' AS type, i.item_name, lr.date_lost AS event_date, s.name FROM LOST_REPORT lr JOIN ITEM i ON lr.item_id=i.item_id JOIN STUDENT s ON lr.student_id=s.student_id\nUNION ALL\nSELECT 'FOUND' AS type, i.item_name, fr.date_found, s.name FROM FOUND_REPORT fr JOIN ITEM i ON fr.item_id=i.item_id JOIN STUDENT s ON fr.student_id=s.student_id\nORDER BY event_date DESC;",
         "Combines lost and found incident filings into a unified chronological feed.")
    ]

    for idx, (title, sql_text, desc) in enumerate(queries_part3):
        col_idx = idx % 2
        row_idx = idx // 2
        c_left = Inches(0.8 + col_idx * 5.95)
        c_top = Inches(1.65 + row_idx * 2.65)
        c_w = Inches(5.75)
        c_h = Inches(2.45)

        add_card(s8, c_left, c_top, c_w, c_h, title, ACCENT_AMBER)

        sql_box = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), c_top + Inches(0.6), c_w - Inches(0.4), Inches(1.15))
        sql_box.fill.solid()
        sql_box.fill.fore_color.rgb = CODE_BG
        sql_box.line.color.rgb = CARD_BORDER
        tf_s = sql_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = Inches(0.08)
        p_s = tf_s.paragraphs[0]
        p_s.text = sql_text
        p_s.font.size = Pt(9.2)
        p_s.font.color.rgb = ACCENT_GREEN
        p_s.font.name = "Consolas"

        d_box = s8.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(1.8), c_w - Inches(0.4), Inches(0.55))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = f"Purpose: {desc}"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 9: PL/SQL STORED PROCEDURES
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "PL/SQL Stored Procedures (2 Marks)", "PROCEDURAL SQL & BUSINESS LOGIC")

    # Procedure 1
    add_card(s9, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.2), "Procedure 1: PROC_SUBMIT_CLAIM", ACCENT_CYAN)
    tb_p1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.5))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True

    p1_lines = [
        ("Parameters:", " IN p_item_id, IN p_claimant_id, IN p_proof, OUT p_new_claim_id, OUT p_result_msg"),
        ("Business Rules Enforced:", ""),
        ("• Verification 1:", " Confirms student is registered in STUDENT table."),
        ("• Verification 2:", " Validates item exists in ITEM table."),
        ("• Verification 3:", " Blocks claim if item is already in RETURNED status."),
        ("• Verification 4:", " Prevents duplicate pending claims by the same student."),
        ("• Action:", " Generates next ID, inserts record into CLAIM with status 'PENDING', and returns transaction status."),
        ("Satisfies:", " FR7 (Submit Claim) & FR10 (Integrity Validation)")
    ]
    for idx, (label, val) in enumerate(p1_lines):
        p = tf_p1.paragraphs[0] if idx == 0 else tf_p1.add_paragraph()
        r1 = p.add_run()
        r1.text = label
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_AMBER if "Satisfies" in label else ACCENT_CYAN
        r1.font.name = "Segoe UI"
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MUTED
        r2.font.name = "Segoe UI"

    # Procedure 2
    add_card(s9, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2), "Procedure 2: PROC_VERIFY_CLAIM", ACCENT_BLUE)
    tb_p2 = s9.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.5))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True

    p2_lines = [
        ("Parameters:", " IN p_claim_id, IN p_admin_id, IN p_decision ('APPROVED'/'REJECTED'), OUT p_result_msg"),
        ("Atomic Operations Enforced:", ""),
        ("• Decision Validation:", " Validates admin authorization and checks claim is PENDING."),
        ("• When APPROVED:", " 1. Updates CLAIM status to 'APPROVED' and sets admin_id."),
        ("  2. Status Propagation:", " Automatically updates parent ITEM status to 'RETURNED'."),
        ("  3. Conflict Resolution:", " Automatically REJECTS all competing pending claims filed for that same item."),
        ("• When REJECTED:", " Sets claim to 'REJECTED' without altering item state."),
        ("Satisfies:", " FR8 (Verify Claims) & FR9 (Automated Status Progression)")
    ]
    for idx, (label, val) in enumerate(p2_lines):
        p = tf_p2.paragraphs[0] if idx == 0 else tf_p2.add_paragraph()
        r1 = p.add_run()
        r1.text = label
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_AMBER if "Satisfies" in label else ACCENT_BLUE
        r1.font.name = "Segoe UI"
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MUTED
        r2.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 10: PL/SQL STORED FUNCTIONS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "PL/SQL Stored Functions (2 Marks)", "ANALYTICAL FUNCTIONS & RETURN VALUES")

    # Function 1
    add_card(s10, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.2), "Function 1: FUNC_CALCULATE_UNCLAIMED_DAYS", ACCENT_GREEN)
    tb_f1 = s10.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.5))
    tf_f1 = tb_f1.text_frame
    tf_f1.word_wrap = True

    f1_lines = [
        ("Signature:", " FUNC_CALCULATE_UNCLAIMED_DAYS(p_item_id NUMBER) RETURN NUMBER"),
        ("Purpose:", " Calculates elapsed aging days an item remains unresolved in the system."),
        ("Calculation Logic:", ""),
        ("• If Status = 'RETURNED':", " Calculates exact elapsed days between date_reported and the approved claim_date."),
        ("• If Status in ('LOST', 'FOUND'):", " Computes ROUND(SYSDATE - date_reported)."),
        ("• Exception Handling:", " Returns -1 if item ID is not found in registry."),
        ("Satisfies:", " FR11 (Calculate days an item is unclaimed)")
    ]
    for idx, (label, val) in enumerate(f1_lines):
        p = tf_f1.paragraphs[0] if idx == 0 else tf_f1.add_paragraph()
        r1 = p.add_run()
        r1.text = label
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_AMBER if "Satisfies" in label else ACCENT_GREEN
        r1.font.name = "Segoe UI"
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MUTED
        r2.font.name = "Segoe UI"

    # Function 2
    add_card(s10, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2), "Function 2: FUNC_GET_STUDENT_ACTIVITY", ACCENT_CYAN)
    tb_f2 = s10.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.5))
    tf_f2 = tb_f2.text_frame
    tf_f2.word_wrap = True

    f2_lines = [
        ("Signature:", " FUNC_GET_STUDENT_ACTIVITY(p_student_id VARCHAR2) RETURN VARCHAR2"),
        ("Purpose:", " Generates an aggregated summary string of a student's system activity."),
        ("Aggregated Metrics:", ""),
        ("• Lost Count:", " SELECT COUNT(*) FROM LOST_REPORT WHERE student_id = ..."),
        ("• Found Count:", " SELECT COUNT(*) FROM FOUND_REPORT WHERE student_id = ..."),
        ("• Claims Count:", " SELECT COUNT(*) FROM CLAIM WHERE claimant_student_id = ..."),
        ("Sample Output:", " 'Arahat Gaikwad [24BYB0182] -> Lost Filed: 1 | Found Filed: 2 | Claims Submitted: 1'"),
        ("Satisfies:", " FR1 & FR13 (Student Activity Analytics)")
    ]
    for idx, (label, val) in enumerate(f2_lines):
        p = tf_f2.paragraphs[0] if idx == 0 else tf_f2.add_paragraph()
        r1 = p.add_run()
        r1.text = label
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_AMBER if "Satisfies" in label else ACCENT_CYAN
        r1.font.name = "Segoe UI"
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MUTED
        r2.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 11: PL/SQL EXPLICIT CURSOR
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "PL/SQL Explicit Cursor Implementation (2 Marks)", "BATCH PROCESSING & MULTI-RECORD AUDIT")

    # Left: Code & Lifecycle Card
    add_card(s11, Inches(0.8), Inches(1.65), Inches(6.8), Inches(5.2), "Explicit Cursor: PROC_FLAG_LONG_UNCLAIMED_ITEMS", ACCENT_CYAN)
    tb_c_code = s11.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(6.4), Inches(4.5))
    tf_cc = tb_c_code.text_frame
    tf_cc.word_wrap = True

    cursor_code = [
        "CURSOR cur_unclaimed_items IS",
        "    SELECT i.item_id, i.item_name, i.status, i.date_reported, l.building",
        "    FROM ITEM i JOIN LOCATION l ON i.location_id = l.location_id",
        "    WHERE i.status IN ('LOST', 'FOUND')",
        "      AND (SYSDATE - i.date_reported) >= p_days_threshold;",
        "",
        "BEGIN",
        "    OPEN cur_unclaimed_items; -- 1. OPEN Cursor",
        "    LOOP",
        "        FETCH cur_unclaimed_items INTO v_item_rec; -- 2. FETCH Row",
        "        EXIT WHEN cur_unclaimed_items%NOTFOUND;    -- 3. Check %NOTFOUND",
        "        v_count := v_count + 1;",
        "        DBMS_OUTPUT.PUT_LINE(v_item_rec.item_id || ' | ' || ...);",
        "    END LOOP;",
        "    CLOSE cur_unclaimed_items; -- 4. CLOSE Cursor",
        "    p_total_flagged := v_count;",
        "END;"
    ]
    for idx, ctext in enumerate(cursor_code):
        p = tf_cc.paragraphs[0] if idx == 0 else tf_cc.add_paragraph()
        p.text = ctext
        p.font.size = Pt(10)
        p.font.color.rgb = ACCENT_GREEN if any(k in ctext for k in ["CURSOR", "OPEN", "FETCH", "EXIT", "CLOSE"]) else TEXT_MUTED
        p.font.name = "Consolas"

    # Right: Rationale & Execution Card
    add_card(s11, Inches(7.8), Inches(1.65), Inches(4.7), Inches(5.2), "Lifecycle & Business Significance", ACCENT_AMBER)
    tb_c_desc = s11.shapes.add_textbox(Inches(8.0), Inches(2.2), Inches(4.3), Inches(4.5))
    tf_cd = tb_c_desc.text_frame
    tf_cd.word_wrap = True

    cursor_features = [
        ("Requirement Satisfied:", " Explicit Cursor for processing multiple records."),
        ("1. DECLARE:", " Defines structured query filtering active items exceeding the aging threshold."),
        ("2. OPEN:", " Allocates memory context area and initializes query result set."),
        ("3. FETCH:", " Advances row pointer sequentially and populates record structure."),
        ("4. %NOTFOUND:", " Evaluates cursor state to terminate loop cleanly."),
        ("5. CLOSE:", " Releases database memory resources."),
        ("", ""),
        ("Application Value (FR12):", " Allows campus security to scan thousands of records in bulk and flag abandoned items for campus auction or disposal.")
    ]
    for idx, (label, val) in enumerate(cursor_features):
        p = tf_cd.paragraphs[0] if idx == 0 else tf_cd.add_paragraph()
        r1 = p.add_run()
        r1.text = label + " "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_AMBER if "Application" in label else ACCENT_CYAN
        r1.font.name = "Segoe UI"
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MUTED
        r2.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 12: PL/SQL DATABASE TRIGGERS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "PL/SQL Database Triggers (2 Marks)", "EVENT-DRIVEN DATABASE AUTOMATION")

    # Trigger 1
    add_card(s12, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.2), "Trigger 1: TRG_PREVENT_CLAIM_ON_RETURNED", ACCENT_AMBER)
    tb_t1 = s12.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.5))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True

    t1_lines = [
        ("Timing & Level:", " BEFORE INSERT ON CLAIM (Row-Level)"),
        ("Business Purpose:", " Prevents fraudulent or duplicate claims on items that have already been returned to their owner."),
        ("Trigger Logic:", ""),
        ("  SELECT status INTO v_status FROM ITEM", ""),
        ("  WHERE item_id = :NEW.item_id;", ""),
        ("  IF v_status = 'RETURNED' THEN", ""),
        ("      RAISE_APPLICATION_ERROR(-20001,", ""),
        ("      'Integrity Violation: Item already RETURNED.');", ""),
        ("  END IF;", ""),
        ("Outcome:", " The INSERT operation is immediately rolled back by the database engine. Zero dirty data."),
        ("Satisfies:", " FR10 (Prevent claims on returned items)")
    ]
    for idx, (label, val) in enumerate(t1_lines):
        p = tf_t1.paragraphs[0] if idx == 0 else tf_t1.add_paragraph()
        if "Timing" in label or "Business" in label or "Outcome" in label or "Satisfies" in label:
            r1 = p.add_run()
            r1.text = label + " "
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = ACCENT_AMBER
            r1.font.name = "Segoe UI"
            r2 = p.add_run()
            r2.text = val
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = TEXT_MUTED
            r2.font.name = "Segoe UI"
        else:
            p.text = label
            p.font.size = Pt(10)
            p.font.color.rgb = ACCENT_GREEN
            p.font.name = "Consolas"

    # Trigger 2
    add_card(s12, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2), "Trigger 2: TRG_AUTO_UPDATE_ITEM_STATUS", ACCENT_GREEN)
    tb_t2 = s12.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.5))
    tf_t2 = tb_t2.text_frame
    tf_t2.word_wrap = True

    t2_lines = [
        ("Timing & Level:", " AFTER UPDATE OF claim_status ON CLAIM (Row-Level)"),
        ("Business Purpose:", " Automatically transitions parent item status to 'RETURNED' upon claim approval without requiring manual double-entry."),
        ("Trigger Logic:", ""),
        ("  IF :NEW.claim_status = 'APPROVED' AND", ""),
        ("     (:OLD.claim_status != 'APPROVED') THEN", ""),
        ("      UPDATE ITEM", ""),
        ("      SET status = 'RETURNED'", ""),
        ("      WHERE item_id = :NEW.item_id;", ""),
        ("  END IF;", ""),
        ("Outcome:", " Synchronizes child and parent entity states atomically."),
        ("Satisfies:", " FR9 (Update item status automatically)")
    ]
    for idx, (label, val) in enumerate(t2_lines):
        p = tf_t2.paragraphs[0] if idx == 0 else tf_t2.add_paragraph()
        if "Timing" in label or "Business" in label or "Outcome" in label or "Satisfies" in label:
            r1 = p.add_run()
            r1.text = label + " "
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = ACCENT_GREEN
            r1.font.name = "Segoe UI"
            r2 = p.add_run()
            r2.text = val
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = TEXT_MUTED
            r2.font.name = "Segoe UI"
        else:
            p.text = label
            p.font.size = Pt(10)
            p.font.color.rgb = ACCENT_GREEN
            p.font.name = "Consolas"

    # =========================================================================
    # SLIDE 13: EXECUTION PROOF & TECHNICAL VALIDATION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Execution Proof & Technical Validation (1 Mark)", "VERIFICATION & TEST RUNS")

    proof_cards = [
        ("PL/SQL Anonymous Block Output",
         "--- Testing Functions ---\nUnclaimed Days for Item 1002 (AirPods): 14 days\nStudent Summary: Arahat Gaikwad [24BYB0182] -> Lost: 1 | Found: 2 | Claims: 1\n\n--- Testing Cursor Batch Processing ---\nITEM ID   ITEM NAME               STATUS   DAYS   LOCATION\n1002      Apple AirPods Pro 2     FOUND    14     SJT\n1004      Blue Hydro Flask        LOST     11     Foodys\n1007      Fastrack Analog Watch   FOUND    7      Sports Complex\nTotal Long-Unclaimed Items Processed: 3",
         ACCENT_CYAN),
        ("Procedure & Trigger 2 Verification",
         "--- Testing PROC_SUBMIT_CLAIM ---\nSUCCESS: Claim #411 submitted successfully in PENDING status.\n\n--- Testing PROC_VERIFY_CLAIM & Trigger 2 ---\nSUCCESS: Claim #411 APPROVED.\n[TRIGGER FIRED: TRG_AUTO_UPDATE_ITEM_STATUS]\nItem #1005 status automatically updated to 'RETURNED'.\nCompeting pending claims for Item #1005 automatically REJECTED.",
         ACCENT_GREEN),
        ("Trigger 1 Integrity Rejection Proof",
         "--- Testing Trigger 1 (Negative Test) ---\nAttempting INSERT into CLAIM for Item #1001 (Already 'RETURNED'):\n\nORA-20001: Integrity Rule Violation: Item #1001 has already been RETURNED to its owner. New claims are disallowed.\nORA-06512: at \"TRG_PREVENT_CLAIM_ON_RETURNED\", line 7\n[RESULT]: Database aborted invalid transaction.",
         ACCENT_AMBER)
    ]

    for idx, (title, out_text, col) in enumerate(proof_cards):
        c_left = Inches(0.8 + idx * 3.95)
        c_top = Inches(1.65)
        c_w = Inches(3.75)
        c_h = Inches(5.2)

        add_card(s13, c_left, c_top, c_w, c_h, title, col)

        tb = s13.shapes.add_textbox(c_left + Inches(0.15), c_top + Inches(0.65), c_w - Inches(0.3), c_h - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = out_text
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.font.name = "Consolas"

    # =========================================================================
    # SLIDE 14: SUMMARY & REVIEW III READINESS
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Summary & Readiness for Review III", "DELIVERABLES CHECKLIST & NEXT STEPS")

    # Left: Review II Completed Deliverables
    add_card(s14, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.2), "Review II Deliverables Completed", ACCENT_GREEN)
    tb_r2 = s14.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.5))
    tf_r2 = tb_r2.text_frame
    tf_r2.word_wrap = True

    comp_pts = [
        "✔ DDL & Relational Schema: 7 Tables in 3NF with PK, FK, CHECK, UNIQUE, NOT NULL & DEFAULT constraints.",
        "✔ Data Population: 10+ records populated per table (70+ total rows) with INSERT/UPDATE/DELETE tests.",
        "✔ SQL Queries: 16 Meaningful queries covering Inner/Left Joins, Group By, Having, Subqueries, Sets & Window ranking.",
        "✔ Stored Procedures: PROC_SUBMIT_CLAIM and PROC_VERIFY_CLAIM for robust transaction processing.",
        "✔ Stored Functions: FUNC_CALCULATE_UNCLAIMED_DAYS and FUNC_GET_STUDENT_ACTIVITY.",
        "✔ Explicit Cursor: PROC_FLAG_LONG_UNCLAIMED_ITEMS with complete Open, Fetch, Loop, and Close lifecycle.",
        "✔ Database Triggers: TRG_PREVENT_CLAIM_ON_RETURNED and TRG_AUTO_UPDATE_ITEM_STATUS."
    ]
    for idx, cpt in enumerate(comp_pts):
        p = tf_r2.paragraphs[0] if idx == 0 else tf_r2.add_paragraph()
        p.text = cpt
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE if idx % 2 == 0 else TEXT_MUTED
        p.font.name = "Segoe UI"

    # Right: Review III Readiness
    add_card(s14, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2), "Review III: Integrated System Demonstration", ACCENT_CYAN)
    tb_r3 = s14.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.5))
    tf_r3 = tb_r3.text_frame
    tf_r3.word_wrap = True

    r3_pts = [
        "1. Integrated Database Application:",
        "   • Interactive Python application connecting via SQLite & Oracle Database (oracledb).",
        "",
        "2. 5 End-to-End Real-World Transactions:",
        "   • User Operation -> SQL/PLSQL -> Database Processing -> Update -> Result flow.",
        "",
        "3. Live Walkthrough & Faculty Evaluation:",
        "   • Walkthrough mode answers all 5 evaluation questions live on screen.",
        "",
        "4. Formal Project Report:",
        "   • 10-section comprehensive technical report matching Section 5 guidelines.",
        "",
        "Thank You! Ready for Questions & Live Demonstration."
    ]
    for idx, rpt in enumerate(r3_pts):
        p = tf_r3.paragraphs[0] if idx == 0 else tf_r3.add_paragraph()
        p.text = rpt
        p.font.size = Pt(11)
        if "1." in rpt or "2." in rpt or "3." in rpt or "4." in rpt:
            p.font.bold = True
            p.font.color.rgb = ACCENT_CYAN
        elif "Thank You" in rpt:
            p.font.bold = True
            p.font.size = Pt(13)
            p.font.color.rgb = ACCENT_AMBER
        else:
            p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

    # Save Presentation
    out_dir = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project"
    out_path = os.path.join(out_dir, "Campus_Lost_and_Found_System_Review2.pptx")
    prs.save(out_path)
    print(f"Presentation successfully saved to: {out_path}")

    # Also save a copy in Downloads root for convenience
    root_path = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_System_Review2.pptx"
    prs.save(root_path)
    print(f"Copy also saved to: {root_path}")

if __name__ == "__main__":
    create_presentation()
