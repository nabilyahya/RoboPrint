---
aliases: [Robonarim Print Server, Local Print Server]
tags: [print-server, pos, thermal-printer, robonarim]
title: "Robonarim — Local Print Server (Windows, USB / POS-58)"
description: "A small practical print server that accepts print jobs (text + optional logo) and sends raw ESC/POS bytes to a local USB thermal printer (tested with POS-58 / Zjiang ZJ-5890K). Includes a lightweight web UI and two print modes."
icon: "🖨️"
---

# Robonarim — Local Print Server (Windows, USB / POS-58) 🖨️

> **Short summary**  
> A small, practical print server that accepts print jobs (text + optional logo) and sends raw ESC/POS bytes to a local USB thermal printer (tested with **POS-58 / Zjiang ZJ-5890K**). Includes a lightweight web UI (`roboprint-local.html`) for manual testing and two print modes.

---

## 🎯 Features — المميزات
- **Two print modes**
  - `main` — normal invoice / receipt layout (header, separator, full text).
  - `ticket` — compact ticket layout (small line spacing, fits visually into a tiny **4cm × 2cm** area).
- Auto-generated date `DD/MM/YYYY` in UI templates.  
- Optional logo upload (sent as Base64). Server can be extended to convert logo → ESC/POS raster using **Pillow**.  
- Simple API endpoint: `POST /print` (supports `printer`, `text`, `mode`, `logo`).  
- Works reliably on **Windows** (uses `pywin32` / `win32print`).

---

## 📂 Contents — مكونات المشروع
- `print_server.py` — Flask server that sends RAW ESC/POS to Windows printers via `win32print`.  
- `roboprint-local.html` — browser UI to choose printer, build templates and send print jobs.  
- Optional: `direct_print.py` — quick direct-print test script.

---

## ⚙️ Prerequisites — المتطلبات
- **Windows** (server uses `win32print`).  
- **Python 3.8+** (3.11 recommended if compatibility issues arise).  
- Thermal printer installed in Windows (e.g. **POS-58** driver).  
- Basic command-line familiarity.

---

## 🚀 Quick start (Windows) — بداية سريعة
Follow these commands in PowerShell inside your project folder.

```powershell
# 1. Clone & enter repo (example)
git clone <your-repo-url>
cd repo-folder

# 2. Create & activate virtual environment
python -m venv venv
.env\Scripts\Activate

# 3. Install dependencies
pip install --upgrade pip setuptools wheel
pip install flask pywin32

# Optional (for image raster support)
pip install pillow
```

- Ensure `roboprint-local.html` is placed in the same folder as `print_server.py`.
- Start the server:
```powershell
python print_server.py
```
- Open the UI: `http://localhost:5000/` — choose printer, mode (`main` or `ticket`), adjust name/code, optionally upload a logo, then click **Print**.

---

## 🔌 API (short) — واجهة برمجة التطبيقات
### `GET /printers`
Return JSON list of available Windows printers.

### `POST /print`
Send print job. JSON body:
```json
{
  "printer": "POS-58",
  "text": "Musteri Adi: Ahmet Yilmaz\nMusteri Kodu: 1234567\nTeslim Tarihi: 05/10/2025",
  "mode": "ticket",    // "main" or "ticket"
  "logo": "data:image/png;base64,...." // optional
}
```

> Tip: Add a simple API key check using the `x-api-key` header in `print_server.py` for basic protection when exposing the service.

---

## 🛠️ Notes & Tips — ملاحظات ونصائح
- **Ticket size**: The `ticket` mode compacts text and reduces line spacing to visually fit a small ticket. Physical paper width is still the printer's width (typically 58mm). For pixel-perfect 4×2 cm output, render the ticket as an image at target DPI and print as ESC/POS raster.  
- **Logo support**: If you need crisp logo printing, install `Pillow` and enable raster conversion on the server (Base64 → PIL → 1-bit dither → ESC/POS raster).  
- **Encoding**: Turkish characters are handled by trying `cp1254` → `cp857` → `utf-8`. Force `cp1254` if you see garbled text.  
- **Cut command**: If `GS V 0` (`\x1D\x56\x00`) doesn't cut, try variants like `\x1D\x56\x41\x00`.

---

## ✅ Next steps (integration ideas)
- Connect your **Next.js** app: client → Next API route → forward to this print server (secure with `x-api-key`).  
- Convert `print_server.py` to an EXE with `pyinstaller` (see separate instructions) for portable deployment.  
- Enable image/raster printing for accurate ticket sizes and logo fidelity.

---

## License & Credits
Recommend **MIT** license for this repo. Add a `LICENSE` file if you want to open-source.

---

If you want, I can:
- produce an **Obsidian vault** layout with this README and additional notes, or  
- generate a `README` that includes build commands for `pyinstaller` and a ready-made `.spec` file.

