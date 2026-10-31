-- =============================================================================
-- VIT - School of Computer Science Engineering and Information Systems
-- Course: BCSE302L - Database Systems
-- Project Title: Campus Lost and Found Management System
-- Student: Arahat Gaikwad (Reg No: 24BYB0182)
-- Script 05: Demonstration of DML Operations (INSERT, UPDATE, DELETE)
-- Satisfies: FR15 and Evaluation Criteria for DML and Data Population
-- =============================================================================

SET LINESIZE 160;
SET PAGESIZE 50;

PROMPT =========================================================================
PROMPT PART 1: DEMONSTRATION OF INSERT OPERATIONS
PROMPT =========================================================================

-- 1. Insert a new student
PROMPT [1.1] Registering a new Student...
INSERT INTO STUDENT (student_id, name, email, phone)
VALUES ('24BCS9999', 'Rishi Mukherjee', 'rishi.mukherjee2024@vitstudent.ac.in', '9898989898');

-- 2. Insert a new location
PROMPT [1.2] Adding a new Campus Location...
INSERT INTO LOCATION (location_id, location_name, building)
VALUES (111, 'Smart Conference Hall 1', 'Technology Tower (TT)');

-- 3. Insert a newly reported item
PROMPT [1.3] Filing a newly reported Lost Item...
INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id)
VALUES (1099, 'HP Wireless Mouse', 'Grey HP bluetooth optical mouse with rechargeable battery', 'Electronics', SYSDATE, 'LOST', 111, '24BCS9999');

-- 4. Insert corresponding lost report
PROMPT [1.4] Inserting detailed Lost Incident Report...
INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details)
VALUES (299, 1099, '24BCS9999', SYSDATE, 'Left mouse on conference table during afternoon club meeting.');

-- Verify Inserts
PROMPT Verify newly inserted records:
SELECT student_id, name, email FROM STUDENT WHERE student_id = '24BCS9999';
SELECT item_id, item_name, status, location_id FROM ITEM WHERE item_id = 1099;
SELECT lost_report_id, item_id, student_id FROM LOST_REPORT WHERE lost_report_id = 299;

COMMIT;


PROMPT =========================================================================
PROMPT PART 2: DEMONSTRATION OF UPDATE OPERATIONS
PROMPT =========================================================================

-- 1. Update Student contact information
PROMPT [2.1] Updating phone number of student '24BCS9999'...
UPDATE STUDENT
SET phone = '9123456780'
WHERE student_id = '24BCS9999';

-- 2. Update Item description and status
PROMPT [2.2] Updating Item description and category for item 1099...
UPDATE ITEM
SET description = 'Grey HP bluetooth optical mouse with USB-C dongle attached',
    category = 'Computer Accessories'
WHERE item_id = 1099;

-- 3. Update an existing pending claim
PROMPT [2.3] Updating claim 402 with administrative review note...
UPDATE CLAIM
SET proof_description = proof_description || ' [Admin Note: Photo verified at desk.]'
WHERE claim_id = 402;

-- Verify Updates
PROMPT Verify updated records:
SELECT student_id, name, phone FROM STUDENT WHERE student_id = '24BCS9999';
SELECT item_id, item_name, category, description FROM ITEM WHERE item_id = 1099;
SELECT claim_id, proof_description FROM CLAIM WHERE claim_id = 402;

COMMIT;


PROMPT =========================================================================
PROMPT PART 3: DEMONSTRATION OF DELETE OPERATIONS
PROMPT =========================================================================

-- 1. Insert a temporary duplicate claim to demonstrate safe deletion
PROMPT [3.1] Inserting a temporary claim for demonstration...
INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status)
VALUES (499, 1099, '24BCS9999', SYSDATE, 'Temporary claim accidentally submitted twice', 'PENDING');

PROMPT Verify record before deletion:
SELECT claim_id, item_id, claimant_student_id, claim_status FROM CLAIM WHERE claim_id = 499;

-- 2. Delete the temporary claim
PROMPT [3.2] Deleting the duplicate claim record...
DELETE FROM CLAIM
WHERE claim_id = 499;

PROMPT Verify record after deletion (should return 0 rows):
SELECT claim_id, item_id, claimant_student_id FROM CLAIM WHERE claim_id = 499;

-- 3. Delete the temporary demo report and item
PROMPT [3.3] Cleaning up temporary demo item and report...
DELETE FROM LOST_REPORT WHERE lost_report_id = 299;
DELETE FROM ITEM WHERE item_id = 1099;
DELETE FROM LOCATION WHERE location_id = 111;
DELETE FROM STUDENT WHERE student_id = '24BCS9999';

COMMIT;

PROMPT =========================================================================
PROMPT DML OPERATIONS COMPLETED AND COMMITTED SUCCESSFULLY.
PROMPT =========================================================================
