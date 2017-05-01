import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

df = pd.read_csv('/Users/giridhar.manoharan/Documents/data_incubator/CollegeScorecard_Raw_Data/MERGED2013_14_PP.csv')
print(df)

# Average SAT score for students
df_4_deg = df[df["HIGHDEG"] == 4]
df_4_deg["SAT_AVG_ALL"].mean()

# pearson correlation
df_corr = df[["SAT_AVG", "ENRL_ORIG_YR4_RT"]]
df_corr = df_corr[df_corr["SAT_AVG"].notnull()]
df_corr = df_corr[df_corr["ENRL_ORIG_YR4_RT"].notnull()]
df_corr = df_corr[df_corr["ENRL_ORIG_YR4_RT"] != 'PrivacySuppressed']
df_corr["ENRL_ORIG_YR4_RT"] = df_corr["ENRL_ORIG_YR4_RT"].astype("float64")
df_corr.corr(method='pearson')

# average percentage difference between high and low income students who graduate within 4 years
df_4yr_deg = df[df["HIGHDEG"] == 4]
df_4yr_deg = df[["LO_INC_COMP_ORIG_YR4_RT", "MD_INC_COMP_ORIG_YR4_RT", "HI_INC_COMP_ORIG_YR4_RT"]]
df_4yr_deg = df_4yr_deg.convert_objects(convert_numeric=True).dropna()
print(df_4yr_deg["HI_INC_COMP_ORIG_YR4_RT"].mean() - df_4yr_deg["LO_INC_COMP_ORIG_YR4_RT"].mean())

# two sampled t-test and p-value
np.log10(ttest_ind(df_4yr_deg["HI_INC_COMP_ORIG_YR4_RT"], df_4yr_deg["LO_INC_COMP_ORIG_YR4_RT"])[1])


# metric to evaluate diversity of a school's student body
df.columns.get_loc("UGDS_WHITE") # 292
df.columns.get_loc("UGDS_HISPOLD") # 305
df_ethnic = df.ix[:, 292:306]
df_ethnic.replace(0.0, np.NaN, inplace=True)
df_ethnic["min"] = df_ethnic.min(axis=1, skipna=True, numeric_only=True)
df_ethnic["max"] = df_ethnic.max(axis=1, skipna=True, numeric_only=True)
df_ethnic = df_ethnic[df_ethnic["max"] != df_ethnic["min"]]
df_ethnic["diff"] = df_ethnic["max"] - df_ethnic["min"]
df_ethnic["diff"].min()


#average share of enrollment of undergraduate women
file_names = ["MERGED2001_02_PP.csv", "MERGED2002_03_PP.csv", "MERGED2003_04_PP.csv", "MERGED2004_05_PP.csv", "MERGED2005_06_PP.csv", "MERGED2006_07_PP.csv", "MERGED2007_08_PP.csv", "MERGED2008_09_PP.csv", "MERGED2009_10_PP.csv", "MERGED2010_11_PP.csv"]
UGDS_WOMEN_enrol_mean = 0.0
for fname in file_names:
    df = pd.read_csv('./CollegeScorecard_Raw_Data/'+fname)
    print(df["UGDS_WOMEN"].mean())
    UGDS_WOMEN_enrol_mean += df["UGDS_WOMEN"].mean()
UGDS_WOMEN_enrol_mean /= len(file_names)
print('Mean: '+str(UGDS_WOMEN_enrol_mean))

# largest probability an academic institution in that region is located in a city
df = pd.read_csv('./CollegeScorecard_Raw_Data/MERGED1996_97_PP.csv')
file_names = ["MERGED1997_98_PP.csv", "MERGED1998_99_PP.csv", "MERGED1999_00_PP.csv", "MERGED2000_01_PP.csv", "MERGED2001_02_PP.csv", "MERGED2002_03_PP.csv", "MERGED2003_04_PP.csv", "MERGED2004_05_PP.csv", "MERGED2005_06_PP.csv", "MERGED2006_07_PP.csv", "MERGED2007_08_PP.csv", "MERGED2008_09_PP.csv", "MERGED2009_10_PP.csv", "MERGED2010_11_PP.csv", "MERGED2011_12_PP.csv", "MERGED2012_13_PP.csv", "MERGED2013_14_PP.csv", "MERGED2014_15_PP.csv"]
for fname in file_names:
    df = df.append(pd.read_csv('./CollegeScorecard_Raw_Data/'+fname))
    df = df.drop_duplicates(subset='UNITID')
df = df.drop_duplicates(subset='UNITID')
df_rg = df[["UNITID","REGION","LOCALE"]].dropna().groupby(by=['REGION'])
max_prob = 0.0
for name, group in df_rg:
    prob = float(len(df_rg.get_group(name)[df_rg.get_group(name)['LOCALE'] <= 13].index)) / float(len(df_rg.get_group(name).index))
    print(name, len(df_rg.get_group(name)[df_rg.get_group(name)['LOCALE'] <= 13].index), len(df_rg.get_group(name).index), prob)
    max_prob = max(prob, max_prob)
print("Max Probability: "+str(max_prob))


######### ROUGH WORK ##########
df.columns.get_loc("SAT_AVG")
df.columns.get_loc("SAT_AVG_ALL")
df.columns.get_loc("UGDS")
df.iloc[:50, (59,60,290)]

df.iloc[:10, 59].notnull()

df[df["SAT_AVG_ALL"].notnull()].iloc[:10, (60, 290)]


df1 = df[["HIGHDEG", "SAT_AVG_ALL", "UGDS"]].copy()
df1 = df1[df1.UGDS.notnull()]
df1 = df1[df1.SAT_AVG_ALL.notnull()]
df1 = df1[df1["HIGHDEG"] == 4]
df1["UGDS_4"] = df1["UGDS"] / 4
df1["SAT_TOTAL"] = df1["SAT_AVG_ALL"] * df1["UGDS_4"]
df1["SAT_TOTAL"].sum() / df1["UGDS_4"].sum()