"""
Generate a clean screenshot of the Web Application for the Review 3 Report.
"""

import os
from PIL import Image, ImageDraw, ImageFont

out_dir = r"c:\Users\gaikw\Downloads\Campus_Lost_and_Found_Project\screenshots"
os.makedirs(out_dir, exist_ok=True)

font_ui = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_ui_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 16)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 12)
font_stat_num = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 24)
font_stat_lbl = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)

def draw_web_app_screenshot():
    width = 960
    height = 680
    img = Image.new("RGB", (width, height), color="#0F172A")
    draw = ImageDraw.Draw(img)

    # Browser chrome titlebar
    draw.rectangle([0, 0, width - 1, 38], fill="#1E293B")
    draw.line([0, 38, width, 38], fill="#334155", width=1)
    
    # Window buttons
    draw.ellipse([14, 13, 24, 23], fill="#EF4444")
    draw.ellipse([30, 13, 40, 23], fill="#F59E0B")
    draw.ellipse([46, 13, 56, 23], fill="#10B981")

    # Address bar
    draw.rounded_rectangle([75, 7, width - 120, 31], radius=6, fill="#0F172A", outline="#334155")
    draw.text((95, 11), "🔒 http://localhost:5000  —  Campus Lost & Found System (Review III Portal)", fill="#94A3B8", font=font_ui)

    # Header section
    draw.rectangle([0, 39, width, 95], fill="#1E293B")
    draw.line([0, 95, width, 95], fill="#334155", width=1)
    
    # App icon & Brand
    draw.rounded_rectangle([20, 48, 56, 84], radius=8, fill="#38BDF8")
    draw.text((27, 52), "📦", font=ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 22))
    
    draw.text((68, 48), "Campus Lost & Found Management System", fill="#F8FAFC", font=font_title)
    draw.text((68, 70), "Review III – Integrated Database Application | VIT Vellore (SCORE)", fill="#94A3B8", font=font_stat_lbl)

    # Student badge on right
    draw.rounded_rectangle([width - 320, 52, width - 20, 82], radius=15, fill="#0F172A", outline="#334155")
    draw.ellipse([width - 310, 63, width - 302, 71], fill="#34D399")
    draw.text((width - 295, 59), "Arahat Gaikwad (24BYB0182)", fill="#F8FAFC", font=font_ui_bold)

    # Navigation Tabs
    nav_y = 105
    tabs = [
        ("📊 Catalog & Search", True),
        ("🎓 Student Services", False),
        ("🛡️ Security Admin", False),
        ("⚡ Review III Live Suite", False),
        ("📈 SQL Reports", False)
    ]
    cur_x = 20
    for name, is_active in tabs:
        tw = int(draw.textlength(name, font=font_ui)) + 24
        if is_active:
            draw.rounded_rectangle([cur_x, nav_y, cur_x + tw, nav_y + 30], radius=6, fill="#38BDF8")
            draw.text((cur_x + 12, nav_y + 6), name, fill="#0F172A", font=font_ui_bold)
        else:
            draw.rounded_rectangle([cur_x, nav_y, cur_x + tw, nav_y + 30], radius=6, fill="#1E293B", outline="#334155")
            draw.text((cur_x + 12, nav_y + 6), name, fill="#94A3B8", font=font_ui)
        cur_x += tw + 10

    # 4 Stat Cards
    stat_y = 150
    card_w = 215
    stats = [
        ("TOTAL CATALOG ITEMS", "12", "10 Campus Locations", "#38BDF8"),
        ("ACTIVE LOST ITEMS", "3", "Misplaced by Students", "#FB7185"),
        ("TURNED-IN FOUND ITEMS", "5", "Awaiting Verification", "#2DD4BF"),
        ("PENDING CLAIMS", "4", "Awaiting Admin Review", "#FBBF24")
    ]
    for idx, (title, val, sub, accent) in enumerate(stats):
        cx = 20 + idx * (card_w + 20)
        draw.rounded_rectangle([cx, stat_y, cx + card_w, stat_y + 85], radius=10, fill="#1E293B", outline="#334155")
        draw.rectangle([cx, stat_y, cx + card_w, stat_y + 3], fill=accent)
        draw.text((cx + 14, stat_y + 10), title, fill="#94A3B8", font=font_stat_lbl)
        draw.text((cx + 14, stat_y + 26), val, fill="#F8FAFC", font=font_stat_num)
        draw.text((cx + 14, stat_y + 62), sub, fill="#64748B", font=font_stat_lbl)

    # Main Card: Catalog Table
    cat_y = 250
    draw.rounded_rectangle([20, cat_y, width - 20, height - 25], radius=10, fill="#1E293B", outline="#334155")
    
    # Card Header
    draw.text((36, cat_y + 14), "🔍 Campus Lost & Found Master Catalog (Integrated Database Query)", fill="#F8FAFC", font=font_ui_bold)
    draw.rounded_rectangle([width - 165, cat_y + 12, width - 36, cat_y + 32], radius=10, fill="#0F172A", outline="#334155")
    draw.text((width - 152, cat_y + 15), "● 12 Items Indexed", fill="#38BDF8", font=font_stat_lbl)

    # Search Bar Mockup
    search_y = cat_y + 44
    draw.rounded_rectangle([36, search_y, 450, search_y + 28], radius=6, fill="#0F172A", outline="#334155")
    draw.text((46, search_y + 6), "Search by keyword, building, or category...", fill="#64748B", font=font_ui)
    
    draw.rounded_rectangle([460, search_y, 600, search_y + 28], radius=6, fill="#0F172A", outline="#334155")
    draw.text((470, search_y + 6), "All Categories ▾", fill="#94A3B8", font=font_ui)

    draw.rounded_rectangle([610, search_y, 740, search_y + 28], radius=6, fill="#0F172A", outline="#334155")
    draw.text((620, search_y + 6), "All Statuses ▾", fill="#94A3B8", font=font_ui)

    # Table Header
    th_y = search_y + 40
    draw.rectangle([36, th_y, width - 36, th_y + 28], fill="#0F172A")
    draw.line([36, th_y + 28, width - 36, th_y + 28], fill="#334155", width=1)
    
    cols = [
        ("ITEM ID", 50),
        ("ITEM NAME", 130),
        ("CATEGORY", 350),
        ("STATUS", 510),
        ("CAMPUS LOCATION", 620),
        ("REPORTED BY", 810)
    ]
    for cname, cx in cols:
        draw.text((cx, th_y + 6), cname, fill="#94A3B8", font=font_stat_lbl)

    # Table Rows
    rows = [
        ("1001", "VIT Student ID Card", "Identity Cards", "RETURNED", "#34D399", "Central Library (Reading Hall)", "Arahat Gaikwad (24BYB0182)"),
        ("1002", "Apple AirPods Pro 2", "Electronics", "FOUND", "#38BDF8", "Silver Jubilee Tower (SJT 401)", "Rohan Sharma (24BCE1001)"),
        ("1003", "Casio Scientific Calculator", "Electronics", "CLAIMED", "#FBBF24", "Technology Tower (TT 214)", "Ananya Iyer (24BCE1045)"),
        ("1004", "Blue Hydro Flask Bottle", "Personal Accessories", "LOST", "#FB7185", "Foodys Central Cafeteria", "Vikas Patel (24BEE0210)"),
        ("1005", "Database Systems Concepts", "Books & Study Material", "FOUND", "#38BDF8", "Central Library Reference Desk", "Sneha Reddy (24BCS0315)"),
        ("1006", "Hostel Room Key Set (3 keys)", "Keys", "RETURNED", "#34D399", "Men's Hostel D Block", "Karthik Raja (24BME0512)"),
        ("1007", "Fastrack Black Analog Watch", "Personal Accessories", "FOUND", "#38BDF8", "Indoor Sports Complex", "Priya Menon (24BCE2190)"),
        ("1008", "Lenovo 65W Type-C Charger", "Electronics", "LOST", "#FB7185", "Silver Jubilee Tower (SJT 401)", "Aditya Verma (24BEC0420)")
    ]

    r_y = th_y + 32
    for r in rows:
        draw.line([36, r_y + 24, width - 36, r_y + 24], fill="#233246", width=1)
        draw.text((cols[0][1], r_y + 4), f"#{r[0]}", fill="#F8FAFC", font=font_code)
        draw.text((cols[1][1], r_y + 4), r[1], fill="#F8FAFC", font=font_ui)
        draw.text((cols[2][1], r_y + 4), r[2], fill="#94A3B8", font=font_ui)
        
        # Status Pill
        stat_text = r[3]
        accent = r[4]
        draw.rounded_rectangle([cols[3][1], r_y + 2, cols[3][1] + 75, r_y + 20], radius=8, fill="#0F172A", outline=accent)
        draw.text((cols[3][1] + 10, r_y + 4), stat_text, fill=accent, font=font_stat_lbl)

        draw.text((cols[4][1], r_y + 4), r[5], fill="#CBD5E1", font=font_ui)
        draw.text((cols[5][1], r_y + 4), r[6], fill="#94A3B8", font=font_ui)

        r_y += 30

    save_path = os.path.join(out_dir, "screenshot_10_web_portal.png")
    img.save(save_path)
    print("Web App Screenshot saved to:", save_path)

if __name__ == "__main__":
    draw_web_app_screenshot()
