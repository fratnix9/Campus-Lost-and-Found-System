-- =============================================================================
-- VIT - School of Computer Science Engineering and Information Systems
-- Course: BCSE302L - Database Systems
-- Project Title: Campus Lost and Found Management System
-- Student: Arahat Gaikwad (Reg No: 24BYB0182)
-- Script 02: DML - Realistic Sample Data Population (10+ records per table)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. POPULATE LOCATION (10 Records)
-- -----------------------------------------------------------------------------
INSERT INTO LOCATION (location_id, location_name, building) VALUES (101, 'Room 401 Lab', 'Silver Jubilee Tower (SJT)');
INSERT INTO LOCATION (location_id, location_name, building) VALUES (102, 'Main Reading Hall', 'Central Library');
INSERT INTO LOCATION (location_id, location_name, building) VALUES (103, 'Ground Floor Cafeteria', 'Foodys Central');
INSERT INTO LOCATION (location_id, location_name, building) VALUES (104, 'Main Stage and Seating Area', 'Anna Auditorium');
INSERT INTO LOCATION (location_id, location_name, building) VALUES (105, 'Room 214 Smart Classroom', 'Technology Tower (TT)');
INSERT INTO LOCATION (location_id, location_name, building) VALUES (106, 'Physics Laboratory', 'Periyar EVR Block (PRP)');
INSERT INTO LOCATION (location_id, location_name, building) VALUES (107, 'Badminton Court', 'Indoor Sports Complex');
INSERT INTO LOCATION (location_id, location_name, building) VALUES (108, 'Mess Hall Block D', 'Men''s Hostel D Block');
INSERT INTO LOCATION (location_id, location_name, building) VALUES (109, 'Common Study Lounge', 'Women''s Hostel B Block');
INSERT INTO LOCATION (location_id, location_name, building) VALUES (110, 'Dean Office Reception', 'Main Building (MB)');

-- -----------------------------------------------------------------------------
-- 2. POPULATE STUDENT (10 Records)
-- -----------------------------------------------------------------------------
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BYB0182', 'Arahat Gaikwad', 'arahat.gaikwad2024@vitstudent.ac.in', '9876543210');
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BCE1001', 'Rohan Sharma', 'rohan.sharma2024@vitstudent.ac.in', '9876543211');
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BCE1045', 'Ananya Iyer', 'ananya.iyer2024@vitstudent.ac.in', '9876543212');
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BEE0210', 'Vikas Patel', 'vikas.patel2024@vitstudent.ac.in', '9876543213');
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BCS0315', 'Sneha Reddy', 'sneha.reddy2024@vitstudent.ac.in', '9876543214');
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BME0512', 'Karthik Raja', 'karthik.raja2024@vitstudent.ac.in', '9876543215');
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BCE2190', 'Priya Menon', 'priya.menon2024@vitstudent.ac.in', '9876543216');
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BEC0420', 'Aditya Verma', 'aditya.verma2024@vitstudent.ac.in', '9876543217');
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BIT0115', 'Meera Nair', 'meera.nair2024@vitstudent.ac.in', '9876543218');
INSERT INTO STUDENT (student_id, name, email, phone) VALUES ('24BCE0882', 'Tanmay Sen', 'tanmay.sen2024@vitstudent.ac.in', '9876543219');

-- -----------------------------------------------------------------------------
-- 3. POPULATE ADMIN (10 Records)
-- -----------------------------------------------------------------------------
INSERT INTO ADMIN (admin_id, name, email) VALUES (1, 'Dr. K. Raman', 'k.raman@vit.ac.in');
INSERT INTO ADMIN (admin_id, name, email) VALUES (2, 'Officer Ramesh Nair', 'ramesh.nair@security.vit.ac.in');
INSERT INTO ADMIN (admin_id, name, email) VALUES (3, 'Mrs. S. Vijayalakshmi', 'svijaya@library.vit.ac.in');
INSERT INTO ADMIN (admin_id, name, email) VALUES (4, 'Chief Warden S. Gupta', 'chiefwarden.mh@vit.ac.in');
INSERT INTO ADMIN (admin_id, name, email) VALUES (5, 'Officer Rajesh Singh', 'rajesh.singh@security.vit.ac.in');
INSERT INTO ADMIN (admin_id, name, email) VALUES (6, 'Mrs. Kalpana Das', 'kalpana.das@hostel.vit.ac.in');
INSERT INTO ADMIN (admin_id, name, email) VALUES (7, 'Mr. Arun Kumar', 'arun.kumar@admin.vit.ac.in');
INSERT INTO ADMIN (admin_id, name, email) VALUES (8, 'Security In-Charge Peter', 'peter.security@vit.ac.in');
INSERT INTO ADMIN (admin_id, name, email) VALUES (9, 'Dr. Deepa Chandran', 'deepa.chandran@vit.ac.in');
INSERT INTO ADMIN (admin_id, name, email) VALUES (10, 'Officer Selvam M.', 'selvam.m@security.vit.ac.in');

