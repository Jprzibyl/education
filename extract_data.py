### import modules ###
import pandas as pd
import json
import os
import dhs_f
import fnmatch
import pyreadstat
import re


## questionaires ##
questionaires = ['IR', 'MR', 'PR']
min_dhs_version = 5

### paths ###
## data ##
dhs_path = r"/mnt/datadisk/data/surveys/DHS_final_raw_data/"
dhs_extras_p = r"/mnt/datadisk/data/surveys/DHS_info/"

## project ##
projects_p = r"/mnt/datadisk/data/Projects/education/"
codes_to_keep_f = projects_p + 'pca/ressources/codes_and_questions.json'

## codes/questions we want to keep ##
# Opening JSON file
with open(codes_to_keep_f, 'r') as file:
    # returns JSON object as
    # a dictionary
    codes_to_keep = json.load(file)


def extract_survey_data(questionaire):

    dhs_d_all, country_d, data_file_types_d, typ_l, dhs_dirs_d = \
        dhs_f.load_dhs_data(dhs_path, dhs_extras_p)
    pathes = {}

    # catch all files
    for i, types in dhs_d_all.items():
        if 'GE' in types and questionaire in types:
            if int(i[2]) >= min_dhs_version:
                for (dirrpath, dirrnames, filenames) in os.walk(dhs_dirs_d[i][types.index(questionaire)]):
                    for file in filenames:
                        if fnmatch.fnmatch(file, '*.sav') or fnmatch.fnmatch(file, '*.SAV'):
                            # also get GE folder for matching
                            splitted_p = os.path.normpath(dhs_dirs_d[i][types.index('GE')]).split(os.sep)
                            pathes[splitted_p[-1]] = dirrpath + '/' + file
    print(len(pathes), pathes)

    df_l = []
    meta_l = []

    print(pathes)
    # iterate over files
    for n, (ge_f, path) in enumerate(pathes.items()):
        print('________________________', n, '(', len(pathes), ')', ' __________________________________')
        print(path)
        print(ge_f)
        try:
            df, meta = pyreadstat.read_sav(path, encoding='LATIN1')
        except:
            print("Encoding Error:", path)
            continue

        relevant_code, relevant_columns = codes_to_keep[questionaire].keys(), codes_to_keep[questionaire].values()
        #only use relevant columns
        df = df[df.columns[df.columns.isin(relevant_code)]]

        for column_code, column_name in meta.column_names_to_labels.items():
            if re.search('NA -.*?|^NA - .*?|^na -.*?|^na-.*?|.*?- NA$|NA - |NA -|-NA|NA-', column_name):
                df.drop(df.filter(column_code).columns, axis=1, inplace=True)


        df.reset_index(drop=True)

        # add GEID for matching files
        df["GEID"] = ge_f
        df_l.append(df)

    # concatenating
    df = pd.concat(
        df_l,
        axis=0,
        # join="outer",
        ignore_index=True,
        # keys=None,
        # levels=None,
        # names=None,
        verify_integrity=False,
        # copy=True,
    )

    # safe as csv
    df.to_csv(projects_p + f'pca/ressources/{questionaire}.csv')

    return df


for questionaire in questionaires:
    extract_survey_data(questionaire)

