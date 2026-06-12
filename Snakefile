configfile: "config/config.yaml"

import os
from glob import glob

GENOMES_DIR = config["input"]["genomes_dir"]
GENOME_FILES = sorted(glob(f"{GENOMES_DIR}/*.*fa*") + glob(f"{GENOMES_DIR}/*.fna"))
SAMPLES = sorted({os.path.basename(f).split('.')[0] for f in GENOME_FILES})

rule all:
    input:
        "results/tables/genome_qc.tsv",
        "results/tables/ecology_genomics_merged.tsv",
        "results/tables/comparative_master_table.tsv",
        "results/figures/genome_qc_overview.pdf"

rule genome_qc:
    input:
        genomes=GENOME_FILES
    output:
        "results/tables/genome_qc.tsv"
    shell:
        "python scripts/python/genome_qc.py --genomes-dir {GENOMES_DIR} --out {output}"

rule prepare_metadata:
    input:
        qc="results/tables/genome_qc.tsv"
    output:
        "results/tables/ecology_genomics_merged.tsv"
    params:
        metadata=config["input"]["metadata"]
    shell:
        "python scripts/python/merge_metadata.py --qc {input.qc} --metadata {params.metadata} --out {output}"

rule comparative_master_table:
    input:
        merged="results/tables/ecology_genomics_merged.tsv"
    output:
        "results/tables/comparative_master_table.tsv"
    shell:
        "python scripts/python/build_master_table.py --merged {input.merged} --out {output}"

rule genome_qc_figures:
    input:
        qc="results/tables/genome_qc.tsv"
    output:
        "results/figures/genome_qc_overview.pdf"
    shell:
        "python scripts/python/plot_genome_qc.py --qc {input.qc} --out {output}"

# Optional heavy rules. Run explicitly, e.g.:
# snakemake results/busco/{sample}/short_summary.txt --cores 8 --use-conda
rule busco:
    input:
        genome=lambda wildcards: glob(f"{GENOMES_DIR}/{wildcards.sample}.*fa*")[0]
    output:
        directory("results/busco/{sample}")
    threads: config["params"]["threads"]
    params:
        lineage=config["params"]["busco_lineage"]
    shell:
        "busco -i {input.genome} -m genome -l {params.lineage} -o {wildcards.sample} --out_path results/busco -c {threads}"

rule augustus_predict:
    input:
        genome=lambda wildcards: glob(f"{GENOMES_DIR}/{wildcards.sample}.*fa*")[0]
    output:
        gff="results/annotation/{sample}.augustus.gff",
        proteins="results/proteomes/{sample}.faa"
    params:
        species=config["params"]["augustus_species"]
    shell:
        "bash scripts/bash/run_augustus_extract_proteins.sh {input.genome} {wildcards.sample} {output.gff} {output.proteins} {params.species}"

rule mat_detect:
    input:
        genome=lambda wildcards: glob(f"{GENOMES_DIR}/{wildcards.sample}.*fa*")[0]
    output:
        "results/mat/{sample}.mat_summary.tsv"
    shell:
        "python scripts/python/detect_mat_locus.py --genome {input.genome} --sample {wildcards.sample} --out {output}"

rule bgc_placeholder:
    input:
        proteins="results/proteomes/{sample}.faa"
    output:
        "results/bgc/{sample}.bgc_summary.tsv"
    shell:
        "python scripts/python/summarise_bgc_placeholder.py --proteins {input.proteins} --sample {wildcards.sample} --out {output}"
