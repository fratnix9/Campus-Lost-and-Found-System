-- =============================================================================
-- VIT - School of Computer Science Engineering and Information Systems
-- Course: BCSE302L - Database Systems
-- Project Title: Campus Lost and Found Management System
-- Student: Arahat Gaikwad (Reg No: 24BYB0182)
-- Script 06: Master Run All (Executes full suite in order)
-- =============================================================================

PROMPT =========================================================================
PROMPT STEP 1: EXECUTING TABLE CREATION AND CONSTRAINTS (DDL)
PROMPT =========================================================================
@@01_create_tables.sql

PROMPT =========================================================================
PROMPT STEP 2: POPULATING SAMPLE DATA (10+ RECORDS PER TABLE)
PROMPT =========================================================================
@@02_insert_sample_data.sql

PROMPT =========================================================================
PROMPT STEP 3: COMPILING PL/SQL PROCEDURES, FUNCTIONS, CURSOR, AND TRIGGERS
PROMPT =========================================================================
@@04_plsql_components.sql

PROMPT =========================================================================
PROMPT STEP 4: RUNNING 15+ MEANINGFUL SQL QUERIES
PROMPT =========================================================================
@@03_queries.sql

PROMPT =========================================================================
PROMPT STEP 5: RUNNING DML DEMONSTRATION (INSERT, UPDATE, DELETE)
PROMPT =========================================================================
@@05_dml_demonstration.sql

PROMPT =========================================================================
PROMPT ALL SCRIPTS EXECUTED SUCCESSFULLY!
PROMPT =========================================================================
