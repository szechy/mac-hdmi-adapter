---
name: symbols-show-all-pins
description: "User expects schematic symbols to show every physical pin of the part, not KiCad's hidden/stacked pins"
metadata:
  node_type: memory
  type: feedback
  originSessionId: fbd4e7ac-0bd3-4c14-810f-10b81ce5d9c2
  modified: 2026-10-03T20:13:52.457Z
---

When making schematic symbols, show one visible pin per physical pad, numbered as in the manufacturer's datasheet. Don't use KiCad's stock trick of hiding a pin and stacking it on another (e.g. `Crystal_GND24`), or footprints with duplicate pad numbers.

**Why:** The user questioned the ABM8-272-T3 crystal symbol on 2026-10-02 because it showed three pins for a four-pin part ("i thought the component is four pins").

**How to apply:** For parts in [[mac-vintage-hdmi-project]], unhide stacked pins and renumber duplicate pads to match the datasheet (done for the crystal and the Würth 434133025816 switch).
