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
## Scientific Motivation

This repository was developed from comparative genomics workflows originally established during research on the evolution of reproductive systems and secondary metabolism in lichen-forming fungi.

The framework implemented here generalizes analytical approaches developed in the following studies:

### Evolution of reproductive systems
> Pizarro D., Dal Grande F., Leavitt S.D., Dyer P.S., Schmitt I., Crespo A., Lumbsch H.T. & Divakar P.K. (2019) **Whole-genome sequence data uncover widespread heterothallism in the largest group of lichen-forming fungi.** *Genome Biology and Evolution* 11(3): 721–730.

### Evolution of secondary metabolism
> Pizarro D., Divakar P.K., Grewe F., Crespo A., Dal Grande F. & Lumbsch H.T. (2020) **Genome-wide analysis of biosynthetic gene clusters reveals correlated gene loss with absence of usnic acid in lichen-forming fungi.** *Genome Biology and Evolution* 12(10): 1858–1868.

The current repository extends these concepts into a unified and reproducible comparative genomics framework applicable to lichen-forming fungi and other non-model eukaryotic systems.

---

## Quick start

```bash
git clone https://github.com/dapizarro/LichenComparativeGenomics.git
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

## Project Status

### Active Development

This repository is an actively maintained research resource. The workflow consolidates methodologies developed across published studies and ongoing comparative genomics projects. Additional modules, analytical approaches, and visualization tools will continue to be incorporated as development progresses. Although individual components have been applied in peer-reviewed research, the complete integrated workflow described here has not yet been formally published as a standalone software paper.

---

## Citation

If you use this framework, please cite the associated papers and software tools used in the workflow.

---

## License

MIT License.
