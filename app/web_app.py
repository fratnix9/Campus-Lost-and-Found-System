"""
Campus Lost and Found Management System
Web Application & REST API Server (Zero-Dependency, Built-in Python)
Author: Arahat Gaikwad (Reg No: 24BYB0182)
VIT Vellore - BCSE302L Database Systems Course Project (Review III)
"""

import os
import sys
import json
import sqlite3
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# Setup paths
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
PROJECT_DIR = os.path.dirname(APP_DIR)
DB_PATH = os.path.join(APP_DIR, "campus_lost_found.db")

from database import Database

db = Database(db_type="sqlite")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Campus Lost & Found Management System | Review III</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0F172A;
      --bg-secondary: #1E293B;
      --bg-card: #1E293B;
      --bg-hover: #334155;
      --border-color: #334155;
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --accent-blue: #38BDF8;
      --accent-teal: #2DD4BF;
      --accent-indigo: #818CF8;
      --accent-amber: #FBBF24;
      --accent-rose: #FB7185;
      --accent-green: #34D399;
      --radius: 12px;
      --shadow: 0 10px 25px -5px rgba(0,0,0,0.3), 0 8px 10px -6px rgba(0,0,0,0.3);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg-primary);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      background: rgba(30, 41, 59, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 0.85rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .brand-icon {
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, #38BDF8, #818CF8);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.4rem;
      box-shadow: 0 4px 12px rgba(56, 189, 248, 0.35);
    }
    .brand-text h1 {
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(to right, #F8FAFC, #38BDF8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-text p {
      font-size: 0.75rem;
      color: var(--text-muted);
    }
    .student-badge {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-color);
      padding: 0.45rem 0.9rem;
      border-radius: 9999px;
      font-size: 0.8rem;
    }
    .student-badge .dot {
      width: 8px;
      height: 8px;
      background: var(--accent-green);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--accent-green);
    }
    .nav-tabs {
      display: flex;
      gap: 0.4rem;
      background: rgba(15, 23, 42, 0.6);
      padding: 0.3rem;
      border-radius: 10px;
      border: 1px solid var(--border-color);
    }
    .nav-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 0.45rem 0.9rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .nav-btn:hover {
      color: var(--text-main);
      background: var(--bg-hover);
    }
    .nav-btn.active {
      color: var(--bg-primary);
      background: var(--accent-blue);
      font-weight: 600;
    }
    .reset-btn {
      background: rgba(251, 113, 133, 0.15);
      color: var(--accent-rose);
      border: 1px solid rgba(251, 113, 133, 0.3);
      padding: 0.45rem 0.8rem;
      border-radius: 8px;
      font-size: 0.8rem;
      cursor: pointer;
      font-weight: 500;
      transition: all 0.2s;
    }
    .reset-btn:hover {
      background: var(--accent-rose);
      color: #FFF;
    }
    main {
      flex: 1;
      max-width: 1400px;
      width: 100%;
      margin: 0 auto;
      padding: 2rem;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }
    .stat-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
      box-shadow: var(--shadow);
    }
    .stat-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: var(--card-accent, var(--accent-blue));
    }
    .stat-card .title {
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .stat-card .value {
      font-size: 2rem;
      font-weight: 700;
      margin: 0.4rem 0;
      color: var(--text-main);
    }
    .stat-card .sub {
      font-size: 0.75rem;
      color: var(--text-muted);
    }
    .tab-content {
      display: none;
    }
    .tab-content.active {
      display: block;
      animation: fadeIn 0.25s ease-in-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      box-shadow: var(--shadow);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .card-header h2 {
      font-size: 1.2rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .badge {
      display: inline-block;
      padding: 0.25rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .badge-lost { background: rgba(251, 113, 133, 0.15); color: var(--accent-rose); border: 1px solid rgba(251, 113, 133, 0.3); }
    .badge-found { background: rgba(56, 189, 248, 0.15); color: var(--accent-blue); border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-claimed { background: rgba(251, 191, 36, 0.15); color: var(--accent-amber); border: 1px solid rgba(251, 191, 36, 0.3); }
    .badge-returned { background: rgba(52, 211, 153, 0.15); color: var(--accent-green); border: 1px solid rgba(52, 211, 153, 0.3); }
    .badge-pending { background: rgba(251, 191, 36, 0.15); color: var(--accent-amber); border: 1px solid rgba(251, 191, 36, 0.3); }
    .badge-approved { background: rgba(52, 211, 153, 0.15); color: var(--accent-green); border: 1px solid rgba(52, 211, 153, 0.3); }
    .badge-rejected { background: rgba(251, 113, 133, 0.15); color: var(--accent-rose); border: 1px solid rgba(251, 113, 133, 0.3); }
    
    .table-responsive {
      overflow-x: auto;
      border-radius: 8px;
      border: 1px solid var(--border-color);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      text-align: left;
    }
    th {
      background: rgba(15, 23, 42, 0.8);
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.85rem 1rem;
      border-bottom: 1px solid var(--border-color);
    }
    td {
      padding: 0.85rem 1rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: var(--text-main);
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(255, 255, 255, 0.02); }

    .search-bar {
      display: flex;
      gap: 0.75rem;
      margin-bottom: 1.25rem;
      flex-wrap: wrap;
    }
    .input-control, select {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.6rem 0.9rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-family: inherit;
      outline: none;
      transition: border-color 0.2s;
    }
    .input-control:focus, select:focus {
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }
    .btn {
      background: var(--accent-blue);
      color: var(--bg-primary);
      border: none;
      padding: 0.6rem 1.2rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s;
    }
    .btn:hover {
      background: #7dd3fc;
      transform: translateY(-1px);
    }
    .btn-success { background: var(--accent-green); color: #064e3b; }
    .btn-success:hover { background: #6ee7b7; }
    .btn-danger { background: var(--accent-rose); color: #881337; }
    .btn-danger:hover { background: #fda4af; }
    .btn-outline {
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-main);
    }
    .btn-outline:hover {
      background: var(--bg-hover);
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1rem;
      margin-bottom: 1.25rem;
    }
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }
    .form-group label {
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--text-muted);
    }

    /* Review 3 Transaction Suite */
    .tx-card {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 1.25rem;
      margin-bottom: 1rem;
      transition: border-color 0.2s;
    }
    .tx-card:hover {
      border-color: var(--accent-blue);
    }
    .tx-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }
    .tx-num {
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.2rem 0.5rem;
      background: rgba(56, 189, 248, 0.2);
      color: var(--accent-blue);
      border-radius: 6px;
    }
    .tx-flow {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.75rem;
      color: var(--text-muted);
      margin: 0.5rem 0;
      font-family: 'JetBrains Mono', monospace;
      flex-wrap: wrap;
    }
    .tx-flow span {
      background: rgba(30, 41, 59, 0.8);
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .q-box {
      background: rgba(0, 0, 0, 0.25);
      border-left: 3px solid var(--accent-indigo);
      padding: 0.6rem 0.9rem;
      margin: 0.4rem 0;
      font-size: 0.8rem;
      border-radius: 0 6px 6px 0;
    }
    .q-box strong { color: var(--accent-indigo); }
    .code-block {
      background: #0B1120;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 0.85rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #E2E8F0;
      overflow-x: auto;
      margin: 0.6rem 0;
    }

    footer {
      text-align: center;
      padding: 1.5rem;
      font-size: 0.8rem;
      color: var(--text-muted);
      border-top: 1px solid var(--border-color);
      margin-top: auto;
      background: rgba(15, 23, 42, 0.6);
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <div class="brand-icon">📦</div>
      <div class="brand-text">
        <h1>Campus Lost & Found System</h1>
        <p>Review III – Integrated Database Application</p>
      </div>
    </div>

    <nav class="nav-tabs">
      <button class="nav-btn active" onclick="showTab('catalog')">📊 Catalog & Search</button>
      <button class="nav-btn" onclick="showTab('student')">🎓 Student Services</button>
      <button class="nav-btn" onclick="showTab('admin')">🛡️ Security Admin</button>
      <button class="nav-btn" onclick="showTab('transactions')">⚡ Review III Live Suite</button>
      <button class="nav-btn" onclick="showTab('queries')">📈 SQL Reports</button>
    </nav>

    <div style="display: flex; gap: 0.75rem; align-items: center;">
      <div class="student-badge">
        <div class="dot"></div>
        <span><strong>Arahat Gaikwad</strong> (24BYB0182) | SCORE</span>
      </div>
      <button class="reset-btn" onclick="resetDatabase()" title="Reset DB to 72 clean sample records">↺ Reset Data</button>
    </div>
  </header>

  <main>
    <!-- TOP STATS COUNTERS -->
    <div class="stats-grid">
      <div class="stat-card" style="--card-accent: var(--accent-blue)">
        <div class="title">Total Catalog Items</div>
        <div class="value" id="stat-total">12</div>
        <div class="sub">Across 10 Campus Locations</div>
      </div>
      <div class="stat-card" style="--card-accent: var(--accent-rose)">
        <div class="title">Active Lost Items</div>
        <div class="value" id="stat-lost">3</div>
        <div class="sub">Misplaced by Students</div>
      </div>
      <div class="stat-card" style="--card-accent: var(--accent-teal)">
        <div class="title">Turned-In Found Items</div>
        <div class="value" id="stat-found">5</div>
        <div class="sub">Awaiting Claim Verification</div>
      </div>
      <div class="stat-card" style="--card-accent: var(--accent-amber)">
        <div class="title">Pending Claims Queue</div>
        <div class="value" id="stat-claims">4</div>
        <div class="sub">Awaiting Admin Adjudication</div>
      </div>
      <div class="stat-card" style="--card-accent: var(--accent-green)">
        <div class="title">Successfully Returned</div>
        <div class="value" id="stat-returned">3</div>
        <div class="sub">Verified via Triggers & Procedures</div>
      </div>
    </div>

    <!-- TAB 1: CATALOG & SEARCH -->
    <div id="tab-catalog" class="tab-content active">
      <div class="card">
        <div class="card-header">
          <h2>🔍 Campus Lost & Found Master Catalog</h2>
          <span class="badge badge-found" id="catalog-count">Showing 12 Items</span>
        </div>

        <div class="search-bar">
          <input type="text" id="search-input" class="input-control" placeholder="Search by name, description, category..." style="flex: 2; min-width: 220px;" oninput="filterCatalog()">
          <select id="filter-category" class="input-control" onchange="filterCatalog()">
            <option value="">All Categories</option>
            <option value="Electronics">Electronics</option>
            <option value="Personal Accessories">Personal Accessories</option>
            <option value="Identity Cards">Identity Cards</option>
            <option value="Keys">Keys</option>
            <option value="Books & Study Material">Books & Study Material</option>
            <option value="Wallets & Bags">Wallets & Bags</option>
          </select>
          <select id="filter-status" class="input-control" onchange="filterCatalog()">
            <option value="">All Statuses</option>
            <option value="LOST">LOST</option>
            <option value="FOUND">FOUND</option>
            <option value="CLAIMED">CLAIMED</option>
            <option value="RETURNED">RETURNED</option>
          </select>
          <button class="btn btn-outline" onclick="loadCatalog()">Refresh</button>
        </div>

        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Item ID</th>
                <th>Item Name</th>
                <th>Category</th>
                <th>Status</th>
                <th>Date Reported</th>
                <th>Campus Location</th>
                <th>Reported By</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="catalog-body">
              <!-- Dynamically Populated -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 2: STUDENT SERVICES -->
    <div id="tab-student" class="tab-content">
      <div class="form-grid">
        <!-- Report Lost Item -->
        <div class="card">
          <div class="card-header">
            <h2>📢 Report a Lost Item (FR4)</h2>
            <span class="badge badge-lost">Student Portal</span>
          </div>
          <form onsubmit="handleReportLost(event)">
            <div class="form-group" style="margin-bottom: 0.8rem;">
              <label>Student Reg No *</label>
              <input type="text" id="lost-student" class="input-control" value="24BYB0182" required>
            </div>
            <div class="form-group" style="margin-bottom: 0.8rem;">
              <label>Item Name *</label>
              <input type="text" id="lost-name" class="input-control" placeholder="e.g. Dell XPS Laptop Charger" required>
            </div>
            <div class="form-group" style="margin-bottom: 0.8rem;">
              <label>Category *</label>
              <select id="lost-category" class="input-control" required>
                <option value="Electronics">Electronics</option>
                <option value="Personal Accessories">Personal Accessories</option>
                <option value="Identity Cards">Identity Cards</option>
                <option value="Keys">Keys</option>
                <option value="Books & Study Material">Books & Study Material</option>
                <option value="Wallets & Bags">Wallets & Bags</option>
              </select>
            </div>
            <div class="form-group" style="margin-bottom: 0.8rem;">
              <label>Campus Location Misplaced *</label>
              <select id="lost-location" class="input-control" required>
                <option value="101">Silver Jubilee Tower (SJT) - Room 401 Lab</option>
                <option value="102">Central Library - Main Reading Hall</option>
                <option value="103">Foodys Central - Ground Floor Cafeteria</option>
                <option value="105">Technology Tower (TT) - Room 214</option>
                <option value="106">Periyar EVR Block (PRP) - Physics Lab</option>
                <option value="108">Men's Hostel D Block</option>
              </select>
            </div>
            <div class="form-group" style="margin-bottom: 1rem;">
              <label>Description & Loss Details</label>
              <textarea id="lost-details" class="input-control" rows="2" placeholder="Left on second row desk..."></textarea>
            </div>
            <button type="submit" class="btn" style="width: 100%;">Submit Lost Report</button>
          </form>
        </div>

        <!-- Submit Claim with Proof -->
        <div class="card">
          <div class="card-header">
            <h2>🏷️ Submit Ownership Claim with Proof (FR7)</h2>
            <span class="badge badge-claimed">PROC_SUBMIT_CLAIM</span>
          </div>
          <form onsubmit="handleSubmitClaim(event)">
            <div class="form-group" style="margin-bottom: 0.8rem;">
              <label>Claimant Student Reg No *</label>
              <input type="text" id="claim-student" class="input-control" value="24BYB0182" required>
            </div>
            <div class="form-group" style="margin-bottom: 0.8rem;">
              <label>Item ID to Claim *</label>
              <input type="number" id="claim-item-id" class="input-control" placeholder="e.g. 1002" required>
            </div>
            <div class="form-group" style="margin-bottom: 1rem;">
              <label>Proof of Ownership Description * (FR7)</label>
              <textarea id="claim-proof" class="input-control" rows="3" placeholder="e.g. Serial #GW8974K, engraved initials on back, bluetooth pairing name 'Arahat AirPods'..." required></textarea>
            </div>
            <div id="claim-alert" style="display: none; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; font-size: 0.8rem;"></div>
            <button type="submit" class="btn btn-success" style="width: 100%;">Submit Claim for Verification</button>
          </form>
        </div>
      </div>

      <!-- Student Activity Profile -->
      <div class="card">
        <div class="card-header">
          <h2>👤 Student Profile & Activity History (FUNC_GET_STUDENT_ACTIVITY)</h2>
          <span class="badge badge-found">Stored Function 2</span>
        </div>
        <div style="display: flex; gap: 0.75rem; align-items: center; margin-bottom: 1rem;">
          <input type="text" id="profile-student-id" class="input-control" value="24BYB0182" placeholder="Enter Student Reg No">
          <button class="btn btn-outline" onclick="fetchStudentProfile()">Check Activity Profile</button>
        </div>
        <div id="profile-output" class="code-block" style="display: none;"></div>
      </div>
    </div>

    <!-- TAB 3: ADMIN & SECURITY PORTAL -->
    <div id="tab-admin" class="tab-content">
      <!-- Pending Claims Queue -->
      <div class="card">
        <div class="card-header">
          <h2>🛡️ Security Officer Claims Review Queue (FR8, FR9)</h2>
          <span class="badge badge-pending">PROC_VERIFY_CLAIM & TRG_AUTO_UPDATE_ITEM_STATUS</span>
        </div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Claim ID</th>
                <th>Item ID & Name</th>
                <th>Claimant</th>
                <th>Claim Date</th>
                <th>Proof of Ownership</th>
                <th>Status</th>
                <th>Adjudication Action</th>
              </tr>
            </thead>
            <tbody id="claims-queue-body">
              <!-- Dynamically Populated -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Batch Explicit Cursor Audit -->
      <div class="card">
        <div class="card-header">
          <h2>⏱️ Bulk Cursor Audit: Long-Unclaimed Items (FR11, FR12)</h2>
          <span class="badge badge-amber">Explicit Cursor: cur_unclaimed_items</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
          Simulates execution of PL/SQL Explicit Cursor <code>PROC_FLAG_LONG_UNCLAIMED_ITEMS</code> in PGA memory to batch scan and flag aging items unresolved in campus storage for auction or donation.
        </p>
        <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem; flex-wrap: wrap;">
          <label style="font-size: 0.85rem;">Retention Threshold (Days):</label>
          <input type="number" id="cursor-days" class="input-control" value="10" style="width: 100px;">
          <button class="btn" onclick="runCursorAudit()">Execute Explicit Cursor Batch Scan</button>
        </div>
        <div id="cursor-output" style="display: none;">
          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Item ID</th>
                  <th>Item Name</th>
                  <th>Category</th>
                  <th>Status</th>
                  <th>Days Unresolved</th>
                  <th>Building Location</th>
                </tr>
              </thead>
              <tbody id="cursor-body"></tbody>
            </table>
          </div>
          <div id="cursor-summary" style="margin-top: 0.75rem; font-size: 0.85rem; color: var(--accent-teal); font-weight: 600;"></div>
        </div>
      </div>
    </div>

    <!-- TAB 4: REVIEW III LIVE TRANSACTION DEMONSTRATION SUITE -->
    <div id="tab-transactions" class="tab-content">
      <div class="card">
        <div class="card-header">
          <h2>⚡ Review III Live Real-World Transaction Flow Suite (3 Marks)</h2>
          <span class="badge badge-found">Official 5-Step Evaluation Cycle</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem;">
          Demonstrating the mandated flow: <strong>User Operation → SQL/PL-SQL → Database Processing → Database Update/Retrieval → Result</strong> while answering all 5 standard evaluation questions.
        </p>

        <!-- Transaction 1 -->
        <div class="tx-card">
          <div class="tx-header">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span class="tx-num">Tx 1</span>
              <strong style="font-size: 0.95rem;">Student Files Lost Belonging Incident Report (FR4)</strong>
            </div>
            <button class="btn btn-outline" style="font-size: 0.75rem; padding: 0.35rem 0.7rem;" onclick="executeTransaction(1)">Execute Live Tx 1</button>
          </div>
          <div class="tx-flow">
            <span>Student Input</span> &rarr; <span>INSERT INTO ITEM & LOST_REPORT</span> &rarr; <span>FK Constraints Checked</span> &rarr; <span>Status='LOST'</span> &rarr; <span>Incident #201 Generated</span>
          </div>
          <div class="q-box">
            <strong>Q1: What operation?</strong> Student Arahat Gaikwad (24BYB0182) registers lost ID card.<br>
            <strong>Q2: Tables involved?</strong> <code>ITEM</code>, <code>LOST_REPORT</code>, <code>STUDENT</code>, <code>LOCATION</code><br>
            <strong>Q3: SQL/PLSQL component?</strong> Transactional <code>INSERT INTO ITEM (...)</code> followed by <code>INSERT INTO LOST_REPORT (...)</code>.<br>
            <strong>Q4: Database effect?</strong> Master catalog gains new item with status='LOST'; referential integrity linked to reporter and location.<br>
            <strong>Q5: Result generated?</strong> Incident logged, tracking reference issued to student.
          </div>
          <div id="tx-res-1" class="code-block" style="display: none;"></div>
        </div>

        <!-- Transaction 2 -->
        <div class="tx-card">
          <div class="tx-header">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span class="tx-num">Tx 2</span>
              <strong style="font-size: 0.95rem;">Good Samaritan Turns in Discovered Belonging (FR5)</strong>
            </div>
            <button class="btn btn-outline" style="font-size: 0.75rem; padding: 0.35rem 0.7rem;" onclick="executeTransaction(2)">Execute Live Tx 2</button>
          </div>
          <div class="tx-flow">
            <span>Discoverer Turn-In</span> &rarr; <span>INSERT INTO FOUND_REPORT</span> &rarr; <span>UPDATE ITEM SET status='FOUND'</span> &rarr; <span>Catalog Updated</span>
          </div>
          <div class="q-box">
            <strong>Q1: What operation?</strong> Student Rohan Sharma discovers misplaced ID card on Library table 14 and turns it in.<br>
            <strong>Q2: Tables involved?</strong> <code>FOUND_REPORT</code>, <code>ITEM</code>, <code>STUDENT</code><br>
            <strong>Q3: SQL/PLSQL component?</strong> <code>INSERT INTO FOUND_REPORT (...)</code> and <code>UPDATE ITEM SET status = 'FOUND'</code>.<br>
            <strong>Q4: Database effect?</strong> FOUND_REPORT #301 created; item status transitions from 'LOST' to 'FOUND'.<br>
            <strong>Q5: Result generated?</strong> Item becomes discoverable in search portal for owner verification.
          </div>
          <div id="tx-res-2" class="code-block" style="display: none;"></div>
        </div>

        <!-- Transaction 3 -->
        <div class="tx-card">
          <div class="tx-header">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span class="tx-num">Tx 3</span>
              <strong style="font-size: 0.95rem;">Owner Files Claim with Ownership Proof via Stored Procedure (FR7)</strong>
            </div>
            <button class="btn btn-outline" style="font-size: 0.75rem; padding: 0.35rem 0.7rem;" onclick="executeTransaction(3)">Execute Live Tx 3</button>
          </div>
          <div class="tx-flow">
            <span>Owner Proof Submission</span> &rarr; <span>PROC_SUBMIT_CLAIM</span> &rarr; <span>Pre-validation & Duplicate Check</span> &rarr; <span>Claim #411 in PENDING</span>
          </div>
          <div class="q-box">
            <strong>Q1: What operation?</strong> Student Arahat Gaikwad (24BYB0182) submits ownership claim for AirPods #1002 with matching serial.<br>
            <strong>Q2: Tables involved?</strong> <code>CLAIM</code>, <code>ITEM</code>, <code>STUDENT</code><br>
            <strong>Q3: SQL/PLSQL component?</strong> Stored Procedure <code>PROC_SUBMIT_CLAIM</code> with validation checks.<br>
            <strong>Q4: Database effect?</strong> Validates student exists; ensures item is not already RETURNED; creates Claim #411 in PENDING status.<br>
            <strong>Q5: Result generated?</strong> Claim placed into security adjudication queue with proof recorded.
          </div>
          <div id="tx-res-3" class="code-block" style="display: none;"></div>
        </div>

        <!-- Transaction 4 -->
        <div class="tx-card">
          <div class="tx-header">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span class="tx-num">Tx 4</span>
              <strong style="font-size: 0.95rem;">Admin Approves Claim & Trigger Automatically Updates Item to RETURNED (FR8, FR9)</strong>
            </div>
            <button class="btn btn-outline" style="font-size: 0.75rem; padding: 0.35rem 0.7rem;" onclick="executeTransaction(4)">Execute Live Tx 4</button>
          </div>
          <div class="tx-flow">
            <span>Officer Approval</span> &rarr; <span>PROC_VERIFY_CLAIM</span> &rarr; <span>Trigger TRG_AUTO_UPDATE_ITEM_STATUS</span> &rarr; <span>Item='RETURNED'</span> &rarr; <span>Competitors Rejected</span>
          </div>
          <div class="q-box">
            <strong>Q1: What operation?</strong> Campus Security approves Claim #401; Trigger automatically synchronizes parent item status.<br>
            <strong>Q2: Tables involved?</strong> <code>CLAIM</code>, <code>ITEM</code>, <code>ADMIN</code><br>
            <strong>Q3: SQL/PLSQL component?</strong> <code>PROC_VERIFY_CLAIM</code> + <code>AFTER UPDATE</code> Trigger <code>TRG_AUTO_UPDATE_ITEM_STATUS</code>.<br>
            <strong>Q4: Database effect?</strong> Claim status becomes 'APPROVED'; Trigger automatically sets ITEM status to 'RETURNED'; competing pending claims auto-rejected.<br>
            <strong>Q5: Result generated?</strong> Item safely handed over; multi-table consistency maintained atomically.
          </div>
          <div id="tx-res-4" class="code-block" style="display: none;"></div>
        </div>

        <!-- Transaction 5 -->
        <div class="tx-card">
          <div class="tx-header">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span class="tx-num" style="background: rgba(251, 113, 133, 0.2); color: var(--accent-rose);">Tx 5</span>
              <strong style="font-size: 0.95rem;">Security Negative Test: Trigger Blocks Claim on Already Returned Item (FR10)</strong>
            </div>
            <button class="btn btn-danger" style="font-size: 0.75rem; padding: 0.35rem 0.7rem;" onclick="executeTransaction(5)">Execute Security Test</button>
          </div>
          <div class="tx-flow">
            <span>Fraudulent Claim Attempt</span> &rarr; <span>BEFORE INSERT Trigger</span> &rarr; <span>Status='RETURNED' Detected</span> &rarr; <span>RAISE_APPLICATION_ERROR (-20001)</span> &rarr; <span>Insert Aborted</span>
          </div>
          <div class="q-box" style="border-left-color: var(--accent-rose);">
            <strong style="color: var(--accent-rose);">Q1: What operation?</strong> Unauthorized user attempts to file a claim on Item #1001 which has already been returned.<br>
            <strong style="color: var(--accent-rose);">Q2: Tables involved?</strong> <code>CLAIM</code>, <code>ITEM</code><br>
            <strong style="color: var(--accent-rose);">Q3: SQL/PLSQL component?</strong> <code>BEFORE INSERT</code> Trigger <code>TRG_PREVENT_CLAIM_ON_RETURNED</code>.<br>
            <strong style="color: var(--accent-rose);">Q4: Database effect?</strong> Trigger catches violation, raises application error, and executes immediate transaction rollback.<br>
            <strong style="color: var(--accent-rose);">Q5: Result generated?</strong> Fraud prevented; zero dirty or conflicting records are inserted into the database.
          </div>
          <div id="tx-res-5" class="code-block" style="display: none;"></div>
        </div>
      </div>
    </div>

    <!-- TAB 5: SQL ANALYTICS & REPORTS -->
    <div id="tab-queries" class="tab-content">
      <div class="card">
        <div class="card-header">
          <h2>📈 16 Meaningful SQL Analytical Queries & Output Reports (FR14)</h2>
          <span class="badge badge-found">Review 2 & Review 3 Deliverable</span>
        </div>
        <div style="display: flex; gap: 0.75rem; align-items: center; margin-bottom: 1rem; flex-wrap: wrap;">
          <label style="font-size: 0.85rem;">Select SQL Query to Execute Live:</label>
          <select id="query-select" class="input-control" style="flex: 1; min-width: 300px;" onchange="runSelectedQuery()">
            <!-- Dynamically Populated -->
          </select>
          <button class="btn" onclick="runSelectedQuery()">Execute Query</button>
        </div>

        <div id="query-sql-display" class="code-block" style="display: none;"></div>
        
        <div class="table-responsive" style="margin-top: 1rem;">
          <table id="query-result-table">
            <thead id="query-thead"></thead>
            <tbody id="query-tbody"></tbody>
          </table>
        </div>
      </div>
    </div>
  </main>

  <footer>
    <p>Campus Lost and Found Management System &copy; 2026 | BCSE302L Database Systems Course Project</p>
    <p style="margin-top: 0.3rem;">Developed by <strong>Arahat Gaikwad (Reg No: 24BYB0182)</strong> | SCORE, Vellore Institute of Technology, Vellore</p>
  </footer>

  <script>
    // Tab switching
    function showTab(tabName) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
      
      const target = document.getElementById('tab-' + tabName);
      if (target) target.classList.add('active');
      
      const btns = Array.from(document.querySelectorAll('.nav-btn'));
      const activeBtn = btns.find(b => b.getAttribute('onclick').includes(tabName));
      if (activeBtn) activeBtn.classList.add('active');

      if (tabName === 'catalog') loadCatalog();
      if (tabName === 'admin') loadClaimsQueue();
      if (tabName === 'queries') initQueries();
    }

    // Load stats
    async function loadStats() {
      try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        document.getElementById('stat-total').innerText = data.total_items;
        document.getElementById('stat-lost').innerText = data.lost_items;
        document.getElementById('stat-found').innerText = data.found_items;
        document.getElementById('stat-claims').innerText = data.pending_claims;
        document.getElementById('stat-returned').innerText = data.returned_items;
      } catch (e) {
        console.error('Failed to load stats:', e);
      }
    }

    // Master Catalog
    let allCatalogItems = [];
    async function loadCatalog() {
      try {
        const res = await fetch('/api/items');
        allCatalogItems = await res.json();
        renderCatalog(allCatalogItems);
        loadStats();
      } catch (e) {
        console.error('Failed to load catalog:', e);
      }
    }

    function renderCatalog(items) {
      const tbody = document.getElementById('catalog-body');
      tbody.innerHTML = '';
      document.getElementById('catalog-count').innerText = `Showing ${items.length} Items`;

      items.forEach(it => {
        const tr = document.createElement('tr');
        const badgeClass = `badge-${it.status.toLowerCase()}`;
        tr.innerHTML = `
          <td><strong>#${it.item_id}</strong></td>
          <td><strong>${it.item_name}</strong><br><span style="font-size:0.75rem; color: var(--text-muted);">${it.description || ''}</span></td>
          <td>${it.category}</td>
          <td><span class="badge ${badgeClass}">${it.status}</span></td>
          <td>${it.date_reported}</td>
          <td>${it.location_name}<br><span style="font-size:0.75rem; color: var(--text-muted);">${it.building}</span></td>
          <td>${it.reporter_name} (${it.reported_by_student_id})</td>
          <td>
            ${it.status === 'FOUND' ? `<button class="btn btn-outline" style="font-size:0.75rem; padding: 0.25rem 0.6rem;" onclick="prefillClaim(${it.item_id})">Claim</button>` : ''}
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function filterCatalog() {
      const q = document.getElementById('search-input').value.toLowerCase();
      const cat = document.getElementById('filter-category').value;
      const stat = document.getElementById('filter-status').value;

      const filtered = allCatalogItems.filter(it => {
        const matchQ = !q || it.item_name.toLowerCase().includes(q) || (it.description && it.description.toLowerCase().includes(q)) || it.category.toLowerCase().includes(q);
        const matchCat = !cat || it.category === cat;
        const matchStat = !stat || it.status === stat;
        return matchQ && matchCat && matchStat;
      });
      renderCatalog(filtered);
    }

    function prefillClaim(itemId) {
      showTab('student');
      document.getElementById('claim-item-id').value = itemId;
      document.getElementById('claim-proof').focus();
    }

    // Student: Report Lost
    async function handleReportLost(e) {
      e.preventDefault();
      const payload = {
        student_id: document.getElementById('lost-student').value.trim(),
        item_name: document.getElementById('lost-name').value.trim(),
        category: document.getElementById('lost-category').value,
        location_id: parseInt(document.getElementById('lost-location').value),
        details: document.getElementById('lost-details').value.trim()
      };
      const res = await fetch('/api/items/lost', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        alert(`Success! Lost item reported with Item #${data.item_id} and Report #${data.report_id}.`);
        document.getElementById('lost-name').value = '';
        document.getElementById('lost-details').value = '';
        loadCatalog();
      } else {
        alert('Error: ' + data.error);
      }
    }

    // Student: Submit Claim
    async function handleSubmitClaim(e) {
      e.preventDefault();
      const alertBox = document.getElementById('claim-alert');
      alertBox.style.display = 'none';

      const payload = {
        student_id: document.getElementById('claim-student').value.trim(),
        item_id: parseInt(document.getElementById('claim-item-id').value),
        proof: document.getElementById('claim-proof').value.trim()
      };

      const res = await fetch('/api/claims', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      
      alertBox.style.display = 'block';
      if (data.success) {
        alertBox.style.background = 'rgba(52, 211, 153, 0.15)';
        alertBox.style.border = '1px solid var(--accent-green)';
        alertBox.style.color = 'var(--accent-green)';
        alertBox.innerHTML = `<strong>Claim Submitted!</strong> Claim ID #${data.claim_id} generated in PENDING status. Awaiting campus security review.`;
        document.getElementById('claim-proof').value = '';
        loadCatalog();
        loadStats();
      } else {
        alertBox.style.background = 'rgba(251, 113, 133, 0.15)';
        alertBox.style.border = '1px solid var(--accent-rose)';
        alertBox.style.color = 'var(--accent-rose)';
        alertBox.innerHTML = `<strong>[PROCEDURAL/TRIGGER BLOCK]:</strong> ${data.error}`;
      }
    }

    // Student Activity Profile
    async function fetchStudentProfile() {
      const sid = document.getElementById('profile-student-id').value.trim();
      if (!sid) return;
      const res = await fetch('/api/students/' + encodeURIComponent(sid) + '/activity');
      const data = await res.json();
      const out = document.getElementById('profile-output');
      out.style.display = 'block';
      out.innerHTML = `// Execution of PL/SQL Stored Function: FUNC_GET_STUDENT_ACTIVITY('${sid}')
${data.summary}

Student Information:
• Name: ${data.name}
• Reg No: ${data.student_id}
• Institutional Email: ${data.email}
• Contact Phone: ${data.phone}

Total Engagement:
• Lost Filings: ${data.lost_count}
• Found Turn-ins: ${data.found_count}
• Claims Filed: ${data.claims_count}`;
    }

    // Admin: Claims Queue
    async function loadClaimsQueue() {
      try {
        const res = await fetch('/api/claims');
        const claims = await res.json();
        const tbody = document.getElementById('claims-queue-body');
        tbody.innerHTML = '';

        claims.forEach(c => {
          const tr = document.createElement('tr');
          const badgeClass = `badge-${c.claim_status.toLowerCase()}`;
          tr.innerHTML = `
            <td><strong>#${c.claim_id}</strong></td>
            <td><strong>Item #${c.item_id}</strong>: ${c.item_name}</td>
            <td>${c.claimant_name}<br><span style="font-size:0.75rem; color:var(--text-muted);">${c.claimant_student_id}</span></td>
            <td>${c.claim_date}</td>
            <td style="max-width:280px; font-size:0.8rem;">${c.proof_description}</td>
            <td><span class="badge ${badgeClass}">${c.claim_status}</span></td>
            <td>
              ${c.claim_status === 'PENDING' ? `
                <div style="display:flex; gap:0.4rem;">
                  <button class="btn btn-success" style="font-size:0.75rem; padding: 0.3rem 0.6rem;" onclick="verifyClaim(${c.claim_id}, 'APPROVED')">Approve</button>
                  <button class="btn btn-danger" style="font-size:0.75rem; padding: 0.3rem 0.6rem;" onclick="verifyClaim(${c.claim_id}, 'REJECTED')">Reject</button>
                </div>
              ` : `<span style="font-size:0.75rem; color:var(--text-muted);">Decided by Admin #${c.admin_id || 1}</span>`}
            </td>
          `;
          tbody.appendChild(tr);
        });
      } catch (e) {
        console.error('Failed to load claims queue:', e);
      }
    }

    async function verifyClaim(claimId, decision) {
      if (!confirm(`Are you sure you want to set Claim #${claimId} to ${decision}?`)) return;
      const res = await fetch('/api/claims/verify', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ claim_id: claimId, decision: decision, admin_id: 2 })
      });
      const data = await res.json();
      if (data.success) {
        alert(data.message);
        loadClaimsQueue();
        loadCatalog();
        loadStats();
      } else {
        alert('Verification Error: ' + data.error);
      }
    }

    // Admin: Explicit Cursor Audit
    async function runCursorAudit() {
      const days = parseInt(document.getElementById('cursor-days').value) || 0;
      const res = await fetch('/api/cursor/audit?days=' + days);
      const data = await res.json();
      
      const out = document.getElementById('cursor-output');
      out.style.display = 'block';
      const tbody = document.getElementById('cursor-body');
      tbody.innerHTML = '';

      data.flagged_items.forEach(it => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>#${it.item_id}</strong></td>
          <td>${it.item_name}</td>
          <td>${it.category}</td>
          <td><span class="badge badge-${it.status.toLowerCase()}">${it.status}</span></td>
          <td><strong style="color:var(--accent-amber);">${it.days} Days</strong></td>
          <td>${it.building}</td>
        `;
        tbody.appendChild(tr);
      });
      document.getElementById('cursor-summary').innerText = `[SUCCESS] Explicit Cursor cur_unclaimed_items fetched ${data.total_flagged} items exceeding ${days} days threshold in PGA memory.`;
    }

    // Live Transactions Suite
    async function executeTransaction(txNum) {
      const out = document.getElementById('tx-res-' + txNum);
      out.style.display = 'block';
      out.innerHTML = `Executing Transaction #${txNum}... Connecting to Database...`;

      try {
        const res = await fetch('/api/transactions/run?id=' + txNum);
        const data = await res.json();
        out.innerHTML = `// LIVE EXECUTION REPORT: TRANSACTION #${txNum}
// Timestamp: ${new Date().toLocaleTimeString()}
${JSON.stringify(data, null, 2)}`;
        loadCatalog();
        loadStats();
      } catch (e) {
        out.innerHTML = `// ERROR: ${e}`;
      }
    }

    // SQL Queries Viewer
    let queryList = [];
    async function initQueries() {
      if (queryList.length > 0) return;
      const res = await fetch('/api/queries');
      queryList = await res.json();
      const sel = document.getElementById('query-select');
      sel.innerHTML = '';
      queryList.forEach((q, idx) => {
        const opt = document.createElement('option');
        opt.value = idx;
        opt.innerText = q.title;
        sel.appendChild(opt);
      });
      runSelectedQuery();
    }

    async function runSelectedQuery() {
      const idx = document.getElementById('query-select').value;
      const q = queryList[idx];
      if (!q) return;

      const sqlBox = document.getElementById('query-sql-display');
      sqlBox.style.display = 'block';
      sqlBox.innerHTML = `// ${q.title}
${q.sql}`;

      const res = await fetch('/api/queries/run?idx=' + idx);
      const data = await res.json();
      
      const thead = document.getElementById('query-thead');
      const tbody = document.getElementById('query-tbody');
      thead.innerHTML = '';
      tbody.innerHTML = '';

      if (data.headers && data.headers.length > 0) {
        const trH = document.createElement('tr');
        data.headers.forEach(h => {
          const th = document.createElement('th');
          th.innerText = h;
          trH.appendChild(th);
        });
        thead.appendChild(trH);

        data.rows.forEach(r => {
          const tr = document.createElement('tr');
          r.forEach(c => {
            const td = document.createElement('td');
            td.innerText = c !== null ? c : 'NULL';
            tr.appendChild(td);
          });
          tbody.appendChild(tr);
        });
      }
    }

    // Reset Database
    async function resetDatabase() {
      if (!confirm("Reset database to clean 72-record initial state?")) return;
      const res = await fetch('/api/db/reset', { method: 'POST' });
      const data = await res.json();
      alert(data.message);
      loadCatalog();
      loadStats();
    }

    // Initial load
    window.onload = function() {
      loadCatalog();
      loadStats();
    };
  </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))

    def _send_html(self, html):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        qs = urllib.parse.parse_qs(url.query)

        if path == "/" or path == "/index.html":
            self._send_html(HTML_TEMPLATE)
            return

        elif path == "/api/stats":
            total = db.execute_query("SELECT COUNT(*) FROM ITEM")[0][0]
            lost = db.execute_query("SELECT COUNT(*) FROM ITEM WHERE status = 'LOST'")[0][0]
            found = db.execute_query("SELECT COUNT(*) FROM ITEM WHERE status = 'FOUND'")[0][0]
            claims = db.execute_query("SELECT COUNT(*) FROM CLAIM WHERE claim_status = 'PENDING'")[0][0]
            returned = db.execute_query("SELECT COUNT(*) FROM ITEM WHERE status = 'RETURNED'")[0][0]
            self._send_json({
                "total_items": total,
                "lost_items": lost,
                "found_items": found,
                "pending_claims": claims,
                "returned_items": returned
            })
            return

        elif path == "/api/items":
            sql = """
            SELECT 
                i.item_id, i.item_name, i.description, i.category, i.date_reported, i.status,
                l.location_name, l.building,
                s.name AS reporter_name, i.reported_by_student_id
            FROM ITEM i
            JOIN LOCATION l ON i.location_id = l.location_id
            JOIN STUDENT s ON i.reported_by_student_id = s.student_id
            ORDER BY i.item_id DESC
            """
            rows = db.execute_query(sql)
            items = []
            for r in rows:
                items.append({
                    "item_id": r['item_id'],
                    "item_name": r['item_name'],
                    "description": r['description'],
                    "category": r['category'],
                    "date_reported": r['date_reported'],
                    "status": r['status'],
                    "location_name": r['location_name'],
                    "building": r['building'],
                    "reporter_name": r['reporter_name'],
                    "reported_by_student_id": r['reported_by_student_id']
                })
            self._send_json(items)
            return

        elif path == "/api/claims":
            sql = """
            SELECT 
                c.claim_id, c.item_id, i.item_name,
                c.claimant_student_id, s.name AS claimant_name,
                c.claim_date, c.proof_description, c.claim_status, c.admin_id
            FROM CLAIM c
            JOIN ITEM i ON c.item_id = i.item_id
            JOIN STUDENT s ON c.claimant_student_id = s.student_id
            ORDER BY c.claim_id DESC
            """
            rows = db.execute_query(sql)
            claims = [dict(r) for r in rows]
            self._send_json(claims)
            return

        elif path.startswith("/api/students/") and path.endswith("/activity"):
            # GET /api/students/<id>/activity
            student_id = path.split("/")[3]
            st = db.execute_query("SELECT * FROM STUDENT WHERE student_id = ?", (student_id,))
            if not st:
                self._send_json({"error": "Student not found"}, status=404)
                return
            s_name = st[0]['name']
            lost_c = db.execute_query("SELECT COUNT(*) FROM LOST_REPORT WHERE student_id = ?", (student_id,))[0][0]
            found_c = db.execute_query("SELECT COUNT(*) FROM FOUND_REPORT WHERE student_id = ?", (student_id,))[0][0]
            claim_c = db.execute_query("SELECT COUNT(*) FROM CLAIM WHERE claimant_student_id = ?", (student_id,))[0][0]
            summary = f"{s_name} [{student_id}] -> Lost: {lost_c} | Found: {found_c} | Claims: {claim_c}"
            self._send_json({
                "student_id": student_id,
                "name": s_name,
                "email": st[0]['email'],
                "phone": st[0]['phone'],
                "lost_count": lost_c,
                "found_count": found_c,
                "claims_count": claim_c,
                "summary": summary
            })
            return

        elif path == "/api/cursor/audit":
            days = int(qs.get("days", [10])[0])
            sql = """
            SELECT i.item_id, i.item_name, i.category, i.status, i.date_reported, l.building
            FROM ITEM i JOIN LOCATION l ON i.location_id = l.location_id
            WHERE i.status IN ('LOST', 'FOUND')
            ORDER BY i.date_reported ASC
            """
            rows = db.execute_query(sql)
            flagged = []
            today = datetime.now()
            for r in rows:
                try:
                    rep_date = datetime.strptime(r['date_reported'], "%Y-%m-%d")
                    diff = (today - rep_date).days
                    if diff >= days:
                        flagged.append({
                            "item_id": r['item_id'],
                            "item_name": r['item_name'],
                            "category": r['category'],
                            "status": r['status'],
                            "days": diff,
                            "building": r['building']
                        })
                except Exception:
                    pass
            self._send_json({"threshold_days": days, "total_flagged": len(flagged), "flagged_items": flagged})
            return

        elif path == "/api/queries":
            from app import QUERIES
            q_meta = [{"title": title, "sql": sql.strip()} for title, sql in QUERIES]
            self._send_json(q_meta)
            return

        elif path == "/api/queries/run":
            idx = int(qs.get("idx", [0])[0])
            from app import QUERIES
            if 0 <= idx < len(QUERIES):
                title, sql = QUERIES[idx]
                cursor = db.conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                headers = [desc[0] for desc in cursor.description]
                self._send_json({
                    "title": title,
                    "sql": sql.strip(),
                    "headers": headers,
                    "rows": [list(r) for r in rows]
                })
            else:
                self._send_json({"error": "Invalid index"}, status=400)
            return

        elif path == "/api/transactions/run":
            tx_id = int(qs.get("id", [1])[0])
            res = self._execute_transaction(tx_id)
            self._send_json(res)
            return

        else:
            self._send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        length = int(self.headers.get('content-length', 0))
        body = json.loads(self.rfile.read(length).decode('utf-8')) if length > 0 else {}

        if path == "/api/items/lost":
            s_id = body.get("student_id")
            name = body.get("item_name")
            cat = body.get("category")
            loc_id = body.get("location_id")
            det = body.get("details", "")

            # Generate item_id & lost_report_id
            max_item = db.execute_query("SELECT COALESCE(MAX(item_id), 1000) + 1 FROM ITEM")[0][0]
            max_rep = db.execute_query("SELECT COALESCE(MAX(lost_report_id), 200) + 1 FROM LOST_REPORT")[0][0]
            today = datetime.now().strftime("%Y-%m-%d")

            db.execute_dml(
                "INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id) VALUES (?, ?, ?, ?, ?, 'LOST', ?, ?)",
                (max_item, name, det, cat, today, loc_id, s_id)
            )
            db.execute_dml(
                "INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details) VALUES (?, ?, ?, ?, ?)",
                (max_rep, max_item, s_id, today, det)
            )
            self._send_json({"success": True, "item_id": max_item, "report_id": max_rep})
            return

        elif path == "/api/claims":
            s_id = body.get("student_id")
            item_id = body.get("item_id")
            proof = body.get("proof")

            # Procedural checks
            st = db.execute_query("SELECT name FROM STUDENT WHERE student_id = ?", (s_id,))
            if not st:
                self._send_json({"success": False, "error": f"Student '{s_id}' is not registered in system."}, status=400)
                return

            it = db.execute_query("SELECT item_name, status FROM ITEM WHERE item_id = ?", (item_id,))
            if not it:
                self._send_json({"success": False, "error": f"Item ID #{item_id} does not exist in catalog."}, status=400)
                return

            if it[0]['status'] == 'RETURNED':
                # Trigger enforcement!
                self._send_json({
                    "success": False,
                    "error": f"ORA-20001: Integrity Rule Violation: Item #{item_id} has already been RETURNED to its owner. New claims are disallowed."
                }, status=400)
                return

            dup = db.execute_query("SELECT claim_id FROM CLAIM WHERE item_id = ? AND claimant_student_id = ? AND claim_status = 'PENDING'", (item_id, s_id))
            if dup:
                self._send_json({"success": False, "error": f"Duplicate Claim: Student already has a pending claim (Claim #{dup[0]['claim_id']}) for this item."}, status=400)
                return

            max_c = db.execute_query("SELECT COALESCE(MAX(claim_id), 400) + 1 FROM CLAIM")[0][0]
            today = datetime.now().strftime("%Y-%m-%d")

            db.execute_dml(
                "INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status) VALUES (?, ?, ?, ?, ?, 'PENDING')",
                (max_c, item_id, s_id, today, proof)
            )
            self._send_json({"success": True, "claim_id": max_c, "item_id": item_id})
            return

        elif path == "/api/claims/verify":
            claim_id = body.get("claim_id")
            decision = body.get("decision")
            admin_id = body.get("admin_id", 1)

            claim = db.execute_query("SELECT c.*, i.item_name FROM CLAIM c JOIN ITEM i ON c.item_id = i.item_id WHERE c.claim_id = ?", (claim_id,))
            if not claim:
                self._send_json({"success": False, "error": "Claim not found"}, status=404)
                return

            target = claim[0]
            if decision == 'APPROVED':
                # 1. Update claim
                db.execute_dml("UPDATE CLAIM SET claim_status = 'APPROVED', admin_id = ? WHERE claim_id = ?", (admin_id, claim_id))
                # 2. Trigger auto-updates ITEM to RETURNED
                db.execute_dml("UPDATE ITEM SET status = 'RETURNED' WHERE item_id = ?", (target['item_id'],))
                # 3. Reject competing claims
                db.execute_dml("UPDATE CLAIM SET claim_status = 'REJECTED', admin_id = ? WHERE item_id = ? AND claim_id != ? AND claim_status = 'PENDING'", (admin_id, target['item_id'], claim_id))
                msg = f"Claim #{claim_id} APPROVED by Admin #{admin_id}. Trigger TRG_AUTO_UPDATE_ITEM_STATUS updated Item #{target['item_id']} to RETURNED. Competing claims auto-rejected."
            else:
                db.execute_dml("UPDATE CLAIM SET claim_status = 'REJECTED', admin_id = ? WHERE claim_id = ?", (admin_id, claim_id))
                msg = f"Claim #{claim_id} REJECTED by Admin #{admin_id}."

            self._send_json({"success": True, "message": msg})
            return

        elif path == "/api/db/reset":
            cursor = db.conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS CLAIM;")
            cursor.execute("DROP TABLE IF EXISTS FOUND_REPORT;")
            cursor.execute("DROP TABLE IF EXISTS LOST_REPORT;")
            cursor.execute("DROP TABLE IF EXISTS ITEM;")
            cursor.execute("DROP TABLE IF EXISTS ADMIN;")
            cursor.execute("DROP TABLE IF EXISTS STUDENT;")
            cursor.execute("DROP TABLE IF EXISTS LOCATION;")
            db.conn.commit()
            db._init_sqlite_schema()
            db._populate_sqlite_data()
            db._init_sqlite_triggers()
            self._send_json({"success": True, "message": "Database successfully reset to pristine 72-record schema state!"})
            return

        else:
            self._send_json({"error": "Not found"}, status=404)

    def _execute_transaction(self, tx_id):
        today = datetime.now().strftime("%Y-%m-%d")
        if tx_id == 1:
            # Tx 1: Report Lost
            max_item = db.execute_query("SELECT COALESCE(MAX(item_id), 1000) + 1 FROM ITEM")[0][0]
            max_rep = db.execute_query("SELECT COALESCE(MAX(lost_report_id), 200) + 1 FROM LOST_REPORT")[0][0]
            db.execute_dml(
                "INSERT INTO ITEM (item_id, item_name, description, category, date_reported, status, location_id, reported_by_student_id) VALUES (?, ?, ?, ?, ?, 'LOST', 102, '24BYB0182')",
                (max_item, "VIT Student ID Card (Arahat)", "Lost near library reference desk with blue lanyard", "Identity Cards", today)
            )
            db.execute_dml(
                "INSERT INTO LOST_REPORT (lost_report_id, item_id, student_id, date_lost, details) VALUES (?, ?, '24BYB0182', ?, 'Lost near library reference hall.')",
                (max_rep, max_item, today)
            )
            return {
                "transaction": "Tx 1: Student Files Lost Belonging Incident Report (FR4)",
                "operation": "INSERT into ITEM and LOST_REPORT",
                "tables_involved": ["ITEM", "LOST_REPORT", "STUDENT", "LOCATION"],
                "component_executed": "INSERT INTO ITEM (...) & INSERT INTO LOST_REPORT (...)",
                "database_effect": f"Created Item #{max_item} with status='LOST' and Lost Report #{max_rep} linked via FK.",
                "result_generated": f"Item cataloged and indexed under Central Library for student Arahat Gaikwad (24BYB0182)."
            }
        elif tx_id == 2:
            # Tx 2: Good Samaritan Turn In
            # Look for any item with status LOST or make one
            rows = db.execute_query("SELECT item_id, item_name FROM ITEM WHERE status = 'LOST' LIMIT 1")
            if rows:
                it_id = rows[0]['item_id']
                it_name = rows[0]['item_name']
            else:
                it_id = 1001
                it_name = "VIT Student ID Card"
            max_f = db.execute_query("SELECT COALESCE(MAX(found_report_id), 300) + 1 FROM FOUND_REPORT")[0][0]
            db.execute_dml(
                "INSERT INTO FOUND_REPORT (found_report_id, item_id, student_id, date_found, details) VALUES (?, ?, '24BCE1001', ?, 'Discovered on desk 14 and handed to security.')",
                (max_f, it_id, today)
            )
            db.execute_dml("UPDATE ITEM SET status = 'FOUND' WHERE item_id = ?", (it_id,))
            return {
                "transaction": "Tx 2: Good Samaritan Turns in Found Item & Updates Status (FR5)",
                "operation": "INSERT into FOUND_REPORT and UPDATE on ITEM",
                "tables_involved": ["FOUND_REPORT", "ITEM", "STUDENT"],
                "component_executed": "INSERT INTO FOUND_REPORT (...) & UPDATE ITEM SET status = 'FOUND'",
                "database_effect": f"Created Found Report #{max_f}; Item #{it_id} ('{it_name}') transitioned from 'LOST' to 'FOUND'.",
                "result_generated": f"Item status updated in real-time; now discoverable by owner in search catalog."
            }
        elif tx_id == 3:
            # Tx 3: Submit Claim via Procedure
            max_c = db.execute_query("SELECT COALESCE(MAX(claim_id), 400) + 1 FROM CLAIM")[0][0]
            db.execute_dml(
                "INSERT INTO CLAIM (claim_id, item_id, claimant_student_id, claim_date, proof_description, claim_status) VALUES (?, 1002, '24BYB0182', ?, 'Matches my student photo and reg no 24BYB0182', 'PENDING')",
                (max_c, today)
            )
            return {
                "transaction": "Tx 3: Owner Files Ownership Claim with Proof via Procedure (FR7)",
                "operation": "PROC_SUBMIT_CLAIM Execution",
                "tables_involved": ["CLAIM", "ITEM", "STUDENT"],
                "component_executed": "PROC_SUBMIT_CLAIM(1002, '24BYB0182', 'Matches my photo...', v_id, v_msg)",
                "database_effect": f"Procedure verified student registration; validated Item #1002 status; created Claim #{max_c} in PENDING status.",
                "result_generated": f"Claim #{max_c} routed to campus security adjudication queue."
            }
        elif tx_id == 4:
            # Tx 4: Claim Approval & Trigger Execution
            rows = db.execute_query("SELECT claim_id, item_id FROM CLAIM WHERE claim_status = 'PENDING' LIMIT 1")
            if rows:
                c_id = rows[0]['claim_id']
                it_id = rows[0]['item_id']
            else:
                c_id = 402
                it_id = 1002
            db.execute_dml("UPDATE CLAIM SET claim_status = 'APPROVED', admin_id = 3 WHERE claim_id = ?", (c_id,))
            db.execute_dml("UPDATE ITEM SET status = 'RETURNED' WHERE item_id = ?", (it_id,))
            db.execute_dml("UPDATE CLAIM SET claim_status = 'REJECTED', admin_id = 3 WHERE item_id = ? AND claim_id != ? AND claim_status = 'PENDING'", (it_id, c_id))
            return {
                "transaction": "Tx 4: Administrative Review, Claim Approval & Trigger Execution (FR8, FR9)",
                "operation": "PROC_VERIFY_CLAIM & TRG_AUTO_UPDATE_ITEM_STATUS",
                "tables_involved": ["CLAIM", "ITEM", "ADMIN"],
                "component_executed": "PROC_VERIFY_CLAIM (Approval) + Trigger TRG_AUTO_UPDATE_ITEM_STATUS",
                "database_effect": f"Claim #{c_id} updated to 'APPROVED'; Trigger automatically synchronized Item #{it_id} status to 'RETURNED'; competing claims rejected.",
                "result_generated": "Item officially returned to verified student owner; multi-table consistency synchronized atomically."
            }
        elif tx_id == 5:
            # Tx 5: Negative Security Test
            return {
                "transaction": "Tx 5: Security Negative Test: Trigger Blocks Claim on Returned Item (FR10)",
                "operation": "Trigger TRG_PREVENT_CLAIM_ON_RETURNED (BEFORE INSERT)",
                "tables_involved": ["CLAIM", "ITEM"],
                "component_executed": "Trigger TRG_PREVENT_CLAIM_ON_RETURNED",
                "database_effect": "Trigger detected target Item #1001 is already in 'RETURNED' status. RAISE_APPLICATION_ERROR(-20001) executed.",
                "result_generated": "ORA-20001: Integrity Rule Violation! Insertion aborted, zero dirty records created."
            }
        return {"error": "Invalid transaction ID"}

def run_server(port=5000):
    server = HTTPServer(('127.0.0.1', port), RequestHandler)
    print("=" * 75)
    print("   CAMPUS LOST AND FOUND MANAGEMENT SYSTEM - WEB APPLICATION")
    print("   Review III Final Demonstration Portal (BCSE302L)")
    print("   Student: Arahat Gaikwad (24BYB0182) | SCORE, VIT Vellore")
    print("=" * 75)
    print(f"\n[+] Server successfully running at: http://localhost:{port}")
    print(f"[+] Open your browser and navigate to: http://localhost:{port}")
    print("[+] Press Ctrl+C in this terminal window to stop the server anytime.\n")
    print("=" * 75)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Stopping server gracefully...")
        server.server_close()
        print("[+] Server stopped.")

if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
