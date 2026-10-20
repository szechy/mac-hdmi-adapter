"""Add an impedance-control table (from the project's tuning profiles) on User.3 'Impedance'.

usage: python3 add_imp_table.py <in.kicad_pcb> <kicad_pro> <out.kicad_pcb>
"""
import json, re, sys, uuid
import pcbnew

src, pro_path, dst = sys.argv[1:4]
LAYER_STD, LAYER_NAME = "User.3", "Impedance"
X0, Y0 = 0.0, 70.0                 # mm; board outline bottom is y ~62.65
TXT, THK = 1.2, 0.15               # cell text size / stroke
MARGIN = 0.6                       # cell margin
LINE = TXT * 1.62                  # stroke-font line pitch

pro = json.load(open(pro_path))
profiles = pro["tuning_profiles"]["tuning_profiles_impedance_geometric"]
nc_for = {c["tuning_profile"]: c["name"] for c in pro["net_settings"]["classes"] if c.get("tuning_profile")}

LNUM = {"F.Cu": "L1", "In1.Cu": "L2", "In2.Cu": "L3", "B.Cu": "L4"}
MIL = 0.0254

# Layout facts the profiles don't carry. Coplanar = GND pour on the signal layer at the
# 0.3 mm zone clearance along most of the route (USB 89%, 50_SE B.Cu 60%; HDMI 39%, 50_SE F.Cu 25%).
COPLANAR = {("USB_90R", "F.Cu"), ("50_SE", "B.Cu")}
POSITION = {
    ("HDMI_100R", "F.Cu"): "HDMI_CLK, HDMI_LN0-2 pairs:\nJ1 (HDMI) -> D7/D8 -> U1",
    ("USB_90R", "F.Cu"): "USB2_D_P/N pair:\nJ2 (USB-C) -> R5/R6 -> U3",
    ("50_SE", "F.Cu"): "ADV7611_Y0-7, LLC:\nU1 -> R30-R44, R56 -> U3",
    ("50_SE", "B.Cu"): "ADV7611_Y0-7_RP2350, LLC_RP2350:\nR30-R44, R56 -> U3",
}

# Column layout follows JLCPCB's Required_impedance_control.xlsx (its D:E merge is one column here)
header = ["Signal Layer", "Reference Layer", "Impedance Type", "Trace Width (mil)",
          "Trace Spacing (mil)", "Impedance (ohm) ±10%", "Position"]
rows = []
for p in profiles:
    diff = p["type"] == 1
    for e in p["layer_entries"]:
        key = (p["profile_name"], e["signal_layer"])
        refs = [LNUM[l] for l in (e["top_reference_layer"], e["bottom_reference_layer"]) if l != "UNDEFINED"]
        kind = ("Differential Pair" if diff else "Single Ended") + \
               (" (Coplanar)" if key in COPLANAR else " (Non coplanar)")
        rows.append([LNUM[e["signal_layer"]], " / ".join(refs), kind,
                     "%.2f" % (e["width"] / 1e6 / MIL),
                     "%.2f" % (e["diff_pair_gap"] / 1e6 / MIL) if diff else "-",
                     "%g" % p["target_impedance"], POSITION[key]])
grid = [header] + rows

# measure strings with KiCad's own stroke font
board = pcbnew.BOARD()
def text_w(s, bold):
    t = pcbnew.PCB_TEXT(board)
    t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(TXT), pcbnew.FromMM(TXT)))
    t.SetTextThickness(pcbnew.FromMM(THK))
    t.SetBold(bold)
    w = 0
    for line in s.split("\n"):
        t.SetText(line)
        w = max(w, pcbnew.ToMM(t.GetTextBox(None).GetWidth()))
    return w

col_w = [round(max(text_w(r[c], r is header) for r in grid) + 2 * MARGIN + 0.8, 2)
         for c in range(len(header))]

def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'

def u():
    return '"%s"' % uuid.uuid4()

