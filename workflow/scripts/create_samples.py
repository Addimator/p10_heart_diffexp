import pandas as pd
import numpy as np
import openpyxl


excel_file = snakemake.input["desc"]
output_file = snakemake.output[0]

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


df["t3_vs_ctr_in_gs_mi"] = df.apply(
    lambda row: (
        "+"
        if row["behandlung"] == "T3" and row["genotyp"] == "GS" and row["op"] == "MI"
        else (
            "-"
            if row["behandlung"] == "Ctr"
            and row["genotyp"] == "GS"
            and row["op"] == "MI"
            else ""
        )
    ),
    axis=1,
)
df["t3_vs_ctr_in_ko_mi"] = df.apply(
    lambda row: (
        "+"
        if row["behandlung"] == "T3" and row["genotyp"] == "KO" and row["op"] == "MI"
        else (
            "-"
            if row["behandlung"] == "Ctr"
            and row["genotyp"] == "KO"
            and row["op"] == "MI"
            else ""
        )
    ),
    axis=1,
)
df["t3_vs_ctr_in_wt_mi"] = df.apply(
    lambda row: (
        "+"
        if row["behandlung"] == "T3" and row["genotyp"] == "WT" and row["op"] == "MI"
        else (
            "-"
            if row["behandlung"] == "Ctr"
            and row["genotyp"] == "WT"
            and row["op"] == "MI"
            else ""
        )
    ),
    axis=1,
)
df["t3_vs_ctr_in_gs_sham"] = df.apply(
    lambda row: (
        "+"
        if row["behandlung"] == "T3" and row["genotyp"] == "GS" and row["op"] == "Sham"
        else (
            "-"
            if row["behandlung"] == "Ctr"
            and row["genotyp"] == "GS"
            and row["op"] == "Sham"
            else ""
        )
    ),
    axis=1,
)
df["t3_vs_ctr_in_ko_sham"] = df.apply(
    lambda row: (
        "+"
        if row["behandlung"] == "T3" and row["genotyp"] == "KO" and row["op"] == "Sham"
        else (
            "-"
            if row["behandlung"] == "Ctr"
            and row["genotyp"] == "KO"
            and row["op"] == "Sham"
            else ""
        )
    ),
    axis=1,
)
df["t3_vs_ctr_in_wt_sham"] = df.apply(
    lambda row: (
        "+"
        if row["behandlung"] == "T3" and row["genotyp"] == "WT" and row["op"] == "Sham"
        else (
            "-"
            if row["behandlung"] == "Ctr"
            and row["genotyp"] == "WT"
            and row["op"] == "Sham"
            else ""
        )
    ),
    axis=1,
)


df.to_csv(output_file, sep="\t", index=False)
