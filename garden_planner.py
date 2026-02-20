"""
Square Foot Garden Planner
A Tkinter desktop app for planning raised-bed vegetable gardens.
"""

import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ─── Crop Database ────────────────────────────────────────────────────────────

CROP_DATA = {
    # ── Original crops ────────────────────────────────────────────────────────
    "Tomatoes":         {"plants_per_sqft": 1,  "color": "#E74C3C", "spacing": "18–24 in", "icon": "🍅"},
    "Peppers":          {"plants_per_sqft": 1,  "color": "#E67E22", "spacing": "12–15 in", "icon": "🌶️"},
    "Lettuce":          {"plants_per_sqft": 4,  "color": "#A8E063", "spacing": "6 in",     "icon": "🥬"},
    "Spinach":          {"plants_per_sqft": 9,  "color": "#27AE60", "spacing": "4 in",     "icon": "🍃"},
    "Carrots":          {"plants_per_sqft": 16, "color": "#F39C12", "spacing": "3 in",     "icon": "🥕"},
    "Radishes":         {"plants_per_sqft": 16, "color": "#E91E8C", "spacing": "3 in",     "icon": "🌸"},
    "Beans":            {"plants_per_sqft": 9,  "color": "#8BC34A", "spacing": "4 in",     "icon": "🫘"},
    "Basil":            {"plants_per_sqft": 4,  "color": "#1ABC9C", "spacing": "6 in",     "icon": "🌿"},
    "Cucumbers":        {"plants_per_sqft": 2,  "color": "#48C9B0", "spacing": "8 in",     "icon": "🥒"},
    "Zucchini":         {"plants_per_sqft": 1,  "color": "#F1C40F", "spacing": "18 in",    "icon": "🟢"},
    "Kale":             {"plants_per_sqft": 1,  "color": "#1E8449", "spacing": "12 in",    "icon": "🌱"},
    "Onions":           {"plants_per_sqft": 16, "color": "#BB8FCE", "spacing": "3 in",     "icon": "🧅"},
    "Peas":             {"plants_per_sqft": 8,  "color": "#A9DFBF", "spacing": "4–6 in",  "icon": "🫛"},
    # ── New crops ─────────────────────────────────────────────────────────────
    "Broccoli":         {"plants_per_sqft": 1,  "color": "#2E86AB", "spacing": "12 in",    "icon": "🥦"},
    "Cauliflower":      {"plants_per_sqft": 1,  "color": "#D5D8DC", "spacing": "12 in",    "icon": "⚪"},
    "Cabbage":          {"plants_per_sqft": 1,  "color": "#7DCEA0", "spacing": "12 in",    "icon": "💚"},
    "Brussels Sprouts": {"plants_per_sqft": 1,  "color": "#52BE80", "spacing": "12 in",    "icon": "🥦"},
    "Sweet Corn":       {"plants_per_sqft": 4,  "color": "#F9E79F", "spacing": "6 in",     "icon": "🌽"},
    "Pumpkin":          {"plants_per_sqft": 1,  "color": "#DC7633", "spacing": "24–36 in", "icon": "🎃"},
    "Watermelon":       {"plants_per_sqft": 1,  "color": "#EC407A", "spacing": "18–24 in", "icon": "🍉"},
    "Cantaloupe":       {"plants_per_sqft": 1,  "color": "#FFAB76", "spacing": "18–24 in", "icon": "🍈"},
    "Eggplant":         {"plants_per_sqft": 1,  "color": "#7B2D8B", "spacing": "18 in",    "icon": "🍆"},
    "Sweet Potatoes":   {"plants_per_sqft": 4,  "color": "#B7770D", "spacing": "6 in",     "icon": "🍠"},
    "Garlic":           {"plants_per_sqft": 16, "color": "#F0E6D3", "spacing": "3 in",     "icon": "🧄"},
    "Leeks":            {"plants_per_sqft": 9,  "color": "#82E0AA", "spacing": "4 in",     "icon": "🌾"},
    "Beets":            {"plants_per_sqft": 9,  "color": "#8E44AD", "spacing": "4 in",     "icon": "🔴"},
    "Swiss Chard":      {"plants_per_sqft": 4,  "color": "#D98880", "spacing": "6 in",     "icon": "🍀"},
    "Arugula":          {"plants_per_sqft": 4,  "color": "#A9CCE3", "spacing": "6 in",     "icon": "🥗"},
    "Cilantro":         {"plants_per_sqft": 9,  "color": "#58D68D", "spacing": "4 in",     "icon": "🌿"},
    "Parsley":          {"plants_per_sqft": 4,  "color": "#17A589", "spacing": "6 in",     "icon": "🪴"},
    "Dill":             {"plants_per_sqft": 4,  "color": "#ABEBC6", "spacing": "6 in",     "icon": "🌼"},
    "Sunflowers":       {"plants_per_sqft": 1,  "color": "#F4D03F", "spacing": "12 in",    "icon": "🌻"},
    "Strawberries":     {"plants_per_sqft": 4,  "color": "#CB4335", "spacing": "6 in",     "icon": "🍓"},
}

