import consts as CONSTS
import plotly.express as px

rewrite_unfallk_wahr = {
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
    CONSTS.UNFALLKLASSE_WAHR: rewrite_unfallk_wahr,
    CONSTS.LICHTVERHAELTNISSE: rewrite_licht,
    CONSTS.STRASSENVERHAELTNISSE: rewrite_strassen_ver,
    CONSTS.STRASSENART: rewrite_strassen_typ,
    CONSTS.TAGKATEGORIE: rewrite_tag_kategorie,
}


customColoringMap = {
    CONSTS.UNFALLART: px.colors.sequential.Aggrnyl,
    CONSTS.UNFALLTYP: px.colors.sequential.Aggrnyl,
    CONSTS.UNFALLKLASSE_WAHR: [
        "rgb(255, 0, 0)",
        "rgb(0, 255, 0)",
        "rgb(0, 0, 255)",
    ],
    CONSTS.LICHTVERHAELTNISSE: px.colors.sequential.Aggrnyl,
    CONSTS.STRASSENVERHAELTNISSE: px.colors.sequential.Aggrnyl,
    CONSTS.STRASSENART: px.colors.sequential.Aggrnyl,
    CONSTS.TAGKATEGORIE: px.colors.sequential.Aggrnyl,
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


participants_checklist =[
    {'label': 'Fußgänger', 'value': CONSTS.ISTFUSS},
    {'label': 'Motorrad', 'value': CONSTS.ISTKRAD},
    {'label': 'PKW', 'value': CONSTS.ISTPKW},
    {'label': 'Fahrrad', 'value': CONSTS.ISTRAD},
    {'label': 'Sonstiges', 'value': CONSTS.ISTSONSTIG},
]

participants_view_checklist =[
    {'label': 'Fußgänger', 'value': CONSTS.ISTFUSS, 'disabled':True},
    {'label': 'Motorrad', 'value': CONSTS.ISTKRAD, 'disabled':True},
    {'label': 'PKW', 'value': CONSTS.ISTPKW, 'disabled':True},
    {'label': 'Fahrrad', 'value': CONSTS.ISTRAD, 'disabled':True},
    {'label': 'Sonstiges', 'value': CONSTS.ISTSONSTIG, 'disabled':True},
]