row_h = [round(max(s.count("\n") for s in r) * LINE + TXT + 2 * MARGIN + 0.4, 3) for r in grid]
ty = Y0 + 4.0
cells = []
for r, row in enumerate(grid):
    x = X0
    y = ty + sum(row_h[:r])
    for c, s in enumerate(row):
        ROW_H = row_h[r]
        bold = " (bold yes)" if r == 0 else ""
        cells.append(
            f'(table_cell {q(s)} (start {x:.4g} {y:.4g}) (end {x + col_w[c]:.4g} {y + ROW_H:.4g}) '
            f'(margins {MARGIN} {MARGIN} {MARGIN} {MARGIN}) (span 1 1) (layer "{LAYER_STD}") (uuid {u()}) '
            f'(effects (font (size {TXT} {TXT}) (thickness {THK}){bold}) (justify left top)))')
        x += col_w[c]

tbl_uuid, title_uuid, notes_uuid = u(), u(), u()
table = (f'(table (column_count {len(header)}) (uuid {tbl_uuid}) (layer "{LAYER_STD}") '
         f'(border (external yes) (header yes) (stroke (width 0.2) (type solid))) '
         f'(separators (rows yes) (cols yes) (stroke (width 0.1) (type solid))) '
         f'(column_widths {" ".join("%g" % w for w in col_w)}) '
         f'(row_heights {" ".join("%g" % h for h in row_h)}) '
         f'(cells {" ".join(cells)}))')

title = (f'(gr_text "IMPEDANCE CONTROL TABLE" (at {X0} {Y0 + 2.5} 0) (layer "{LAYER_STD}") (uuid {title_uuid}) '
         f'(effects (font (size 2 2) (thickness 0.3) (bold yes)) (justify left bottom)))')

notes_txt = (
    "NOTES:\n"
    "1. Target impedances are from the KiCad tuning profiles. Fabricator may adjust\n"
    "    trace width and spacing to meet target impedance.\n"
    "2. Stackup: 4 layers, 1.6 mm (JLC04161H-7628). Cu L1/L4 35 um, L2/L3 15.2 um.\n"
    "    L1-L2 and L3-L4: 7628 prepreg 0.2104 mm (Er 4.4). L2-L3: core 1.065 mm (Er 4.43).\n"
    "    Solder mask 15 um (Er 3.8).\n"
    "3. Coplanar rows: GND pour on the signal layer is 0.3 mm (11.81 mil) from the trace edge.\n"
    "4. Trace Spacing is edge-to-edge within a differential pair.")
notes_y = ty + sum(row_h) + 2.0
notes = (f'(gr_text {q(notes_txt)} (at {X0} {notes_y:.4g} 0) (layer "{LAYER_STD}") (uuid {notes_uuid}) '
         f'(effects (font (size {TXT} {TXT}) (thickness {THK})) (justify left top)))')

group = f'(group "Impedance table" (uuid {u()}) (members {tbl_uuid} {title_uuid} {notes_uuid}))'

pcb = open(src, encoding="utf-8").read()
if '(43 "User.3" user)' in pcb:
    pcb = pcb.replace('(43 "User.3" user)', f'(43 "User.3" user "{LAYER_NAME}")', 1)
assert f'(43 "User.3" user "{LAYER_NAME}")' in pcb
tail = "\t(embedded_fonts no)\n)"
assert pcb.rstrip().endswith(tail)
i = pcb.rstrip().rfind(tail)
pcb = pcb[:i] + "\t" + title + "\n\t" + table + "\n\t" + notes + "\n\t" + group + "\n" + pcb[i:]
open(dst, "w", encoding="utf-8").write(pcb)

# load + save through KiCad to validate and normalise formatting; also add the layer to the plot set
b = pcbnew.LoadBoard(dst)
ps = b.GetPlotOptions()
sel = ps.GetLayerSelection()
sel.AddLayer(pcbnew.User_3)
ps.SetLayerSelection(sel)
b.SetPlotOptions(ps)
pcbnew.SaveBoard(dst, b)

print("col widths", col_w, "table width %.1f" % sum(col_w))
for r in grid:
    print(r)
