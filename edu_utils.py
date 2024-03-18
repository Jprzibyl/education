import pandas as pd
import numpy as np
import random
import os

def create_split(path, split_name, train_share=0.8, mode=None, label_column='Female Education PCA'):

    df = pd.read_csv(path+".csv")

    try:
        df.drop(columns='Unnamed: 0.1', inplace=True)
    except:
        pass

    df.dropna(subset=label_column, inplace=True)


    if mode=="train_test_validation":

        test_share = (1-train_share)/2+train_share
        train, validate, test = \
                      np.split(df.sample(frac=1, random_state=42),
                               [int(train_share*len(df)), int(test_share*len(df))])

        print(path, split_name, train_share)
        print("Train:", round(len(train)/len(df), 3))
        print("Test:", round(len(test)/len(df), 3))
        print("Validate:", round(len(validate)/len(df), 3))
        print("")

        train[split_name] = "train"
        validate[split_name] = "validation"
        test[split_name] = "test"

        dataframe = pd.concat([train, test, validate])

    if mode=="cross_validation":

        split1, split2, split3, split4, split5 = \
            np.split(df.sample(frac=1, random_state=42),
                     [int((1/5) * len(df)), int((1/5)*2 * len(df)), int((1/5)*3 * len(df)), int((1/5)*4 * len(df))])

        print(path, split_name)
        print("split1:", round(len(split1) / len(df), 3))
        print("split2:", round(len(split2) / len(df), 3))
        print("split3:", round(len(split3) / len(df), 3))
        print("split4:", round(len(split4) / len(df), 3))
        print("split5:", round(len(split5) / len(df), 3))
        print("")

        split1[split_name] = "split1"
        split2[split_name] = "split2"
        split3[split_name] = "split3"
        split4[split_name] = "split4"
        split5[split_name] = "split5"

        dataframe = pd.concat([split1, split2, split3, split4, split5])

    if mode==None:
        print(path, "Split: Sustain Bench")
        print("Train:", round(len(df[df["Split: Sustain Bench"] == "train"].index) / len(df), 3))
        print("Test:", round(len(df[df["Split: Sustain Bench"] == "test"].index) / len(df), 3))
        print("Validate:", round(len(df[df["Split: Sustain Bench"] == "validation"].index) / len(df), 3))
        print("")

        dataframe = df.dropna(subset="Split: Sustain Bench").copy()

    return

create_split("/mnt/datadisk/data/Projects/education/inputs/label/Education_Labels",
             "Random Split (Cross Val)", mode="cross_validation")


create_split("/mnt/datadisk/data/Projects/education/inputs/label/Education_Labels_Rural",
             "Random Split (Cross Val) Rural", mode="cross_validation")
create_split("/mnt/datadisk/data/Projects/education/inputs/label/Education_Labels_Urban",
             "Random Split (Cross Val) Urban", mode="cross_validation")


import itertools
listOLists = [
    [0.00001, 0.001]  # cfg.lr #[0.00001, 0.0001, 0.001, 0.01, 0.1]
    , [0.9]  # cfg.momentum #[0.3, 0.6, 0.9]
    , [32]
    , ['vgg16']  # 'vgg16', 'vgg19'
    # cfg.model_name #['vgg16', 'vgg19',  'resnet50', 'resnet152', 'inceptionv3', 'xception', 'densnet121', 'densnet201']
    , [20, 100]  # False/0:Non-trainable params: 0
    , ["SGD"]
    , [0.2]
    , [False, True]
    ]

c = []
for combination in itertools.product(*listOLists):
    c.append(combination)
    print(combination)
print(len(c))