SURFACE_DATA = {
    "garden":  {"color": None,      "icon": ""},     # uses EMPTY_COLOR when no crop
    "grass":   {"color": "#7EC850", "icon": "🌱"},
    "pathway": {"color": "#A0856B", "icon": "🧱"},
    "gravel":  {"color": "#B0B0B0", "icon": "⬡"},
    "mulch":   {"color": "#5C3A1E", "icon": "🪵"},
    "water":   {"color": "#5DADE2", "icon": "💧"},
    "unused":  {"color": "#E8E8E8", "icon": ""},
}

SURFACE_ORDER = ["garden", "grass", "pathway", "gravel", "mulch", "water", "unused"]

EMPTY_COLOR     = "#E8DCC8"
GRID_LINE_COLOR = "#7D6B4F"
HOVER_COLOR     = "#FFD700"
CELL_SIZE       = 100  # pixels per square foot
PAD             = 30   # canvas edge padding


def _text_color(hex_color):
    """Return '#000000' or '#ffffff' for best readability on hex_color."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "#000000" if brightness > 128 else "#ffffff"


# ─── Main Application ─────────────────────────────────────────────────────────

class GardenPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Square Foot Garden Planner")
        self.root.configure(bg="#2D5016")

        self.rows = 4
        self.cols = 8
        self.grid_data      = {}    # (row, col) -> crop name or None
        self.notes          = {}    # (row, col) -> str
        self.irrigation     = {}    # (row, col) -> "drip" | "spray"
        self.soil           = {}    # (row, col) -> soil amendment key
        self.cell_types     = {}    # (row, col) -> surface string; absent = "garden"
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
        garden_menu.add_command(label="Edit Garden Layout…", command=self._resize_garden)
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

        self.canvas.bind("<Button-1>",        self._on_click)
        self.canvas.bind("<Double-Button-1>", self._on_double_click)
        self.canvas.bind("<Button-3>",        self._on_right_click)
        self.canvas.bind("<Motion>",          self._on_hover)
        self.canvas.bind("<Leave>",           lambda e: self._clear_hover())

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
            state="readonly", width=16,
            font=("Helvetica", 11),
        )
        self.crop_cb.pack(side=tk.LEFT)

        self.swatch = tk.Label(sel, width=3, relief="solid", bd=1)
        self.swatch.pack(side=tk.LEFT, padx=7)

        self.info_lbl = tk.Label(sel, bg="#2D5016", fg="#C8E6C9", font=("Helvetica", 9))
        self.info_lbl.pack(side=tk.LEFT)

        tk.Label(
            sel, text="Left-click = plant  ·  Double-click = note  ·  Right-click = menu",
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
            if self.cell_types.get((r, c), "garden") == "garden"
        }

    def _is_garden(self, r, c):
        """True if (r, c) is inside the grid and has surface type 'garden'."""
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        return self.cell_types.get((r, c), "garden") == "garden"

    def _draw_grid(self):
        self.canvas.delete("all")
        SZ = CELL_SIZE

        total_w = self.cols * SZ + PAD * 2
        total_h = self.rows * SZ + PAD * 2
        self.canvas.configure(scrollregion=(0, 0, total_w, total_h))

        # Draw each cell
        for r in range(self.rows):
            for c in range(self.cols):
                surface = self.cell_types.get((r, c), "garden")
                x1 = PAD + c * SZ
                y1 = PAD + r * SZ
                x2 = x1 + SZ
                y2 = y1 + SZ

                if surface != "garden":
                    # Non-garden surface cell
                    sdata = SURFACE_DATA[surface]
                    color = sdata["color"]
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color, outline="#C0C0C0", width=1,
                        tags="cell",
                    )
                    txt = _text_color(color)
                    cx, cy = x1 + SZ // 2, y1 + SZ // 2
                    if sdata["icon"]:
                        self.canvas.create_text(
                            cx, cy - 8, text=sdata["icon"],
                            font=("Segoe UI Emoji", 16), fill=txt,
                        )
                    name = surface.capitalize()
                    self.canvas.create_text(
                        cx, cy + 16, text=name,
                        font=("Helvetica", 8), fill=txt,
                    )
                else:
                    # Garden cell — show crop or empty
                    crop  = self.grid_data.get((r, c))
                    color = CROP_DATA[crop]["color"] if crop else EMPTY_COLOR
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color, outline=GRID_LINE_COLOR, width=1,
                        tags="cell",
                    )
                    txt = _text_color(color)
                    cx, cy = x1 + SZ // 2, y1 + SZ // 2
                    if crop:
                        icon  = CROP_DATA[crop]["icon"]
                        n     = CROP_DATA[crop]["plants_per_sqft"]
                        label = crop if len(crop) <= 10 else crop[:9] + "."
                        self.canvas.create_text(
                            cx, cy - 22, text=icon,
                            font=("Segoe UI Emoji", 14), fill=txt,
                        )
                        self.canvas.create_text(
                            cx, cy - 2, text=label,
                            font=("Helvetica", 8, "bold"), fill=txt,
                        )
                        self.canvas.create_text(
                            cx, cy + 14, text=f"× {n}",
                            font=("Helvetica", 8), fill=txt,
                        )
                    else:
                        self.canvas.create_text(
                            x1 + 5, y1 + 5, text=f"{r+1},{c+1}",
                            font=("Helvetica", 6), fill=txt, anchor="nw",
                        )

                    # Note indicator — top-right corner
                    if (r, c) in self.notes:
                        self.canvas.create_text(
                            x2 - 4, y1 + 4, text="📝",
                            font=("Segoe UI Emoji", 9), fill=txt, anchor="ne",
                        )

                    # Irrigation indicator — bottom-left corner
                    irr_icons  = {"drip": "💧", "spray": "🌧️"}
                    irr = self.irrigation.get((r, c))
                    if irr in irr_icons:
                        self.canvas.create_text(
                            x1 + 4, y2 - 4, text=irr_icons[irr],
                            font=("Segoe UI Emoji", 9), fill=txt, anchor="sw",
                        )

                    # Soil indicator — bottom-right corner
                    soil_icons = {
                        "composted":        "♻️",
                        "fertilized":       "⚡",
                        "needs_compost":    "🟤",
                        "needs_fertilizer": "⚠️",
                    }
                    soil = self.soil.get((r, c))
                    if soil in soil_icons:
                        self.canvas.create_text(
                            x2 - 4, y2 - 4, text=soil_icons[soil],
                            font=("Segoe UI Emoji", 9), fill=txt, anchor="se",
                        )

        # Raised-bed border: draw thick brown line on edges adjacent to
        # non-garden cells or grid boundary.
        BORDER_COLOR = "#3E2107"
        BORDER_W = 5
        for r in range(self.rows):
            for c in range(self.cols):
                if not self._is_garden(r, c):
                    continue
                x1 = PAD + c * SZ
                y1 = PAD + r * SZ
                x2 = x1 + SZ
                y2 = y1 + SZ
                if not self._is_garden(r - 1, c):  # top
                    self.canvas.create_line(x1, y1, x2, y1, fill=BORDER_COLOR, width=BORDER_W)
                if not self._is_garden(r + 1, c):  # bottom
                    self.canvas.create_line(x1, y2, x2, y2, fill=BORDER_COLOR, width=BORDER_W)
                if not self._is_garden(r, c - 1):  # left
                    self.canvas.create_line(x1, y1, x1, y2, fill=BORDER_COLOR, width=BORDER_W)
                if not self._is_garden(r, c + 1):  # right
                    self.canvas.create_line(x2, y1, x2, y2, fill=BORDER_COLOR, width=BORDER_W)

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
            if self.cell_types.get((r, c), "garden") != "garden":
                return  # can't plant on non-garden surfaces
            self.grid_data[(r, c)] = self.selected_crop.get()
            self._draw_grid()
            self._update_sidebar()

    def _on_double_click(self, event):
        cell = self._cell_from_event(event)
        if cell:
            r, c = cell
            _NoteDialog(self.root, r, c, self.notes, self._draw_grid)

    def _on_right_click(self, event):
        cell = self._cell_from_event(event)
        if not cell:
            return
        r, c = cell
        surface = self.cell_types.get((r, c), "garden")

        menu = tk.Menu(self.root, tearoff=0)

        if surface == "garden":
            menu.add_command(label="Clear Square", command=lambda: self._clear_square(r, c))

            irr_menu = tk.Menu(menu, tearoff=0)
            irr_menu.add_command(label="None",     command=lambda: self._set_irrigation(r, c, None))
            irr_menu.add_command(label="💧 Drip",  command=lambda: self._set_irrigation(r, c, "drip"))
            irr_menu.add_command(label="🌧️ Spray", command=lambda: self._set_irrigation(r, c, "spray"))
            menu.add_cascade(label="Set Irrigation", menu=irr_menu)

            soil_menu = tk.Menu(menu, tearoff=0)
            soil_menu.add_command(label="None",                command=lambda: self._set_soil(r, c, None))
            soil_menu.add_command(label="♻️ Composted",        command=lambda: self._set_soil(r, c, "composted"))
            soil_menu.add_command(label="⚡ Fertilized",       command=lambda: self._set_soil(r, c, "fertilized"))
            soil_menu.add_command(label="🟤 Needs Compost",   command=lambda: self._set_soil(r, c, "needs_compost"))
            soil_menu.add_command(label="⚠️ Needs Fertilizer", command=lambda: self._set_soil(r, c, "needs_fertilizer"))
            menu.add_cascade(label="Set Soil", menu=soil_menu)

        menu.add_separator()
        surf_menu = tk.Menu(menu, tearoff=0)
        for stype in SURFACE_ORDER:
            label = stype.capitalize()
            if stype == surface:
                label += "  ✓"
            surf_menu.add_command(
                label=label,
                command=lambda s=stype: self._set_surface(r, c, s),
            )
        menu.add_cascade(label="Set Surface", menu=surf_menu)

        menu.tk_popup(event.x_root, event.y_root)

    def _set_surface(self, r, c, surface):
        if surface == "garden":
            self.cell_types.pop((r, c), None)
            # Ensure grid_data entry exists for this garden cell
            if (r, c) not in self.grid_data:
                self.grid_data[(r, c)] = None
        else:
            self.cell_types[(r, c)] = surface
            # Remove crop data for non-garden cells
            self.grid_data.pop((r, c), None)
            self.notes.pop((r, c), None)
            self.irrigation.pop((r, c), None)
            self.soil.pop((r, c), None)
        self._draw_grid()
        self._update_sidebar()

    def _clear_square(self, r, c):
        self.grid_data[(r, c)] = None
        self._draw_grid()
        self._update_sidebar()

    def _set_irrigation(self, r, c, value):
        if value is None:
            self.irrigation.pop((r, c), None)
        else:
            self.irrigation[(r, c)] = value
        self._draw_grid()

    def _set_soil(self, r, c, value):
        if value is None:
            self.soil.pop((r, c), None)
        else:
            self.soil[(r, c)] = value
        self._draw_grid()

    def _on_hover(self, event):
        cell = self._cell_from_event(event)
        if cell != self.hovered_cell:
            self.hovered_cell = cell
            self._draw_hover_highlight()

        if cell:
            r, c = cell
            surface = self.cell_types.get((r, c), "garden")
            if surface != "garden":
                self.status_var.set(
                    f"Row {r+1}, Col {c+1}  ·  {surface.capitalize()}"
                )
            else:
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

        # Stats footer — garden_sq counts only garden-type cells
        total_grid = self.rows * self.cols
        garden_sq  = len(self.grid_data)
        planted_sq = sum(1 for v in self.grid_data.values() if v)
        total_pl   = sum(
            CROP_DATA[v]["plants_per_sqft"]
            for v in self.grid_data.values() if v
        )
        pct = int(100 * planted_sq / garden_sq) if garden_sq else 0
        self.stats_lbl.configure(
            text=(
                f"Garden: {garden_sq} sqft  ·  Total grid: {total_grid} cells\n"
                f"Planted: {planted_sq}/{garden_sq} squares  ({pct}%)\n"
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
            self.cell_types = {}
            self.notes      = {}
            self.irrigation = {}
            self.soil       = {}
            self._init_grid()
            self._draw_grid()
            self._update_sidebar()
            self.root.title("Square Foot Garden Planner")

    def _resize_garden(self):
        dlg = _LayoutDialog(self.root, self.rows, self.cols, self.cell_types)
        self.root.wait_window(dlg.top)
        if dlg.result:
            nr, nc, new_types = dlg.result
            old = self.grid_data.copy()
            self.rows, self.cols = nr, nc
            self.cell_types = new_types
            self._init_grid()
            for (r, c), crop in old.items():
                if r < nr and c < nc and crop:
                    if self.cell_types.get((r, c), "garden") == "garden":
                        self.grid_data[(r, c)] = crop
            self.notes      = {(r, c): v for (r, c), v in self.notes.items()      if r < nr and c < nc and self.cell_types.get((r, c), "garden") == "garden"}
            self.irrigation = {(r, c): v for (r, c), v in self.irrigation.items() if r < nr and c < nc and self.cell_types.get((r, c), "garden") == "garden"}
            self.soil       = {(r, c): v for (r, c), v in self.soil.items()       if r < nr and c < nc and self.cell_types.get((r, c), "garden") == "garden"}
            self._draw_grid()
            self._update_sidebar()

    def _clear_all(self):
        if messagebox.askyesno("Clear All", "Remove all crops from the garden?\n(Layout shape will be kept.)"):
            for key in self.grid_data:
                self.grid_data[key] = None
            self.notes      = {}
            self.irrigation = {}
            self.soil       = {}
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
            "cell_types": {f"{r},{c}": val  for (r, c), val  in self.cell_types.items()},
            "notes":      {f"{r},{c}": note for (r, c), note in self.notes.items()},
            "irrigation": {f"{r},{c}": val  for (r, c), val  in self.irrigation.items()},
            "soil":       {f"{r},{c}": val  for (r, c), val  in self.soil.items()},
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
            self.cell_types = {}
            for key, val in data.get("cell_types", {}).items():
                r, c = map(int, key.split(","))
                if 0 <= r < self.rows and 0 <= c < self.cols and val in SURFACE_DATA:
                    self.cell_types[(r, c)] = val
            self._init_grid()
            for key, crop in data.get("grid", {}).items():
                r, c = map(int, key.split(","))
                if (r, c) in self.grid_data and crop in CROP_DATA:
                    self.grid_data[(r, c)] = crop
            self.notes = {}
            for key, note in data.get("notes", {}).items():
                r, c = map(int, key.split(","))
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.notes[(r, c)] = note
            self.irrigation = {}
            for key, val in data.get("irrigation", {}).items():
                r, c = map(int, key.split(","))
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.irrigation[(r, c)] = val
            self.soil = {}
            for key, val in data.get("soil", {}).items():
                r, c = map(int, key.split(","))
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.soil[(r, c)] = val
            self.current_file = path
            self._draw_grid()
            self._update_sidebar()
            self.root.title(f"Square Foot Garden Planner — {path}")
            self.status_var.set(f"Loaded: {path}")
        except (OSError, ValueError, KeyError) as e:
            messagebox.showerror("Load Error", str(e))


# ─── Note Dialog ──────────────────────────────────────────────────────────────

class _NoteDialog:
    def __init__(self, parent, row, col, notes, refresh_cb):
        self.notes      = notes
        self.key        = (row, col)
        self.refresh_cb = refresh_cb

        self.top = tk.Toplevel(parent)
        self.top.title(f"Note — Row {row+1}, Col {col+1}")
        self.top.resizable(False, False)
        self.top.grab_set()
        self.top.configure(bg="#2D5016")

        tk.Label(
            self.top,
            text=f"Note for square ({row+1}, {col+1}):",
            bg="#2D5016", fg="#F5F5DC",
            font=("Helvetica", 10),
        ).pack(padx=16, pady=(12, 4), anchor="w")

        self.text_widget = tk.Text(
            self.top, width=32, height=4,
            font=("Helvetica", 10), wrap="word",
        )
        self.text_widget.pack(padx=16, pady=4)
        existing = notes.get(self.key, "")
        if existing:
            self.text_widget.insert("1.0", existing)

        btns = tk.Frame(self.top, bg="#2D5016")
        btns.pack(pady=(4, 12))
        ttk.Button(btns, text="Save",       command=self._save ).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Clear Note", command=self._clear).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Cancel",     command=self.top.destroy).pack(side=tk.LEFT, padx=6)

    def _save(self):
        note = self.text_widget.get("1.0", "end-1c").strip()
        if note:
            self.notes[self.key] = note
        else:
            self.notes.pop(self.key, None)
        self.refresh_cb()
        self.top.destroy()

    def _clear(self):
        self.notes.pop(self.key, None)
        self.refresh_cb()
        self.top.destroy()


# ─── Layout Dialog ────────────────────────────────────────────────────────────

class _LayoutDialog:
    MINI_SZ = 28  # pixels per cell in the mini canvas

    def __init__(self, parent, rows, cols, cell_types):
        self.result = None
        self._rows = rows
        self._cols = cols
        # Work on a copy so Cancel discards changes
        self._cell_types = dict(cell_types)

        self.top = tk.Toplevel(parent)
        self.top.title("Edit Garden Layout")
        self.top.resizable(False, False)
        self.top.grab_set()
        self.top.configure(bg="#2D5016")

        tk.Label(
            self.top, text="Edit Garden Layout",
            font=("Georgia", 13, "bold"),
            bg="#2D5016", fg="#F5F5DC",
        ).pack(pady=(16, 8), padx=24)

        # ── Dimension spinners ───────────────────────────────────────────
        dim_frame = tk.Frame(self.top, bg="#2D5016")
        dim_frame.pack(padx=24, pady=4)

        fields = [
            ("Rows:", "rows_var", rows),
            ("Cols:", "cols_var", cols),
        ]
        for label, attr, default in fields:
            tk.Label(
                dim_frame, text=label, bg="#2D5016", fg="#F5F5DC",
                font=("Helvetica", 10),
            ).pack(side=tk.LEFT, padx=(0, 4))
            var = tk.IntVar(value=default)
            setattr(self, attr, var)
            sp = ttk.Spinbox(dim_frame, from_=1, to=20, textvariable=var, width=5)
            sp.pack(side=tk.LEFT, padx=(0, 12))

        ttk.Button(dim_frame, text="Update Grid", command=self._rebuild_canvas).pack(side=tk.LEFT, padx=6)

        # ── Mini canvas ──────────────────────────────────────────────────
        self._canvas_frame = tk.Frame(self.top, bg="#2D5016")
        self._canvas_frame.pack(padx=24, pady=8)

        self.mini_canvas = None
        self._build_mini_canvas()

        # ── Legend strip ─────────────────────────────────────────────────
        leg = tk.Frame(self.top, bg="#2D5016")
        leg.pack(padx=24, pady=(0, 4))
        for stype in SURFACE_ORDER:
            sdata = SURFACE_DATA[stype]
            color = sdata["color"] if sdata["color"] else EMPTY_COLOR
            f = tk.Frame(leg, bg="#2D5016")
            f.pack(side=tk.LEFT, padx=4)
            tk.Label(f, width=2, bg=color, relief="solid", bd=1).pack(side=tk.LEFT, padx=(0, 2))
            tk.Label(f, text=stype.capitalize(), bg="#2D5016", fg="#F5F5DC",
                     font=("Helvetica", 8)).pack(side=tk.LEFT)

        tk.Label(
            self.top,
            text="Left-click = Garden  ·  Right-click = cycle surface type",
            bg="#2D5016", fg="#81C784",
            font=("Helvetica", 8, "italic"),
        ).pack(pady=(0, 4))

        # ── Buttons ──────────────────────────────────────────────────────
        btns = tk.Frame(self.top, bg="#2D5016")
        btns.pack(pady=(4, 14))
        ttk.Button(btns, text="Apply",  command=self._apply).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Cancel", command=self.top.destroy).pack(side=tk.LEFT, padx=6)

    def _build_mini_canvas(self):
        if self.mini_canvas:
            self.mini_canvas.destroy()
        SZ = self.MINI_SZ
        w = self._cols * SZ + 2
        h = self._rows * SZ + 2
        self.mini_canvas = tk.Canvas(
            self._canvas_frame, width=w, height=h,
            bg="#6B4C2A", highlightthickness=1, highlightbackground="#3A7D44",
        )
        self.mini_canvas.pack()
        self.mini_canvas.bind("<Button-1>", self._mini_left_click)
        self.mini_canvas.bind("<Button-3>", self._mini_right_click)
        self._draw_mini()

    def _draw_mini(self):
        self.mini_canvas.delete("all")
        SZ = self.MINI_SZ
        for r in range(self._rows):
            for c in range(self._cols):
                surface = self._cell_types.get((r, c), "garden")
                sdata = SURFACE_DATA[surface]
                color = sdata["color"] if sdata["color"] else EMPTY_COLOR
                x1 = 1 + c * SZ
                y1 = 1 + r * SZ
                x2 = x1 + SZ
                y2 = y1 + SZ
                outline = GRID_LINE_COLOR if surface == "garden" else "#C0C0C0"
                self.mini_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color, outline=outline, width=1,
                )
                if sdata["icon"]:
                    self.mini_canvas.create_text(
                        x1 + SZ // 2, y1 + SZ // 2,
                        text=sdata["icon"], font=("Segoe UI Emoji", 8),
                    )

    def _mini_cell(self, event):
        SZ = self.MINI_SZ
        c = int((event.x - 1) // SZ)
        r = int((event.y - 1) // SZ)
        if 0 <= r < self._rows and 0 <= c < self._cols:
            return r, c
        return None

    def _mini_left_click(self, event):
        cell = self._mini_cell(event)
        if cell:
            self._cell_types.pop(cell, None)  # set to garden
            self._draw_mini()

    def _mini_right_click(self, event):
        cell = self._mini_cell(event)
        if not cell:
            return
        current = self._cell_types.get(cell, "garden")
        idx = SURFACE_ORDER.index(current)
        next_surface = SURFACE_ORDER[(idx + 1) % len(SURFACE_ORDER)]
        if next_surface == "garden":
            self._cell_types.pop(cell, None)
        else:
            self._cell_types[cell] = next_surface
        self._draw_mini()

    def _rebuild_canvas(self):
        nr = self.rows_var.get()
        nc = self.cols_var.get()
        # Prune cell_types outside new bounds
        self._cell_types = {
            (r, c): v for (r, c), v in self._cell_types.items()
            if r < nr and c < nc
        }
        self._rows = nr
        self._cols = nc
        self._build_mini_canvas()

    def _apply(self):
        self.result = (self.rows_var.get(), self.cols_var.get(), dict(self._cell_types))
        self.top.destroy()


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x760")
    root.minsize(1060, 600)
    GardenPlannerApp(root)
    root.mainloop()
