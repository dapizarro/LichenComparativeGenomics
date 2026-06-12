#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
from Bio import SeqIO


def n50(lengths):
    if not lengths:
        return 0
    lengths = sorted(lengths, reverse=True)
    half = sum(lengths) / 2
    acc = 0
    for x in lengths:
        acc += x
        if acc >= half:
            return x
    return 0


def gc(seq):
    s = str(seq).upper()
    valid = sum(1 for b in s if b in "ACGT")
    if valid == 0:
        return 0
    return 100 * (s.count("G") + s.count("C")) / valid


def main():
    p = argparse.ArgumentParser(description="Compute assembly QC metrics from genome FASTA files.")
    p.add_argument("--genomes-dir", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    rows = []
    files = sorted(Path(args.genomes_dir).glob("*.fa*")) + sorted(Path(args.genomes_dir).glob("*.fna"))
    seen = set()
    for fasta in files:
        if fasta in seen:
            continue
        seen.add(fasta)
        sample = fasta.name.split(".")[0]
        lengths, gcs, n_count = [], [], 0
        for rec in SeqIO.parse(str(fasta), "fasta"):
            seq = str(rec.seq).upper()
            lengths.append(len(seq))
            gcs.append(gc(seq))
            n_count += seq.count("N")
        total = sum(lengths)
        rows.append({
            "sample_id": sample,
            "fasta": str(fasta),
            "num_contigs": len(lengths),
            "genome_size_bp": total,
            "n50": n50(lengths),
            "largest_contig_bp": max(lengths) if lengths else 0,
            "gc_percent": round(sum(g * l for g, l in zip(gcs, lengths)) / total, 4) if total else 0,
            "n_bases": n_count,
            "n_percent": round(100 * n_count / total, 4) if total else 0,
        })
    pd.DataFrame(rows).to_csv(args.out, sep="\t", index=False)

if __name__ == "__main__":
    main()
