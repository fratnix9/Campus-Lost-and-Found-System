"""
Test rendering an Oracle SQL Developer screenshot with Pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont

def draw_oracle_window(
    width=900,
    title="Oracle SQL Developer : CAMPUS_LOST_FOUND",
    code_lines=None,
    tab_title="Script Output",
    tab_meta="Task completed in 0.068 seconds",
    output_type="text", # "text" or "grid"
    output_lines=None,
    grid_headers=None,
    grid_rows=None,
    out_path="test_sqldev.png"
):
    code_lines = code_lines or []
    output_lines = output_lines or []

    # Fonts
    font_ui = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    font_ui_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
    font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
    font_code_bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 14)

    # Calculate heights
    titlebar_h = 32
    code_h = max(len(code_lines) * 24 + 20, 60)
    tab_h = 30
    
    if output_type == "text":
        out_h = max(len(output_lines) * 22 + 25, 80)
    elif output_type == "grid":
        out_h = (len(grid_rows) + 1) * 26 + 20
    else:
        out_h = 100

    total_h = titlebar_h + code_h + tab_h + out_h

    img = Image.new("RGB", (width, total_h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # 1. Outer Border
    draw.rectangle([0, 0, width - 1, total_h - 1], outline="#C0C0C0", width=1)

    # 2. Title Bar
    draw.rectangle([1, 1, width - 2, titlebar_h], fill="#F0F0F0")
    draw.line([1, titlebar_h, width - 2, titlebar_h], fill="#D4D4D4", width=1)
    # Red square icon
    draw.rectangle([14, 11, 23, 20], fill="#C00000")
    # Title text
    draw.text((32, 7), title, fill="#222222", font=font_ui)
    # Close icon
    draw.text((width - 24, 7), "✕", fill="#666666", font=font_ui)

    # 3. Code Area
    code_top = titlebar_h + 1
    draw.rectangle([1, code_top, width - 2, code_top + code_h - 1], fill="#FFFFFF")
    
    # Syntax highlighter helper
    keywords = ["SELECT", "FROM", "WHERE", "INSERT INTO", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE", "COMMIT", "EXEC", "JOIN", "ON", "ORDER BY", "GROUP BY", "HAVING", "AND", "OR", "IN", "NOT", "LIKE", "DATE", "SYSDATE", "VARIABLE", "PRINT", "SET SERVEROUTPUT ON", "BEGIN", "END"]

    curr_y = code_top + 10
    for idx, raw_line in enumerate(code_lines, 1):
        # Line number
        draw.text((15, curr_y), f"{idx:>3}", fill="#888888", font=font_code)
        
        # Line content
        x_pos = 60
        if raw_line.strip().startswith("--"):
            # Whole line comment
            draw.text((x_pos, curr_y), raw_line, fill="#008800", font=font_code)
        else:
            # Simple token styling
            parts = raw_line.split("'")
            for p_idx, part in enumerate(parts):
                if p_idx % 2 == 1:
                    # String literal
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
        curr_y += 24

    # 4. Tab Bar
    tab_y = code_top + code_h
    draw.rectangle([1, tab_y, width - 2, tab_y + tab_h], fill="#F4F4F4")
    draw.line([1, tab_y, width - 2, tab_y], fill="#D4D4D4", width=1)
    draw.line([1, tab_y + tab_h, width - 2, tab_y + tab_h], fill="#D4D4D4", width=1)
    
    # Active tab label
    draw.text((15, tab_y + 6), f"{tab_title}  ✕", fill="#111111", font=font_ui_bold)
    # Meta
    draw.text((150, tab_y + 7), tab_meta, fill="#777777", font=font_ui)

    # 5. Output Area
    out_y = tab_y + tab_h + 1
    if output_type == "text":
        draw.rectangle([1, out_y, width - 2, total_h - 2], fill="#FFFFFF")
        curr_out_y = out_y + 10
        for o_line in output_lines:
            col = "#B20000" if "ORA-" in o_line or "Error" in o_line else "#111111"
            draw.text((15, curr_out_y), o_line, fill=col, font=font_code)
            curr_out_y += 22

    elif output_type == "grid":
        # Draw tabular grid
        col_w = (width - 70) // len(grid_headers)
        
        # Header row
        draw.rectangle([1, out_y, width - 2, out_y + 26], fill="#E9EEF3")
        draw.line([1, out_y + 26, width - 2, out_y + 26], fill="#C5D3E0", width=1)
        
        # Row num header
        draw.rectangle([1, out_y, 45, out_y + 26], fill="#E4EBF0")
        draw.line([45, out_y, 45, total_h - 2], fill="#D4DDE5", width=1)
        
        # Headers
        for h_idx, h_text in enumerate(grid_headers):
            hx = 50 + h_idx * col_w
            draw.text((hx + 8, out_y + 5), str(h_text), fill="#2D3E50", font=font_ui_bold)
            draw.line([hx + col_w, out_y, hx + col_w, total_h - 2], fill="#D4DDE5", width=1)
            
        # Rows
        curr_row_y = out_y + 27
        for r_idx, row_vals in enumerate(grid_rows, 1):
            bg = "#FFFFFF" if r_idx % 2 == 1 else "#F8FAFC"
            draw.rectangle([46, curr_row_y, width - 2, curr_row_y + 25], fill=bg)
            draw.rectangle([1, curr_row_y, 45, curr_row_y + 25], fill="#EEF2F6")
            
            # Row number
            draw.text((15, curr_row_y + 4), str(r_idx), fill="#778899", font=font_ui)
            
            # Cells
            for c_idx, val in enumerate(row_vals):
                cx = 50 + c_idx * col_w
                draw.text((cx + 8, curr_row_y + 4), str(val), fill="#222222", font=font_ui)
                
            draw.line([1, curr_row_y + 25, width - 2, curr_row_y + 25], fill="#E4EBF0", width=1)
            curr_row_y += 26

    img.save(out_path)
    print(f"Test image saved to: {out_path}")

if __name__ == "__main__":
    draw_oracle_window(
        code_lines=[
            "-- INSERT: add a new customer and account",
            "INSERT INTO STUDENT VALUES ('24BCS9999', 'Rishi Mukherjee', 'rishi@vit.ac.in', '9898989898');",
            "COMMIT;"
        ],
        output_type="text",
        output_lines=["1 row inserted.", "", "Commit complete."],
        out_path="c:/Users/gaikw/Downloads/Campus_Lost_and_Found_Project/test_sqldev.png"
    )
