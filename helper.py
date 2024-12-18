import consts as CONSTS
import pandas as pd


def prepareData(accidents_data):
    # Prepare data
    accidents_data[CONSTS.CUSTOM_DATETIME] = pd.to_datetime(
        {
            "year": accidents_data[CONSTS.JAHR],
            "month": accidents_data[CONSTS.MONAT],
            "day": 1,
        }
    )  # prepare datetime column
    accidents_data[CONSTS.UNFALLKLASSE_WAHR] = accidents_data[
        CONSTS.UNFALLKLASSE_WAHR
    ].astype(str)
    accidents_data[CONSTS.UNFALLART] = accidents_data[CONSTS.UNFALLART].astype(
        str)
    accidents_data[CONSTS.UNFALLTYP] = accidents_data[CONSTS.UNFALLTYP].astype(
        str)
    accidents_data[CONSTS.LICHTVERHAELTNISSE] = accidents_data[
        CONSTS.LICHTVERHAELTNISSE
    ].astype(str)
    accidents_data[CONSTS.STRASSENVERHAELTNISSE] = accidents_data[
        CONSTS.STRASSENVERHAELTNISSE
    ].astype(str)
    accidents_data[CONSTS.STRASSENART] = accidents_data[CONSTS.STRASSENART].astype(
        str)
    accidents_data[CONSTS.TAGKATEGORIE] = accidents_data[CONSTS.TAGKATEGORIE].astype(
        str)

    return accidents_data


def prepare_marks(date_range_monthly):
    marks_dict = {key: value for key,
                  value in date_range_monthly.items() if key % 3 == 0}
    last_key = list(date_range_monthly.keys())[-1]
    marks_dict[last_key] = date_range_monthly.get(last_key)
    return marks_dict


def generateDateRangeByMinAndMaxDate(df):
    start = str(df[CONSTS.JAHR].min()) + "-" + \
        str(df[CONSTS.MONAT].min()) + "-" + "1"
    end = str(df[CONSTS.JAHR].max()) + "-" + \
        str(df[CONSTS.MONAT].max()) + "-" + "1"
    month_year_range = pd.date_range(
        start=start, end=end, freq="MS"
    )  # MS DateOffset Monthly Starting

    return {
        each: {"label": str(date), "style": {'transform': 'rotate(45deg)'}}
        for each, date in enumerate(month_year_range.unique().strftime("%m.%Y"))
    }
