-- =============================================================================
-- VIT - School of Computer Science Engineering and Information Systems
-- Course: BCSE302L - Database Systems
-- Project Title: Campus Lost and Found Management System
-- Student: Arahat Gaikwad (Reg No: 24BYB0182)
-- Script 01: DDL - Table Creation and Integrity Constraints
-- =============================================================================

-- Clean up existing tables and sequences if they exist
BEGIN
   FOR cur_rec IN (SELECT table_name FROM user_tables WHERE table_name IN 
       ('CLAIM', 'FOUND_REPORT', 'LOST_REPORT', 'ITEM', 'ADMIN', 'STUDENT', 'LOCATION')) LOOP
      EXECUTE IMMEDIATE 'DROP TABLE ' || cur_rec.table_name || ' CASCADE CONSTRAINTS';
   END LOOP;
EXCEPTION
   WHEN OTHERS THEN
      NULL;
END;
/

-- -----------------------------------------------------------------------------
-- 1. LOCATION TABLE
-- Stores campus buildings and specific spots where items are lost or found
-- -----------------------------------------------------------------------------
CREATE TABLE LOCATION (
    location_id     NUMBER(6)       NOT NULL,
    location_name   VARCHAR2(100)   NOT NULL,
    building        VARCHAR2(100)   NOT NULL,
    CONSTRAINT pk_location PRIMARY KEY (location_id)
);

-- -----------------------------------------------------------------------------
-- 2. STUDENT TABLE
-- Stores student profile information for reporters and claimants
-- -----------------------------------------------------------------------------
CREATE TABLE STUDENT (
    student_id      VARCHAR2(20)    NOT NULL,
    name            VARCHAR2(100)   NOT NULL,
    email           VARCHAR2(100)   NOT NULL,
    phone           VARCHAR2(20)    NOT NULL,
    CONSTRAINT pk_student PRIMARY KEY (student_id),
    CONSTRAINT uk_student_email UNIQUE (email)
);

-- -----------------------------------------------------------------------------
-- 3. ADMIN TABLE
-- Stores campus administrative / security personnel managing claims
-- -----------------------------------------------------------------------------
CREATE TABLE ADMIN (
    admin_id        NUMBER(6)       NOT NULL,
    name            VARCHAR2(100)   NOT NULL,
    email           VARCHAR2(100)   NOT NULL,
    CONSTRAINT pk_admin PRIMARY KEY (admin_id),
    CONSTRAINT uk_admin_email UNIQUE (email)
);

-- -----------------------------------------------------------------------------
-- 4. ITEM TABLE
-- Master catalog of reported items (both lost and found)
-- -----------------------------------------------------------------------------
CREATE TABLE ITEM (
    item_id                 NUMBER(8)       NOT NULL,
    item_name               VARCHAR2(100)   NOT NULL,
    description             VARCHAR2(400),
    category                VARCHAR2(50)    NOT NULL,
    date_reported           DATE            DEFAULT SYSDATE NOT NULL,
    status                  VARCHAR2(20)    DEFAULT 'LOST' NOT NULL,
    location_id             NUMBER(6)       NOT NULL,
    reported_by_student_id  VARCHAR2(20)    NOT NULL,
    CONSTRAINT pk_item PRIMARY KEY (item_id),
    CONSTRAINT fk_item_location FOREIGN KEY (location_id)
        REFERENCES LOCATION(location_id),
    CONSTRAINT fk_item_student FOREIGN KEY (reported_by_student_id)
        REFERENCES STUDENT(student_id),
    CONSTRAINT chk_item_status CHECK (status IN ('LOST', 'FOUND', 'CLAIMED', 'RETURNED'))
);

-- -----------------------------------------------------------------------------
-- 5. LOST_REPORT TABLE
-- Specific incident details filed when an item is reported missing
-- -----------------------------------------------------------------------------
CREATE TABLE LOST_REPORT (
    lost_report_id  NUMBER(8)       NOT NULL,
    item_id         NUMBER(8)       NOT NULL,
    student_id      VARCHAR2(20)    NOT NULL,
    date_lost       DATE            DEFAULT SYSDATE NOT NULL,
    details         VARCHAR2(400),
    CONSTRAINT pk_lost_report PRIMARY KEY (lost_report_id),
    CONSTRAINT fk_lost_item FOREIGN KEY (item_id)
        REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_lost_student FOREIGN KEY (student_id)
        REFERENCES STUDENT(student_id)
);

-- -----------------------------------------------------------------------------
-- 6. FOUND_REPORT TABLE
-- Specific incident details filed when a discovered item is turned in
-- -----------------------------------------------------------------------------
CREATE TABLE FOUND_REPORT (
    found_report_id NUMBER(8)       NOT NULL,
    item_id         NUMBER(8)       NOT NULL,
    student_id      VARCHAR2(20)    NOT NULL,
    date_found      DATE            DEFAULT SYSDATE NOT NULL,
    details         VARCHAR2(400),
    CONSTRAINT pk_found_report PRIMARY KEY (found_report_id),
    CONSTRAINT fk_found_item FOREIGN KEY (item_id)
        REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_found_student FOREIGN KEY (student_id)
        REFERENCES STUDENT(student_id)
);

-- -----------------------------------------------------------------------------
-- 7. CLAIM TABLE
-- Verification requests filed by students claiming found items
-- -----------------------------------------------------------------------------
CREATE TABLE CLAIM (
    claim_id            NUMBER(8)       NOT NULL,
    item_id             NUMBER(8)       NOT NULL,
    claimant_student_id VARCHAR2(20)    NOT NULL,
    claim_date          DATE            DEFAULT SYSDATE NOT NULL,
    proof_description   VARCHAR2(500)   NOT NULL,
    claim_status        VARCHAR2(20)    DEFAULT 'PENDING' NOT NULL,
    admin_id            NUMBER(6),
    CONSTRAINT pk_claim PRIMARY KEY (claim_id),
    CONSTRAINT fk_claim_item FOREIGN KEY (item_id)
        REFERENCES ITEM(item_id) ON DELETE CASCADE,
    CONSTRAINT fk_claim_student FOREIGN KEY (claimant_student_id)
        REFERENCES STUDENT(student_id),
    CONSTRAINT fk_claim_admin FOREIGN KEY (admin_id)
        REFERENCES ADMIN(admin_id),
    CONSTRAINT chk_claim_status CHECK (claim_status IN ('PENDING', 'APPROVED', 'REJECTED'))
);

-- Comments on tables and relationships for documentation
COMMENT ON TABLE LOCATION IS 'Campus locations and buildings where items are lost or found';
COMMENT ON TABLE STUDENT IS 'Registered students reporting or claiming items';
COMMENT ON TABLE ADMIN IS 'Campus security or administrative authorities';
COMMENT ON TABLE ITEM IS 'Central items repository tracking lost and found items';
COMMENT ON TABLE LOST_REPORT IS 'Detailed incident reports for lost belongings';
COMMENT ON TABLE FOUND_REPORT IS 'Detailed incident reports for found items';
COMMENT ON TABLE CLAIM IS 'Claims raised by students to retrieve found items';
