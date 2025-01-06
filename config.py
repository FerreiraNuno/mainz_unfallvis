import consts as CONSTS
import plotly.express as px

rewrite_unfallklasse_wahr = {
    "0": "Unfall mit Getöteten",
    "1": "Unfall mit Schwerverletzten",
    "2": "Unfall mit Leichtverletzten",
}
rewrite_unfall_art = {
    "0": "Unfall anderer Art",
    "1": "Zusammenstoß mit anfahrendem/anhaltendem/ruhendem Fahrzeug",
    "2": "Zusammenstoß mit vorausfahrendem/wartendem Fahrzeug",
    "3": "Zusammenstoß mit seitlich in gleicher Richtung fahrendem Fahrzeug",
    "4": "Zusammenstoß mit entgegenkommendem Fahrzeug",
    "5": "Zusammenstoß mit einbiegendem/kreuzendem Fahrzeug",
    "6": "Zusammenstoß zwischen Fahrzeug und Fußgänger",
    "7": "Aufprall auf Fahrbahnhindernis",
    "8": "Abkommen von Fahrbahn nach rechts",
    "9": "Abkommen von Fahrbahn nach links",
}
rewrite_unfall_typ = {
    "1": "Fahrunfall",
    "2": "Abbiegeunfall",
    "3": "Einbiegen / Kreuzen-Unfall",
    "4": "Überschreiten-Unfall",
    "5": "Unfall durch ruhenden Verkehr",
    "6": "Unfall im Längsverkehr",
    "7": "sonstiger Unfall",
}
rewrite_licht = {"0": "Tageslicht", "1": "Dämmerung", "2": "Dunkelheit"}
rewrite_strassen_ver = {
    "0": "trocken",
    "1": "nass/feucht/schlüpfrig",
    "2": "winterglatt",
}
rewrite_tag_kategorie = {"0": "Wochenende", "1": "Wochentag"}
rewrite_strassen_typ = {
    "construction": "Bauarbeiten (construction site)",
    "living_street": "Verkehrsberuhigter Bereich",
    "motorway": "Autobahn",
    "motorway_link": "Autobahnanschluss (motorway link)",
    "path": "Weg (or Pfad for footpaths)",
    "primary": "Hauptstraße (primary road)",
    "primary_link": "Hauptstraßenanschluss (primary road link)",
    "residential": "Wohnstraße",
    "secondary": "Nebenstraße (secondary road)",
    "secondary_link": "Nebenstraßenanschluss (secondary road link)",
    "service": "Serviceweg (or Zubringerstraße for service streets)",
    "tertiary": "Tertiärstraße (tertiary road)",
    "track": "Fahrweg (or Wirtschaftsweg for agricultural/forestry tracks)",
    "trunk": "Schnellstraße (or Hauptverkehrsstraße)",
    "trunk_link": "Schnellstraßenanschluss (trunk road link)",
    "unclassified": "Nicht klassifiziert (unclassified)",
}


rewriteDict = {
    CONSTS.UNFALLART: rewrite_unfall_art,
    CONSTS.UNFALLTYP: rewrite_unfall_typ,
    CONSTS.UNFALLKLASSE_WAHR: rewrite_unfallklasse_wahr,
    CONSTS.LICHTVERHAELTNISSE: rewrite_licht,
    CONSTS.STRASSENVERHAELTNISSE: rewrite_strassen_ver,
    CONSTS.STRASSENART: rewrite_strassen_typ,
    CONSTS.TAGKATEGORIE: rewrite_tag_kategorie,
}


