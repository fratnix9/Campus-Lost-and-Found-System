"""
Generate Review 2 PowerPoint Presentation matching Review 1 exact styling:
- Slide dimensions: 18288000 x 10287000 (Widescreen 16:9)
- Background: #1E2A38 (Dark Navy)
- Cards fill: #2B3B4E (Dark Slate)
- Headings: #F2F5F7 (Bright Silver/White)
- Subtitles / Tags: #7FA8C5 (Soft Cyan/Steel Blue)
- Accent highlights: #4B9CD3, #34D399, #FBBF24
- Real embedded Oracle SQL Developer and PowerShell screenshots
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_review2_presentation():
    prs = Presentation()
    prs.slide_width = 18288000   # 20.0 inches (exact match to Review 1)
    prs.slide_height = 10287000  # 11.25 inches
    blank_layout = prs.slide_layouts[6]

    base_dir = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project"
    ss_dir = os.path.join(base_dir, "screenshots")
    docs_dir = os.path.join(base_dir, "docs")

    # Exact Review 1 Color Palette
    BG_COLOR = RGBColor(30, 42, 56)       # #1E2A38 (Exact Review 1 background)
    CARD_BG = RGBColor(43, 59, 78)        # #2B3B4E (Exact Review 1 card fill)
    CARD_BORDER = RGBColor(58, 77, 100)   # #3A4D64 (Subtle Card Outline)
    TEXT_WHITE = RGBColor(242, 245, 247)  # #F2F5F7 (Exact Review 1 title text)
    TEXT_CYAN = RGBColor(127, 168, 197)   # #7FA8C5 (Exact Review 1 tag text)
    TEXT_MUTED = RGBColor(180, 195, 210)  # #B4C3D2 (Light readable body text)
    ACCENT_GREEN = RGBColor(52, 211, 153) # #34D399 (Emerald Green Accent)
    ACCENT_AMBER = RGBColor(251, 191, 36) # #FBBF24 (Amber Accent)
    ACCENT_BLUE = RGBColor(96, 165, 250)  # #60A5FA (Soft Blue Accent)

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, tag_text):
        # Main Title (Top)
        tb_t = slide.shapes.add_textbox(Inches(0.9), Inches(0.5), Inches(18.2), Inches(0.9))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(32)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        # Subtitle / Tag (Below Title)
        tb_tag = slide.shapes.add_textbox(Inches(0.9), Inches(1.4), Inches(18.2), Inches(0.5))
        tf_tag = tb_tag.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = "Segoe UI"
        p_tag.font.size = Pt(13)
        p_tag.font.bold = True
        p_tag.font.color.rgb = TEXT_CYAN

    def add_card(slide, left, top, width, height, title="", title_color=TEXT_CYAN, fill_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.22), width - Inches(0.5), Inches(0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Segoe UI"
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = title_color

        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Matches Review 1 Title Slide)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    # University Badge
    tb_u = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(17.0), Inches(0.5))
    p_u = tb_u.text_frame.paragraphs[0]
    p_u.text = "VELLORE INSTITUTE OF TECHNOLOGY | BCSE302L - DATABASE SYSTEMS"
    p_u.font.name = "Segoe UI"
    p_u.font.size = Pt(14)
    p_u.font.bold = True
    p_u.font.color.rgb = TEXT_CYAN

    # Main Project Title
    tb_title = s1.shapes.add_textbox(Inches(1.5), Inches(2.4), Inches(17.0), Inches(2.5))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_t1 = tf_title.paragraphs[0]
    p_t1.text = "Campus Lost and Found System"
    p_t1.font.name = "Segoe UI"
    p_t1.font.size = Pt(50)
    p_t1.font.bold = True
    p_t1.font.color.rgb = TEXT_WHITE

    p_t2 = tf_title.add_paragraph()
    p_t2.text = "Review II – Database Implementation"
    p_t2.font.name = "Segoe UI"
    p_t2.font.size = Pt(28)
    p_t2.font.bold = True
    p_t2.font.color.rgb = ACCENT_BLUE

    # Student Card
    add_card(s1, Inches(1.5), Inches(5.8), Inches(12.0), Inches(3.2))
    tb_stud = s1.shapes.add_textbox(Inches(1.9), Inches(6.1), Inches(11.2), Inches(2.6))
    tf_stud = tb_stud.text_frame
    tf_stud.word_wrap = True

    stud_info = [
        ("Student Name:", " Arahat Gaikwad"),
        ("Registration Number:", " 24BYB0182"),
        ("Degree & Branch:", " B.Tech Computer Science and Engineering"),
        ("School:", " School of Computer Science Engineering and Information Systems (SCORE)"),
        ("Evaluation Review:", " Review II – Database Implementation (10 Marks)")
    ]
    for idx, (lbl, val) in enumerate(stud_info):
        p = tf_stud.paragraphs[0] if idx == 0 else tf_stud.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = lbl
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = TEXT_CYAN
        r1.font.name = "Segoe UI"
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(14)
        r2.font.color.rgb = TEXT_WHITE
        r2.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 2: REVIEW II AGENDA (Evaluation Criteria Mapping)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "Review II Evaluation Agenda", "DATABASE IMPLEMENTATION CRITERIA (10 MARKS)")

    criteria = [
        ("1. DDL & Constraints", "2 Marks", "Creation of 7 normalized tables (3NF) with PK, FK, CHECK, UNIQUE, NOT NULL, and DEFAULT rules.", TEXT_CYAN),
        ("2. DML & Population", "1 Mark", "Meaningful campus data with 10+ records/table (72+ total rows) and INSERT, UPDATE, DELETE tests.", ACCENT_BLUE),
        ("3. SQL Queries", "2 Marks", "16 comprehensive queries covering multi-table joins, aggregations, subqueries, and window ranking.", ACCENT_GREEN),
        ("4. Procedures & Functions", "2 Marks", "Business operations: PROC_SUBMIT_CLAIM, PROC_VERIFY_CLAIM, and 2 stored analytical functions.", ACCENT_AMBER),
        ("5. Cursor & Triggers", "2 Marks", "Explicit Cursor batch scan for aging items + 2 automated triggers for status progression & security.", TEXT_CYAN),
        ("6. Technical Viva", "1 Mark", "Execution demonstration, schema rationale, atomic transactions, and relational defense.", ACCENT_BLUE)
    ]

    for idx, (title, marks, desc, col) in enumerate(criteria):
        col_idx = idx % 3
        row_idx = idx // 3
        c_left = Inches(0.9 + col_idx * 6.1)
        c_top = Inches(2.2 + row_idx * 4.1)
        c_w = Inches(5.8)
        c_h = Inches(3.7)

        add_card(s2, c_left, c_top, c_w, c_h)
        tb = s2.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(0.3), c_w - Inches(0.6), c_h - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = col

        p_m = tf.add_paragraph()
        p_m.space_before = Pt(4)
        p_m.space_after = Pt(8)
        p_m.text = f"Weightage: {marks}"
        p_m.font.name = "Segoe UI"
        p_m.font.size = Pt(14)
        p_m.font.bold = True
        p_m.font.color.rgb = ACCENT_AMBER

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: RELATIONAL SCHEMA RECAP (3NF)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "Relational Architecture Recap", "7 NORMALIZED TABLES IN THIRD NORMAL FORM (3NF)")

    # Left Card: 7 Entities
    add_card(s3, Inches(0.9), Inches(2.2), Inches(8.8), Inches(8.2), "7 Core Normalized Entities (3NF)", TEXT_CYAN)
    tb_l = s3.shapes.add_textbox(Inches(1.2), Inches(3.0), Inches(8.2), Inches(7.0))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    t_list = [
        ("LOCATION", "location_id (PK), location_name, building"),
        ("STUDENT", "student_id (PK), name, email (UK), phone"),
        ("ADMIN", "admin_id (PK), name, email (UK)"),
        ("ITEM", "item_id (PK), item_name, description, category, date_reported, status, location_id (FK), reported_by_student_id (FK)"),
        ("LOST_REPORT", "lost_report_id (PK), item_id (FK), student_id (FK), date_lost, details"),
        ("FOUND_REPORT", "found_report_id (PK), item_id (FK), student_id (FK), date_found, details"),
        ("CLAIM", "claim_id (PK), item_id (FK), claimant_student_id (FK), claim_date, proof_description, claim_status, admin_id (FK)")
    ]
    for idx, (tname, tcols) in enumerate(t_list):
        p = tf_l.paragraphs[0] if idx == 0 else tf_l.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {tname}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ACCENT_GREEN
        r1.font.name = "Segoe UI"
        r2 = p.add_run()
        r2.text = tcols
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MUTED
        r2.font.name = "Segoe UI"

    # Right Card: Relationships & Normalization Rationale
    add_card(s3, Inches(10.1), Inches(2.2), Inches(9.0), Inches(8.2), "9 Foreign Key Mappings (1 : N)", ACCENT_BLUE)
    tb_r = s3.shapes.add_textbox(Inches(10.4), Inches(3.0), Inches(8.4), Inches(7.0))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    rels = [
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
        "• 1NF: Atomic values; no repeating groups.",
        "• 2NF: No partial key dependencies; non-keys fully dependent on PK.",
        "• 3NF: No transitive dependencies; reports separated from claims to prevent null bloat."
    ]
    for idx, rtext in enumerate(rels):
        p = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        p.space_after = Pt(3)
        p.text = rtext
        p.font.name = "Segoe UI"
        if "Normalization" in rtext:
            p.font.bold = True
            p.font.size = Pt(14)
            p.font.color.rgb = ACCENT_AMBER
        elif rtext.startswith("•"):
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_WHITE
        else:
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: DDL & CONSTRAINTS (Styled like Review 1 Slide 12)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "DDL & Integrity Constraints (2 Marks)", "DATA INTEGRITY RULES & DOMAIN SPECIFICATIONS")

    c_cards = [
        ("Keys & UNIQUE", TEXT_CYAN, [
            ("PRIMARY KEY", "Every table has an immutable ID column uniquely identifying each row (location_id, student_id, item_id, etc.)."),
            ("FOREIGN KEY", "9 links enforce referential integrity with ON DELETE CASCADE enabled on all report and claim child tables."),
            ("UNIQUE", "Student email and admin institutional email cannot be duplicated across records.")
        ]),
        ("NOT NULL & CHECK", ACCENT_BLUE, [
            ("NOT NULL", "Names, emails, item names, categories, statuses, dates, and proof descriptions must always have a valid value."),
            ("CHECK (status)", "Item status is strictly restricted to:\n'LOST', 'FOUND', 'CLAIMED', or 'RETURNED'."),
            ("CHECK (claim_status)", "Claim status is strictly restricted to:\n'PENDING', 'APPROVED', or 'REJECTED'.")
        ]),
        ("DEFAULT Values", ACCENT_AMBER, [
            ("Claim Status", "DEFAULT 'PENDING' for all initial submissions."),
            ("Date Reported", "DEFAULT SYSDATE automatically logs timestamp."),
            ("Claim Date", "DEFAULT SYSDATE automatically logs timestamp."),
            ("Item Status", "DEFAULT 'LOST' upon initial reporting.")
        ])
    ]

    for idx, (ctitle, ccol, citems) in enumerate(c_cards):
        c_left = Inches(0.9 + idx * 6.1)
        c_top = Inches(2.2)
        c_w = Inches(5.8)
        c_h = Inches(8.2)

        add_card(s4, c_left, c_top, c_w, c_h, ctitle, ccol)
        tb = s4.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(1.0), c_w - Inches(0.6), c_h - Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True

        for i_idx, (head, body) in enumerate(citems):
            p = tf.paragraphs[0] if i_idx == 0 else tf.add_paragraph()
            p.space_before = Pt(8)
            p.space_after = Pt(2)
            r1 = p.add_run()
            r1.text = head + "\n"
            r1.font.name = "Segoe UI"
            r1.font.bold = True
            r1.font.size = Pt(14)
            r1.font.color.rgb = TEXT_WHITE

            r2 = p.add_run()
            r2.text = body
            r2.font.name = "Segoe UI"
            r2.font.size = Pt(12)
            r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 5: DML & POPULATION (With Embedded Screenshot 1)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "DML & Data Population (1 Mark)", "10+ RECORDS PER TABLE (72+ TOTAL ROWS)")

    # Left Card: Population Stats
    add_card(s5, Inches(0.9), Inches(2.2), Inches(8.0), Inches(8.2), "Dataset & DML Verification", TEXT_CYAN)
    tb_dml = s5.shapes.add_textbox(Inches(1.2), Inches(3.0), Inches(7.4), Inches(7.0))
    tf_dml = tb_dml.text_frame
    tf_dml.word_wrap = True

    dml_text = [
        "• Minimum Requirement Satisfied: 10+ records populated per table.",
        "• Total Records Populated: 72+ records across 7 tables.",
        "",
        "Table Population Breakdown:",
        "  1. LOCATION (10 rows): SJT 401, TT 214, Library, PRP, Foodys, MB, Hostels",
        "  2. STUDENT (10 rows): Registered students with valid VIT emails",
        "  3. ADMIN (10 rows): Security officers and library staff",
        "  4. ITEM (12 rows): Electronics, ID Cards, Keys, Books, Accessories",
        "  5. LOST_REPORT (10 rows): Detailed missing article filings",
        "  6. FOUND_REPORT (10 rows): Handed-in discovered items",
        "  7. CLAIM (10 rows): Ownership claims (PENDING, APPROVED, REJECTED)",
        "",
        "DML Transaction Verification (FR15):",
        "  ✔ INSERT: Registered student '24BCS9999' and filed lost mouse #1099",
        "  ✔ UPDATE: Updated student phone and claim review notes",
        "  ✔ DELETE: Safely purged duplicate claim #499 and temporary test item"
    ]
    for idx, dtext in enumerate(dml_text):
        p = tf_dml.paragraphs[0] if idx == 0 else tf_dml.add_paragraph()
        p.space_after = Pt(2)
        p.text = dtext
        p.font.name = "Segoe UI"
        if "Table Population" in dtext or "DML Transaction" in dtext:
            p.font.bold = True
            p.font.size = Pt(13)
            p.font.color.rgb = ACCENT_AMBER
        elif dtext.startswith("•"):
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_WHITE
        else:
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MUTED

    # Right: Embedded Screenshot 1
    add_card(s5, Inches(9.3), Inches(2.2), Inches(9.8), Inches(8.2), "Oracle SQL Developer Execution Proof", ACCENT_GREEN)
    ss1_path = os.path.join(ss_dir, "screenshot_1_dml.png")
    if os.path.exists(ss1_path):
        s5.shapes.add_picture(ss1_path, Inches(9.6), Inches(3.2), Inches(9.2))

    # =========================================================================
    # SLIDE 6: SQL QUERIES - JOINS (With Embedded Screenshot 2)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "SQL Queries: Complex Joins (2 Marks)", "MULTI-TABLE INNER & OUTER JOINS")

    # Left: Query Explanation
    add_card(s6, Inches(0.9), Inches(2.2), Inches(8.0), Inches(8.2), "Query 2: 3-Table Inner Join", TEXT_CYAN)
    tb_q2 = s6.shapes.add_textbox(Inches(1.2), Inches(3.0), Inches(7.4), Inches(7.0))
    tf_q2 = tb_q2.text_frame
    tf_q2.word_wrap = True

    q2_text = [
        "SELECT i.item_id, i.item_name, i.category, i.status,",
        "       s.student_id, s.name AS reporter, l.building",
        "FROM ITEM i",
        "JOIN STUDENT s ON i.reported_by_student_id = s.student_id",
        "JOIN LOCATION l ON i.location_id = l.location_id",
        "ORDER BY i.item_id;",
        "",
        "Query Purpose & Relational Rationale:",
        "• Simultaneously links 3 relational tables (ITEM, STUDENT, and LOCATION).",
        "• Solves the scattered record challenge by presenting item details along with the reporting student's identity and campus building origin.",
        "",
        "Additional Joins in System:",
        "• Query 3 (LEFT OUTER JOIN): Preserves all items, highlighting items with zero submitted claims.",
        "• Query 12 (4-Table Join): Audits approved claims linking claimant, item, building, and approving security officer."
    ]
    for idx, qline in enumerate(q2_text):
        p = tf_q2.paragraphs[0] if idx == 0 else tf_q2.add_paragraph()
        p.space_after = Pt(2)
        p.text = qline
        if idx < 6:
            p.font.name = "Consolas"
            p.font.size = Pt(11)
            p.font.color.rgb = ACCENT_GREEN
        elif "Query Purpose" in qline or "Additional Joins" in qline:
            p.font.name = "Segoe UI"
            p.font.bold = True
            p.font.size = Pt(13)
            p.font.color.rgb = ACCENT_AMBER
        else:
            p.font.name = "Segoe UI"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MUTED

    # Right: Embedded Screenshot 2
    add_card(s6, Inches(9.3), Inches(2.2), Inches(9.8), Inches(8.2), "Query Result Grid in Oracle SQL Developer", ACCENT_BLUE)
    ss2_path = os.path.join(ss_dir, "screenshot_2_queries.png")
    if os.path.exists(ss2_path):
        s6.shapes.add_picture(ss2_path, Inches(9.6), Inches(3.3), Inches(9.2))

    # =========================================================================
    # SLIDE 7: SQL QUERIES - AGGREGATION & GROUPING (2 Marks)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "SQL Queries: Aggregations & Grouping (2 Marks)", "GROUP BY, HAVING HOTSPOTS & WINDOW FUNCTIONS")

    agg_cards = [
        ("Query 4: Category Breakdown", TEXT_CYAN,
         "SELECT category, COUNT(item_id) AS total,\n       SUM(CASE WHEN status='LOST' THEN 1 ELSE 0 END) AS lost,\n       SUM(CASE WHEN status='FOUND' THEN 1 ELSE 0 END) AS found\nFROM ITEM GROUP BY category ORDER BY total DESC;",
         "Uses GROUP BY with conditional aggregation to compute total volume, lost count, and found count across each item category in one atomic scan."),
        ("Query 5: Campus Hotspots (HAVING)", ACCENT_BLUE,
         "SELECT l.building, COUNT(i.item_id) AS incidents\nFROM LOCATION l\nJOIN ITEM i ON l.location_id = i.location_id\nGROUP BY l.building\nHAVING COUNT(i.item_id) >= 2;",
         "Uses the HAVING clause to filter aggregated groups, pinpointing high-loss campus buildings (e.g. SJT and Central Library with >= 2 incidents)."),
        ("Query 15: Window Ranking (DENSE_RANK)", ACCENT_GREEN,
         "SELECT category, COUNT(*) AS total_items,\n       DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS cat_rank\nFROM ITEM GROUP BY category;",
         "Uses the DENSE_RANK() analytical window function to rank categories by incident volume, identifying Electronics and Accessories as the most lost items.")
    ]

    for idx, (qtitle, qcol, qsql, qdesc) in enumerate(agg_cards):
        c_left = Inches(0.9 + idx * 6.1)
        c_top = Inches(2.2)
        c_w = Inches(5.8)
        c_h = Inches(8.2)

        add_card(s7, c_left, c_top, c_w, c_h, qtitle, qcol)
        tb = s7.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(0.9), c_w - Inches(0.6), c_h - Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p_sql = tf.paragraphs[0]
        p_sql.text = qsql
        p_sql.font.name = "Consolas"
        p_sql.font.size = Pt(10.5)
        p_sql.font.color.rgb = ACCENT_GREEN

        p_h = tf.add_paragraph()
        p_h.space_before = Pt(14)
        p_h.space_after = Pt(4)
        p_h.text = "Operational Significance:"
        p_h.font.name = "Segoe UI"
        p_h.font.bold = True
        p_h.font.size = Pt(13)
        p_h.font.color.rgb = ACCENT_AMBER

        p_d = tf.add_paragraph()
        p_d.text = qdesc
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: SQL QUERIES - SUBQUERIES & SETS (2 Marks)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "SQL Queries: Subqueries & Set Operators (2 Marks)", "NESTED SUBQUERIES & UNIFIED CAMPUS FEED")

    sub_cards = [
        ("Query 6: Subquery with IN & NOT IN", TEXT_CYAN,
         "SELECT student_id, name, email FROM STUDENT\nWHERE student_id IN (SELECT student_id FROM LOST_REPORT)\n  AND student_id NOT IN (SELECT claimant_student_id FROM CLAIM);",
         "Isolates students who have reported lost items but have never submitted any claim in the system."),
        ("Query 7: Subquery with NOT EXISTS", ACCENT_BLUE,
         "SELECT item_id, item_name, category, status\nFROM ITEM i\nWHERE NOT EXISTS (SELECT 1 FROM CLAIM c WHERE c.item_id = i.item_id);",
         "Identifies items in the central catalog that currently have zero claims submitted against them."),
        ("Query 8: Correlated Subquery", ACCENT_AMBER,
         "SELECT i.item_id, i.item_name, i.status,\n       (SELECT COUNT(*) FROM CLAIM c WHERE c.item_id = i.item_id) AS total_claims\nFROM ITEM i ORDER BY total_claims DESC;",
         "Correlates outer ITEM rows with inner CLAIM counts to dynamically calculate competing claims volume per item."),
        ("Query 9: Set Operator (UNION ALL)", ACCENT_GREEN,
         "SELECT 'LOST', i.item_name, lr.date_lost, s.name FROM LOST_REPORT lr JOIN ITEM i ON ...\nUNION ALL\nSELECT 'FOUND', i.item_name, fr.date_found, s.name FROM FOUND_REPORT fr JOIN ITEM i ON ...\nORDER BY event_date DESC;",
         "Combines lost reports and found reports into a single, unified chronological activity feed for campus security.")
    ]

    for idx, (stitle, scol, ssql, sdesc) in enumerate(sub_cards):
        col_idx = idx % 2
        row_idx = idx // 2
        c_left = Inches(0.9 + col_idx * 9.2)
        c_top = Inches(2.2 + row_idx * 4.1)
        c_w = Inches(8.9)
        c_h = Inches(3.7)

        add_card(s8, c_left, c_top, c_w, c_h, stitle, scol)
        tb = s8.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(0.8), c_w - Inches(0.6), c_h - Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p_sql = tf.paragraphs[0]
        p_sql.text = ssql
        p_sql.font.name = "Consolas"
        p_sql.font.size = Pt(10)
        p_sql.font.color.rgb = ACCENT_GREEN

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(4)
        p_d.text = f"Purpose: {sdesc}"
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 9: PL/SQL STORED PROCEDURES (With Embedded Screenshot 6)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, "PL/SQL Stored Procedures (2 Marks)", "PROCEDURAL BUSINESS LOGIC & CONFLICT RESOLUTION")

    # Left: Explanation of Procedures
    add_card(s9, Inches(0.9), Inches(2.2), Inches(8.0), Inches(8.2), "Business Procedures Implemented", TEXT_CYAN)
    tb_sp = s9.shapes.add_textbox(Inches(1.2), Inches(3.0), Inches(7.4), Inches(7.0))
    tf_sp = tb_sp.text_frame
    tf_sp.word_wrap = True

    sp_text = [
        "1. PROC_SUBMIT_CLAIM (FR7, FR10):",
        "• Parameters: p_item_id, p_claimant_id, p_proof, OUT p_new_claim_id, OUT p_result_msg",
        "• Business Rules Enforced:",
        "   - Validates student registration in STUDENT table.",
        "   - Validates item existence in ITEM table.",
        "   - Blocks claim if item is already in 'RETURNED' status.",
        "   - Prevents duplicate pending claims by the same student.",
        "   - Inserts new claim in 'PENDING' status and returns ID.",
        "",
        "2. PROC_VERIFY_CLAIM (FR8, FR9):",
        "• Parameters: p_claim_id, p_admin_id, p_decision ('APPROVED'/'REJECTED'), OUT p_result_msg",
        "• When APPROVED:",
        "   - Updates CLAIM status to 'APPROVED' and sets admin_id.",
        "   - Updates parent ITEM status to 'RETURNED'.",
        "   - Conflict Resolution: Automatically REJECTS all competing pending claims filed for that same item."
    ]
    for idx, st in enumerate(sp_text):
        p = tf_sp.paragraphs[0] if idx == 0 else tf_sp.add_paragraph()
        p.space_after = Pt(2)
        p.text = st
        p.font.name = "Segoe UI"
        if st.startswith("1.") or st.startswith("2."):
            p.font.bold = True
            p.font.size = Pt(13)
            p.font.color.rgb = ACCENT_AMBER
        elif "When APPROVED" in st or "Business Rules" in st:
            p.font.bold = True
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_WHITE
        else:
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MUTED

    # Right: Embedded Screenshot 6
    add_card(s9, Inches(9.3), Inches(2.2), Inches(9.8), Inches(8.2), "Execution Proof: PROC_SUBMIT_CLAIM", ACCENT_GREEN)
    ss6_path = os.path.join(ss_dir, "screenshot_6_demo3_claim.png")
    if os.path.exists(ss6_path):
        s9.shapes.add_picture(ss6_path, Inches(9.6), Inches(3.3), Inches(9.2))

    # =========================================================================
    # SLIDE 10: PL/SQL STORED FUNCTIONS (2 Marks)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, "PL/SQL Stored Functions (2 Marks)", "AGING CALCULATIONS & STUDENT PROFILE ANALYTICS")

    f_cards = [
        ("Function 1: FUNC_CALCULATE_UNCLAIMED_DAYS", TEXT_CYAN,
         "CREATE OR REPLACE FUNCTION FUNC_CALCULATE_UNCLAIMED_DAYS (p_item_id NUMBER)\nRETURN NUMBER AS\n    v_date DATE; v_status VARCHAR2(20); v_days NUMBER;\nBEGIN\n    SELECT date_reported, status INTO v_date, v_status FROM ITEM WHERE item_id = p_item_id;\n    IF v_status = 'RETURNED' THEN\n        SELECT MIN(claim_date) INTO v_claim_date FROM CLAIM WHERE item_id = p_item_id AND claim_status = 'APPROVED';\n        v_days := ROUND(v_claim_date - v_date, 1);\n    ELSE\n        v_days := ROUND(SYSDATE - v_date, 1);\n    END IF;\n    RETURN GREATEST(v_days, 0);\nEND;",
         "Satisfies FR11: Computes the exact number of days an item has been sitting unresolved in the system using date arithmetic. Returns 0 if claimed same-day, and handles exceptions safely."),
        ("Function 2: FUNC_GET_STUDENT_ACTIVITY", ACCENT_BLUE,
         "CREATE OR REPLACE FUNCTION FUNC_GET_STUDENT_ACTIVITY (p_student_id VARCHAR2)\nRETURN VARCHAR2 AS\n    v_lost NUMBER := 0; v_found NUMBER := 0; v_claims NUMBER := 0; v_name VARCHAR2(100);\nBEGIN\n    SELECT name INTO v_name FROM STUDENT WHERE student_id = p_student_id;\n    SELECT COUNT(*) INTO v_lost FROM LOST_REPORT WHERE student_id = p_student_id;\n    SELECT COUNT(*) INTO v_found FROM FOUND_REPORT WHERE student_id = p_student_id;\n    SELECT COUNT(*) INTO v_claims FROM CLAIM WHERE claimant_student_id = p_student_id;\n    RETURN v_name || ' [' || p_student_id || '] -> Lost: ' || v_lost || ' | Found: ' || v_found || ' | Claims: ' || v_claims;\nEND;",
         "Satisfies FR1 & FR13: Generates a dynamic, consolidated text summary of a student's system engagement across all report and claim tables in one call.")
    ]

    for idx, (ftitle, fcol, fsql, fdesc) in enumerate(f_cards):
        c_left = Inches(0.9 + idx * 9.2)
        c_top = Inches(2.2)
        c_w = Inches(8.9)
        c_h = Inches(8.2)

        add_card(s10, c_left, c_top, c_w, c_h, ftitle, fcol)
        tb = s10.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(0.9), c_w - Inches(0.6), c_h - Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p_sql = tf.paragraphs[0]
        p_sql.text = fsql
        p_sql.font.name = "Consolas"
        p_sql.font.size = Pt(10)
        p_sql.font.color.rgb = ACCENT_GREEN

        p_h = tf.add_paragraph()
        p_h.space_before = Pt(14)
        p_h.space_after = Pt(4)
        p_h.text = "Operational Purpose:"
        p_h.font.name = "Segoe UI"
        p_h.font.bold = True
        p_h.font.size = Pt(13)
        p_h.font.color.rgb = ACCENT_AMBER

        p_d = tf.add_paragraph()
        p_d.text = fdesc
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 11: PL/SQL EXPLICIT CURSOR (With Embedded Screenshot 9)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, "PL/SQL Explicit Cursor (2 Marks)", "BATCH MULTI-RECORD AUDIT (FR12)")

    # Left: Explanation of Cursor
    add_card(s11, Inches(0.9), Inches(2.2), Inches(8.0), Inches(8.2), "Explicit Cursor Architecture", TEXT_CYAN)
    tb_cur = s11.shapes.add_textbox(Inches(1.2), Inches(3.0), Inches(7.4), Inches(7.0))
    tf_cur = tb_cur.text_frame
    tf_cur.word_wrap = True

    cur_text = [
        "Procedure: PROC_FLAG_LONG_UNCLAIMED_ITEMS",
        "",
        "Explicit Cursor Lifecycle:",
        "1. DECLARE:",
        "   CURSOR cur_unclaimed_items IS",
        "     SELECT item_id, item_name, status, date_reported, building",
        "     FROM ITEM i JOIN LOCATION l ON i.location_id = l.location_id",
        "     WHERE i.status IN ('LOST', 'FOUND')",
        "       AND (SYSDATE - i.date_reported) >= p_days_threshold;",
        "",
        "2. OPEN: Allocates cursor context area in PGA memory.",
        "3. FETCH: Advances row pointer into v_item_rec record structure.",
        "4. %NOTFOUND: Checks termination condition to exit loop cleanly.",
        "5. CLOSE: Releases memory context area back to database engine.",
        "",
        "Administrative Purpose (FR12):",
        "Allows campus security to scan thousands of records in bulk, computing days unresolved and printing an automated batch audit report for disposal or auction."
    ]
    for idx, ct in enumerate(cur_text):
        p = tf_cur.paragraphs[0] if idx == 0 else tf_cur.add_paragraph()
        p.space_after = Pt(2)
        p.text = ct
        p.font.name = "Segoe UI"
        if "Procedure:" in ct or "Administrative Purpose" in ct or "Explicit Cursor Lifecycle" in ct:
            p.font.bold = True
            p.font.size = Pt(13)
            p.font.color.rgb = ACCENT_AMBER
        elif "CURSOR cur" in ct or "SELECT item_id" in ct or "FROM ITEM" in ct or "WHERE i.status" in ct:
            p.font.name = "Consolas"
            p.font.size = Pt(10)
            p.font.color.rgb = ACCENT_GREEN
        else:
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MUTED

    # Right: Embedded Screenshot 9
    add_card(s11, Inches(9.3), Inches(2.2), Inches(9.8), Inches(8.2), "Execution Proof: Cursor Batch Output", ACCENT_GREEN)
    ss9_path = os.path.join(ss_dir, "screenshot_9_demo6_cursor.png")
    if os.path.exists(ss9_path):
        s11.shapes.add_picture(ss9_path, Inches(9.6), Inches(3.2), Inches(9.2))

    # =========================================================================
    # SLIDE 12: DATABASE TRIGGERS (With Embedded Screenshots 7 & 8)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, "PL/SQL Database Triggers (2 Marks)", "EVENT-DRIVEN DATABASE AUTOMATION & INTEGRITY")

    # Left: Trigger 1 (Negative Test)
    add_card(s12, Inches(0.9), Inches(2.2), Inches(8.9), Inches(8.2), "Trigger 1: TRG_PREVENT_CLAIM_ON_RETURNED", ACCENT_AMBER)
    tb_t1 = s12.shapes.add_textbox(Inches(1.2), Inches(3.0), Inches(8.3), Inches(2.8))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    t1_info = [
        "• Timing: BEFORE INSERT ON CLAIM (Row-Level)",
        "• Logic: Checks if ITEM.status = 'RETURNED'. If yes, raises ORA-20001.",
        "• Result: Immediately aborts fraudulent claims on returned items."
    ]
    for idx, t1t in enumerate(t1_info):
        p = tf_t1.paragraphs[0] if idx == 0 else tf_t1.add_paragraph()
        p.text = t1t
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_WHITE if idx == 0 else TEXT_MUTED

    ss8_path = os.path.join(ss_dir, "screenshot_8_demo5_error.png")
    if os.path.exists(ss8_path):
        s12.shapes.add_picture(ss8_path, Inches(1.2), Inches(4.7), Inches(8.3))

    # Right: Trigger 2 (Status Propagation)
    add_card(s12, Inches(10.2), Inches(2.2), Inches(8.9), Inches(8.2), "Trigger 2: TRG_AUTO_UPDATE_ITEM_STATUS", ACCENT_GREEN)
    tb_t2 = s12.shapes.add_textbox(Inches(10.5), Inches(3.0), Inches(8.3), Inches(2.8))
    tf_t2 = tb_t2.text_frame
    tf_t2.word_wrap = True
    t2_info = [
        "• Timing: AFTER UPDATE OF claim_status ON CLAIM (Row-Level)",
        "• Logic: When :NEW.claim_status = 'APPROVED', updates ITEM.status to 'RETURNED'.",
        "• Result: Synchronizes child claim and parent item state atomically."
    ]
    for idx, t2t in enumerate(t2_info):
        p = tf_t2.paragraphs[0] if idx == 0 else tf_t2.add_paragraph()
        p.text = t2t
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_WHITE if idx == 0 else TEXT_MUTED

    ss7_path = os.path.join(ss_dir, "screenshot_7_demo4_verify.png")
    if os.path.exists(ss7_path):
        s12.shapes.add_picture(ss7_path, Inches(10.5), Inches(4.7), Inches(8.3))

    # =========================================================================
    # SLIDE 13: INTEGRATED SYSTEM & CONNECTIVITY (With Embedded Screenshot 3)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_header(s13, "Integrated System Demonstration", "INTERACTIVE APPLICATION & DATABASE CONNECTIVITY")

    # Left: Explanation
    add_card(s13, Inches(0.9), Inches(2.2), Inches(8.0), Inches(8.2), "3-Tier System Architecture", TEXT_CYAN)
    tb_conn = s13.shapes.add_textbox(Inches(1.2), Inches(3.0), Inches(7.4), Inches(7.0))
    tf_conn = tb_conn.text_frame
    tf_conn.word_wrap = True

    conn_text = [
        "Integrated System Features:",
        "",
        "1. Multi-Tier Architecture:",
        "• Presentation Layer: Interactive menu-driven console with dedicated student and admin portals.",
        "• Data Access Layer (database.py): Unified abstraction layer managing transactions, commits, and error handling.",
        "• Database Engine: Compatible with Oracle Database 19c/21c via python-oracledb and embedded relational engine.",
        "",
        "2. Complete Transaction Cycle Demonstrated:",
        "User Operation -> SQL/PLSQL -> Database Processing -> Update -> Result",
        "",
        "3. Real-Time Operations:",
        "• Option 1 & 2: Report Lost & Found Items",
        "• Option 4: Submit Claim with Proof (PROC_SUBMIT_CLAIM)",
        "• Option 6: Adjudicate Claims Queue (PROC_VERIFY_CLAIM)",
        "• Option 7: Bulk Cursor Audit (PROC_FLAG_LONG_UNCLAIMED_ITEMS)",
        "• Option 8: Run all 16 SQL Queries live"
    ]
    for idx, ct in enumerate(conn_text):
        p = tf_conn.paragraphs[0] if idx == 0 else tf_conn.add_paragraph()
        p.space_after = Pt(2)
        p.text = ct
        p.font.name = "Segoe UI"
        if "Integrated System Features:" in ct or "1." in ct or "2." in ct or "3." in ct:
            p.font.bold = True
            p.font.size = Pt(13)
            p.font.color.rgb = ACCENT_AMBER
        elif "User Operation" in ct:
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = ACCENT_GREEN
        else:
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MUTED

    # Right: Embedded Screenshot 3
    add_card(s13, Inches(9.3), Inches(2.2), Inches(9.8), Inches(8.2), "Python Terminal Session (Windows PowerShell)", ACCENT_BLUE)
    ss3_path = os.path.join(ss_dir, "screenshot_3_python_app.png")
    if os.path.exists(ss3_path):
        s13.shapes.add_picture(ss3_path, Inches(9.6), Inches(3.1), Inches(9.2))

    # =========================================================================
    # SLIDE 14: SUMMARY & REVIEW III READINESS (Matches Review 1 Slide 14)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)
    add_header(s14, "Summary & Review III Readiness", "DELIVERABLES CHECKLIST & NEXT STEPS")

    # Left Card: Review II Completed
    add_card(s14, Inches(0.9), Inches(2.2), Inches(8.8), Inches(8.2), "Review II Deliverables Completed (10/10)", ACCENT_GREEN)
    tb_s14l = s14.shapes.add_textbox(Inches(1.2), Inches(3.0), Inches(8.2), Inches(7.0))
    tf_s14l = tb_s14l.text_frame
    tf_s14l.word_wrap = True

    sum_text = [
        "✔ DDL & Relational Schema: 7 Normalized Tables in 3NF with PK, FK, CHECK, UNIQUE, NOT NULL & DEFAULT.",
        "✔ Data Population: 10+ records populated per table (72+ total rows) with INSERT/UPDATE/DELETE tests.",
        "✔ SQL Queries: 16 Meaningful queries covering Inner/Left Joins, Group By, Having, Subqueries, Sets & Window ranking.",
        "✔ Stored Procedures: PROC_SUBMIT_CLAIM and PROC_VERIFY_CLAIM for robust transaction processing.",
        "✔ Stored Functions: FUNC_CALCULATE_UNCLAIMED_DAYS and FUNC_GET_STUDENT_ACTIVITY.",
        "✔ Explicit Cursor: PROC_FLAG_LONG_UNCLAIMED_ITEMS with complete Open, Fetch, Loop, and Close lifecycle.",
        "✔ Database Triggers: TRG_PREVENT_CLAIM_ON_RETURNED and TRG_AUTO_UPDATE_ITEM_STATUS."
    ]
    for idx, st in enumerate(sum_text):
        p = tf_s14l.paragraphs[0] if idx == 0 else tf_s14l.add_paragraph()
        p.space_after = Pt(8)
        p.text = st
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE if idx % 2 == 0 else TEXT_MUTED

    # Right Card: Ready for Review III
    add_card(s14, Inches(10.1), Inches(2.2), Inches(9.0), Inches(8.2), "Review III Transition & Q&A", TEXT_CYAN)
    tb_s14r = s14.shapes.add_textbox(Inches(10.4), Inches(3.0), Inches(8.4), Inches(7.0))
    tf_s14r = tb_s14r.text_frame
    tf_s14r.word_wrap = True

    r3_text = [
        "Review III: Integrated System & Final Demonstration",
        "",
        "1. End-to-End Real-World Transactions:",
        "   Demonstration of 6 complete transactions following the official flow:",
        "   User Operation -> SQL/PLSQL -> Database Processing -> Update -> Result",
        "",
        "2. Live Interactive Demonstration:",
        "   Automated walkthrough mode (Option 9 in app.py) answering all 5 evaluation questions live on screen.",
        "",
        "3. Complete Technical Documentation:",
        "   Word reports generated for both Review II and Review III.",
        "",
        "Thank You!",
        "Arahat Gaikwad (24BYB0182) | SCORE, VIT Vellore",
        "Ready for Questions and Live Demonstration."
    ]
    for idx, rt in enumerate(r3_text):
        p = tf_s14r.paragraphs[0] if idx == 0 else tf_s14r.add_paragraph()
        p.space_after = Pt(2)
        p.text = rt
        p.font.name = "Segoe UI"
        if "Review III:" in rt or "1." in rt or "2." in rt or "3." in rt:
            p.font.bold = True
            p.font.size = Pt(13)
            p.font.color.rgb = ACCENT_AMBER
        elif "Thank You!" in rt:
            p.space_before = Pt(12)
            p.font.bold = True
            p.font.size = Pt(22)
            p.font.color.rgb = ACCENT_BLUE
        elif "Arahat Gaikwad" in rt:
            p.font.bold = True
            p.font.size = Pt(14)
            p.font.color.rgb = TEXT_WHITE
        else:
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MUTED

    # Save Presentation in both locations
    out_dir = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project"
    out_path = os.path.join(out_dir, "Campus_Lost_and_Found_System_Review2.pptx")
    prs.save(out_path)
    print(f"Presentation saved to: {out_path}")

    root_path = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_System_Review2.pptx"
    prs.save(root_path)
    print(f"Copy saved to: {root_path}")

if __name__ == "__main__":
    build_review2_presentation()
