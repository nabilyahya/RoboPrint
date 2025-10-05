# print_server.py (updated - supports main & ticket modes)
from flask import Flask, request, jsonify, send_from_directory
import win32print
import os
import sys
import base64

app = Flask(__name__)

# helper: get printers
def list_printers():
    printers = []
    try:
        for flags, description, name, comment in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS):
            printers.append({"name": name, "description": description})
    except Exception as e:
        print("EnumPrinters error:", e)
    return printers

@app.route('/printers', methods=['GET'])
def printers():
    return jsonify(list_printers())

@app.route('/print', methods=['POST'])
def do_print():
    data = request.get_json() or {}
    printer_name = data.get('printer') or win32print.GetDefaultPrinter()
    text = data.get('text', '')
    mode = data.get('mode', 'main')
    logo_dataurl = data.get('logo')  # optional DataURL

    if not printer_name:
        return jsonify({"ok": False, "error": "No printer found"}), 400

    try:
        # Basic ESC/POS pieces
        INIT = b'\x1B\x40'             # Initialize
        CENTER = b'\x1B\x61\x01'
        LEFT = b'\x1B\x61\x00'
        DOUBLE = b'\x1D\x21\x11'      # double width+height
        NORMAL = b'\x1D\x21\x00'
        CUT = b'\x1D\x56\x00'         # partial cut (may vary by model)
        # Line spacing control:
        SET_LINE_SPACING = lambda n: b'\x1B\x33' + bytes([n])  # ESC 3 n
        RESET_LINE_SPACING = b'\x1B\x32'  # ESC 2 (default)

        # encoding: try windows turkish cp1254, fallback cp857, fallback utf-8
        def encode_text(s):
            for enc in ('cp1254', 'cp857', 'utf-8'):
                try:
                    return s.encode(enc), enc
                except Exception:
                    continue
            return s.encode('utf-8'), 'utf-8'

        if mode == 'main':
            # Build main invoice payload: header large, separator, body text as provided, feed, cut
            header = '   ROBONARIM\n'
            sep = '-------------------------------\n'
            # encode body using helper
            body_bytes, used_enc = encode_text(text + '\n\n\n')
            header_bytes = header.encode(used_enc, errors='replace')
            sep_bytes = sep.encode('ascii', errors='replace')

            data = INIT + CENTER + DOUBLE + header_bytes + NORMAL + sep_bytes + LEFT + body_bytes + CUT

        elif mode == 'ticket':
            # Compact ticket: set small line spacing and use compact layout to fit ~2cm height
            # We set line spacing to 20 dots (~2.5mm) so overall height stays small.
            # Note: exact 2cm depends on printer dots/mm; this is an approximation that works well on common 203dpi printers.
            ls = 20  # line spacing in dots (experimentally chosen)
            body = text.strip()

            # Build sequence:
            # init, set small line spacing, center name + code + date in compact lines, few feeds, reset spacing, cut
            _, used_enc = encode_text(body)
            # We'll send the body as-is; but ensure we don't send too many lines.
            # If user accidentally entered many lines, truncate to first 6.
            lines = body.splitlines()
            lines = [ln.strip() for ln in lines if ln.strip() != '']
            lines = lines[:6]  # keep compact

            payload = bytearray()
            payload += INIT
            payload += SET_LINE_SPACING(ls)   # tighten
            payload += CENTER
            # print each line centered with normal size
            for ln in lines:
                try:
                    payload += ln.encode(used_enc, errors='replace') + b'\n'
                except Exception:
                    payload += ln.encode('utf-8', errors='replace') + b'\n'
            payload += b'\n'  # small feed
            payload += RESET_LINE_SPACING
            payload += CUT
            data = bytes(payload)

        else:
            return jsonify({"ok": False, "error": "Unknown mode"}), 400

        # send to printer as RAW
        h = win32print.OpenPrinter(printer_name)
        try:
            job_id = win32print.StartDocPrinter(h, 1, ("Robonarim Print", None, "RAW"))
            win32print.StartPagePrinter(h)
            win32print.WritePrinter(h, data)
            win32print.EndPagePrinter(h)
            win32print.EndDocPrinter(h)
        finally:
            win32print.ClosePrinter(h)

        return jsonify({"ok": True, "printer": printer_name, "mode": mode})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# serve simple html file if exists
@app.route('/')
def index():
    if os.path.exists('roboprint-local.html'):
        return send_from_directory('.', 'roboprint-local.html')
    return "Print server running. Put roboprint-local.html in same folder."

if __name__ == '__main__':
    app.run(port=5000, debug=True)
