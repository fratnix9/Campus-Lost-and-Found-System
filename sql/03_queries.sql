-- =============================================================================
-- VIT - School of Computer Science Engineering and Information Systems
-- Course: BCSE302L - Database Systems
-- Project Title: Campus Lost and Found Management System
-- Student: Arahat Gaikwad (Reg No: 24BYB0182)
-- Script 03: 15+ Meaningful SQL Queries (Joins, Aggregations, Subqueries, Sets)
-- =============================================================================

SET LINESIZE 200;
SET PAGESIZE 100;

-- -----------------------------------------------------------------------------
-- Query 01: Simple Data Retrieval with WHERE and ORDER BY
-- Description: Retrieve all items currently in 'FOUND' status available for claim.
-- -----------------------------------------------------------------------------
SELECT item_id, item_name, category, date_reported, status
FROM ITEM
WHERE status = 'FOUND'
ORDER BY date_reported ASC;

-- -----------------------------------------------------------------------------
-- Query 02: Multi-Table INNER JOIN (3 Tables)
-- Description: List all reported items with reporter details and location names.
-- -----------------------------------------------------------------------------
SELECT 
    i.item_id,
    i.item_name,
    i.category,
    i.status,
    s.student_id AS reporter_regno,
    s.name AS reporter_name,
    l.location_name,
    l.building
FROM ITEM i
INNER JOIN STUDENT s ON i.reported_by_student_id = s.student_id
INNER JOIN LOCATION l ON i.location_id = l.location_id
ORDER BY i.item_id;

-- -----------------------------------------------------------------------------
-- Query 03: LEFT OUTER JOIN
-- Description: Display all items and any claims filed, highlighting unclaimed items.
-- -----------------------------------------------------------------------------
SELECT 
    i.item_id,
    i.item_name,
    i.status AS item_status,
    NVL(TO_CHAR(c.claim_id), 'NO CLAIM') AS claim_id,
    NVL(c.claim_status, 'UNCLAIMED') AS claim_status,
    c.claimant_student_id
FROM ITEM i
LEFT OUTER JOIN CLAIM c ON i.item_id = c.item_id
ORDER BY i.item_id;

-- -----------------------------------------------------------------------------
-- Query 04: Aggregate Function with GROUP BY
-- Description: Count total items and distinct status count grouped by category.
-- -----------------------------------------------------------------------------
SELECT 
    category,
    COUNT(item_id) AS total_items,
    SUM(CASE WHEN status = 'LOST' THEN 1 ELSE 0 END) AS lost_count,
    SUM(CASE WHEN status = 'FOUND' THEN 1 ELSE 0 END) AS found_count,
    SUM(CASE WHEN status IN ('CLAIMED', 'RETURNED') THEN 1 ELSE 0 END) AS resolved_count
FROM ITEM
GROUP BY category
ORDER BY total_items DESC;

-- -----------------------------------------------------------------------------
-- Query 05: Aggregate with HAVING Clause
-- Description: Identify campus buildings with 2 or more reported incidents.
-- -----------------------------------------------------------------------------
SELECT 
    l.building,
    COUNT(i.item_id) AS incidents_reported
FROM LOCATION l
INNER JOIN ITEM i ON l.location_id = i.location_id
GROUP BY l.building
HAVING COUNT(i.item_id) >= 2
ORDER BY incidents_reported DESC;

-- -----------------------------------------------------------------------------
-- Query 06: Subquery with IN Operator
-- Description: Find students who filed lost reports but have never submitted claims.
-- -----------------------------------------------------------------------------
SELECT student_id, name, email, phone
FROM STUDENT
WHERE student_id IN (SELECT student_id FROM LOST_REPORT)
  AND student_id NOT IN (SELECT claimant_student_id FROM CLAIM);

-- -----------------------------------------------------------------------------
-- Query 07: Subquery with NOT EXISTS
-- Description: Find items that currently have NO claims submitted by anyone.
-- -----------------------------------------------------------------------------
SELECT i.item_id, i.item_name, i.category, i.status, i.date_reported
FROM ITEM i
WHERE NOT EXISTS (
    SELECT 1 
    FROM CLAIM c 
    WHERE c.item_id = i.item_id
);

-- -----------------------------------------------------------------------------
-- Query 08: Correlated Subquery
-- Description: Display each item along with the total count of claims submitted for it.
-- -----------------------------------------------------------------------------
SELECT 
    i.item_id,
    i.item_name,
    i.status,
    (SELECT COUNT(*) FROM CLAIM c WHERE c.item_id = i.item_id) AS total_claims_received
FROM ITEM i
ORDER BY total_claims_received DESC, i.item_id;

