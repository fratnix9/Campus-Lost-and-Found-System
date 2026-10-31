-- =============================================================================
-- VIT - School of Computer Science Engineering and Information Systems
-- Course: BCSE302L - Database Systems
-- Project Title: Campus Lost and Found Management System
-- Student: Arahat Gaikwad (Reg No: 24BYB0182)
-- Script 04: PL/SQL Components (2 Procedures, 2 Functions, 1 Cursor, 2 Triggers)
-- =============================================================================

SET SERVEROUTPUT ON SIZE 1000000;

-- =============================================================================
-- 1. STORED PROCEDURES
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Procedure 1: PROC_SUBMIT_CLAIM
-- Purpose: Submits a new claim after validating student, item, and current status.
-- Satisfies: FR7 (Submit claim with proof) and FR10 (Validation)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE PROC_SUBMIT_CLAIM (
    p_item_id           IN  NUMBER,
    p_claimant_id       IN  VARCHAR2,
    p_proof             IN  VARCHAR2,
    p_new_claim_id      OUT NUMBER,
    p_result_msg        OUT VARCHAR2
) AS
    v_item_count        NUMBER;
    v_student_count     NUMBER;
    v_item_status       VARCHAR2(20);
    v_existing_claim    NUMBER;
    v_max_id            NUMBER;
BEGIN
    -- 1. Check if claimant student exists
    SELECT COUNT(*) INTO v_student_count 
    FROM STUDENT 
    WHERE student_id = p_claimant_id;
    
    IF v_student_count = 0 THEN
        p_new_claim_id := -1;
        p_result_msg := 'ERROR: Student ID ' || p_claimant_id || ' is not registered.';
        RETURN;
    END IF;

    -- 2. Check if item exists and fetch its status
    BEGIN
        SELECT status INTO v_item_status 
        FROM ITEM 
        WHERE item_id = p_item_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_new_claim_id := -1;
            p_result_msg := 'ERROR: Item ID ' || p_item_id || ' does not exist.';
            RETURN;
    END;

    -- 3. Business rule: Cannot claim an already returned item
    IF v_item_status = 'RETURNED' THEN
        p_new_claim_id := -1;
        p_result_msg := 'ERROR: Item ' || p_item_id || ' has already been returned to its owner.';
        RETURN;
    END IF;

    -- 4. Check for duplicate pending claim by same student
    SELECT COUNT(*) INTO v_existing_claim 
    FROM CLAIM 
    WHERE item_id = p_item_id 
      AND claimant_student_id = p_claimant_id 
      AND claim_status = 'PENDING';
      
    IF v_existing_claim > 0 THEN
        p_new_claim_id := -1;
        p_result_msg := 'ERROR: Student already has a pending claim for this item.';
        RETURN;
    END IF;

    -- 5. Generate new claim ID and insert
    SELECT NVL(MAX(claim_id), 400) + 1 INTO v_max_id FROM CLAIM;
    
    INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status, admin_id)
    VALUES (v_max_id, p_item_id, p_claimant_id, SYSDATE, p_proof, 'PENDING', NULL);
    
    p_new_claim_id := v_max_id;
    p_result_msg := 'SUCCESS: Claim #' || v_max_id || ' submitted successfully in PENDING status.';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_new_claim_id := -1;
        p_result_msg := 'SYSTEM EXCEPTION: ' || SQLERRM;
END;
/

-- -----------------------------------------------------------------------------
-- Procedure 2: PROC_VERIFY_CLAIM
-- Purpose: Admin decision processing (APPROVE / REJECT) with automatic resolution.
-- Satisfies: FR8 (Verify claims) and FR9 (Update item status automatically)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE PROC_VERIFY_CLAIM (
    p_claim_id          IN  NUMBER,
    p_admin_id          IN  NUMBER,
    p_decision          IN  VARCHAR2, -- 'APPROVED' or 'REJECTED'
    p_result_msg        OUT VARCHAR2
) AS
    v_claim_count       NUMBER;
    v_admin_count       NUMBER;
    v_curr_status       VARCHAR2(20);
    v_target_item_id    NUMBER;
    v_decision_upper    VARCHAR2(20);
