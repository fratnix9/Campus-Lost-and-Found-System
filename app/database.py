"""
Campus Lost and Found Management System
Database Adapter Layer: Supports SQLite (built-in, zero-config) and Oracle Database (via oracledb)
"""

import os
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_type="sqlite", oracle_config=None):
        self.db_type = db_type
        self.oracle_config = oracle_config
        self.conn = None
        self.connect()

    def connect(self):
        if self.db_type == "oracle":
            try:
                import oracledb
                cfg = self.oracle_config or {}
                self.conn = oracledb.connect(
                    user=cfg.get("user", "c##lostfound"),
                    password=cfg.get("password", "password"),
                    dsn=f"{cfg.get('host', 'localhost')}:{cfg.get('port', 1521)}/{cfg.get('service_name', 'XEPDB1')}"
                )
                print("[INFO] Connected successfully to Oracle Database.")
            except Exception as e:
                print(f"[WARN] Failed to connect to Oracle DB: {e}")
                print("[INFO] Falling back to high-fidelity Local SQLite engine.")
                self.db_type = "sqlite"
                self._connect_sqlite()
        else:
            self._connect_sqlite()

    def _connect_sqlite(self):
        db_file = os.path.join(os.path.dirname(__file__), "campus_lost_found.db")
        is_new = not os.path.exists(db_file)
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")
        if is_new:
            self._init_sqlite_schema()
            self._populate_sqlite_data()
            self._init_sqlite_triggers()

    def _init_sqlite_schema(self):
        cursor = self.conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS LOCATION (
            location_id INTEGER PRIMARY KEY,
            location_name TEXT NOT NULL,
            building TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS STUDENT (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ADMIN (
            admin_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ITEM (
            item_id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            date_reported DATE DEFAULT (DATE('now')),
            status TEXT DEFAULT 'LOST' CHECK (status IN ('LOST', 'FOUND', 'CLAIMED', 'RETURNED')),
            location_id INTEGER NOT NULL REFERENCES LOCATION(location_id),
            reported_by_student_id TEXT NOT NULL REFERENCES STUDENT(student_id)
        );

        CREATE TABLE IF NOT EXISTS LOST_REPORT (
            lost_report_id INTEGER PRIMARY KEY,
            item_id INTEGER NOT NULL REFERENCES ITEM(item_id) ON DELETE CASCADE,
            student_id TEXT NOT NULL REFERENCES STUDENT(student_id),
            date_lost DATE DEFAULT (DATE('now')),
            details TEXT
        );

        CREATE TABLE IF NOT EXISTS FOUND_REPORT (
            found_report_id INTEGER PRIMARY KEY,
            item_id INTEGER NOT NULL REFERENCES ITEM(item_id) ON DELETE CASCADE,
            student_id TEXT NOT NULL REFERENCES STUDENT(student_id),
            date_found DATE DEFAULT (DATE('now')),
            details TEXT
        );

        CREATE TABLE IF NOT EXISTS CLAIM (
            claim_id INTEGER PRIMARY KEY,
            item_id INTEGER NOT NULL REFERENCES ITEM(item_id) ON DELETE CASCADE,
            claimant_student_id TEXT NOT NULL REFERENCES STUDENT(student_id),
            claim_date DATE DEFAULT (DATE('now')),
            proof_description TEXT NOT NULL,
            claim_status TEXT DEFAULT 'PENDING' CHECK (claim_status IN ('PENDING', 'APPROVED', 'REJECTED')),
            admin_id INTEGER REFERENCES ADMIN(admin_id)
        );
        """)
        self.conn.commit()

    def _init_sqlite_triggers(self):
        cursor = self.conn.cursor()
        cursor.executescript("""
        -- Trigger 1: TRG_PREVENT_CLAIM_ON_RETURNED
        CREATE TRIGGER IF NOT EXISTS trg_prevent_claim_on_returned
        BEFORE INSERT ON CLAIM
        FOR EACH ROW
        WHEN (SELECT status FROM ITEM WHERE item_id = NEW.item_id) = 'RETURNED'
        BEGIN
            SELECT RAISE(ABORT, 'Integrity Rule Violation: Item has already been RETURNED to its owner. New claims are disallowed.');
        END;

        -- Trigger 2: TRG_AUTO_UPDATE_ITEM_STATUS
        CREATE TRIGGER IF NOT EXISTS trg_auto_update_item_status
        AFTER UPDATE OF claim_status ON CLAIM
        FOR EACH ROW
        WHEN NEW.claim_status = 'APPROVED'
        BEGIN
            UPDATE ITEM SET status = 'RETURNED' WHERE item_id = NEW.item_id;
        END;
        """)
        self.conn.commit()

    def _populate_sqlite_data(self):
        cursor = self.conn.cursor()
        # Check if already populated
        cursor.execute("SELECT COUNT(*) FROM LOCATION")
        if cursor.fetchone()[0] > 0:
            return

        # 1. Locations
        locations = [
            (101, 'Room 401 Lab', 'Silver Jubilee Tower (SJT)'),
            (102, 'Main Reading Hall', 'Central Library'),
            (103, 'Ground Floor Cafeteria', 'Foodys Central'),
            (104, 'Main Stage & Seating Area', 'Anna Auditorium'),
            (105, 'Room 214 Smart Classroom', 'Technology Tower (TT)'),
            (106, 'Physics Laboratory', 'Periyar EVR Block (PRP)'),
            (107, 'Badminton Court', 'Indoor Sports Complex'),
            (108, 'Mess Hall Block D', "Men's Hostel D Block"),
            (109, 'Common Study Lounge', "Women's Hostel B Block"),
            (110, 'Dean Office Reception', 'Main Building (MB)')
        ]
        cursor.executemany("INSERT INTO LOCATION VALUES (?, ?, ?)", locations)

        # 2. Students
        students = [
            ('24BYB0182', 'Arahat Gaikwad', 'arahat.gaikwad2024@vitstudent.ac.in', '9876543210'),
            ('24BCE1001', 'Rohan Sharma', 'rohan.sharma2024@vitstudent.ac.in', '9876543211'),
            ('24BCE1045', 'Ananya Iyer', 'ananya.iyer2024@vitstudent.ac.in', '9876543212'),
            ('24BEE0210', 'Vikas Patel', 'vikas.patel2024@vitstudent.ac.in', '9876543213'),
            ('24BCS0315', 'Sneha Reddy', 'sneha.reddy2024@vitstudent.ac.in', '9876543214'),
            ('24BME0512', 'Karthik Raja', 'karthik.raja2024@vitstudent.ac.in', '9876543215'),
            ('24BCE2190', 'Priya Menon', 'priya.menon2024@vitstudent.ac.in', '9876543216'),
            ('24BEC0420', 'Aditya Verma', 'aditya.verma2024@vitstudent.ac.in', '9876543217'),
            ('24BIT0115', 'Meera Nair', 'meera.nair2024@vitstudent.ac.in', '9876543218'),
            ('24BCE0882', 'Tanmay Sen', 'tanmay.sen2024@vitstudent.ac.in', '9876543219')
        ]
        cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", students)

        # 3. Admins
        admins = [
            (1, 'Dr. K. Raman', 'k.raman@vit.ac.in'),
            (2, 'Officer Ramesh Nair', 'ramesh.nair@security.vit.ac.in'),
            (3, 'Mrs. S. Vijayalakshmi', 'svijaya@library.vit.ac.in'),
            (4, 'Chief Warden S. Gupta', 'chiefwarden.mh@vit.ac.in'),
            (5, 'Officer Rajesh Singh', 'rajesh.singh@security.vit.ac.in'),
            (6, 'Mrs. Kalpana Das', 'kalpana.das@hostel.vit.ac.in'),
            (7, 'Mr. Arun Kumar', 'arun.kumar@admin.vit.ac.in'),
            (8, 'Security In-Charge Peter', 'peter.security@vit.ac.in'),
            (9, 'Dr. Deepa Chandran', 'deepa.chandran@vit.ac.in'),
            (10, 'Officer Selvam M.', 'selvam.m@security.vit.ac.in')
        ]
        cursor.executemany("INSERT INTO ADMIN VALUES (?, ?, ?)", admins)

        # 4. Items
        items = [
            (1001, 'VIT Student ID Card', 'ID Card belonging to Arahat Gaikwad with lanyard', 'Identity Cards', '2026-10-10', 'RETURNED', 102, '24BYB0182'),
            (1002, 'Apple AirPods Pro 2', 'White AirPods case with blue silicone cover', 'Electronics', '2026-10-12', 'FOUND', 101, '24BCE1001'),
            (1003, 'Black Casio Scientific Calculator', 'Model fx-991EX Classwiz with scratch on back', 'Electronics', '2026-10-14', 'CLAIMED', 105, '24BCE1045'),
            (1004, 'Blue Hydro Flask Water Bottle', '32oz wide mouth insulated flask with campus stickers', 'Personal Accessories', '2026-10-15', 'LOST', 103, '24BEE0210'),
            (1005, 'Database System Concepts Textbook', 'Silberschatz 7th edition hardcover book', 'Books & Study Material', '2026-10-16', 'FOUND', 102, '24BCS0315'),
            (1006, 'Hostel Room Key Set', 'Set of 3 brass keys with metal Marvel keychain', 'Keys', '2026-10-18', 'RETURNED', 108, '24BME0512'),
            (1007, 'Fastrack Black Analog Watch', 'Black dial leather strap watch found near court bench', 'Personal Accessories', '2026-10-19', 'FOUND', 107, '24BCE2190'),
            (1008, 'Lenovo 65W USB-C Charger', 'Original black ThinkPad laptop charger with adapter', 'Electronics', '2026-10-20', 'LOST', 101, '24BEC0420'),
            (1009, 'Brown Leather Wallet', 'Contains driver license and metro card', 'Wallets & Bags', '2026-10-21', 'CLAIMED', 104, '24BIT0115'),
            (1010, 'Noise Smartwatch Champagne Gold', 'ColorFit Pro 4 smartwatch with silicone band', 'Electronics', '2026-10-22', 'LOST', 106, '24BCE0882'),
            (1011, 'Black Umbrella', 'Compact foldable umbrella with auto-open button', 'Personal Accessories', '2026-10-23', 'FOUND', 110, '24BYB0182'),
            (1012, 'Spectacles in Red Case', 'Frameless reading glasses inside red hard shell case', 'Personal Accessories', '2026-10-24', 'FOUND', 109, '24BCS0315')
        ]
        cursor.executemany("INSERT INTO ITEM VALUES (?, ?, ?, ?, ?, ?, ?, ?)", items)

        # 5. Lost Reports
        lost_reports = [
            (201, 1001, '24BYB0182', '2026-10-09', 'Lost ID card while reading near the reference section in Central Library.'),
            (202, 1003, '24BCE1045', '2026-10-13', 'Left scientific calculator on desk row 3 after morning class.'),
            (203, 1004, '24BEE0210', '2026-10-15', 'Misplaced blue water bottle near the juice counter at Foodys.'),
            (204, 1006, '24BME0512', '2026-10-17', 'Keys slipped out of pocket while having dinner in D block mess.'),
            (205, 1008, '24BEC0420', '2026-10-20', 'Forgot Lenovo type-C laptop charger plugged in SJT lab 401.'),
            (206, 1009, '24BIT0115', '2026-10-21', 'Wallet dropped in Anna Auditorium auditorium seating row J.'),
            (207, 1010, '24BCE0882', '2026-10-22', 'Took off smartwatch before physics experiment, forgot to pick it up.'),
            (208, 1002, '24BCE1001', '2026-10-11', 'Misplaced AirPods Pro in computer lab during afternoon session.'),
            (209, 1011, '24BCE2190', '2026-10-22', 'Left black umbrella outside Dean office entrance in rain.'),
            (210, 1012, '24BCE1045', '2026-10-23', 'Left reading glasses in ladies hostel common room table.')
        ]
        cursor.executemany("INSERT INTO LOST_REPORT VALUES (?, ?, ?, ?, ?)", lost_reports)

        # 6. Found Reports
        found_reports = [
            (301, 1001, '24BCE1001', '2026-10-10', 'Found student ID card lying on table 14 of library reading hall.'),
            (302, 1002, '24BYB0182', '2026-10-12', 'Discovered AirPods case under computer bench 22 in SJT 401.'),
            (303, 1003, '24BCS0315', '2026-10-14', 'Handed in calculator found on podium in TT room 214.'),
            (304, 1005, '24BCS0315', '2026-10-16', 'Found database textbook on corner desk at Central Library.'),
            (305, 1006, '24BCE1001', '2026-10-18', 'Picked up hostel room keys from D-block water cooler.'),
            (306, 1007, '24BCE2190', '2026-10-19', 'Found Fastrack wristwatch resting on bleachers at sports complex.'),
            (307, 1009, '24BEE0210', '2026-10-21', 'Turned in brown wallet discovered on auditorium chair.'),
            (308, 1011, '24BYB0182', '2026-10-23', 'Found umbrella stand outside MB dean reception.'),
            (309, 1012, '24BCS0315', '2026-10-24', 'Found eyeglasses in case on study table in B block.'),
            (310, 1004, '24BME0512', '2026-10-24', 'Found insulated water bottle left on outdoor bench near Foodys.')
        ]
        cursor.executemany("INSERT INTO FOUND_REPORT VALUES (?, ?, ?, ?, ?)", found_reports)

        # 7. Claims
        claims = [
            (401, 1001, '24BYB0182', '2026-10-10', 'Matches my student photo, name Arahat Gaikwad, and reg no 24BYB0182.', 'APPROVED', 3),
            (402, 1002, '24BCE1001', '2026-10-13', "Connects to my iPhone named 'Rohan's AirPods' and serial matches box.", 'PENDING', None),
            (403, 1002, '24BEE0210', '2026-10-14', 'I lost white airpods in SJT, but cannot provide original serial bill.', 'REJECTED', 2),
            (404, 1003, '24BCE1045', '2026-10-15', 'Has my initials AI carved on the battery slide cover.', 'APPROVED', 1),
            (405, 1005, '24BCS0315', '2026-10-17', 'VIT library barcode stamp on page 50 matching my book issue slip.', 'APPROVED', 3),
            (406, 1006, '24BME0512', '2026-10-18', 'Keys fit Room 314 D Block lock, verified with hostel warden.', 'APPROVED', 4),
            (407, 1007, '24BCE2190', '2026-10-20', 'Warranty card photo on my phone showing serial number.', 'PENDING', None),
            (408, 1009, '24BIT0115', '2026-10-22', 'Government driving license inside bears my photo and name Meera Nair.', 'APPROVED', 5),
            (409, 1011, '24BCE2190', '2026-10-24', 'Black umbrella with distinct silver tape mark on handle.', 'PENDING', None),
            (410, 1012, '24BCE1045', '2026-10-25', 'Spectacle frame prescription matches my optometrist card (-2.5 both eyes).', 'PENDING', None)
        ]
        cursor.executemany("INSERT INTO CLAIM VALUES (?, ?, ?, ?, ?, ?, ?)", claims)
        self.conn.commit()

    def execute_query(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params or ())
        return cursor.fetchall()

    def execute_dml(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params or ())
        self.conn.commit()
        return cursor.rowcount

    def close(self):
        if self.conn:
            self.conn.close()
