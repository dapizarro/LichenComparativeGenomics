#!/usr/bin/env python3
import argparse
import pandas as pd
from pathlib import Path

def safe_read(path):
    return pd.read_csv(path, sep="\t") if Path(path).exists() else None

def main():
    p = argparse.ArgumentParser(description="Build comparative master table from available module outputs.")
    p.add_argument("--merged", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    master = pd.read_csv(args.merged, sep="\t")
    optional = [
        "results/tables/busco_summary.tsv",
        "results/tables/bgc_summary.tsv",
        "results/tables/mat_locus_summary.tsv",
        "results/tables/orthogroup_counts.tsv",
    ]
    for path in optional:
        df = safe_read(path)
        if df is not None and "sample_id" in df.columns:
            master = master.merge(df, on="sample_id", how="left")
    master.to_csv(args.out, sep="\t", index=False)

if __name__ == "__main__":
    main()
