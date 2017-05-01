import pandas as pd

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



#metric to evaluate diversity of a school's student body
df.columns.get_loc("UGDS_WHITE") # 292
df.columns.get_loc("UGDS_HISPOLD") # 305
df_ethnic = df.ix[:, 292:306]
df_ethnic.replace(0.0, np.NaN, inplace=True)
df_ethnic["min"] = df_ethnic.min(axis=1, skipna=True, numeric_only=True)
df_ethnic["max"] = df_ethnic.max(axis=1, skipna=True, numeric_only=True)
df_ethnic = df_ethnic[df_ethnic["max"] != df_ethnic["min"]]
df_ethnic["diff"] = df_ethnic["max"] - df_ethnic["min"]
df_ethnic["diff"].min()

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