# Construction Materials List Generator

A Python-based construction estimating tool that converts wall dimensions and framing parameters into purchase-ready material quantities.

The project demonstrates how a repetitive construction estimating task can be turned into a simple, repeatable workflow: enter wall dimensions, choose framing spacing and waste, calculate material quantities, and export a clean CSV that can be used for estimating or purchasing.

## Why I built it

Material takeoffs often involve repeating the same calculations across multiple walls or projects. This tool was built to reduce manual math, standardize the calculation process, and create a reusable output that can be carried into a spreadsheet, quote, or purchasing workflow.

It combines **construction-domain logic** with **Python automation** rather than treating estimating as a generic programming exercise.

## Workflow

```mermaid
flowchart LR
    A[Wall dimensions] --> B[Framing parameters]
    B --> C[Python calculation engine]
    C --> D[Waste and purchase rounding]
    D --> E[Material list]
    E --> F[CSV export]
```

### Example input

- Wall length: **156 ft**
- Wall height: **8 ft**
- Stud spacing: **16 in. O.C.**
- Waste factor: **10.5%**

### Example output

| Material | Quantity | Unit |
|---|---:|---|
| 2x4 studs | 131 | each |
| 2x4x8 plates | 65 | each |
| 4x8 sheathing | 44 | sheets |

A sample exported file is included at [examples/materials.csv](examples/materials.csv).

## Features

- Calculates studs, plates, and sheathing from wall dimensions
- Supports **12", 16", and 24" on-center** stud spacing
- Supports a configurable waste percentage
- Validates dimensions, spacing, and waste inputs
- Rounds material purchases up to whole stock units
- Exports a structured CSV material list
- Separates calculation logic from file-export logic
- Includes automated unit tests
- Uses only the Python standard library

## Quick start

Requires Python 3.9+.

```bash
python material_list.py \
  --wall-length 156 \
  --wall-height 8 \
  --stud-spacing 16 \
  --waste 10.5 \
  --output materials.csv
```

Run the tests:

```bash
python -m unittest discover -s tests
```

## Estimating assumptions

The current version intentionally models a **simple continuous framed wall**.

- Stud quantities are based on wall length and selected on-center spacing.
- Plate quantities assume **three runs of plate**: one bottom plate and a double top plate.
- Plates are converted to 8-foot stock quantities.
- Sheathing is calculated using 4x8 sheets covering 32 sq. ft. each.
- The selected waste factor is applied before purchase quantities are rounded up.

The tool does **not currently deduct openings or calculate** door/window framing, headers, king studs, jack studs, cripples, corners, blocking, hardware, engineered components, or code-specific assemblies.

That scope is deliberate: the project establishes a clean calculation engine that can be extended without hiding its assumptions.

## Potential client extensions

The same calculation structure can be expanded for real estimating workflows, including:

- Door and window opening deductions
- Header, king-stud, jack-stud, and cripple calculations
- Multiple wall types or entire projects
- Lumber length optimization
- Supplier SKUs and live/unit pricing
- Labor and material cost estimates
- Excel or Google Sheets export
- PDF quote or takeoff reports
- Web-based estimating interface
- Blueprint/OCR-assisted quantity extraction

## Project structure

```text
materials-list-generator/
├── material_list.py
├── examples/
│   └── materials.csv
├── tests/
│   └── test_material_list.py
└── README.md
```

## What this project demonstrates

- Translating a real business process into software
- Python CLI development
- Construction estimating logic
- Input validation
- Structured data modeling with dataclasses
- CSV generation
- Automated testing
- Designing software for future workflow automation

## Disclaimer

This tool is a planning and workflow-automation example, not an engineered takeoff or code-compliance system. Field conditions, openings, structural requirements, local codes, engineering, and supplier requirements should be verified before materials are purchased.
