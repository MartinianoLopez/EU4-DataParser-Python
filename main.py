import csv
import os

# ── Modelos ──────────────────────────────────────────────────────────────────

class Province:
    def __init__(self, id, name, bmp_color, owner):
        self.id = id
        self.name = name
        self.bmp_color = bmp_color
        self.owner = owner

class Country:
    def __init__(self, tag, name, color):
        self.tag = tag
        self.name = name
        self.color = color

# ── Datos globales ────────────────────────────────────────────────────────────

provinces = []
countries = []

province_by_id = {}
country_paths = {}

# ── Loaders ───────────────────────────────────────────────────────────────────

def loadDefinitions(filepath):

    with open(filepath, "r", encoding="latin-1") as f:

        reader = csv.reader(f, delimiter=";")

        for row in reader:

            if not row or not row[0].isdigit():
                continue

            province_id = int(row[0])

            color = (
                int(row[1]),
                int(row[2]),
                int(row[3])
            )

            name = row[4].strip()

            province = Province(
                id=province_id,
                name=name,
                bmp_color=color,
                owner="NONE"
            )

            provinces.append(province)

            province_by_id[province_id] = province

# ──────────────────────────────────────────────────────────────────────────────

def loadProvincesFiles(folder_path):

    for filename in os.listdir(folder_path):

        if not filename.endswith(".txt"):
            continue

        try:
            province_id = int(filename.split("-")[0])
        except ValueError:
            continue

        province = province_by_id.get(province_id)

        if province is None:
            continue

        filepath = os.path.join(folder_path, filename)

        with open(filepath, "r", encoding="latin-1") as f:

            # solo revisar primeras 5 lineas
            for _ in range(8):

                line = f.readline()

                if not line:
                    break

                line = line.strip()

                if "=" not in line:
                    continue

                left, right = line.split("=", 1)

                if left.strip().lower() != "owner":
                    continue

                tag = (
                    right
                    .strip()
                    .replace('"', '')
                    [:3]
                    .upper()
                )

                province.owner = tag

                break
# ──────────────────────────────────────────────────────────────────────────────

def loadCountryTagToCountryName(filepath):

    with open(filepath, "r", encoding="latin-1") as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split("=")

            if len(parts) != 2:
                continue

            tag = (
                parts[0]
                .strip()
                [:3]
                .upper()
            )

            country_file = (
                parts[1]
                .strip()
                .replace('"', '')
            )

            name = os.path.splitext(
                os.path.basename(country_file)
            )[0]

            country_paths[tag] = country_file

            countries.append(
                Country(
                    tag=tag,
                    name=name,
                    color=(0, 0, 0)
                )
            )

# ──────────────────────────────────────────────────────────────────────────────

def loadOwnerToColor(countries_folder):

    for country in countries:

        filepath = os.path.join(
            countries_folder,
            os.path.basename(country_paths[country.tag])
        )

        try:

            with open(filepath, "r", encoding="latin-1") as f:

                for line in f:

                    line = line.strip()

                    if line.startswith("color"):

                        nums = (
                            line
                            .split("{")[1]
                            .split("}")[0]
                            .strip()
                            .split()
                        )

                        if len(nums) >= 3:

                            country.color = (
                                int(nums[0]),
                                int(nums[1]),
                                int(nums[2])
                            )

                        break

        except FileNotFoundError:
            continue

# ── Export ───────────────────────────────────────────────────────────────────

def exportData(output_folder):

    os.makedirs(output_folder, exist_ok=True)

    # provinces.txt
    # id;r;g;b;name;owner

    with open(
        os.path.join(output_folder, "provinces.txt"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write("id;r;g;b;name;owner\n")

        for p in provinces:

            r, g, b = p.bmp_color

            owner = p.owner if p.owner else "NON"

            f.write(
                f"{p.id};"
                f"{r};"
                f"{g};"
                f"{b};"
                f"{p.name};"
                f"{owner}\n"
            )

    # countries.txt
    # tag;name;r;g;b;money

    with open(
        os.path.join(output_folder, "countries.txt"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write("tag;name;r;g;b;money\n")

        for c in countries:

            r, g, b = c.color

            f.write(
                f"{c.tag};"
                f"{c.name};"
                f"{r};"
                f"{g};"
                f"{b};"
                f"100\n"
            )

# ── Main ──────────────────────────────────────────────────────────────────────

def run(
    definitions_path,
    provinces_folder,
    countries_file,
    countries_folder,
    output_folder
):

    loadDefinitions(definitions_path)

    loadProvincesFiles(provinces_folder)

    loadCountryTagToCountryName(countries_file)

    loadOwnerToColor(countries_folder)

    exportData(output_folder)

    print(
        f"Listo: "
        f"{len(provinces)} provincias y "
        f"{len(countries)} países exportados."
    )

# ── Ejecutar ──────────────────────────────────────────────────────────────────

run(
    "assets/definition.csv",
    "assets/provinces/",
    "assets/00_countries.txt",
    "assets/countries/",
    "output/"
)