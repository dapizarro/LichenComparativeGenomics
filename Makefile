.PHONY: dryrun run clean

dryrun:
	snakemake -n --cores 8 --use-conda

run:
	snakemake --cores 8 --use-conda

clean:
	rm -rf results .snakemake
