import pandas as pd
import os

# excel_file = snakemake.input[0]
# output_file = snakemake.output[0]
excel_file = "/home/adrian/Documents/Promotion/p10_heart/resources/sample_desc.xlsx"
data_path = "/home/adrian/Documents/Promotion/p10_heart/resources/data"
output_file = "/home/adrian/Documents/Promotion/p10_heart/config/utils.tsv"

df = pd.read_excel(excel_file, engine="openpyxl")


df = df.dropna(how="all")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
df.columns = [
    "Tier-ID",
    "Genotyp",
    "Behandlung",
    "OP",
    "RNA Lysate",
]
df = df.dropna(subset=["Tier-ID"])
df = df[df["Behandlung"].notna()]
df_reset = df.reset_index(drop=True)
print(df.to_string())


df["unit"] = 1

# Assign fastqs to sampes
files = os.listdir(data_path)
file_dict = {}
for file in files:
    probe_number = int(file.split("_S")[1].split("_")[0])
    file_dict[probe_number] = file
df["fq1"] = "../data/fastq_machlah_concatenated/" + df["Probe Nr."].map(file_dict)


# Anwenden der Funktion auf den DataFrame
# df['fq1'] = df.apply(create_path, axis=1)
df["fq2"] = "NA"
df["fragment_len_mean"] = "300"
df["fragment_len_sd"] = "100"

samples_to_remove = [14, 23, 28]
df = df[~df["Probe Nr."].isin(samples_to_remove)]

df = df.rename(columns={"Probe Nr.": "sample"})
df.columns = (
    df.columns.str.replace(" ", "_")
    .str.lower()
    .str.replace("ä", "ae")
    .str.replace("ö", "oe")
    .str.replace("ü", "ue")
    .str.replace("ß", "ss")
)
df = df.replace(" ", "_", regex=True)
df = df.dropna(subset=["sample"])
df.reset_index(drop=True, inplace=True)


tsv_data = {
    "sample": df["sample"],
    "unit": df["unit"],
    "fragment_len_mean": df["fragment_len_mean"],
    "fragment_len_sd": df["fragment_len_sd"],
    "fq1": df["fq1"],
    "fq2": df["fq2"],
    "bam_single": "",
    "bam_paired": "",
}

# Konvertiere das Wörterbuch in ein DataFrame für die tsv-Datei
tsv_df = pd.DataFrame(tsv_data)

tsv_df.to_csv(output_file, sep="\t", index=False)
