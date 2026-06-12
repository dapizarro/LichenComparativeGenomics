#!/usr/bin/env python3
import argparse
import pandas as pd
import matplotlib.pyplot as plt

p = argparse.ArgumentParser()
p.add_argument("--qc", required=True)
p.add_argument("--out", required=True)
args = p.parse_args()

df = pd.read_csv(args.qc, sep="\t")
if df.empty:
    raise SystemExit("No genomes found. Add FASTA files to data/raw/genomes/.")

plt.figure(figsize=(max(8, len(df) * 0.35), 4))
plt.bar(df["sample_id"], df["genome_size_bp"] / 1e6)
plt.ylabel("Genome size (Mb)")
plt.xlabel("Sample")
plt.xticks(rotation=90, fontsize=7)
plt.tight_layout()
plt.savefig(args.out)
