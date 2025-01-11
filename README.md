

# IV-2425-Team4 - Dashboard zur visuellen Analyse von Verkehrsunfällen in Mainz

## Projektübersicht

Dieses Projekt umfasst die Entwicklung eines interaktiven Dashboards zur Analyse von Verkehrsunfällen in Mainz. 
Grundlage des Dashboards sind die bereitgestellten Unfalldaten in der `Verkehrsunfalldaten.csv`.

## Zielgruppe

- **Data Scientists**
- **Verkehrsanalysten**

## Funktionen des Dashboards

1. **Visualisierung der Modellklassifikationen**:
   - Anzeige der wahren und vorhergesagten Klassen auf einer interaktiven Karte.
   - Visualisierung der Einflussfaktoren, Beteiligten, des zeitlicher Verlaufs und einer Überblick Sektion in Form von statistischen Diagrammen.

2. **Integration von Unsicherheitsfaktoren**:
   - Darstellung der Unsicherheiten in den Modellvorhersagen pro Datenpunkt, um Unfälle mit hoher und niedriger Sicherheit erkennbar zu machen.

3. **XAI-Komponente**:
   - Integration der SHAP-Werte zur Erklärung der Modellentscheidungen.
   - Visualisierung der SHAP-Werte punktuell für einzelne Unfälle.

4. **Interaktive Analyse**:
- Highlighting und Filtern nach Lichtbedingungen, Straßenbeschaffenheit, Unfallbeteiligten, Unfallklasse, Wetterbedingungen, Tageszeit ...

## Getting started
1. **Voraussetzungen**:
   - Python 3.12.X
   - Abhängigkeiten: `requirements.txt`

2. **Schritte zur Installation**:
    ```bash
    git clone https://github.com/FerreiraNuno/mainz_unfallvis.git
    cd mainz_unfallvis
    conda create -n infovis python=3.12
    conda activate infovis
    pip install -r requirements.txt
    python main.py
    ```
### Icon Attribution

- Icons by [Icons8](https://icons8.com/icons) is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/).