BEGIN
    v_decision_upper := UPPER(TRIM(p_decision));

    -- 1. Validate decision parameter
    IF v_decision_upper NOT IN ('APPROVED', 'REJECTED') THEN
        p_result_msg := 'ERROR: Decision must be either APPROVED or REJECTED.';
        RETURN;
    END IF;

    -- 2. Validate Admin existence
    SELECT COUNT(*) INTO v_admin_count FROM ADMIN WHERE admin_id = p_admin_id;
    IF v_admin_count = 0 THEN
        p_result_msg := 'ERROR: Admin ID ' || p_admin_id || ' does not exist.';
        RETURN;
    END IF;

    -- 3. Validate Claim existence and status
    BEGIN
        SELECT claim_status, item_id INTO v_curr_status, v_target_item_id
        FROM CLAIM
        WHERE claim_id = p_claim_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_result_msg := 'ERROR: Claim ID ' || p_claim_id || ' not found.';
            RETURN;
    END;

    IF v_curr_status != 'PENDING' THEN
        p_result_msg := 'ERROR: Claim #' || p_claim_id || ' is already processed as ' || v_curr_status || '.';
        RETURN;
    END IF;

    -- 4. Process Decision
    IF v_decision_upper = 'APPROVED' THEN
        -- Approve this claim
        UPDATE CLAIM
        SET claim_status = 'APPROVED',
            admin_id = p_admin_id
        WHERE claim_id = p_claim_id;

        -- Update item status to RETURNED
        UPDATE ITEM
        SET status = 'RETURNED'
        WHERE item_id = v_target_item_id;

        -- Reject any competing pending claims for the same item
        UPDATE CLAIM
        SET claim_status = 'REJECTED',
            admin_id = p_admin_id
        WHERE item_id = v_target_item_id
          AND claim_id != p_claim_id
          AND claim_status = 'PENDING';

        p_result_msg := 'SUCCESS: Claim #' || p_claim_id || ' APPROVED. Item #' || v_target_item_id || ' marked RETURNED.';
    ELSE
        -- Reject this specific claim
        UPDATE CLAIM
        SET claim_status = 'REJECTED',
            admin_id = p_admin_id
        WHERE claim_id = p_claim_id;

        p_result_msg := 'SUCCESS: Claim #' || p_claim_id || ' REJECTED by Admin #' || p_admin_id || '.';
    END IF;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_result_msg := 'SYSTEM EXCEPTION: ' || SQLERRM;
END;
/


-- =============================================================================
-- 2. STORED FUNCTIONS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Function 1: FUNC_CALCULATE_UNCLAIMED_DAYS
-- Purpose: Calculates number of days an item has been reported/unresolved.
-- Satisfies: FR11 (Calculate days an item is unclaimed)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FUNC_CALCULATE_UNCLAIMED_DAYS (
    p_item_id IN NUMBER
) RETURN NUMBER AS
    v_date_reported DATE;
    v_status        VARCHAR2(20);
    v_claim_date    DATE;
    v_days          NUMBER;
BEGIN
    SELECT date_reported, status INTO v_date_reported, v_status
    FROM ITEM
    WHERE item_id = p_item_id;

    IF v_status = 'RETURNED' THEN
        -- Time taken until first approved claim
        SELECT MIN(claim_date) INTO v_claim_date
        FROM CLAIM
        WHERE item_id = p_item_id AND claim_status = 'APPROVED';

        IF v_claim_date IS NOT NULL THEN
            v_days := ROUND(v_claim_date - v_date_reported, 1);
        ELSE
            v_days := ROUND(SYSDATE - v_date_reported, 1);
        END IF;
    ELSE
        -- Still in system
        v_days := ROUND(SYSDATE - v_date_reported, 1);
    END IF;

    RETURN GREATEST(v_days, 0);
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN -1;
    WHEN OTHERS THEN
        RETURN -99;
END;
/

-- -----------------------------------------------------------------------------
-- Function 2: FUNC_GET_STUDENT_ACTIVITY
-- Purpose: Returns a consolidated text summary of a student's system engagement.
-- Satisfies: FR1 (Student profile analytics)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FUNC_GET_STUDENT_ACTIVITY (
    p_student_id IN VARCHAR2
) RETURN VARCHAR2 AS
    v_lost_count   NUMBER := 0;
    v_found_count  NUMBER := 0;
    v_claims_count NUMBER := 0;
    v_student_name VARCHAR2(100);
