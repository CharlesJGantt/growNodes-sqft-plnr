# growNodes Square-Foot Garden Planner

**By Charles Gantt · The Makers Workbench · v1.0**

A lightweight, no-fuss desktop app for planning raised-bed vegetable gardens using the square-foot gardening method. Pick your crops, click to plant them on a visual grid, and instantly see how many plants fit in your bed — no spreadsheet required.

---

## Features

- **Visual grid-based garden layout** — each cell represents one square foot of your raised bed
- **13 built-in crops** with scientifically-based planting density and spacing data:
  - Tomatoes, Peppers, Lettuce, Spinach, Carrots, Radishes, Beans, Basil, Cucumbers, Zucchini, Kale, Onions, Peas
- **Click to plant, right-click to clear** — intuitive point-and-click editing
- **Hover tooltips** — hover over any cell to see the crop name, plants-per-sqft, and recommended spacing in the status bar
- **Color-coded cells** — every crop has its own distinct color so your layout is easy to read at a glance
- **Crop legend** — sidebar panel shows all available crops with their color swatch and plants-per-sqft count
- **Live planted summary** — sidebar updates in real time showing how many squares and total plants you've committed to each crop
- **Bed statistics** — running totals for bed size, squares planted, percentage filled, and total plant count
- **Resizable garden bed** — set rows and columns anywhere from 1×1 up to 20×20; existing crops within the new boundary are preserved
- **Scrollable canvas** — works comfortably with large garden beds that exceed your screen size
- **Save & load layouts** — layouts are saved as plain `.json` files you can back up, share, or version-control
- **Save / Save As / Open** — full file workflow with keyboard shortcuts (Ctrl+N, Ctrl+O, Ctrl+S)
- **New Garden** — quickly reset to a blank 4×8 default bed
- **Clear All** — wipe every cell at once with a single confirmation prompt

---

## Requirements

- **Python 3.x** (3.8 or newer recommended)
- **Tkinter** — comes built into the standard Python installation on Windows, macOS, and most Linux distros. No extra packages needed.

> If you're on Linux and Tkinter is missing, install it with:
> `sudo apt install python3-tk` (Debian/Ubuntu) or the equivalent for your distro.

---

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python garden_planner.py
```

That's it. No virtual environment, no `pip install`, no setup step.

---

## How to Use

### Creating a Garden

When the app opens you'll see a default **4 × 8 bed** (4 rows deep, 8 columns wide = 32 square feet). That's a common raised-bed size, but you can change it any time.

To resize your bed, go to **Garden → Resize Garden Bed** and enter the number of rows and columns you want (up to 20 × 20). Any crops that fall outside the new boundary will be removed; everything inside is kept.

To start completely fresh, use **File → New Garden** (or Ctrl+N).

### Planting Crops

1. Choose a crop from the **Plant:** dropdown at the bottom of the canvas. A color swatch and spacing info will appear next to it.
2. **Left-click** any empty square to plant that crop there.
3. **Right-click** any planted square to clear it.
4. Hover your mouse over any cell to see its row/column coordinates, crop name, density, and spacing in the status bar.

The sidebar updates live as you plant, showing a breakdown of squares and total plants per crop, plus overall bed stats.

### Saving and Loading Layouts

- **File → Save** (Ctrl+S) — saves to the current file, or prompts for a location if this is a new layout.
- **File → Save As** — always prompts for a file name and location.
- **File → Open** (Ctrl+O) — loads a previously saved `.json` layout file.

Layout files are plain JSON, so they're easy to back up or share with a friend.

---

## Version 1.0

This is the first public release of growNodes Square-Foot Garden Planner. The core workflow — plan your bed, plant your crops, save your layout — is fully functional and ready for real-world use.

Future releases are planned and may include things like:

- Companion planting tips and compatibility warnings
- Custom crop editor (add your own plants and spacing data)
- Seasonal planting calendar integration
- Print / export to PDF or image
- Multiple beds in a single project file
- Undo / redo support

If you have ideas or run into issues, feel free to open an issue on the project repository.

---

## Credits

Built by **Charles Gantt** for **The Makers Workbench**.

> *The Makers Workbench — practical tools for people who build things.*
