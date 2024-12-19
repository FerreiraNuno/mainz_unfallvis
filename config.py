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
    CONSTS.UNFALLART: {
        "0": "rgb(255, 99, 132)",   # Unfall anderer Art
        # Zusammenstoß mit anfahrendem/anhaltendem/ruhendem Fahrzeug
        "1": "rgb(54, 162, 235)",
        # Zusammenstoß mit vorausfahrendem/wartendem Fahrzeug
        "2": "rgb(255, 206, 86)",
        # Zusammenstoß mit seitlich in gleicher Richtung fahrendem Fahrzeug
        "3": "rgb(75, 192, 192)",
        # Zusammenstoß mit entgegenkommendem Fahrzeug
        "4": "rgb(153, 102, 255)",
        # Zusammenstoß mit einbiegendem/kreuzendem Fahrzeug
        "5": "rgb(255, 159, 64)",
        # Zusammenstoß zwischen Fahrzeug und Fußgänger
        "6": "rgb(201, 203, 207)",
        "7": "rgb(140, 30, 140)",   # Aufprall auf Fahrbahnhindernis
        "8": "rgb(99, 255, 132)",   # Abkommen von Fahrbahn nach rechts
        "9": "rgb(132, 132, 132)",  # Abkommen von Fahrbahn nach links
    },
    CONSTS.UNFALLTYP: {
        "1": "rgb(255, 0, 0)",     # Fahrunfall
        "2": "rgb(0, 128, 0)",     # Abbiegeunfall
        "3": "rgb(0, 0, 255)",     # Einbiegen / Kreuzen-Unfall
        "4": "rgb(255, 165, 0)",   # Überschreiten-Unfall
        "5": "rgb(128, 0, 128)",   # Unfall durch ruhenden Verkehr
        "6": "rgb(75, 0, 130)",    # Unfall im Längsverkehr
        "7": "rgb(169, 169, 169)",  # sonstiger Unfall
    },
    CONSTS.UNFALLKLASSE_WAHR: {
        "0": "red",
        "1": "orange",
        "2": "green",
    },
    CONSTS.LICHTVERHAELTNISSE: {
        # Tageslicht (bright yellow, represents daylight)
        "0": "rgb(255, 223, 0)",
        "1": "rgb(255, 140, 0)",   # Dämmerung (orange, represents twilight)
        # Dunkelheit (dark blue, represents darkness)
        "2": "rgb(50, 50, 150)"
    },
    CONSTS.STRASSENVERHAELTNISSE: {
        # trocken (dry) - Green to indicate safety/stability.
        "0": "rgb(34, 139, 34)",
        # nass/feucht/schlüpfrig (wet/slippery) - Blue to signify water or moisture.
        "1": "rgb(70, 130, 180)",
        # winterglatt (icy) - Snowy white to represent wintery/icy conditions.
        "2": "rgb(255, 250, 250)"
    },
    CONSTS.STRASSENART: {
        # Wochenende (Weekend) - Vibrant red-orange to symbolize activity and leisure.
        "0": "rgb(255, 69, 0)",
        # Wochentag (Weekday) - Calm blue to represent routine and workdays.
        "1": "rgb(30, 144, 255)"
    },
    CONSTS.TAGKATEGORIE: {
        # Bauarbeiten - Orange for construction zones.
        "construction": "rgb(255, 165, 0)",
        # Verkehrsberuhigter Bereich - Green for calm residential areas.
        "living_street": "rgb(50, 205, 50)",
        # Autobahn - Blue for major highways.
        "motorway": "rgb(0, 0, 255)",
        # Autobahnanschluss - Light blue for motorway connections.
        "motorway_link": "rgb(0, 191, 255)",
        # Weg - Brown for paths or footways.
        "path": "rgb(160, 82, 45)",
        # Hauptstraße - Bright red for main roads.
        "primary": "rgb(255, 69, 0)",
        # Hauptstraßenanschluss - Orange-red for primary road links.
        "primary_link": "rgb(255, 140, 0)",
        # Wohnstraße - Light blue for residential streets.
        "residential": "rgb(173, 216, 230)",
        # Nebenstraße - Gold for secondary roads.
        "secondary": "rgb(255, 215, 0)",
        # Nebenstraßenanschluss - Darker gold for secondary road links.
        "secondary_link": "rgb(218, 165, 32)",
        # Serviceweg - Silver for service streets.
        "service": "rgb(192, 192, 192)",
        # Tertiärstraße - Olive for tertiary roads.
        "tertiary": "rgb(128, 128, 0)",
        # Fahrweg - Dark brown for agricultural/forestry tracks.
        "track": "rgb(139, 69, 19)",
        # Schnellstraße - Indigo for high-speed roads.
        "trunk": "rgb(75, 0, 130)",
        # Schnellstraßenanschluss - Purple for trunk road links.
        "trunk_link": "rgb(123, 104, 238)",
        # Nicht klassifiziert - Grey for unclassified roads.
        "unclassified": "rgb(169, 169, 169)",
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