customColoringMap = {
    "normal": {
        CONSTS.UNFALLART: {
            "0": "rgb(255, 99, 132)",
            "1": "rgb(54, 162, 235)",
            "2": "rgb(255, 206, 86)",
            "3": "rgb(75, 192, 192)",
            "4": "rgb(153, 102, 255)",
            "5": "rgb(255, 159, 64)",
            "6": "rgb(201, 203, 207)",
            "7": "rgb(140, 30, 140)",
            "8": "rgb(99, 255, 132)",
            "9": "rgb(132, 132, 132)",
        },
        CONSTS.UNFALLTYP: {
            "1": "rgb(255, 0, 0)",
            "2": "rgb(0, 128, 0)",
            "3": "rgb(0, 0, 255)",
            "4": "rgb(255, 165, 0)",
            "5": "rgb(128, 0, 128)",
            "6": "rgb(75, 0, 130)",
            "7": "rgb(169, 169, 169)",
        },
        CONSTS.UNFALLKLASSE_WAHR: {
            "0": "red",
            "1": "orange",
            "2": "green",
        },
        CONSTS.LICHTVERHAELTNISSE: {
            "0": "rgb(255, 223, 0)",
            "1": "rgb(255, 140, 0)",
            "2": "rgb(50, 50, 150)"
        },
        CONSTS.STRASSENVERHAELTNISSE: {
            "0": "rgb(34, 139, 34)",
            "1": "rgb(70, 130, 180)",
            "2": "rgb(255, 250, 250)"
        },
        CONSTS.STRASSENART: {
            "0": "rgb(255, 69, 0)",
            "1": "rgb(30, 144, 255)"
        },
        CONSTS.TAGKATEGORIE: {
            "construction": "rgb(255, 165, 0)",
            "living_street": "rgb(50, 205, 50)",
            "motorway": "rgb(0, 0, 255)",
            "motorway_link": "rgb(0, 191, 255)",
            "path": "rgb(160, 82, 45)",
            "primary": "rgb(255, 69, 0)",
            "primary_link": "rgb(255, 140, 0)",
            "residential": "rgb(173, 216, 230)",
            "secondary": "rgb(255, 215, 0)",
            "secondary_link": "rgb(218, 165, 32)",
            "service": "rgb(192, 192, 192)",
            "tertiary": "rgb(128, 128, 0)",
            "track": "rgb(139, 69, 19)",
            "trunk": "rgb(75, 0, 130)",
            "trunk_link": "rgb(123, 104, 238)",
            "unclassified": "rgb(169, 169, 169)",
        },
    },
    "protanopia": {
        CONSTS.UNFALLART: {
            "0": "rgb(200, 60, 80)",
            "1": "rgb(80, 120, 180)",
            "2": "rgb(240, 200, 80)",
            "3": "rgb(80, 160, 160)",
            "4": "rgb(140, 100, 200)",
            "5": "rgb(240, 140, 60)",
            "6": "rgb(180, 180, 180)",
            "7": "rgb(120, 20, 120)",
            "8": "rgb(80, 200, 110)",
            "9": "rgb(120, 120, 120)",
        },
        CONSTS.UNFALLTYP: {
            "1": "rgb(180, 0, 0)",
            "2": "rgb(0, 100, 0)",
            "3": "rgb(0, 0, 180)",
            "4": "rgb(200, 140, 0)",
            "5": "rgb(100, 0, 100)",
            "6": "rgb(50, 0, 100)",
            "7": "rgb(120, 120, 120)",
        },
        CONSTS.UNFALLKLASSE_WAHR: {
            "0": "red",
            "1": "yellow",
            "2": "blue",
        },
        CONSTS.LICHTVERHAELTNISSE: {
            "0": "rgb(200, 200, 50)",
            "1": "rgb(200, 120, 50)",
            "2": "rgb(50, 50, 120)"
        },
        CONSTS.STRASSENVERHAELTNISSE: {
            "0": "rgb(50, 100, 50)",
            "1": "rgb(50, 100, 150)",
            "2": "rgb(230, 230, 230)"
        },
        CONSTS.STRASSENART: {
            "0": "rgb(200, 50, 30)",
            "1": "rgb(60, 120, 180)"
        },
        CONSTS.TAGKATEGORIE: {
            "construction": "rgb(200, 140, 50)",
            "living_street": "rgb(80, 160, 80)",
            "motorway": "rgb(50, 50, 180)",
            "motorway_link": "rgb(50, 100, 180)",
            "path": "rgb(120, 60, 40)",
            "primary": "rgb(200, 50, 50)",
            "primary_link": "rgb(200, 100, 50)",
            "residential": "rgb(140, 180, 230)",
            "secondary": "rgb(200, 180, 50)",
            "secondary_link": "rgb(180, 140, 60)",
            "service": "rgb(160, 160, 160)",
            "tertiary": "rgb(100, 100, 50)",
            "track": "rgb(100, 60, 40)",
            "trunk": "rgb(60, 20, 100)",
            "trunk_link": "rgb(100, 80, 180)",
            "unclassified": "rgb(120, 120, 120)",
        },
    },
    "tritanopia": {
        CONSTS.UNFALLART: {
            "0": "rgb(220, 80, 80)",
            "1": "rgb(90, 140, 180)",
            "2": "rgb(230, 210, 100)",
            "3": "rgb(90, 170, 150)",
            "4": "rgb(150, 120, 200)",
            "5": "rgb(220, 140, 60)",
            "6": "rgb(170, 170, 170)",
            "7": "rgb(110, 30, 110)",
            "8": "rgb(90, 200, 100)",
            "9": "rgb(120, 120, 120)",
        },
        CONSTS.UNFALLTYP: {
            "1": "rgb(180, 50, 50)",
            "2": "rgb(50, 100, 50)",
            "3": "rgb(60, 60, 170)",
            "4": "rgb(200, 150, 50)",
            "5": "rgb(100, 50, 100)",
            "6": "rgb(50, 20, 100)",
            "7": "rgb(120, 120, 120)",
        },
        CONSTS.UNFALLKLASSE_WAHR: {
            "0": "red",
            "1": "orange",
            "2": "teal",
        },
        CONSTS.LICHTVERHAELTNISSE: {
            "0": "rgb(200, 200, 80)",
            "1": "rgb(200, 150, 50)",
            "2": "rgb(60, 80, 150)"
        },
        CONSTS.STRASSENVERHAELTNISSE: {
            "0": "rgb(60, 120, 60)",
            "1": "rgb(70, 120, 150)",
            "2": "rgb(240, 240, 240)"
        },
        CONSTS.STRASSENART: {
            "0": "rgb(210, 60, 50)",
            "1": "rgb(70, 140, 180)"
        },
        CONSTS.TAGKATEGORIE: {
            "construction": "rgb(210, 150, 50)",
            "living_street": "rgb(80, 170, 80)",
            "motorway": "rgb(60, 70, 170)",
            "motorway_link": "rgb(60, 100, 170)",
            "path": "rgb(140, 80, 60)",
            "primary": "rgb(210, 60, 50)",
            "primary_link": "rgb(210, 110, 60)",
            "residential": "rgb(160, 200, 230)",
            "secondary": "rgb(210, 190, 80)",
            "secondary_link": "rgb(190, 150, 60)",
            "service": "rgb(160, 160, 160)",
            "tertiary": "rgb(100, 110, 60)",
            "track": "rgb(120, 80, 60)",
            "trunk": "rgb(60, 30, 110)",
            "trunk_link": "rgb(100, 90, 170)",
            "unclassified": "rgb(130, 130, 130)",
        },
    },
}


