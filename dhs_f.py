import os
import csv
import fnmatch
import numpy as np


def load_dhs_data(dhs_path, dhs_extras_p, return_paths=False):
    for (dirrpath, dirrnames, filenames) in os.walk(dhs_path):
        print(dirrpath, dirrnames, filenames)
        #only these folder are needed
        break

    dirrnames.sort()

    ctry_s = set()
    typ_s = set()
    file_format_s = set()
    file_format_d = {'FL': 'flat', 'SV': 'SPSS'}

    dhs_d_all = {}
    dhs_dirs_d = {}
    for dirr in dirrnames:
        ctry = dirr[:2]
        ctry_s.add(ctry)
        typ = dirr[2:4]
        typ_s.add(typ)
        vrsn = dirr[4:5]
        # vrsnb is release version (if corrections have been made) - needs to be seperated for matching purposes
        vrsnb = dirr[5:6]
        try:
            if type(int(vrsnb)) == int:
                survey_n = 1
        except ValueError:
            if vrsnb in 'ABCDEFGH':
                survey_n = 2
            elif vrsnb in 'IJKLMNOPQ':
                survey_n = 3
            elif vrsnb in 'RSTUVWXYZ':
                survey_n = 4
            else:
                raise IOError("this version should not exist: " + vrsnb)
        survey_n = str(survey_n)
        file_format = dirr[6:]
        file_format_s.add(file_format)
        k = ctry + vrsn + survey_n
        #only select shps and spss data
        if file_format == 'SV':
            try:
                dhs_d_all[k].append(typ)
                dhs_dirs_d[k].append(dirrpath + dirr)
            except KeyError:
                dhs_d_all[k] = [typ]
                dhs_dirs_d[k] = [dirrpath + dirr]
        else:
            if typ == 'GE':
                try:
                    dhs_d_all[k].append(typ)
                    dhs_dirs_d[k].append(dirrpath + dirr)
                except KeyError:
                    dhs_d_all[k] = [typ]
                    dhs_dirs_d[k] = [dirrpath + dirr]

    dhs_d_all = dict(sorted(dhs_d_all.items()))
    # print(dhs_d_all)


    ctry_l = list(ctry_s)
    ctry_l.sort()
    typ_l = list(typ_s)
    typ_l.sort()


    country_d = {}
    input_file = csv.reader(open(f"{dhs_extras_p}/country_codes.csv"), delimiter='\t')
    for row in input_file:
        country_d[row[0]] = row[1]

    data_file_types_d = {}
    input_file = csv.reader(open(f"{dhs_extras_p}/data_file_types.csv"), delimiter='\t')
    for row in input_file:
        data_file_types_d[row[0]] = row[1]

    return dhs_d_all, country_d, data_file_types_d, typ_l, dhs_dirs_d