-- -----------------------------------------------------------------------------
-- Query 09: Set Operator (UNION ALL)
-- Description: Unified Campus Activity Timeline combining Lost and Found events.
-- -----------------------------------------------------------------------------
SELECT 
    'LOST' AS event_type,
    lr.lost_report_id AS report_id,
    i.item_name,
    lr.date_lost AS event_date,
    s.name AS student_name,
    lr.details
FROM LOST_REPORT lr
JOIN ITEM i ON lr.item_id = i.item_id
JOIN STUDENT s ON lr.student_id = s.student_id
UNION ALL
SELECT 
    'FOUND' AS event_type,
    fr.found_report_id AS report_id,
    i.item_name,
    fr.date_found AS event_date,
    s.name AS student_name,
    fr.details
FROM FOUND_REPORT fr
JOIN ITEM i ON fr.item_id = i.item_id
JOIN STUDENT s ON fr.student_id = s.student_id
ORDER BY event_date DESC;

-- -----------------------------------------------------------------------------
-- Query 10: Pattern Matching and Case-Insensitive Search
-- Description: Search for electronics and gadgets containing keywords.
-- -----------------------------------------------------------------------------
SELECT item_id, item_name, description, category, status
FROM ITEM
WHERE UPPER(item_name) LIKE '%AIRPODS%' 
   OR UPPER(description) LIKE '%CHARGER%'
   OR UPPER(item_name) LIKE '%CALCULATOR%';

-- -----------------------------------------------------------------------------
-- Query 11: Date Arithmetic and Unclaimed Age Calculation
-- Description: Calculate how many days each item has remained in the system.
-- -----------------------------------------------------------------------------
SELECT 
    item_id,
    item_name,
    status,
    TO_CHAR(date_reported, 'YYYY-MM-DD') AS report_date,
    ROUND(SYSDATE - date_reported, 1) AS days_in_system
FROM ITEM
ORDER BY days_in_system DESC;

-- -----------------------------------------------------------------------------
-- Query 12: Comprehensive 4-Table Join for Verification Audit
-- Description: Approved claims showing claimant, item, location, and approving admin.
-- -----------------------------------------------------------------------------
SELECT 
    c.claim_id,
    s.name AS claimant_name,
    s.student_id AS claimant_id,
    i.item_name,
    l.location_name || ' (' || l.building || ')' AS item_location,
    a.name AS approved_by_admin,
    TO_CHAR(c.claim_date, 'YYYY-MM-DD') AS claim_date
FROM CLAIM c
JOIN STUDENT s ON c.claimant_student_id = s.student_id
JOIN ITEM i ON c.item_id = i.item_id
JOIN LOCATION l ON i.location_id = l.location_id
JOIN ADMIN a ON c.admin_id = a.admin_id
WHERE c.claim_status = 'APPROVED';

-- -----------------------------------------------------------------------------
-- Query 13: Subquery with ALL / Comparison Against Average
-- Description: Find items whose days in system exceed the overall average.
-- -----------------------------------------------------------------------------
SELECT 
    item_id,
    item_name,
    category,
    status,
    ROUND(SYSDATE - date_reported, 1) AS days_unresolved
FROM ITEM
WHERE (SYSDATE - date_reported) > (
    SELECT AVG(SYSDATE - date_reported) FROM ITEM
);

-- -----------------------------------------------------------------------------
-- Query 14: Conditional Aggregation (Admin Verification Summary)
-- Description: Break down claim review decisions made by each campus administrator.
-- -----------------------------------------------------------------------------
SELECT 
    a.admin_id,
    a.name AS admin_name,
    COUNT(c.claim_id) AS total_reviewed,
    SUM(CASE WHEN c.claim_status = 'APPROVED' THEN 1 ELSE 0 END) AS approved_claims,
    SUM(CASE WHEN c.claim_status = 'REJECTED' THEN 1 ELSE 0 END) AS rejected_claims
FROM ADMIN a
LEFT JOIN CLAIM c ON a.admin_id = c.admin_id
GROUP BY a.admin_id, a.name
ORDER BY total_reviewed DESC;

-- -----------------------------------------------------------------------------
-- Query 15: Analytical Window Function (DENSE_RANK)
-- Description: Rank categories by the total volume of lost and found incidents.
-- -----------------------------------------------------------------------------
SELECT 
    category,
    COUNT(*) AS total_items,
    DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS popularity_rank
FROM ITEM
GROUP BY category;

-- -----------------------------------------------------------------------------
-- Query 16 (Bonus): High-Conflict Detection Query
-- Description: Find items that have multiple competing claims filed by different students.
-- -----------------------------------------------------------------------------
SELECT 
    c.item_id,
    i.item_name,
    COUNT(c.claim_id) AS competing_claims_count
FROM CLAIM c
JOIN ITEM i ON c.item_id = i.item_id
GROUP BY c.item_id, i.item_name
HAVING COUNT(c.claim_id) > 1;