highlighting_dropdown = [
    CONSTS.UNFALLKLASSE_WAHR,
    CONSTS.UNFALLART,
    CONSTS.UNFALLTYP,
    CONSTS.LICHTVERHAELTNISSE,
    CONSTS.STRASSENVERHAELTNISSE,
    CONSTS.STRASSENART,
    CONSTS.TAGKATEGORIE,
]


participants_checklist = [
    {'label': 'Fußgänger', 'value': CONSTS.ISTFUSS},
    {'label': 'Motorrad', 'value': CONSTS.ISTKRAD},
    {'label': 'PKW', 'value': CONSTS.ISTPKW},
    {'label': 'Fahrrad', 'value': CONSTS.ISTRAD},
    {'label': 'Sonstiges', 'value': CONSTS.ISTSONSTIG},
]

participants_view_checklist = [
    {'label': 'Fußgänger', 'value': CONSTS.ISTFUSS, 'disabled': True},
    {'label': 'Motorrad', 'value': CONSTS.ISTKRAD, 'disabled': True},
    {'label': 'PKW', 'value': CONSTS.ISTPKW, 'disabled': True},
    {'label': 'Fahrrad', 'value': CONSTS.ISTRAD, 'disabled': True},
    {'label': 'Sonstiges', 'value': CONSTS.ISTSONSTIG, 'disabled': True},
]
