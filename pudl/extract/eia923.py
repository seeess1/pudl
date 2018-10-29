"""
Retrieve data from EIA Form 923 spreadsheets for analysis.

This modules pulls data from EIA's published Excel spreadsheets.

This code is for use analyzing EIA Form 923 data. Currenly only
years 2009-2016 work, as they share nearly identical file formatting.
"""

import pandas as pd
import os.path
import glob
from pudl.settings import SETTINGS
import pudl.constants as pc

###########################################################################
# Helper functions & other objects to ingest & process Energy Information
# Administration (EIA) Form 923 data.
###########################################################################


def datadir(year, basedir=SETTINGS['eia923_data_dir']):
    """
    Data directory search for EIA Form 923.

    Args:
        year (int): The year that we're trying to read data for.
        basedir (os.path): Directory in which EIA923 data resides.
    Returns:
        path to appropriate EIA 923 data directory.
    """
    # These are the only years we've got...
    assert year in pc.data_years['eia923']
    if year < 2008:
        return os.path.join(basedir, 'f906920_{}'.format(year))
    else:
        return os.path.join(basedir, 'f923_{}'.format(year))


def get_eia923_file(yr, basedir=SETTINGS['eia923_data_dir']):
    """
    Given a year, return the appopriate EIA923 excel file.

    Args:
        year (int): The year that we're trying to read data for.
        basedir (os.path): Directory in which EIA923 data resides.
    Returns:
        path to EIA 923 spreadsheets corresponding to a given year.
    """
    assert(yr >= min(pc.working_years['eia923'])),\
        "EIA923 file selection only works for 2009 & later."
    eia923_filematch = glob.glob(os.path.join(
        datadir(yr, basedir=basedir), '*2_3_4*'))
    # There can only be one!
    assert len(eia923_filematch) == 1, \
        'Multiple matching EIA923 spreadsheets found for {}'.format(yr)
    return eia923_filematch[0]


def get_eia923_column_map(page, year):
    """
    Given a year and EIA923 page, return info required to slurp it from Excel.

    The format of the EIA923 has changed slightly over the years, and so it
    is not completely straightforward to pull information from the spreadsheets
    into our analytical framework. This function looks up a map of the various
    tabs in the spreadsheet by year and page, and returns the information
    needed to name the data fields in a standardized way, and pull the right
    cells from each year & page into our database.

    Args:
        page (str): The string label indicating which page of the EIA923 we
            are attempting to read in. Must be one of the following:
                - 'generation_fuel'
                - 'stocks'
                - 'boiler_fuel'
                - 'generator'
                - 'fuel_receipts_costs'
                - 'plant_frame'
        year (int): The year that we're trying to read data for.

    Returns:
        sheet_name (int): An integer indicating which page in the worksheet
            the data should be pulled from. 0 is the first page, 1 is the
            second page, etc. For use by pandas.read_excel()
        skiprows (int): An integer indicating how many rows should be skipped
            at the top of the sheet being read in, before the header row that
            contains the strings which will be converted into column names in
            the dataframe which is created by pandas.read_excel()
        column_map (dict): A dictionary that maps the names of the columns
            in the year being read in, to the canonical EIA923 column names
            (i.e. the column names as they are in 2014-2016). This dictionary
            will be used by DataFrame.rename(). The keys are the column names
            in the dataframe as read from older years, and the values are the
            canonmical column names.  All should be stripped of leading and
            trailing whitespace, converted to lower case, and have internal
            non-alphanumeric characters replaced with underscores.
    """
    sheet_name = pc.tab_map_eia923.at[year, page]
    skiprows = pc.skiprows_eia923.at[year, page]

    page_to_df = {
        'generation_fuel': pc.generation_fuel_map_eia923,
        'stocks': pc.stocks_map_eia923,
        'boiler_fuel': pc.boiler_fuel_map_eia923,
        'generator': pc.generator_map_eia923,
        'fuel_receipts_costs': pc.fuel_receipts_costs_map_eia923,
        'plant_frame': pc.plant_frame_map_eia923}

    d = page_to_df[page].loc[year].to_dict()

    column_map = {}
    for k, v in d.items():
        column_map[v] = k

    return (sheet_name, skiprows, column_map)


