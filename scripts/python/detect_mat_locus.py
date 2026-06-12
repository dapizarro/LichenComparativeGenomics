#!/usr/bin/env python3
"""Lightweight MAT locus screening placeholder.

This script searches for diagnostic strings in FASTA headers/sequences when full BLAST databases are not configured.
For production use, replace with tBLASTn against MAT1-1 alpha, MAT1-2 HMG, APN2 and SLA2 references.
"""
import argparse
from Bio import SeqIO

p = argparse.ArgumentParser()
p.add_argument("--genome", required=True)
p.add_argument("--sample", required=True)
p.add_argument("--out", required=True)
args = p.parse_args()

text = ""
for rec in SeqIO.parse(args.genome, "fasta"):
    text += rec.id.upper() + "\n"

has_11 = any(x in text for x in ["MAT1-1", "MAT1_1", "ALPHA"])
has_12 = any(x in text for x in ["MAT1-2", "MAT1_2", "HMG"])
if has_11 and has_12:
    call = "candidate_homothallic_or_mixed_metagenome"
elif has_11:
    call = "MAT1-1"
elif has_12:
    call = "MAT1-2"
else:
    call = "not_detected_requires_tblastn"

with open(args.out, "w") as out:
    out.write("sample_id\tmat_call\thas_MAT1_1\thas_MAT1_2\tnote\n")
    out.write(f"{args.sample}\t{call}\t{int(has_11)}\t{int(has_12)}\tUse production BLAST/HMM workflow for final analyses.\n")
