Robonarim — Local Print Server (Windows, USB / POS-58)

A small, practical print server that accepts print jobs (text + optional logo) and sends raw ESC/POS bytes to a local USB thermal printer (tested with POS-58 / Zjiang ZJ-5890K).
Includes a lightweight web UI (roboprint-local.html) for manual testing and two print modes:

main — normal invoice / receipt layout (header, separator, full text).

ticket — compact ticket layout (small line spacing, fits visually into a tiny 4cm × 2cm area).

This README explains installation, usage, API, Next.js integration, customization and debugging.

Contents

print_server.py — Flask server that sends RAW ESC/POS to Windows printers via win32print.

roboprint-local.html — browser UI to choose printer, build templates and send print jobs.

Optional: direct_print.py — quick direct-print test script.

Features

Print text in two modes: main and ticket.

Auto-generated date DD/MM/YYYY in UI templates.

Optional logo upload (sent as Base64). Server can be extended to convert logo → ESC/POS raster (Pillow).

Simple API (/print) with optional API key header for basic security.

Works reliably on Windows (uses pywin32/win32print).

Prerequisites

Windows (server uses win32print).

Python 3.8+ (3.11 recommended if compatibility issues arise).

Thermal printer installed in Windows (e.g. POS-58 driver).

Basic command-line familiarity.

Quick start (Windows)

Clone the repo and cd into it:
git clone <your-repo-url>
cd repo-folder

Create & activate a virtual environment:
python -m venv venv
.\venv\Scripts\Activate

Install dependencies:
pip install --upgrade pip setuptools wheel
pip install flask pywin32
Optional (for image raster support):
pip install pillow

Place roboprint-local.html in the same folder as print_server.py (it already is in this repo).

Start the server:
python print_server.py

Open UI in the browser:
http://localhost:5000/ — choose printer, mode (main or ticket), adjust name/code, optionally upload a logo, then click Print.

