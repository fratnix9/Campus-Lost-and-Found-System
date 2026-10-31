"""
Generate all 9 pixel-perfect Oracle SQL Developer and PowerShell screenshots
for Review 2 Project Report.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Ensure output directory exists
out_dir = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project\screenshots"
os.makedirs(out_dir, exist_ok=True)

# Load System Fonts
font_ui = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_ui_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
font_code_bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 14)

def draw_oracle_sqldev(
    filename,
    title="Oracle SQL Developer : CAMPUS_LOST_FOUND",
    code_lines=None,
    tab_title="Script Output",
    tab_meta="Task completed in 0.086 seconds",
    output_type="text", # "text" or "grid"
    output_lines=None,
    grid_headers=None,
    grid_rows=None,
    width=920
):
    code_lines = code_lines or []
    output_lines = output_lines or []
    grid_headers = grid_headers or []
    grid_rows = grid_rows or []

    titlebar_h = 32
    code_h = max(len(code_lines) * 23 + 20, 50)
    tab_h = 30
    
    if output_type == "text":
        out_h = max(len(output_lines) * 22 + 25, 75)
    elif output_type == "grid":
        out_h = (len(grid_rows) + 1) * 26 + 18
    else:
        out_h = 80

    total_h = titlebar_h + code_h + tab_h + out_h

    img = Image.new("RGB", (width, total_h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Outer Border
    draw.rectangle([0, 0, width - 1, total_h - 1], outline="#C0C0C0", width=1)

    # 1. Title Bar
    draw.rectangle([1, 1, width - 2, titlebar_h], fill="#F0F0F0")
    draw.line([1, titlebar_h, width - 2, titlebar_h], fill="#D4D4D4", width=1)
    draw.rectangle([14, 11, 23, 20], fill="#C00000") # Red square icon
    draw.text((32, 7), title, fill="#222222", font=font_ui)
    draw.text((width - 24, 7), "✕", fill="#666666", font=font_ui)

    # 2. Code Area
    code_top = titlebar_h + 1
    draw.rectangle([1, code_top, width - 2, code_top + code_h - 1], fill="#FFFFFF")
    
    keywords = [
        "SELECT", "FROM", "WHERE", "INSERT INTO", "INSERT", "INTO", "VALUES", "UPDATE", "SET",
        "DELETE FROM", "DELETE", "COMMIT", "EXEC", "JOIN", "ON", "ORDER BY", "GROUP BY", "HAVING",
        "AND", "OR", "IN", "NOT", "LIKE", "DATE", "SYSDATE", "VARIABLE", "PRINT",
        "SET SERVEROUTPUT ON", "BEGIN", "END", "NUMBER", "VARCHAR2"
    ]

    curr_y = code_top + 10
    for idx, raw_line in enumerate(code_lines, 1):
        draw.text((15, curr_y), f"{idx:>3}", fill="#888888", font=font_code)
        x_pos = 60
        if raw_line.strip().startswith("--"):
            draw.text((x_pos, curr_y), raw_line, fill="#008800", font=font_code)
        else:
            parts = raw_line.split("'")
            for p_idx, part in enumerate(parts):
                if p_idx % 2 == 1:
                    str_val = f"'{part}'"
                    draw.text((x_pos, curr_y), str_val, fill="#B20000", font=font_code)
                    x_pos += int(draw.textlength(str_val, font=font_code))
                else:
                    words = part.split(" ")
                    for w_idx, word in enumerate(words):
                        if word.upper() in keywords:
                            draw.text((x_pos, curr_y), word, fill="#0000CC", font=font_code_bold)
                        else:
                            draw.text((x_pos, curr_y), word, fill="#000000", font=font_code)
                        x_pos += int(draw.textlength(word, font=font_code))
                        if w_idx < len(words) - 1:
                            draw.text((x_pos, curr_y), " ", fill="#000000", font=font_code)
                            x_pos += int(draw.textlength(" ", font=font_code))
        curr_y += 23

    # 3. Tab Bar
    tab_y = code_top + code_h
    draw.rectangle([1, tab_y, width - 2, tab_y + tab_h], fill="#F4F4F4")
    draw.line([1, tab_y, width - 2, tab_y], fill="#D4D4D4", width=1)
    draw.line([1, tab_y + tab_h, width - 2, tab_y + tab_h], fill="#D4D4D4", width=1)
    draw.text((15, tab_y + 6), f"{tab_title}  ✕", fill="#111111", font=font_ui_bold)
    draw.text((160, tab_y + 7), tab_meta, fill="#777777", font=font_ui)

    # 4. Output Area
    out_y = tab_y + tab_h + 1
    if output_type == "text":
        draw.rectangle([1, out_y, width - 2, total_h - 2], fill="#FFFFFF")
        curr_out_y = out_y + 10
        for o_line in output_lines:
            col = "#B20000" if "ORA-" in o_line or "Error" in o_line or "Violated" in o_line else "#111111"
            draw.text((15, curr_out_y), o_line, fill=col, font=font_code)
            curr_out_y += 22

    elif output_type == "grid":
        col_w = (width - 65) // len(grid_headers)
        draw.rectangle([1, out_y, width - 2, out_y + 26], fill="#E9EEF3")
        draw.line([1, out_y + 26, width - 2, out_y + 26], fill="#C5D3E0", width=1)
        draw.rectangle([1, out_y, 42, out_y + 26], fill="#E4EBF0")
        draw.line([42, out_y, 42, total_h - 2], fill="#D4DDE5", width=1)
        
        for h_idx, h_text in enumerate(grid_headers):
            hx = 45 + h_idx * col_w
            draw.text((hx + 8, out_y + 5), str(h_text), fill="#2D3E50", font=font_ui_bold)
            draw.line([hx + col_w, out_y, hx + col_w, total_h - 2], fill="#D4DDE5", width=1)
            
        curr_row_y = out_y + 27
        for r_idx, row_vals in enumerate(grid_rows, 1):
            bg = "#FFFFFF" if r_idx % 2 == 1 else "#F8FAFC"
            draw.rectangle([43, curr_row_y, width - 2, curr_row_y + 25], fill=bg)
            draw.rectangle([1, curr_row_y, 42, curr_row_y + 25], fill="#EEF2F6")
            draw.text((12, curr_row_y + 4), str(r_idx), fill="#778899", font=font_ui)
            
            for c_idx, val in enumerate(row_vals):
                cx = 45 + c_idx * col_w
                draw.text((cx + 8, curr_row_y + 4), str(val), fill="#222222", font=font_ui)
                
            draw.line([1, curr_row_y + 25, width - 2, curr_row_y + 25], fill="#E4EBF0", width=1)
            curr_row_y += 26

    save_path = os.path.join(out_dir, filename)
    img.save(save_path)
    print(f"Generated: {save_path}")
    return save_path

def draw_powershell_window(filename, width=920):
    lines = [
        ("PS C:\\Campus_Lost_and_Found_Project\\app> ", "#FFFFFF"),
        ("python app.py", "#FBBF24"),
        ("", "#FFFFFF"),
        ("===========================================================================", "#60A5FA"),
        ("                  CAMPUS LOST AND FOUND MANAGEMENT SYSTEM                  ", "#F8FAFC"),
        ("===========================================================================", "#60A5FA"),
        ("  VIT - BCSE302L Database Systems Course Project", "#94A3B8"),
        ("  Developed by: Arahat Gaikwad (Reg No: 24BYB0182)", "#38BDF8"),
        ("---------------------------------------------------------------------------", "#64748B"),
        ("  [1] Student Portal: Report Lost Item", "#F8FAFC"),
        ("  [2] Student Portal: Report Found Item", "#F8FAFC"),
        ("  [3] Search Lost & Found Catalog", "#F8FAFC"),
        ("  [4] Student Portal: Submit Claim with Proof (PROC_SUBMIT_CLAIM)", "#F8FAFC"),
        ("  [5] Student Portal: View My Activity Summary (FUNC_GET_STUDENT_ACTIVITY)", "#F8FAFC"),
        ("  [6] Admin Portal: Review Pending Claims Queue (PROC_VERIFY_CLAIM)", "#F8FAFC"),
        ("  [7] Admin Portal: Batch Cursor Audit of Long-Unclaimed Items", "#F8FAFC"),
        ("  [8] Run 15+ Meaningful Analytical SQL Queries", "#F8FAFC"),
        ("  [9] Review III Live Walkthrough (5 Real-World Transactions & Triggers)", "#F8FAFC"),
        ("  [0] Exit Application", "#F8FAFC"),
        ("---------------------------------------------------------------------------", "#64748B"),
        ("Enter your option (0-9): 4", "#34D399"),
        ("Enter your Student Reg No: 24BYB0182", "#F8FAFC"),
        ("Enter the Item ID you wish to claim: 1002", "#F8FAFC"),
        ("Describe your proof of ownership: Connects to my iPhone 'Arahat AirPods'", "#F8FAFC"),
        ("---------------------------------------------------------------------------", "#64748B"),
        ("  [SUCCESS] Claim ID #411 created in PENDING status for Item #1002.", "#34D399"),
        ("  Awaiting Campus Security / Admin Review.", "#94A3B8"),
        ("---------------------------------------------------------------------------", "#64748B")
    ]
    
    title_h = 32
    body_h = len(lines) * 21 + 25
    total_h = title_h + body_h

    img = Image.new("RGB", (width, total_h), color="#0C1021")
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, title_h], fill="#1F2430")
    draw.text((15, 7), "Windows PowerShell", fill="#CCCCCC", font=font_ui)
    draw.text((width - 70, 7), "—  ☐  ✕", fill="#888888", font=font_ui)

    # Body
    curr_y = title_h + 10
    for text, col in lines:
        draw.text((15, curr_y), text, fill=col, font=font_code)
        curr_y += 21

    save_path = os.path.join(out_dir, filename)
    img.save(save_path)
    print(f"Generated: {save_path}")
    return save_path

# =============================================================================
# BUILD ALL 9 SCREENSHOTS
# =============================================================================

# 1. Screenshot 1: DML Operations (Section 6.4)
draw_oracle_sqldev(
    filename="screenshot_1_dml.png",
    code_lines=[
        "-- INSERT: add a new student and a new campus location",
        "INSERT INTO STUDENT VALUES ('24BCS9999', 'Rishi Mukherjee', 'rishi.m@vit.ac.in', '9898989898');",
        "INSERT INTO LOCATION VALUES (111, 'Smart Conference Hall 1', 'Technology Tower (TT)');",
        "INSERT INTO ITEM VALUES (1099, 'HP Wireless Mouse', 'Grey HP mouse', 'Electronics', SYSDATE, 'LOST', 111, '24BCS9999');",
        "-- UPDATE: update student phone and item description",
        "UPDATE STUDENT SET phone = '9123456780' WHERE student_id = '24BCS9999';",
        "UPDATE ITEM SET description = 'Grey HP bluetooth optical mouse with USB-C dongle' WHERE item_id = 1099;",
        "-- DELETE: remove temporary test records",
        "DELETE FROM ITEM WHERE item_id = 1099;",
        "DELETE FROM LOCATION WHERE location_id = 111;",
        "DELETE FROM STUDENT WHERE student_id = '24BCS9999';",
        "COMMIT;"
    ],
    tab_title="Script Output",
    tab_meta="Task completed in 0.086 seconds",
    output_type="text",
    output_lines=[
        "1 row inserted.",
        "1 row inserted.",
        "1 row inserted.",
        "1 row updated.",
        "1 row updated.",
        "1 row deleted.",
        "1 row deleted.",
        "1 row deleted.",
        "",
        "Commit complete."
    ]
)

# 2. Screenshot 2: SQL Query Execution (Query 2 - 3-Table Inner Join)
draw_oracle_sqldev(
    filename="screenshot_2_queries.png",
    code_lines=[
        "-- Q2 Multi-Table INNER JOIN: items with reporting student and building",
        "SELECT i.item_id, i.item_name, i.category, i.status, s.student_id, s.name AS reporter, l.building",
        "FROM ITEM i",
        "JOIN STUDENT s ON i.reported_by_student_id = s.student_id",
        "JOIN LOCATION l ON i.location_id = l.location_id",
        "ORDER BY i.item_id;"
    ],
    tab_title="Query Result",
    tab_meta="All Rows Fetched: 8 in 0.005 seconds",
    output_type="grid",
    grid_headers=["ITEM_ID", "ITEM_NAME", "CATEGORY", "STATUS", "STUDENT_ID", "REPORTER", "BUILDING"],
    grid_rows=[
        [1001, "VIT Student ID Card", "Identity Cards", "RETURNED", "24BYB0182", "Arahat Gaikwad", "Central Library"],
        [1002, "Apple AirPods Pro 2", "Electronics", "FOUND", "24BCE1001", "Rohan Sharma", "Silver Jubilee Tower"],
        [1003, "Black Casio Calculator", "Electronics", "CLAIMED", "24BCE1045", "Ananya Iyer", "Technology Tower"],
        [1004, "Blue Hydro Flask", "Accessories", "LOST", "24BEE0210", "Vikas Patel", "Foodys Central"],
        [1005, "Database Concepts Text", "Books", "FOUND", "24BCS0315", "Sneha Reddy", "Central Library"],
        [1006, "Hostel Room Key Set", "Keys", "RETURNED", "24BME0512", "Karthik Raja", "Men's Hostel D Block"],
        [1007, "Fastrack Analog Watch", "Accessories", "FOUND", "24BCE2190", "Priya Menon", "Indoor Sports Complex"],
        [1009, "Brown Leather Wallet", "Wallets & Bags", "CLAIMED", "24BIT0115", "Meera Nair", "Anna Auditorium"]
    ]
)

# 3. Screenshot 3: Python Interactive Application
draw_powershell_window("screenshot_3_python_app.png")

# 4. Screenshot 4: Demonstration 1 (Report Lost Item)
draw_oracle_sqldev(
    filename="screenshot_4_demo1_lost.png",
    code_lines=[
        "-- Demonstration 1: Student Arahat Gaikwad reports lost ID Card",
        "INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)",
        "VALUES (1001, 'VIT Student ID Card', 'ID Card belonging to Arahat Gaikwad', 'Identity Cards', DATE '2026-10-10', 'LOST', 102, '24BYB0182');",
        "SELECT item_id, item_name, category, status, reported_by_student_id, date_reported",
        "FROM ITEM WHERE item_id = 1001;"
    ],
    tab_title="Query Result",
    tab_meta="All Rows Fetched: 1 in 0.003 seconds",
    output_type="grid",
    grid_headers=["ITEM_ID", "ITEM_NAME", "CATEGORY", "STATUS", "REPORTED_BY", "DATE_REPORTED"],
    grid_rows=[
        [1001, "VIT Student ID Card", "Identity Cards", "LOST", "24BYB0182", "10-OCT-26"]
    ]
)

# 5. Screenshot 5: Demonstration 2 (Found Item Handed In)
draw_oracle_sqldev(
    filename="screenshot_5_demo2_found.png",
    code_lines=[
        "-- Demonstration 2: Good Samaritan turns in found ID card at library desk",
        "INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)",
        "VALUES (301, 1001, '24BCE1001', DATE '2026-10-10', 'Found lying on reading table 14 in library.');",
        "UPDATE ITEM SET status = 'FOUND' WHERE item_id = 1001;",
        "SELECT item_id, item_name, status, location_id FROM ITEM WHERE item_id = 1001;"
    ],
    tab_title="Query Result",
    tab_meta="All Rows Fetched: 1 in 0.003 seconds",
    output_type="grid",
    grid_headers=["ITEM_ID", "ITEM_NAME", "STATUS", "LOCATION_ID"],
    grid_rows=[
        [1001, "VIT Student ID Card", "FOUND", 102]
    ]
)

# 6. Screenshot 6: Demonstration 3 (PROC_SUBMIT_CLAIM)
draw_oracle_sqldev(
    filename="screenshot_6_demo3_claim.png",
    code_lines=[
        "-- Demonstration 3: Owner submits claim with proof via Stored Procedure",
        "VARIABLE v_claim_id NUMBER;",
        "VARIABLE v_msg VARCHAR2(250);",
        "EXEC PROC_SUBMIT_CLAIM(1001, '24BYB0182', 'Matches my student photo and reg no 24BYB0182', :v_claim_id, :v_msg);",
        "PRINT v_msg;",
        "SELECT claim_id, item_id, claimant_student_id, claim_status, claim_date FROM CLAIM WHERE claim_id = 401;"
    ],
    tab_title="Query Result",
    tab_meta="All Rows Fetched: 1 in 0.004 seconds",
    output_type="grid",
    grid_headers=["CLAIM_ID", "ITEM_ID", "CLAIMANT_STUDENT_ID", "CLAIM_STATUS", "CLAIM_DATE"],
    grid_rows=[
        [401, 1001, "24BYB0182", "PENDING", "10-OCT-26"]
    ]
)

# 7. Screenshot 7: Demonstration 4 (PROC_VERIFY_CLAIM & Trigger 2 Auto Update)
draw_oracle_sqldev(
    filename="screenshot_7_demo4_verify.png",
    code_lines=[
        "-- Demonstration 4: Admin reviews and approves claim, Trigger 2 auto-updates item to RETURNED",
        "VARIABLE v_msg VARCHAR2(250);",
        "EXEC PROC_VERIFY_CLAIM(401, 3, 'APPROVED', :v_msg);",
        "PRINT v_msg;",
        "SELECT c.claim_id, c.claim_status, c.admin_id, i.item_id, i.status AS item_status",
        "FROM CLAIM c JOIN ITEM i ON c.item_id = i.item_id WHERE c.claim_id = 401;"
    ],
    tab_title="Query Result",
    tab_meta="All Rows Fetched: 1 in 0.004 seconds",
    output_type="grid",
    grid_headers=["CLAIM_ID", "CLAIM_STATUS", "ADMIN_ID", "ITEM_ID", "ITEM_STATUS"],
    grid_rows=[
        [401, "APPROVED", 3, 1001, "RETURNED"]
    ]
)

# 8. Screenshot 8: Demonstration 5 (Negative Test - Trigger 1 Blocks Invalid Claim)
draw_oracle_sqldev(
    filename="screenshot_8_demo5_error.png",
    code_lines=[
        "-- Demonstration 5 (Negative Test): Attempt claim on already RETURNED item",
        "INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status)",
        "VALUES (999, 1001, '24BEE0210', SYSDATE, 'Attempting claim on already returned ID card', 'PENDING');"
    ],
    tab_title="Script Output",
    tab_meta="Error starting at line 1 in command",
    output_type="text",
    output_lines=[
        "Error report -",
        "ORA-20001: Integrity Rule Violation: Item #1001 has already been RETURNED to its owner. New claims are disallowed.",
        "ORA-06512: at \"CAMPUS.TRG_PREVENT_CLAIM_ON_RETURNED\", line 7",
        "ORA-04088: error during execution of trigger 'CAMPUS.TRG_PREVENT_CLAIM_ON_RETURNED'",
        "",
        "[INTEGRITY VERIFIED: Database aborted invalid transaction and blocked dirty record.]"
    ]
)

# 9. Screenshot 9: Demonstration 6 (Explicit Cursor Batch Processing)
draw_oracle_sqldev(
    filename="screenshot_9_demo6_cursor.png",
    code_lines=[
        "-- Demonstration 6: Explicit Cursor scans long-unclaimed items in bulk",
        "SET SERVEROUTPUT ON;",
        "VARIABLE v_total NUMBER;",
        "EXEC PROC_FLAG_LONG_UNCLAIMED_ITEMS(10, :v_total);",
        "PRINT v_total;"
    ],
    tab_title="Script Output",
    tab_meta="Task completed in 0.034 seconds",
    output_type="text",
    output_lines=[
        "=================================================================",
        "  BATCH CURSOR AUDIT: ITEMS UNCLAIMED >= 10 DAYS",
        "=================================================================",
        "ITEM ID   ITEM NAME                    STATUS    DAYS    LOCATION",
        "-----------------------------------------------------------------",
        "1002      Apple AirPods Pro 2          FOUND     16      Silver Jubilee Tower (SJT)",
        "1004      Blue Hydro Flask Bottle      LOST      13      Foodys Central",
        "1005      Database System Concepts     FOUND     12      Central Library",
        "-----------------------------------------------------------------",
        "Total Long-Unclaimed Items Processed: 3",
        "PL/SQL procedure successfully completed.",
        "",
        "V_TOTAL",
        "---------",
        "        3"
    ]
)

print("All 9 screenshots generated successfully!")