BEGIN
    SELECT name INTO v_student_name
    FROM STUDENT
    WHERE student_id = p_student_id;

    SELECT COUNT(*) INTO v_lost_count   FROM LOST_REPORT  WHERE student_id = p_student_id;
    SELECT COUNT(*) INTO v_found_count  FROM FOUND_REPORT WHERE student_id = p_student_id;
    SELECT COUNT(*) INTO v_claims_count FROM CLAIM        WHERE claimant_student_id = p_student_id;

    RETURN v_student_name || ' [' || p_student_id || '] -> ' ||
           'Lost Filed: ' || v_lost_count || ' | ' ||
           'Found Filed: ' || v_found_count || ' | ' ||
           'Claims Submitted: ' || v_claims_count;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 'Student not found in registry.';
    WHEN OTHERS THEN
        RETURN 'Error generating activity summary.';
END;
/


-- =============================================================================
-- 3. EXPLICIT CURSOR IMPLEMENTATION
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Procedure 3 (Cursor Demonstration): PROC_FLAG_LONG_UNCLAIMED_ITEMS
-- Purpose: Scans all items using an explicit cursor and flags items unclaimed > threshold.
-- Satisfies: FR12 (Flag long-unclaimed items in bulk) and Minimum Cursor Requirement
-- -----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE PROC_FLAG_LONG_UNCLAIMED_ITEMS (
    p_days_threshold IN  NUMBER,
    p_total_flagged  OUT NUMBER
) AS
    -- Explicit Cursor Declaration
    CURSOR cur_unclaimed_items IS
        SELECT 
            i.item_id,
            i.item_name,
            i.category,
            i.status,
            i.date_reported,
            l.location_name,
            l.building
        FROM ITEM i
        JOIN LOCATION l ON i.location_id = l.location_id
        WHERE i.status IN ('LOST', 'FOUND')
          AND (SYSDATE - i.date_reported) >= p_days_threshold
        ORDER BY i.date_reported ASC;

    -- Record structure matching cursor
    v_item_rec cur_unclaimed_items%ROWTYPE;
    v_count    NUMBER := 0;
    v_days     NUMBER;
BEGIN
    DBMS_OUTPUT.PUT_LINE('=================================================================');
    DBMS_OUTPUT.PUT_LINE('  BATCH CURSOR AUDIT: ITEMS UNCLAIMED >= ' || p_days_threshold || ' DAYS');
    DBMS_OUTPUT.PUT_LINE('=================================================================');
    DBMS_OUTPUT.PUT_LINE(RPAD('ITEM ID', 10) || RPAD('ITEM NAME', 30) || RPAD('STATUS', 10) || RPAD('DAYS', 8) || 'LOCATION');
    DBMS_OUTPUT.PUT_LINE('-----------------------------------------------------------------');

    -- Open Cursor
    OPEN cur_unclaimed_items;
    
    LOOP
        -- Fetch row by row
        FETCH cur_unclaimed_items INTO v_item_rec;
        EXIT WHEN cur_unclaimed_items%NOTFOUND;

        v_count := v_count + 1;
        v_days := ROUND(SYSDATE - v_item_rec.date_reported, 1);

        DBMS_OUTPUT.PUT_LINE(
            RPAD(TO_CHAR(v_item_rec.item_id), 10) ||
            RPAD(SUBSTR(v_item_rec.item_name, 1, 28), 30) ||
            RPAD(v_item_rec.status, 10) ||
            RPAD(TO_CHAR(v_days), 8) ||
            v_item_rec.building
        );
    END LOOP;

    -- Close Cursor
    CLOSE cur_unclaimed_items;

    DBMS_OUTPUT.PUT_LINE('-----------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('Total Long-Unclaimed Items Processed: ' || v_count);
    DBMS_OUTPUT.PUT_LINE('=================================================================');

    p_total_flagged := v_count;
EXCEPTION
    WHEN OTHERS THEN
        IF cur_unclaimed_items%ISOPEN THEN
            CLOSE cur_unclaimed_items;
        END IF;
        DBMS_OUTPUT.PUT_LINE('Cursor processing error: ' || SQLERRM);
        p_total_flagged := -1;
END;
/


-- =============================================================================
-- 4. DATABASE TRIGGERS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Trigger 1: TRG_PREVENT_CLAIM_ON_RETURNED
-- Type: BEFORE INSERT ON CLAIM (Row-Level)
-- Purpose: Prevents filing a new claim on an item that has already been returned.
-- Satisfies: FR10 (Prevent claims on returned items)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_PREVENT_CLAIM_ON_RETURNED
BEFORE INSERT ON CLAIM
FOR EACH ROW
DECLARE
    v_status VARCHAR2(20);
BEGIN
    SELECT status INTO v_status
    FROM ITEM
    WHERE item_id = :NEW.item_id;

    IF v_status = 'RETURNED' THEN
        RAISE_APPLICATION_ERROR(
            -20001, 
            'Integrity Rule Violation: Item #' || :NEW.item_id || ' has already been RETURNED to its owner. New claims are disallowed.'
        );
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'Referenced item #' || :NEW.item_id || ' does not exist.');
END;
/

