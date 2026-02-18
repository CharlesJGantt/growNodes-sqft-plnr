"""
Square Foot Garden Planner
A Tkinter desktop app for planning raised-bed vegetable gardens.
"""

import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ─── Crop Database ────────────────────────────────────────────────────────────

CROP_DATA = {
    "Tomatoes":  {"plants_per_sqft": 1,  "color": "#E74C3C", "spacing": "18–24 in"},
    "Peppers":   {"plants_per_sqft": 1,  "color": "#E67E22", "spacing": "12–15 in"},
    "Lettuce":   {"plants_per_sqft": 4,  "color": "#A8E063", "spacing": "6 in"},
    "Spinach":   {"plants_per_sqft": 9,  "color": "#27AE60", "spacing": "4 in"},
    "Carrots":   {"plants_per_sqft": 16, "color": "#F39C12", "spacing": "3 in"},
    "Radishes":  {"plants_per_sqft": 16, "color": "#E91E8C", "spacing": "3 in"},
    "Beans":     {"plants_per_sqft": 9,  "color": "#8BC34A", "spacing": "4 in"},
    "Basil":     {"plants_per_sqft": 4,  "color": "#1ABC9C", "spacing": "6 in"},
    "Cucumbers": {"plants_per_sqft": 2,  "color": "#48C9B0", "spacing": "8 in"},
    "Zucchini":  {"plants_per_sqft": 1,  "color": "#F1C40F", "spacing": "18 in"},
    "Kale":      {"plants_per_sqft": 1,  "color": "#1E8449", "spacing": "12 in"},
    "Onions":    {"plants_per_sqft": 16, "color": "#BB8FCE", "spacing": "3 in"},
    "Peas":      {"plants_per_sqft": 8,  "color": "#A9DFBF", "spacing": "4–6 in"},
}

EMPTY_COLOR     = "#E8DCC8"
GRID_LINE_COLOR = "#7D6B4F"
HOVER_COLOR     = "#FFD700"
CELL_SIZE       = 80   # pixels per square foot
PAD             = 30   # canvas edge padding


# ─── Main Application ─────────────────────────────────────────────────────────

class GardenPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Square Foot Garden Planner")
        self.root.configure(bg="#2D5016")

        self.rows = 4
        self.cols = 8
        self.grid_data = {}        # (row, col) -> crop name or None
        self.current_file = None
        self.hovered_cell = None
        self.selected_crop = tk.StringVar(value="Tomatoes")

        self._build_menu()
        self._build_ui()
        self._init_grid()
        self._draw_grid()
        self._update_sidebar()

    # ─── Menu Bar ─────────────────────────────────────────────────────────────

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Garden",  accelerator="Ctrl+N", command=self._new_garden)
        file_menu.add_command(label="Open…",        accelerator="Ctrl+O", command=self._load_file)
        file_menu.add_command(label="Save",          accelerator="Ctrl+S", command=self._save_file)
        file_menu.add_command(label="Save As…",      command=self._save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        garden_menu = tk.Menu(menubar, tearoff=0)
        garden_menu.add_command(label="Resize Garden Bed…", command=self._resize_garden)
        garden_menu.add_command(label="Clear All Squares",   command=self._clear_all)
        menubar.add_cascade(label="Garden", menu=garden_menu)

        self.root.config(menu=menubar)
        self.root.bind("<Control-n>", lambda e: self._new_garden())
        self.root.bind("<Control-o>", lambda e: self._load_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())

    # ─── UI Layout ────────────────────────────────────────────────────────────

    def _build_ui(self):
        outer = tk.Frame(self.root, bg="#2D5016")
        outer.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # ── Left: canvas + controls ──────────────────────────────────────────
        left = tk.Frame(outer, bg="#2D5016")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            left, text="Square Foot Garden Planner",
            font=("Georgia", 16, "bold"),
            bg="#2D5016", fg="#F5F5DC",
        ).pack(pady=(0, 8))

        # Canvas with scrollbars
        cv_wrap = tk.Frame(left, bg="#2D5016")
        cv_wrap.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            cv_wrap, bg="#6B4C2A",
            highlightthickness=3,
            highlightbackground="#3A7D44",
            cursor="hand2",
        )
        h_bar = ttk.Scrollbar(cv_wrap, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_bar = ttk.Scrollbar(cv_wrap, orient=tk.VERTICAL,   command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_bar.set, yscrollcommand=v_bar.set)

        h_bar.pack(side=tk.BOTTOM, fill=tk.X)
        v_bar.pack(side=tk.RIGHT,  fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.canvas.bind("<Motion>",   self._on_hover)
        self.canvas.bind("<Leave>",    lambda e: self._clear_hover())

        # Crop selector bar
        sel = tk.Frame(left, bg="#2D5016", pady=8)
        sel.pack(fill=tk.X)

        tk.Label(
            sel, text="Plant:", bg="#2D5016", fg="#F5F5DC",
            font=("Helvetica", 11, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 4))

        self.crop_cb = ttk.Combobox(
            sel, textvariable=self.selected_crop,
            values=list(CROP_DATA.keys()),
            state="readonly", width=13,
            font=("Helvetica", 11),
        )
        self.crop_cb.pack(side=tk.LEFT)

        self.swatch = tk.Label(sel, width=3, relief="solid", bd=1)
        self.swatch.pack(side=tk.LEFT, padx=7)

        self.info_lbl = tk.Label(sel, bg="#2D5016", fg="#C8E6C9", font=("Helvetica", 9))
        self.info_lbl.pack(side=tk.LEFT)

        tk.Label(
            sel, text="Left-click = plant  ·  Right-click = clear",
            bg="#2D5016", fg="#7CB87C", font=("Helvetica", 9),
        ).pack(side=tk.RIGHT, padx=6)

        self.selected_crop.trace_add("write", self._refresh_swatch)
        self._refresh_swatch()

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(
            left, textvariable=self.status_var,
            bg="#1A3209", fg="#A5D6A7",
            font=("Helvetica", 9), anchor="w", padx=8, pady=3,
        ).pack(fill=tk.X, pady=(4, 0))

        # ── Right: sidebar ───────────────────────────────────────────────────
        self._build_sidebar(outer)

    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg="#1A3209", width=238, relief="ridge", bd=2)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(12, 0))
        sidebar.pack_propagate(False)

        def section(text):
            tk.Label(
                sidebar, text=text, bg="#1A3209", fg="#F5F5DC",
                font=("Helvetica", 10, "bold"),
            ).pack(pady=(12, 2), padx=10, anchor="w")
            ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X, padx=8, pady=(0, 4))

        # Legend
        section("CROP LEGEND")
        leg = tk.Frame(sidebar, bg="#1A3209")
        leg.pack(fill=tk.X, padx=8)

        for crop, data in CROP_DATA.items():
            row = tk.Frame(leg, bg="#1A3209")
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, width=3, bg=data["color"], relief="solid", bd=1
                     ).pack(side=tk.LEFT, padx=(0, 6))
            tk.Label(
                row,
                text=f"{crop}  ({data['plants_per_sqft']}/sqft)",
                bg="#1A3209", fg="#E8F5E9",
                font=("Helvetica", 8), anchor="w",
            ).pack(side=tk.LEFT)

        # Planted summary
        section("PLANTED SUMMARY")
        self.summary_frame = tk.Frame(sidebar, bg="#1A3209")
        self.summary_frame.pack(fill=tk.BOTH, expand=True, padx=8)

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X, padx=8, pady=6)
        self.stats_lbl = tk.Label(
            sidebar, bg="#1A3209", fg="#81C784",
            font=("Helvetica", 9), justify="left", padx=8,
        )
        self.stats_lbl.pack(anchor="w", pady=(0, 10))

    # ─── Grid Drawing ─────────────────────────────────────────────────────────

    def _init_grid(self):
        self.grid_data = {
            (r, c): None
            for r in range(self.rows)
            for c in range(self.cols)
        }

    def _draw_grid(self):
        self.canvas.delete("all")
        SZ = CELL_SIZE

        total_w = self.cols * SZ + PAD * 2
        total_h = self.rows * SZ + PAD * 2
        self.canvas.configure(scrollregion=(0, 0, total_w, total_h))

        # Raised-bed border
        self.canvas.create_rectangle(
            PAD - 8, PAD - 8,
            PAD + self.cols * SZ + 8,
            PAD + self.rows * SZ + 8,
            fill="#3E2107", outline="#1F0F03", width=5,
        )

        # Draw each cell
        for r in range(self.rows):
            for c in range(self.cols):
                crop  = self.grid_data.get((r, c))
                color = CROP_DATA[crop]["color"] if crop else EMPTY_COLOR
                x1 = PAD + c * SZ
                y1 = PAD + r * SZ
                x2 = x1 + SZ
                y2 = y1 + SZ

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color, outline=GRID_LINE_COLOR, width=1,
                    tags="cell",
                )

                if crop:
                    n     = CROP_DATA[crop]["plants_per_sqft"]
                    label = crop if len(crop) <= 7 else crop[:6] + "."
                    cx, cy = x1 + SZ // 2, y1 + SZ // 2
                    self.canvas.create_text(
                        cx, cy - 8, text=label,
                        font=("Helvetica", 8, "bold"), fill="#111111",
                    )
                    self.canvas.create_text(
                        cx, cy + 8, text=f"× {n}",
                        font=("Helvetica", 8), fill="#333333",
                    )
                else:
                    self.canvas.create_text(
                        x1 + 5, y1 + 4, text=f"{r+1},{c+1}",
                        font=("Helvetica", 6), fill="#B0A090", anchor="nw",
                    )

        # Row numbers (left)
        for r in range(self.rows):
            self.canvas.create_text(
                PAD - 12, PAD + r * SZ + SZ // 2,
                text=str(r + 1),
                font=("Helvetica", 8, "bold"), fill="#F5F5DC", anchor="e",
            )

        # Column numbers (top)
        for c in range(self.cols):
            self.canvas.create_text(
                PAD + c * SZ + SZ // 2, PAD - 12,
                text=str(c + 1),
                font=("Helvetica", 8, "bold"), fill="#F5F5DC", anchor="s",
            )

        self._draw_hover_highlight()

    # ─── Canvas Interaction ───────────────────────────────────────────────────

    def _cell_from_event(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        col = int((cx - PAD) // CELL_SIZE)
        row = int((cy - PAD) // CELL_SIZE)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None

    def _on_click(self, event):
        cell = self._cell_from_event(event)
        if cell:
            r, c = cell
            self.grid_data[(r, c)] = self.selected_crop.get()
            self._draw_grid()
            self._update_sidebar()

    def _on_right_click(self, event):
        cell = self._cell_from_event(event)
        if cell:
            r, c = cell
            self.grid_data[(r, c)] = None
            self._draw_grid()
            self._update_sidebar()

    def _on_hover(self, event):
        cell = self._cell_from_event(event)
        if cell != self.hovered_cell:
            self.hovered_cell = cell
            self._draw_hover_highlight()

        if cell:
            r, c = cell
            crop = self.grid_data.get(cell)
            if crop:
                n  = CROP_DATA[crop]["plants_per_sqft"]
                sp = CROP_DATA[crop]["spacing"]
                self.status_var.set(
                    f"Row {r+1}, Col {c+1}  ·  {crop}  ·  "
                    f"{n} plant(s)/sqft  ·  Spacing: {sp}"
                )
            else:
                self.status_var.set(
                    f"Row {r+1}, Col {c+1}  ·  Empty  —  "
                    f"click to plant {self.selected_crop.get()}"
                )
        else:
            self.status_var.set("Ready")

    def _clear_hover(self):
        self.hovered_cell = None
        self._draw_hover_highlight()
        self.status_var.set("Ready")

    def _draw_hover_highlight(self):
        self.canvas.delete("hover")
        if self.hovered_cell:
            r, c = self.hovered_cell
            x1 = PAD + c * CELL_SIZE
            y1 = PAD + r * CELL_SIZE
            self.canvas.create_rectangle(
                x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE,
                outline=HOVER_COLOR, width=3, tags="hover",
            )

    # ─── Sidebar Updates ──────────────────────────────────────────────────────

    def _refresh_swatch(self, *_):
        crop = self.selected_crop.get()
        if crop not in CROP_DATA:
            return
        d = CROP_DATA[crop]
        self.swatch.configure(bg=d["color"])
        self.info_lbl.configure(
            text=f"{d['plants_per_sqft']} plant(s)/sqft  ·  Spacing: {d['spacing']}"
        )

    def _update_sidebar(self):
        for w in self.summary_frame.winfo_children():
            w.destroy()

        # Tally planted squares per crop
        counts = {}
        for crop in self.grid_data.values():
            if crop:
                counts[crop] = counts.get(crop, 0) + 1

        if not counts:
            tk.Label(
                self.summary_frame, text="Nothing planted yet.",
                bg="#1A3209", fg="#6A9E6A",
                font=("Helvetica", 9, "italic"),
            ).pack(pady=10)
        else:
            for crop in sorted(counts):
                squares = counts[crop]
                total   = squares * CROP_DATA[crop]["plants_per_sqft"]
                row = tk.Frame(self.summary_frame, bg="#1A3209")
                row.pack(fill=tk.X, pady=2)

                tk.Label(row, width=3, bg=CROP_DATA[crop]["color"],
                         relief="solid", bd=1).pack(side=tk.LEFT, padx=(0, 5))
                tk.Label(
                    row, text=crop, bg="#1A3209", fg="#F5F5DC",
                    font=("Helvetica", 9, "bold"), anchor="w",
                ).pack(side=tk.LEFT)
                tk.Label(
                    row, text=f"{squares} sq · {total} plants",
                    bg="#1A3209", fg="#81C784",
                    font=("Helvetica", 8),
                ).pack(side=tk.RIGHT)

        # Stats footer
        total_sq   = self.rows * self.cols
        planted_sq = sum(1 for v in self.grid_data.values() if v)
        total_pl   = sum(
            CROP_DATA[v]["plants_per_sqft"]
            for v in self.grid_data.values() if v
        )
        pct = int(100 * planted_sq / total_sq) if total_sq else 0
        self.stats_lbl.configure(
            text=(
                f"Bed: {self.rows} × {self.cols}  ({total_sq} sqft)\n"
                f"Planted: {planted_sq}/{total_sq} squares  ({pct}%)\n"
                f"Total plants: {total_pl}"
            )
        )

    # ─── Garden Actions ───────────────────────────────────────────────────────

    def _new_garden(self):
        if messagebox.askyesno(
            "New Garden",
            "Start a new garden?\nUnsaved changes will be lost.",
        ):
            self.current_file = None
            self.rows, self.cols = 4, 8
            self._init_grid()
            self._draw_grid()
            self._update_sidebar()
            self.root.title("Square Foot Garden Planner")

    def _resize_garden(self):
        dlg = _ResizeDialog(self.root, self.rows, self.cols)
        self.root.wait_window(dlg.top)
        if dlg.result:
            nr, nc = dlg.result
            old = self.grid_data.copy()
            self.rows, self.cols = nr, nc
            self._init_grid()
            for (r, c), crop in old.items():
                if r < nr and c < nc and crop:
                    self.grid_data[(r, c)] = crop
            self._draw_grid()
            self._update_sidebar()

    def _clear_all(self):
        if messagebox.askyesno("Clear All", "Remove all crops from the garden?"):
            for key in self.grid_data:
                self.grid_data[key] = None
            self._draw_grid()
            self._update_sidebar()

    # ─── File I/O ─────────────────────────────────────────────────────────────

    def _save_file(self):
        if self.current_file:
            self._write_json(self.current_file)
        else:
            self._save_as()

    def _save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Garden layout", "*.json"), ("All files", "*.*")],
            title="Save Garden Layout",
        )
        if path:
            self.current_file = path
            self._write_json(path)

    def _write_json(self, path):
        payload = {
            "rows": self.rows,
            "cols": self.cols,
            "grid": {
                f"{r},{c}": crop
                for (r, c), crop in self.grid_data.items()
                if crop
            },
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            self.root.title(f"Square Foot Garden Planner — {path}")
            self.status_var.set(f"Saved: {path}")
        except OSError as e:
            messagebox.showerror("Save Error", str(e))

    def _load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Garden layout", "*.json"), ("All files", "*.*")],
            title="Open Garden Layout",
        )
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self.rows = int(data["rows"])
            self.cols = int(data["cols"])
            self._init_grid()
            for key, crop in data.get("grid", {}).items():
                r, c = map(int, key.split(","))
                if (r, c) in self.grid_data and crop in CROP_DATA:
                    self.grid_data[(r, c)] = crop
            self.current_file = path
            self._draw_grid()
            self._update_sidebar()
            self.root.title(f"Square Foot Garden Planner — {path}")
            self.status_var.set(f"Loaded: {path}")
        except (OSError, ValueError, KeyError) as e:
            messagebox.showerror("Load Error", str(e))


# ─── Resize Dialog ────────────────────────────────────────────────────────────

class _ResizeDialog:
    def __init__(self, parent, rows, cols):
        self.result = None

        self.top = tk.Toplevel(parent)
        self.top.title("Resize Garden Bed")
        self.top.resizable(False, False)
        self.top.grab_set()
        self.top.configure(bg="#2D5016")

        tk.Label(
            self.top, text="Resize Garden Bed",
            font=("Georgia", 13, "bold"),
            bg="#2D5016", fg="#F5F5DC",
        ).grid(row=0, column=0, columnspan=2, pady=(16, 12), padx=24)

        fields = [
            ("Rows (depth / length):", "rows_var", rows),
            ("Columns (width):",       "cols_var", cols),
        ]
        for i, (label, attr, default) in enumerate(fields):
            tk.Label(
                self.top, text=label, bg="#2D5016", fg="#F5F5DC",
                font=("Helvetica", 10),
            ).grid(row=i + 1, column=0, sticky="e", padx=12, pady=6)

            var = tk.IntVar(value=default)
            setattr(self, attr, var)
            ttk.Spinbox(self.top, from_=1, to=20, textvariable=var, width=8
                        ).grid(row=i + 1, column=1, padx=12, pady=6, sticky="w")

        tk.Label(
            self.top,
            text="Crops outside the new boundary will be removed.",
            bg="#2D5016", fg="#81C784",
            font=("Helvetica", 8, "italic"),
        ).grid(row=3, column=0, columnspan=2, pady=(2, 4))

        btns = tk.Frame(self.top, bg="#2D5016")
        btns.grid(row=4, column=0, columnspan=2, pady=14)
        ttk.Button(btns, text="Apply",  command=self._apply   ).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Cancel", command=self.top.destroy).pack(side=tk.LEFT, padx=6)

    def _apply(self):
        self.result = (self.rows_var.get(), self.cols_var.get())
        self.top.destroy()


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1160x730")
    root.minsize(920, 560)
    GardenPlannerApp(root)
    root.mainloop()
