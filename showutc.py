#!/usr/bin/env python3
"""showutc: ekranın sağ üst köşesinde Unix zaman damgası ve saat gösteren küçük pencere.

Gösterilenler:
  - Ham Unix zamanı (ms, 1970-01-01 00:00 UTC'den beri)
  - Yerel saat  SS:DD:ss.mmm
  - UTC saat    SS:DD:ss.mmm

Kullanım:  showutc            (terminalden; Ctrl+C ya da pencerede Esc / sağ tık ile kapanır)
           showutc --left     (sol üst köşeye koy)
Pencere sürüklenerek taşınabilir; çift tık raw değeri panoya kopyalar.
"""

import argparse
import signal
import time
import tkinter as tk
from datetime import datetime, timezone

REFRESH_MS = 15          # ~60 Hz; ms hanesi akıcı görünür
MARGIN = 12              # ekran kenarından boşluk
BG, FG, DIM, ACCENT = "#11181f", "#e2e8f0", "#7a8c9c", "#00d68f"
MONO = ("DejaVu Sans Mono", 11)


def main():
    parser = argparse.ArgumentParser(description="Unix zaman damgası göstergesi")
    parser.add_argument("--left", action="store_true", help="sol üst köşeye yerleştir")
    args = parser.parse_args()

    root = tk.Tk()
    root.title("showutc")
    root.overrideredirect(True)          # çerçevesiz
    root.attributes("-topmost", True)    # her zaman üstte
    root.configure(bg=BG)

    frame = tk.Frame(root, bg=BG, padx=10, pady=6,
                     highlightthickness=1, highlightbackground="#2a3744")
    frame.pack()
    raw = tk.Label(frame, font=(MONO[0], 13, "bold"), fg=ACCENT, bg=BG, anchor="e")
    local = tk.Label(frame, font=MONO, fg=FG, bg=BG, anchor="e")
    utc = tk.Label(frame, font=MONO, fg=DIM, bg=BG, anchor="e")
    for label in (raw, local, utc):
        label.pack(fill="x")

    def tick():
        now_ns = time.time_ns()
        ms = now_ns // 1_000_000
        stamp = datetime.fromtimestamp(ms / 1000)
        raw.configure(text=f"{ms}")
        local.configure(text=f"yerel {stamp:%H:%M:%S}.{ms % 1000:03d}")
        utc.configure(text=f"UTC   {datetime.fromtimestamp(ms / 1000, timezone.utc):%H:%M:%S}.{ms % 1000:03d}")
        root.after(REFRESH_MS, tick)

    def place():
        root.update_idletasks()
        w, h = root.winfo_reqwidth(), root.winfo_reqheight()
        x = MARGIN if args.left else root.winfo_screenwidth() - w - MARGIN
        root.geometry(f"+{x}+{MARGIN}")

    # Sürükleyerek taşıma
    drag = {"x": 0, "y": 0}

    def start_drag(event):
        drag["x"], drag["y"] = event.x_root - root.winfo_x(), event.y_root - root.winfo_y()

    def do_drag(event):
        root.geometry(f"+{event.x_root - drag['x']}+{event.y_root - drag['y']}")

    def copy_raw(_event):
        root.clipboard_clear()
        root.clipboard_append(raw.cget("text"))

    for widget in (root, frame, raw, local, utc):
        widget.bind("<ButtonPress-1>", start_drag)
        widget.bind("<B1-Motion>", do_drag)
        widget.bind("<Double-Button-1>", copy_raw)
        widget.bind("<Button-3>", lambda _e: root.destroy())
    root.bind("<Escape>", lambda _e: root.destroy())

    # Terminalde Ctrl+C ile kapanabilsin (Tk döngüsü sinyali kendiliğinden görmez).
    signal.signal(signal.SIGINT, lambda *_: root.destroy())
    def poll_signals():
        root.after(200, poll_signals)
    poll_signals()

    tick()
    place()
    root.mainloop()


if __name__ == "__main__":
    main()
