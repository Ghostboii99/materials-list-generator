# Materials List Generator

A Python-based construction estimating tool that converts wall dimensions and framing parameters into purchase-ready material quantities. The tool automates repetitive calculations for studs, plates, and sheathing, applies configurable waste factors, validates inputs, and exports the results to CSV for estimating and purchasing workflows.

## Features

- Calculates studs, plates, and sheathing from wall length and height
- Supports configurable stud spacing and waste percentage
- Rounds purchases up to whole stock units
- Exports a clean CSV material list
- Uses only the Python standard library

## Quick start

```bash
python material_list.py --wall-length 156 --wall-height 8 --stud-spacing 16 --waste 10.5 --output materials.csv
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Example output

| Material | Quantity | Unit |
|---|---:|---|
| 2x4 studs | 131 | each |
| 2x4x8 plates | 65 | each |
| 4x8 sheathing | 44 | sheets |

> Estimates are planning aids. Field conditions, openings, local codes, engineering, and supplier requirements must be verified before purchase.
