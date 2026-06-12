#!/usr/bin/env python3
import argparse
from Bio import SeqIO

p = argparse.ArgumentParser()
p.add_argument("--proteins", required=True)
p.add_argument("--sample", required=True)
p.add_argument("--out", required=True)
args = p.parse_args()

num_proteins = sum(1 for _ in SeqIO.parse(args.proteins, "fasta"))
with open(args.out, "w") as out:
    out.write("sample_id\tnum_proteins\tnum_bgcs\tnum_nr_pks\tnote\n")
    out.write(f"{args.sample}\t{num_proteins}\tNA\tNA\tRun antiSMASH/fungiSMASH for final BGC calls.\n")
