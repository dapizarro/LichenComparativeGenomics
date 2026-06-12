# LichenComparativeGenomics

**End-to-end comparative and evolutionary genomics workflow for lichen-forming fungi starting from genome FASTA assemblies.**

This repository provides a reproducible framework to analyse lichen fungal genomes from raw genome assemblies (`*.fasta`, `*.fa`, `*.fna`) and produce comparative genomic tables, phylogenomic trees, biosynthetic gene cluster summaries, mating-type locus classifications, ecological trait integrations, and phylogenetic comparative models.

The project is designed around two major biological axes:

1. **Genome evolution of secondary metabolism**  
   Detection and comparison of biosynthetic gene clusters (BGCs), including the presence/absence of candidate clusters such as the putative usnic acid BGC.

2. **Evolution of reproductive systems**  
   Detection and classification of the MAT locus, including MAT1-1, MAT1-2, heterothallic/homothallic patterns, and synteny with canonical flanking genes such as `APN2` and `SLA2`.

Both axes are integrated into a broader comparative genomics framework including BUSCO-based genome completeness, orthology, phylogenomics, gene-family evolution, synteny, ecological metadata integration, and phylogenetic comparative methods.

---

## Quick start

```bash
git clone https://github.com/YOUR_USER/LichenComparativeGenomics.git
cd LichenComparativeGenomics

mamba env create -f envs/lichencomparativegenomics.yml
mamba activate lichencomparativegenomics

# Put your genome FASTA files here:
# data/raw/genomes/*.fasta

snakemake --cores 8 --use-conda
```

For a dry run:

```bash
snakemake -n --cores 8 --use-conda
```

---

## Input data

### Required

Place genome assemblies here:

```text
data/raw/genomes/
├── Evernia_prunastri.fasta
├── Usnea_florida.fasta
├── Parmelia_sulcata.fasta
└── ...
```

Each filename becomes the `sample_id` unless a metadata table is provided.

### Optional metadata

```text
data/metadata/samples.tsv
```

Required column:

```text
sample_id
```

Recommended columns:

```text
species	genus	family	order	chemotype	usnic_acid	atranorin	reproductive_mode	substrate	climate_zone	latitude	longitude
```

Example:

```tsv
sample_id	species	family	chemotype	usnic_acid	reproductive_mode	substrate	climate_zone
Evernia_prunastri	Evernia prunastri	Parmeliaceae	UA+	1	sexual	bark	temperate
Parmelia_sulcata	Parmelia sulcata	Parmeliaceae	UA-	0	sexual	bark	temperate
```

---

## Main outputs

```text
results/tables/
├── genome_qc.tsv
├── busco_summary.tsv
├── bgc_summary.tsv
├── bgc_presence_absence.tsv
├── mat_locus_summary.tsv
├── orthogroup_counts.tsv
├── ecology_genomics_merged.tsv
└── comparative_master_table.tsv

results/phylogenomics/
├── supermatrix.faa
├── partitions.txt
└── species_tree.treefile

results/evolutionary_models/
├── phylogenetic_signal.tsv
├── pgls_results.tsv
└── ancestral_state_results.tsv

results/figures/
├── genome_qc_overview.pdf
├── bgc_heatmap.pdf
├── mat_distribution_tree.pdf
├── comparative_pca.pdf
└── pgls_effects.pdf
```

---

## Workflow overview

```text
Genome FASTA assemblies
        │
        ├── Genome QC
        │     └── length, GC, N50, number of contigs
        │
        ├── BUSCO completeness
        │     └── completeness tables + single-copy orthologs
        │
        ├── Gene prediction / annotation
        │     └── proteins, CDS, GFF
        │
        ├── BGC prediction
        │     └── antiSMASH summaries + BGC matrices
        │
        ├── MAT locus detection
        │     └── MAT1-1 / MAT1-2 / candidate homothallism
        │
        ├── Orthology inference
        │     └── orthogroups and gene-family counts
        │
        ├── Phylogenomics
        │     └── BUSCO/ortholog alignments + IQ-TREE species tree
        │
        └── Comparative models
              └── ecology integration, PGLS, phylogenetic signal, ASR
```

---

## Recommended repository fields for GitHub

**Repository name**

```text
LichenComparativeGenomics
```

**Description**

```text
Reproducible workflow for comparative genomics, BGC evolution, mating-type locus evolution and phylogenomic analyses of lichen-forming fungi.
```

**Topics**

```text
lichen-genomics comparative-genomics phylogenomics fungal-genomics bgc antismash busco orthofinder mating-type phylogenetic-comparative-methods
```

---

## Citation

If you use this framework, please cite the associated papers and software tools used in the workflow.

---

## License

MIT License.
