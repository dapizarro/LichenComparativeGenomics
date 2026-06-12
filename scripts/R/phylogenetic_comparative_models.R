#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(ape)
  library(caper)
  library(phytools)
  library(tidyverse)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  stop("Usage: phylogenetic_comparative_models.R <treefile> <traits.tsv> <outdir>")
}

treefile <- args[1]
traits_file <- args[2]
outdir <- args[3]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

tree <- read.tree(treefile)
traits <- read_tsv(traits_file, show_col_types = FALSE)
if (!"sample_id" %in% colnames(traits)) stop("traits table requires sample_id")

traits <- traits %>% filter(sample_id %in% tree$tip.label)
row.names(traits) <- traits$sample_id
tree <- drop.tip(tree, setdiff(tree$tip.label, traits$sample_id))

numeric_traits <- traits %>% select(where(is.numeric)) %>% colnames()

signal_results <- list()
for (tr in numeric_traits) {
  x <- traits[[tr]]
  names(x) <- traits$sample_id
  x <- x[tree$tip.label]
  if (sum(!is.na(x)) > 5) {
    lambda <- tryCatch(phylosig(tree, x, method="lambda", test=TRUE), error=function(e) NULL)
    if (!is.null(lambda)) {
      signal_results[[tr]] <- tibble(trait=tr, lambda=lambda$lambda, logL=lambda$logL, P=lambda$P)
    }
  }
}
if (length(signal_results) > 0) {
  bind_rows(signal_results) %>% write_tsv(file.path(outdir, "phylogenetic_signal.tsv"))
}

# Example PGLS: genome_size_bp ~ gc_percent, if available
if (all(c("genome_size_bp", "gc_percent") %in% colnames(traits))) {
  comp <- comparative.data(tree, traits, names.col="sample_id", vcv=TRUE, warn.dropped=TRUE)
  fit <- tryCatch(pgls(genome_size_bp ~ gc_percent, data=comp, lambda="ML"), error=function(e) NULL)
  if (!is.null(fit)) {
    sink(file.path(outdir, "pgls_genome_size_gc.txt"))
    print(summary(fit))
    sink()
  }
}