-- -----------------------------------------------------------------------------
-- Trigger 2: TRG_AUTO_UPDATE_ITEM_STATUS
-- Type: AFTER UPDATE OF claim_status ON CLAIM (Row-Level)
-- Purpose: Automatically updates ITEM status to 'RETURNED' when claim is approved.
-- Satisfies: FR9 (Update item status automatically)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_AUTO_UPDATE_ITEM_STATUS
AFTER UPDATE OF claim_status ON CLAIM
FOR EACH ROW
BEGIN
    IF :NEW.claim_status = 'APPROVED' AND (:OLD.claim_status IS NULL OR :OLD.claim_status != 'APPROVED') THEN
        UPDATE ITEM
        SET status = 'RETURNED'
        WHERE item_id = :NEW.item_id;
    END IF;
END;
/


-- =============================================================================
-- 5. VERIFICATION AND DEMONSTRATION ANONYMOUS BLOCKS
-- =============================================================================

-- Demo Block 1: Test Functions
DECLARE
    v_days NUMBER;
    v_summary VARCHAR2(250);
BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Testing Functions ---');
    v_days := FUNC_CALCULATE_UNCLAIMED_DAYS(1002);
    DBMS_OUTPUT.PUT_LINE('Unclaimed Days for Item 1002 (AirPods): ' || v_days);

    v_summary := FUNC_GET_STUDENT_ACTIVITY('24BYB0182');
    DBMS_OUTPUT.PUT_LINE('Student Summary: ' || v_summary);
END;
/

-- Demo Block 2: Test Cursor Procedure
DECLARE
    v_total NUMBER;
BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Testing Cursor Batch Processing ---');
    PROC_FLAG_LONG_UNCLAIMED_ITEMS(0, v_total);
    DBMS_OUTPUT.PUT_LINE('Returned flagged count: ' || v_total);
END;
/

-- Demo Block 3: Test Procedure and Trigger 2 (Claim Submission and Verification)
DECLARE
    v_new_id NUMBER;
    v_msg    VARCHAR2(250);
BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Testing Procedure 1: Submit Claim ---');
    PROC_SUBMIT_CLAIM(
        p_item_id => 1005,
        p_claimant_id => '24BCE1001',
        p_proof => 'Library entry stamp and serial matches book slip.',
        p_new_claim_id => v_new_id,
        p_result_msg => v_msg
    );
    DBMS_OUTPUT.PUT_LINE(v_msg);

    DBMS_OUTPUT.PUT_LINE('--- Testing Procedure 2 and Trigger 2: Verify Claim ---');
    IF v_new_id > 0 THEN
        PROC_VERIFY_CLAIM(
            p_claim_id => v_new_id,
            p_admin_id => 3,
            p_decision => 'APPROVED',
            p_result_msg => v_msg
        );
        DBMS_OUTPUT.PUT_LINE(v_msg);
    END IF;
END;
/

-- Demo Block 4: Test Trigger 1 (Expect error on returned item)
DECLARE
    v_err_msg VARCHAR2(300);
BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Testing Trigger 1: Prevent Claim on Returned Item ---');
    BEGIN
        INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status)
        VALUES (999, 1001, '24BCE1001', SYSDATE, 'Attempting claim on already returned ID card', 'PENDING');
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Trigger 1 Successfully Blocked Invalid Claim: ' || SQLERRM);
    END;
END;
/