def get_eia923_page(page, eia923_xlsx,
                    years=[2011, 2012, 2013, 2014, 2015, 2016],
                    verbose=True):
    """
    Read a single table from several years of EIA923 data. Return a DataFrame.

    Args:
        page (str): The string label indicating which page of the EIA923 we
        are attempting to read in. The page argument must be exactly one of the
        following strings:
            - 'generation_fuel'
            - 'stocks'
            - 'boiler_fuel'
            - 'generator'
            - 'fuel_receipts_costs'
            - 'plant_frame'

      years (list): The set of years to read into the dataframe.

    Returns:
        pandas.DataFrame: A dataframe containing the data from the selected
            page and selected years from EIA 923.
    """
    assert min(years) >= min(pc.working_years['eia923']),\
        "EIA923 works for 2009 and later. {} requested.".format(min(years))
    assert page in pc.tab_map_eia923.columns and page != 'year_index',\
        "Unrecognized EIA 923 page: {}".format(page)

    if verbose:
        print('Converting EIA 923 {} to DataFrame...'.format(page))
    df = pd.DataFrame()
    for yr in years:
        sheet_name, skiprows, column_map = get_eia923_column_map(page, yr)
        newdata = pd.read_excel(eia923_xlsx[yr],
                                sheet_name=sheet_name,
                                skiprows=skiprows)

        # Clean column names: lowercase, underscores instead of white space,
        # no non-alphanumeric characters
        newdata.columns = newdata.columns.str.replace('[^0-9a-zA-Z]+', ' ')
        newdata.columns = newdata.columns.str.strip().str.lower()
        newdata.columns = newdata.columns.str.replace(' ', '_')

        # Drop columns that start with "reserved" because they are empty
        to_drop = [c for c in newdata.columns if c[:8] == 'reserved']
        newdata.drop(to_drop, axis=1, inplace=True)

        # stocks tab is missing a YEAR column for some reason. Add it!
        if page == 'stocks':
            newdata['report_year'] = yr

        newdata = newdata.rename(columns=column_map)
        if page == 'stocks':
            newdata = newdata.rename(columns={
                'unnamed_0': 'census_division_and_state'})

        # Drop the fields with plant_id_eia 99999 or 999999.
        # These are state index
        if page != 'stocks':
            newdata = newdata[~newdata.plant_id_eia.isin([99999, 999999])]

        df = df.append(newdata)

    return df


def get_eia923_xlsx(years, verbose=True):
    """
    Read in Excel files to create Excel objects.

    Rather than reading in the same Excel files several times, we can just
    read them each in once (one per year) and use the ExcelFile object to
    refer back to the data in memory.

    Args:
        years: The years that we're trying to read data for.
    Returns:
        xlsx file of EIA Form 923 for input year(s)
    """
    eia923_xlsx = {}
    if verbose:
        print("Reading EIA 923 spreadsheet data")
    for yr in years:
        if verbose:
            print("    {}...".format(yr))
        eia923_xlsx[yr] = pd.ExcelFile(get_eia923_file(yr))
    return eia923_xlsx


def extract(eia923_years=pc.working_years['eia923'],
            verbose=True):
    """Extract all EIA 923 tables."""
    eia923_raw_dfs = {}
    if not eia923_years:
        if verbose:
            print('Not extracting EIA 923.')
        return eia923_raw_dfs

    # Prep for ingesting EIA923
    # Create excel objects
    eia923_xlsx = get_eia923_xlsx(eia923_years,
                                  verbose=verbose)

    # Create DataFrames
    for page in pc.tab_map_eia923.columns:
        if page != 'plant_frame':
            eia923_raw_dfs[page] = get_eia923_page(page, eia923_xlsx,
                                                   years=eia923_years,
                                                   verbose=verbose)

    return eia923_raw_dfs
