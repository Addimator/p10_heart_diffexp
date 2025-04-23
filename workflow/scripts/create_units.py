import pandas as pd
import numpy as np
import os


excel_file = snakemake.input["desc"]
data_path = snakemake.input["data"]

output_file = snakemake.output[0]
# excel_file = "/home/adrian/Documents/Promotion/p10_heart/resources/sample_desc.xlsx"
# data_path = "/home/adrian/Documents/Promotion/p10_heart/resources/data"
# output_file = "/home/adrian/Documents/Promotion/p10_heart/config/units.tsv"


# Read excel and create header
df = pd.read_excel(excel_file, engine="openpyxl")


df = df.dropna(how="all")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
df.columns = [
    "sample",
    "genotyp",
    "behandlung",
    "op",
    "number",
    "geburtsdatum",
    "stamm",
    "seziertag",
]
df = df.dropna(subset=["sample"])
df = df[df["behandlung"].notna()]
df["number"] = df["number"].str.lstrip("#")
df["op"] = df["op"].replace("sham", "Sham")
df = df.reset_index(drop=True)
df["unit"] = 1

# Assign fastqs to sampes
files = os.listdir(data_path)
file_dict = {}
for file in files:
    probe_number = file.split("_")[0]
    file_dict[probe_number] = file


df["fq1"] = "resources/data/" + df["number"].map(file_dict)
print(df)

# Anwenden der Funktion auf den DataFrame
# df['fq1'] = df.apply(create_path, axis=1)
df["fq2"] = "NA"
df["fragment_len_mean"] = "300"
df["fragment_len_sd"] = "100"

df = df[["sample", "unit", "fragment_len_mean", "fragment_len_sd", "fq1"]]

df.to_csv(output_file, sep="\t", index=False)
