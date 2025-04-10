import pandas as pd
import numpy as np


# excel_file = snakemake.input[0]
# output_file = snakemake.output[0]
excel_file = "/home/adrian/Documents/Promotion/p10_heart/resources/sample_desc.xlsx"
output_file = "/home/adrian/Documents/Promotion/p10_heart/config/samples.tsv"


# Read excel and create header
df = pd.read_excel(excel_file, engine="openpyxl")


df = df.dropna(how="all")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
df.columns = [
    "id",
    "genotyp",
    "behandlung",
    "op",
    "number",
]
df = df.dropna(subset=["Tier-ID"])
df = df[df["Behandlung"].notna()]
df = df.reset_index(drop=True)

print(df.to_string())
# df = df.iloc[2:]
# df.columns = df.iloc[0]
# df = df[1:]
# df.reset_index(drop=True, inplace=True)
# # Comparision A
# df["trpalk_vs_wt"] = df.apply(
#     lambda row: (
#         "+"
#         if row["Probe Nr."] in [x for x in range(1, 18) if x != 14]
#         else "-" if row["Probe Nr."] in [x for x in range(18, 22)] else ""
#     ),
#     axis=1,
# )
# # Comparision B
# df["ptc_vs_atc_schilddruese"] = df.apply(
#     lambda row: (
#         "+"
#         if row["Probe Nr."] in [2, 6, 10, 11, 12, 13, 15]
#         else "-" if row["Probe Nr."] in [1, 3, 4, 5, 7, 8, 9, 16, 17] else ""
#     ),
#     axis=1,
# )
# df["ptc_vs_wt_schilddruese"] = df.apply(
#     lambda row: (
#         "+"
#         if row["Probe Nr."] in [2, 6, 10, 11, 12, 13, 15]
#         else "-" if row["Probe Nr."] in [x for x in range(18, 22)] else ""
#     ),
#     axis=1,
# )
# df["atc_vs_wt_schilddruese"] = df.apply(
#     lambda row: (
#         "+"
#         if row["Probe Nr."] in [1, 3, 4, 5, 7, 8, 9, 16, 17]
#         else "-" if row["Probe Nr."] in [x for x in range(18, 22)] else ""
#     ),
#     axis=1,
# )
# # Comparision C
# df["alk_inh_vs_solvent"] = df.apply(
#     lambda row: (
#         "+"
#         if row["Probe Nr."] in [1, 2, 3, 5, 6, 7, 9, 10, 13, 15, 16]
#         else "-" if row["Probe Nr."] in [4, 8, 11, 12, 17] else ""
#     ),
#     axis=1,
# )
# # Comparision D
# df["ptc_vs_atc_zellenvergleich"] = df.apply(
#     lambda row: (
#         "+"
#         if row["Probe Nr."] in [x for x in range(22, 27) if x != 23]
#         else "-" if row["Probe Nr."] in [x for x in range(27, 32) if x != 28] else ""
#     ),
#     axis=1,
# )
# samples_to_remove = [14, 23, 28]
# df = df[~df["Probe Nr."].isin(samples_to_remove)]
# df = df.rename(columns={"Probe Nr.": "sample", "Alter (d)": "alter_in_tagen"})
# print(df)
# df.columns = (
#     df.columns.str.replace(" ", "_")
#     .str.replace(":", "")
#     .str.lower()
#     .str.replace("ä", "ae")
#     .str.replace("ö", "oe")
#     .str.replace("ü", "ue")
#     .str.replace("ß", "ss")
# )
# df = df.replace(" ", "_", regex=True)
# df = df.dropna(subset=["sample"])
# df.reset_index(drop=True, inplace=True)
# # tsv_data = {
# #     'sample': df['sample_name'],
# #     'treatment': df['treatment'],
# #     'cohort': df['cohort'],
# #     'genotype': df['genotype'],
# #     'ldc_t3_in_wt_vs_ldc_in_wt_liver': df['ldc_t3_in_wt_vs_ldc_in_wt_liver'],
# #     'ldc_t3_in_wt_vs_ldc_t3_in_heptrbko_liver': df['ldc_t3_in_wt_vs_ldc_t3_in_heptrbko_liver'],
# #     'etoh_in_wt_vs_ldc_in_wt_liver': df['etoh_in_wt_vs_ldc_in_wt_liver'],
# #     'etoh_t3_in_wt_vs_etoh_in_wt_liver': df['etoh_t3_in_wt_vs_etoh_in_wt_liver'],
# #     'etoh_t3_in_wt_vs_etoh_t3_in_heptrbko_liver': df['etoh_t3_in_wt_vs_etoh_t3_in_heptrbko_liver'],
# #     'etoh_mgl_in_wt_vs_etho_in_wt_liver': df['etoh_mgl_in_wt_vs_etho_in_wt_liver'],
# #     'ldc_mgl_in_wt_vs_ldc_in_wt_liver': df['ldc_mgl_in_wt_vs_ldc_in_wt_liver'],
# #     'ldc_t3_in_wt_vs_ldc_in_wt_wat': df['ldc_t3_in_wt_vs_ldc_in_wt_wat'],
# #     'ldc_t3_in_wt_vs_ldc_t3_in_heptrbko_wat': df['ldc_t3_in_wt_vs_ldc_t3_in_heptrbko_wat'],
# #     'etoh_in_wt_vs_ldc_in_wt_wat': df['etoh_in_wt_vs_ldc_in_wt_wat'],
# #     'etoh_t3_in_wt_vs_etoh_in_wt_wat': df['etoh_t3_in_wt_vs_etoh_in_wt_wat'],
# #     'etoh_t3_in_wt_vs_etoh_t3_in_heptrbko_wat': df['etoh_t3_in_wt_vs_etoh_t3_in_heptrbko_wat'],
# #     'etoh_mgl_in_wt_vs_etho_in_wt_wat': df['etoh_mgl_in_wt_vs_etho_in_wt_wat'],
# #     'etoh_t3_in_wt_vs_ldc_in_wt_liver': df['etoh_t3_in_wt_vs_ldc_in_wt_liver'],
# #     'etoh_mgl_in_wt_vs_ldc_in_wt_liver': df['etoh_mgl_in_wt_vs_ldc_in_wt_liver']
# # }
# # # Konvertiere das Wörterbuch in ein DataFrame für die tsv-Datei
# # tsv_df = pd.DataFrame(tsv_data)
# # # Speichern der Daten im TSV-Format ohne Index und mit Tabulator als Trennzeichen
# df.to_csv(output_file, sep="\t", index=False)
