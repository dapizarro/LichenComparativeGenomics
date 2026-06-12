#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd

def main():
    p = argparse.ArgumentParser(description="Merge genome QC with ecological/chemical metadata.")
    p.add_argument("--qc", required=True)
    p.add_argument("--metadata", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    qc = pd.read_csv(args.qc, sep="\t")
    if Path(args.metadata).exists():
        meta = pd.read_csv(args.metadata, sep="\t")
        if "sample_id" not in meta.columns:
            raise SystemExit("Metadata must contain a 'sample_id' column.")
        out = qc.merge(meta, on="sample_id", how="left")
    else:
        out = qc.copy()
        for col in ["species", "family", "chemotype", "usnic_acid", "reproductive_mode", "substrate", "climate_zone"]:
            out[col] = "NA"
    out.to_csv(args.out, sep="\t", index=False)

if __name__ == "__main__":
    main()
