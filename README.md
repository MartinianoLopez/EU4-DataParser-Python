# EU4 Data Parser

Parses Europa Universalis IV game files into clean, structured text files
for easier use in external projects (e.g. C++).

## Assets Structure

Place the following game files in `/assets` before running:

```phyton
assets/
├── countries/
│   └── (country files from game)
├── provinces/
│   └── (province files from game)
├── 00_countries.txt
└── definition.csv
```

## Output Format

```phyton
**countries.txt**
tag;name;r;g;b;money
SWE;Sweden;8;82;165;100

**provinces.txt**
id;r;g;b;name;owner
1;128;34;64;Stockholm;SWE
```

## What it does

- Reads raw game files from `/assets`
- Cross-references `definition.csv` to resolve province ownership
- Outputs clean CSV-style files to `/output`

## Usage

1. Copy game files into `/assets` following the structure above
2. Run the scriptP