-- -----------------------------------------------------------------------------
-- 4. POPULATE ITEM (12 Records: covers LOST, FOUND, CLAIMED, RETURNED)
-- -----------------------------------------------------------------------------
INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1001, 'VIT Student ID Card', 'ID Card belonging to Arahat Gaikwad with lanyard', 'Identity Cards', TO_DATE('2026-10-10', 'YYYY-MM-DD'), 'RETURNED', 102, '24BYB0182');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1002, 'Apple AirPods Pro 2', 'White AirPods case with blue silicone cover', 'Electronics', TO_DATE('2026-10-12', 'YYYY-MM-DD'), 'FOUND', 101, '24BCE1001');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1003, 'Black Casio Scientific Calculator', 'Model fx-991EX Classwiz with scratch on back', 'Electronics', TO_DATE('2026-10-14', 'YYYY-MM-DD'), 'CLAIMED', 105, '24BCE1045');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1004, 'Blue Hydro Flask Water Bottle', '32oz wide mouth insulated flask with campus stickers', 'Personal Accessories', TO_DATE('2026-10-15', 'YYYY-MM-DD'), 'LOST', 103, '24BEE0210');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1005, 'Database System Concepts Textbook', 'Silberschatz 7th edition hardcover book', 'Books and Study Material', TO_DATE('2026-10-16', 'YYYY-MM-DD'), 'FOUND', 102, '24BCS0315');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1006, 'Hostel Room Key Set', 'Set of 3 brass keys with metal Marvel keychain', 'Keys', TO_DATE('2026-10-18', 'YYYY-MM-DD'), 'RETURNED', 108, '24BME0512');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1007, 'Fastrack Black Analog Watch', 'Black dial leather strap watch found near court bench', 'Personal Accessories', TO_DATE('2026-10-19', 'YYYY-MM-DD'), 'FOUND', 107, '24BCE2190');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1008, 'Lenovo 65W USB-C Charger', 'Original black ThinkPad laptop charger with adapter', 'Electronics', TO_DATE('2026-10-20', 'YYYY-MM-DD'), 'LOST', 101, '24BEC0420');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1009, 'Brown Leather Wallet', 'Contains driver license and metro card', 'Wallets and Bags', TO_DATE('2026-10-21', 'YYYY-MM-DD'), 'CLAIMED', 104, '24BIT0115');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1010, 'Noise Smartwatch Champagne Gold', 'ColorFit Pro 4 smartwatch with silicone band', 'Electronics', TO_DATE('2026-10-22', 'YYYY-MM-DD'), 'LOST', 106, '24BCE0882');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1011, 'Black Umbrella', 'Compact foldable umbrella with auto-open button', 'Personal Accessories', TO_DATE('2026-10-23', 'YYYY-MM-DD'), 'FOUND', 110, '24BYB0182');

INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1012, 'Spectacles in Red Case', 'Frameless reading glasses inside red hard shell case', 'Personal Accessories', TO_DATE('2026-10-24', 'YYYY-MM-DD'), 'FOUND', 109, '24BCS0315');

-- -----------------------------------------------------------------------------
-- 5. POPULATE LOST_REPORT (10 Records)
-- -----------------------------------------------------------------------------
INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (201, 1001, '24BYB0182', TO_DATE('2026-10-09', 'YYYY-MM-DD'), 'Lost ID card while reading near the reference section in Central Library.');

INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (202, 1003, '24BCE1045', TO_DATE('2026-10-13', 'YYYY-MM-DD'), 'Left scientific calculator on desk row 3 after morning class.');

INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (203, 1004, '24BEE0210', TO_DATE('2026-10-15', 'YYYY-MM-DD'), 'Misplaced blue water bottle near the juice counter at Foodys.');

INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (204, 1006, '24BME0512', TO_DATE('2026-10-17', 'YYYY-MM-DD'), 'Keys slipped out of pocket while having dinner in D block mess.');

INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (205, 1008, '24BEC0420', TO_DATE('2026-10-20', 'YYYY-MM-DD'), 'Forgot Lenovo type-C laptop charger plugged in SJT lab 401.');

INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (206, 1009, '24BIT0115', TO_DATE('2026-10-21', 'YYYY-MM-DD'), 'Wallet dropped in Anna Auditorium auditorium seating row J.');

INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (207, 1010, '24BCE0882', TO_DATE('2026-10-22', 'YYYY-MM-DD'), 'Took off smartwatch before physics experiment, forgot to pick it up.');

INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (208, 1002, '24BCE1001', TO_DATE('2026-10-11', 'YYYY-MM-DD'), 'Misplaced AirPods Pro in computer lab during afternoon session.');

INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (209, 1011, '24BCE2190', TO_DATE('2026-10-22', 'YYYY-MM-DD'), 'Left black umbrella outside Dean office entrance in rain.');

INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (210, 1012, '24BCE1045', TO_DATE('2026-10-23', 'YYYY-MM-DD'), 'Left reading glasses in ladies hostel common room table.');

-- -----------------------------------------------------------------------------
-- 6. POPULATE FOUND_REPORT (10 Records)
-- -----------------------------------------------------------------------------
INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (301, 1001, '24BCE1001', TO_DATE('2026-10-10', 'YYYY-MM-DD'), 'Found student ID card lying on table 14 of library reading hall.');

INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (302, 1002, '24BYB0182', TO_DATE('2026-10-12', 'YYYY-MM-DD'), 'Discovered AirPods case under computer bench 22 in SJT 401.');

INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (303, 1003, '24BCS0315', TO_DATE('2026-10-14', 'YYYY-MM-DD'), 'Handed in calculator found on podium in TT room 214.');

INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (304, 1005, '24BCS0315', TO_DATE('2026-10-16', 'YYYY-MM-DD'), 'Found database textbook on corner desk at Central Library.');

INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (305, 1006, '24BCE1001', TO_DATE('2026-10-18', 'YYYY-MM-DD'), 'Picked up hostel room keys from D-block water cooler.');

INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (306, 1007, '24BCE2190', TO_DATE('2026-10-19', 'YYYY-MM-DD'), 'Found Fastrack wristwatch resting on bleachers at sports complex.');

INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (307, 1009, '24BEE0210', TO_DATE('2026-10-21', 'YYYY-MM-DD'), 'Turned in brown wallet discovered on auditorium chair.');

INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (308, 1011, '24BYB0182', TO_DATE('2026-10-23', 'YYYY-MM-DD'), 'Found umbrella stand outside MB dean reception.');

INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (309, 1012, '24BCS0315', TO_DATE('2026-10-24', 'YYYY-MM-DD'), 'Found eyeglasses in case on study table in B block.');

INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details)
VALUES (310, 1004, '24BME0512', TO_DATE('2026-10-24', 'YYYY-MM-DD'), 'Found insulated water bottle left on outdoor bench near Foodys.');

-- -----------------------------------------------------------------------------
-- 7. POPULATE CLAIM (10 Records: covers PENDING, APPROVED, REJECTED)
-- -----------------------------------------------------------------------------
INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (401, 1001, '24BYB0182', TO_DATE('2026-10-10', 'YYYY-MM-DD'), 'Matches my student photo, name Arahat Gaikwad, and reg no 24BYB0182.', 'APPROVED', 3);

INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (402, 1002, '24BCE1001', TO_DATE('2026-10-13', 'YYYY-MM-DD'), 'Connects to my iPhone named "Rohan''s AirPods" and serial matches box.', 'PENDING', NULL);

INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (403, 1002, '24BEE0210', TO_DATE('2026-10-14', 'YYYY-MM-DD'), 'I lost white airpods in SJT, but cannot provide original serial bill.', 'REJECTED', 2);

INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (404, 1003, '24BCE1045', TO_DATE('2026-10-15', 'YYYY-MM-DD'), 'Has my initials AI carved on the battery slide cover.', 'APPROVED', 1);

INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (405, 1005, '24BCS0315', TO_DATE('2026-10-17', 'YYYY-MM-DD'), 'VIT library barcode stamp on page 50 matching my book issue slip.', 'APPROVED', 3);

INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (406, 1006, '24BME0512', TO_DATE('2026-10-18', 'YYYY-MM-DD'), 'Keys fit Room 314 D Block lock, verified with hostel warden.', 'APPROVED', 4);

INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (407, 1007, '24BCE2190', TO_DATE('2026-10-20', 'YYYY-MM-DD'), 'Warranty card photo on my phone showing serial number.', 'PENDING', NULL);

INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (408, 1009, '24BIT0115', TO_DATE('2026-10-22', 'YYYY-MM-DD'), 'Government driving license inside bears my photo and name Meera Nair.', 'APPROVED', 5);

INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (409, 1011, '24BCE2190', TO_DATE('2026-10-24', 'YYYY-MM-DD'), 'Black umbrella with distinct silver tape mark on handle.', 'PENDING', NULL);

INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
VALUES (410, 1012, '24BCE1045', TO_DATE('2026-10-25', 'YYYY-MM-DD'), 'Spectacle frame prescription matches my optometrist card (-2.5 both eyes).', 'PENDING', NULL);

COMMIT;
