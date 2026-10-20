---
name: mac-vintage-hdmi-project
description: Goal and part choices for the mac-vintage-hdmi KiCad 10 board (ADV7611 HDMI receiver); project-local library location
metadata:
  node_type: memory
  type: project
  originSessionId: fbd4e7ac-0bd3-4c14-810f-10b81ce5d9c2
  modified: 2026-10-19T21:51:19.915Z
---

The user is designing an HDMI receiver PCB ("mac-vintage-hdmi") in KiCad 10, built around the Analog Devices ADV7611 (64-lead LQFP_EP, ADI package SW-64-3, 5x5mm exposed pad = GND). Project-local library nickname `mac-vintage-hdmi` lives at `ee/mac-vintage-hdmi/lib/` (registered in the project's sym-lib-table / fp-lib-table), created 2026-10-02 from KiCad's stock `Interface_HDMI:ADV7611` and `Package_QFP:LQFP-64-1EP_10x10mm_P0.5mm_EP5x5mm` after verifying both against the datasheet and ADI's SW-64-3 drawing.

**Why:** Stock parts were verified correct; the local copy pins them to the project and points the 3D model at the EP6.5 STEP (the EP5x5 STEP isn't shipped).

Also in the library (added 2026-10-02): Lattice ICE40HX4K-TQ144 FPGA from SnapEDA (symbol + `QFP50P2200X2200X160-144N` footprint + STEP in `lib/mac-vintage-hdmi.3dshapes/`). Its 107 I/O pins were verified against Project IceStorm's `8k-tq144:4k` pin table; power/config pin numbers were not checked against Lattice's pinout file, but on 2026-10-13 they were found to match KiCad's stock `FPGA_Lattice:ICE40HX4K-TQ144`, and the 7 NC pins SnapEDA omitted (35, 36, 50, 51, 58, 77, 133) were added to the Power unit so all 144 pins are present. The SnapEDA STEP is Y-up and needs `rotate -90 0 0`.

Also copied unchanged from KiCad stock (2026-10-02, user said "just copy"): RP2350A/B and RP2354A/B symbols (RP2354x `extends` RP2350x) plus QFN-60/QFN-80 footprints (plain + ThermalVias). The user picked RP2354B as the part they want. Their 3D model STEPs aren't installed. On 2026-10-13 the user asked for RP2354B to have no hidden pins: the parent RP2350B symbol was redrawn, then at the user's request each IOVDD pin was placed among its package-neighbour GPIO pins on the sides (6 on the right, pins 50/60 on the left by the ADC GPIOs; 3 DVDD on top; body extended downward). RP2350 has a single IOVDD domain, so this grouping is physical, not electrical; RP2350A/RP2354A still have KiCad's hidden stacked pins.

Added 2026-10-08: `ICE40UP5K-SG48I` symbol (4 units, from KiCad stock `FPGA_Lattice:ICE40UP5K-SG48ITR`, all 48 pins verified against Lattice's SG48 pinout xlsx; pin 30 VCC unhidden, VCCPLL changed to power_in) plus `QFN-48-1EP_7x7mm_P0.5mm_EP5.3x5.3mm` footprints (plain + ThermalVias). The user was considering it as a smaller replacement for the HX4K-TQ144 (same FPGA as the pico2-ice reference); whether they switched was not settled. KiCad's stock symbol points at an EP5.6 footprint, which exceeds Lattice's 5.20–5.50 mm paddle. Lattice docs download fine with curl + browser UA from `latticesemi.com/view_document?document_id=N` (51968 UltraPlus datasheet, 51971 UP5K pinout xlsx, 213 package diagrams).

Also added 2026-10-08: `MHPA1010RGBDT` (Meihua 1x1 mm common-anode RGB LED, LCSC C404280; symbol from stock `Device:LED_ARGB`, hand-built footprint `LED_RGB_Meihua_MHPA1010RGBDT_1x1mm` per datasheet land pattern, no 3D model). LCSC datasheets: `datasheet.lcsc.com/lcsc/<file>.pdf` returns an HTML viewer; the real PDF is at `wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/<file>.pdf`.

Added 2026-10-14 for the speaker/audio path (ADV7611 I2S → DAC → LM386 → 63 Ω single-ended speaker, one terminal grounded): `PT8211-S` (Princeton 16-bit stereo DAC, LCSC C92004; hand-drawn symbol, pins 1 BCK 2 WS 3 DIN 4 GND 5 VDD 6 LCH 7 NC 8 RCH per datasheet; LSB-justified input, so ADV7611 must be set to right-justified 16-bit; TM8211 datasheet says WS high = left) and `LM386M-1` (copy of stock `Amplifier_Audio:LM386`, pins checked against TI table). Both use `SOIC-8_3.9x4.9mm_P1.27mm`, copied unchanged from stock. At that point the I2S nets connected only to the ADV7611 (U1 pins 48–51).

**How to apply:** Add new project parts to this library; convert vendor (SnapEDA) files with `kicad-cli sym/fp upgrade` before merging, and render a 3D check (`kicad-cli pcb render` on a temp board) since vendor STEP models are often mis-rotated. Open DFM caveat: the `_ThermalVias` variant has 0.2mm-drill vias and paste windows over the vias; the user hasn't chosen a fab yet. See [[adi-docs-access]].

Added 2026-10-15: `PTV09A` (Bourns 9 mm pot; 5 visible pins, 1/3 ends, 2 wiper, 4/5 metal mounting tabs) with hand-built footprints `Potentiometer_Bourns_PTV09A_RearMount` (-1/-4, shaft perpendicular to PCB; tabs 10.6 c-c, 7.0 above pins) and `_SideMount` (-2/-3/-7/-8; tabs 10.0 c-c, 3.3 above pins), oval 1.8x2.2 slots per the datasheet. KiCad's stock PTV09A-1 footprint has 8.8 mm tab spacing, which contradicts the datasheet, and duplicate "MP" pads. Which variant the user will buy was not settled; the symbol defaults to RearMount. No 3D models (KiCad 3D models aren't installed). Also `TLV9061IDBVR` (flattened from stock `TLV9061xDBV`/`MCP6L91T-EOT`; pins checked against SBOS839N Table 5-1) + stock `SOT-23-5` copied unchanged.
Also 2026-10-15: `Conn_01x02` (stock, unchanged except Footprint = `PinHeader_1x02_P2.54mm_Vertical_SMD_Pin1Left` and fp filter widened to `*:*_1x??_*` so project-lib footprints match) plus stock `_Pin1Left` and `_Pin1Right` 1x02 SMD header footprints. No specific header part number chosen.

2026-10-16: USB-C J2 switched from the mid-mount Amphenol 12401948E412A (its footprint carried Edge.Cuts notch lines) to top-mount HRO TYPE-C-31-M-12 (LCSC C165948) at the user's request. Added `TYPE-C-31-M-12` symbol (stock USB_C_Receptacle_USB2.0_16P graphics, 16 visible pins: combined pads numbered "A1/B12", "B1/A12", "A4/B9", "B4/A9" as on the HRO drawing; shell legs S1-S4) and footprint `USB_C_Receptacle_HRO_TYPE-C-31-M-12` built from the HRO 2020-12-08 drawing (stock KiCad version's signal pads differ). power.kicad_sch J2 was rewired by script; netlist verified identical. The project has two top-level sheets (Data, Power) and no sheet symbols, so kicad-cli on mac-vintage-hdmi.kicad_sch only sees one sheet. Exporting each sheet separately and merging by name is WRONG here: the Power sheet stacks several global labels on one wire (CVDD+PVDD+DVDD_1V8, DVDDIO+TVDD_3V3), and a per-sheet export keeps only one name, so U1's PVDD/DVDD/TVDD look unconnected. For a true netlist/ERC (done 2026-10-18), copy both sheets into a scratch dir as data.kicad_sch/power.kicad_sch and add a root `mac-vintage-hdmi.kicad_sch` with two `(sheet ...)` symbols whose uuids are the top-level sheet uuids (05ea0ec1-beac-48db-ac0f-53255a4cab75 Data, 13e48c44-097d-4a9e-b5ad-c93c72414a8b Power). The existing instance paths then resolve and all refs come out right. kicad-cli is at /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli (not on PATH).

2026-10-18 state: the main design no longer has an FPGA. ADV7611 Y[7:0] (P15..P8) + DE/HS/VS/LLC go straight to RP2354B GPIO24-31/18/22/23/20 for PIO capture, and the iCE40 variant lives in the separate `mac-vintage-hdmi-ice40/` folder. RP2354B GPIO8-11 drive the Mac Classic analog board via TXU0104 → J5 (Molex Mini-Fit 14-pin). J5 pinout was checked against the Bomarc 820-0525-A drawing: 1 +12V, 2/3 +5V, 4 VSYNC, 5 HSYNC, 6 video, 7 speaker, 8 -12V, 9 brightness PWM, 10/11/14 GND, and 12/13 joined to analog-board ground (the speaker return), so grounding 12/13 is correct. A design review that day found an explicit no-connect flag on U3 pin 60 (IOVDD) on the Data sheet.

Added 2026-10-18: `AOTA-B201610S3R3-101-T` (Abracon polarity-marked 3.3 µH RP235x VREG inductor; Device:L graphics plus a filled dot at pin 1) and footprint `L_Abracon_AOTA-B201610S3R3-101-T_2.0x1.6mm`. The footprint uses Abracon's land pattern (1.00x1.60 pads, 1.00 gap), which is larger than Raspberry Pi's `L_pol_2016` (0.7x1.7 at ±0.7). The 3D model is a stand-in, stock `L_Changjiang_FTC201610S.step`. Pin/pad 1 is the dot, and it goes to VOUT/DVDD (+1V1), with pad 2 to VREG_LX. Three sources confirm this: RP2350 datasheet Figs. 25/26/28 (PDF pp. 411-414) and the pico2-ice PCB. Abracon's own sketch labels the dot "+" (current in), which contradicts RP; follow RP. Datasheet saved to `datasheets/rp2350/`. Schematic L1 was NOT swapped yet. Its current generic L has pin 1 on VREG_LX, so a straight symbol swap would put the dot on the wrong net. By 2026-10-19 it HAD been swapped (now L2, AOTA footprint) and exactly that happened: L2 pad 1/dot is on VREG_LX — flagged in the 2026-10-19 layout review as reversed. The user fixed it the same day (board saved 12:01: L2 pad 1 = +1V1), and moved CIN C13 / COUT C14 to stock 0402 stacked under L2 in an RP-style block. Re-read the board before quoting its state; it changes during sessions.

2026-10-19 layout review (PCB fully routed, 0 unconnected, netlist parity clean): board 137.4x64 mm, JLC04161H-7628 4L, all parts top. Layers: F.Cu signals+pours / In1 solid GND / In2 +3V3 plane with ADV7611 + +1V1 islands and +5V/+12V traces / B.Cu GND pour + signals (B.Cu signals reference split In2). Field-solver (2D FD, mask 15 µm) results for this stackup: HDMI 0.249/0.203 mm ≈ 97–102 Ω diff; USB 0.3345/0.2032 ≈ 85–89 Ω; SE 0.2 mm ≈ 65 Ω, 0.3 mm ≈ 54–55 Ω, 0.35 mm ≈ 50 Ω. Main open items raised: RP2354B VREG layout deviates from RP2350 DS §6.3.8 (CIN via planes, single PGND via, no In1 cut under LX, AVDD/FB near LX); U5/U6 LDO tab copper; 96 vias-in-pad (no fill/cap); pixel-bus 33 Ω resistors mid-line at J8 instead of at ADV7611.

2026-10-19 re-check (board saved 14:06):
- **Fixed:** C1, M3 (except R47), M4, M5 (4 parallel 0 Ω).
- **Partly fixed:** C2, H1, M1, M2, M6.
- **Not done:** H2 (now 118 vias-in-pad), L1, L4, L5.
- **New blockers:**
  - R47 (LRCLK 33 Ω) has both pins on one net. A local label has the same name as the global label.
  - C8 GND pad is unconnected.
  - C55 is unrouted.
- **VREG follow-ups:**
  - Add an In1 cut-out under LX.
  - Centre L2 on pin 63 (x 85.25).
  - Set the LX zone to Solid and trim it so it doesn't fill between L2's pads.
  - The +1V1 vias sit in L2's pad.
  - The second 4.7 µF is still missing.
  - These fixes were trial-tested DRC-clean on a scratch copy.
- **KiCad 10 rule behaviour:**
  - The user's rule `A.intersectsArea('VREG')` is what lets the LX strip fill between C13/C14.
  - Changing it to `A... && B.intersectsArea('VREG')` stops the strip filling.
  - `A.Type != 'Zone' && A.intersectsArea('VREG')` fills identically.
  - The board-wide GND zone also satisfies the plain rule, so DRC checks GND pour at 0.15 everywhere, while the filler still uses 0.3.

2026-10-19 14:45 save: 0 unconnected, parity clean (154 nets).
- **Fixed:**
  - All three blockers. R47 is on `I2S_ADV7611_LRCLK_R`.
  - M6 fully. FB4 and FB5 now split U5's output (`+3V3_ADV7611`) into DVDDIO and TVDD. Added 10 µF: C56 on PVDD, C57 on DVDDIO, C58 on TVDD.
- **VREG:**
  - L2 is now at (85.25, 41.75) and C14 at y 40.25, so the C13/C14 + pads are only 0.2 mm apart.
  - The In1 `LX_CUT` rule area is in.
  - Still open: the LX zone uses a Thermal connection, so a 0.5 mm gap keeps fill off pad 2's north edge. It runs between L2's pads and enters by one east spoke.
  - Tested fix: Solid connection, trim the outline to stop at x 84.9, and add an F.Cu fill keep-out between L2's pads. Without that keep-out, the GND pour fills under the body.
  - The +1V1 vias are still in L2 pad 1, and the second 4.7 µF is still missing.
- **Unchanged:** H1 (U6 has no top copper), H2 (120 vias-in-pad), M1 (R56/R39/R41/R43 not moved), the U1-area part of M2, L1, L3, L4, L5.

Also added 2026-10-18:
- `BLM18KG601SN1D` (Murata 0603 ferrite bead, LCSC C85833; stock Device:FerriteBead graphics, Reference FB) plus stock `L_0603_1608Metric_Pad1.05x0.95mm_HandSolder` copied unchanged. It was recommended for isolating the ADV7611 PVDD/CVDD/TVDD rails but is not placed in the schematic yet.
- `MA3X704A` (Panasonic Schottky, the CEC pull-up diode on ADI's eval board). The symbol is from stock Diode:BAT54W (same 1=A, 2=NC, 3=K pinout) with the hidden stacked NC pin moved out to a visible stub. The footprint is stock `SC-59` copied unchanged, checked against Panasonic's "Mini 3-pin" (TO-236/SC-59) drawing.
- Panasonic's site is unreachable. The MA3X704A datasheet came from datasheet4u (`/download/<id>/` page, then `/pdf/<id>/<part>.pdf`), and distributor pages 403 or sit behind Cloudflare.
- The MA3X704A's lifecycle is unconfirmed. Panasonic's semis went to Nuvoton in 2020, and sibling MA3X parts show obsolete.
- Datasheets saved as `datasheets/ma3x704a.pdf` and `datasheets/blm18kg601sn1.pdf`.

Library convention: no LCSC/MPN fields on symbols; the LCSC number goes in Description.

2026-10-19: U12 instance (power.kicad_sch) switched from PT8211-S to Titan Micro TM8211-TA2302 (LCSC C22381766; PT8211-S C92004 was out of stock). Only the instance's Value/Datasheet/Description changed, and the user approved an instance-level `LCSC` field. The library symbol is still named `PT8211-S`. This is the first LCSC field in the design.
2026-10-19 later: the user asked for hidden instance-level `LCSC_Alt` fields (fallback LCSC numbers, recorded for their own reference when ordering from JLC): D12 C232585 (BAS70LT1G), J8/J9/J10/J12 C3294463 (HCTL PZ254-2-05-S SMD 2x5), SW1/SW2 C116501 (C&K PTS810 SJM), U4/U5 C6186 (AMS1117-3.3), U12 C92004 (PT8211-S). Only U12 has a primary `LCSC` field. U6 (1.8 V NCP1117) has no alt field.
