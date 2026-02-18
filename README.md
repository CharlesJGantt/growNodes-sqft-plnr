# growNodes Square-Foot Garden Planner

**By Charles Gantt · The Makers Workbench · v1.1**

A lightweight, no-fuss desktop app for planning raised-bed vegetable gardens using the square-foot gardening method. Pick your crops, click to plant them on a visual grid, and instantly see how many plants fit in your bed — no spreadsheet required.

---

## Features

- **Visual grid-based garden layout** — each cell represents one square foot of your raised bed
- **33 built-in crops** with scientifically-based planting density and spacing data:
  - Tomatoes, Peppers, Lettuce, Spinach, Carrots, Radishes, Beans, Basil, Cucumbers, Zucchini, Kale, Onions, Peas, Broccoli, Cauliflower, Cabbage, Brussels Sprouts, Sweet Corn, Pumpkin, Watermelon, Cantaloupe, Eggplant, Sweet Potatoes, Garlic, Leeks, Beets, Swiss Chard, Arugula, Cilantro, Parsley, Dill, Sunflowers, Strawberries
- **Emoji crop icons** — each crop displays a relevant emoji icon inside its cell for quick visual identification
- **Smart text contrast** — crop labels and all in-cell overlays automatically switch between black and white text based on the cell's background color, so every label stays readable regardless of crop color
- **Left-click to plant, double-click to add a note, right-click for options** — intuitive point-and-click editing
- **Per-square notes** — double-click any square to attach a typed note; squares with a note show a 📝 indicator in the top-right corner
- **Right-click context menu** with three sections:
  - **Clear Square** — removes the crop from that cell
  - **Set Irrigation** — tag the square as None, 💧 Drip, or 🌧️ Spray; the icon appears in the bottom-left corner
  - **Set Soil** — tag the square as None, ♻️ Composted, ⚡ Fertilized, 🟤 Needs Compost, or ⚠️ Needs Fertilizer; the icon appears in the bottom-right corner
- **Hover tooltips** — hover over any cell to see the crop name, plants-per-sqft, and recommended spacing in the status bar
- **Color-coded cells** — every crop has its own distinct color so your layout is easy to read at a glance
- **Crop legend** — sidebar panel shows all available crops with their color swatch and plants-per-sqft count
- **Live planted summary** — sidebar updates in real time showing how many squares and total plants you've committed to each crop
- **Bed statistics** — running totals for bed size, squares planted, percentage filled, and total plant count
- **Resizable garden bed** — set rows and columns anywhere from 1×1 up to 20×20; existing crops, notes, irrigation, and soil tags within the new boundary are all preserved
- **Scrollable canvas** — works comfortably with large garden beds that exceed your screen size
- **Save & load layouts** — layouts are saved as plain `.json` files that include your crops, notes, irrigation tags, and soil tags; easy to back up, share, or version-control
- **Save / Save As / Open** — full file workflow with keyboard shortcuts (Ctrl+N, Ctrl+O, Ctrl+S)
- **New Garden** — quickly reset to a blank 4×8 default bed
- **Clear All** — wipe every cell at once with a single confirmation prompt

---

## Screenshots

![growNodes Garden Planner - empty bed](https://github.com/user-attachments/assets/899979c9-5525-42a5-bc41-d80203c8c934)

![growNodes Garden Planner - planted layout](https://github.com/user-attachments/assets/144e8f65-7e38-4bce-b3ae-e6d4f457959c)

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

To resize your bed, go to **Garden → Resize Garden Bed** and enter the number of rows and columns you want (up to 20 × 20). Any crops, notes, and tags that fall outside the new boundary will be removed; everything inside is kept.

To start completely fresh, use **File → New Garden** (or Ctrl+N).

### Planting Crops

1. Choose a crop from the **Plant:** dropdown at the bottom of the canvas. A color swatch and spacing info will appear next to it.
2. **Left-click** any square to plant that crop there.
3. Hover your mouse over any cell to see its row/column coordinates, crop name, density, and spacing in the status bar.

The sidebar updates live as you plant, showing a breakdown of squares and total plants per crop, plus overall bed stats.

### Adding Notes

**Double-click** any square to open a small note dialog. Type whatever you want — transplant date, seed source, reminders — then click **Save**. A 📝 icon appears in the top-right corner of squares that have a note. Double-click again to edit or clear it.

### Irrigation and Soil Tags

**Right-click** any square to open the context menu:

- **Clear Square** — removes the crop from that cell.
- **Set Irrigation** — choose None, 💧 Drip, or 🌧️ Spray. The selected icon appears in the **bottom-left** corner of the cell.
- **Set Soil** — choose None, ♻️ Composted, ⚡ Fertilized, 🟤 Needs Compost, or ⚠️ Needs Fertilizer. The selected icon appears in the **bottom-right** corner of the cell.

These tags are saved with your layout and are fully independent of the crop planted in that square.

### Saving and Loading Layouts

- **File → Save** (Ctrl+S) — saves to the current file, or prompts for a location if this is a new layout.
- **File → Save As** — always prompts for a file name and location.
- **File → Open** (Ctrl+O) — loads a previously saved `.json` layout file.

Layout files are plain JSON and include your crops, notes, irrigation tags, and soil tags, so everything is preserved between sessions.

---

## Changelog

### v1.1
- Expanded crop database from 13 to 33 crops — added Broccoli, Cauliflower, Cabbage, Brussels Sprouts, Sweet Corn, Pumpkin, Watermelon, Cantaloupe, Eggplant, Sweet Potatoes, Garlic, Leeks, Beets, Swiss Chard, Arugula, Cilantro, Parsley, Dill, Sunflowers, and Strawberries
- Added emoji crop icons displayed inside each planted cell
- Smart text contrast — all in-cell labels and overlay icons now automatically use black or white text based on the cell's background brightness
- Increased cell size from 80 to 100 px to comfortably fit the emoji, name, count, and corner indicators
- Per-square notes via double-click (📝 corner indicator; saved to JSON)
- Right-click context menu replacing the old right-click-to-clear behavior, with Irrigation and Soil submenus (icons saved to JSON)
- Sidebar bed stats now count only active plantable squares

### v1.0
- Initial public release

---

## Credits

Built by **Charles Gantt** for **The Makers Workbench**.

> *The Makers Workbench — practical tools for people who build things.*
