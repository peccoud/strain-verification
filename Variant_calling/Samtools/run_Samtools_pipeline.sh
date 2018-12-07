#!/bin/bash
orig_bam1="../Processed_bams/GRL1691.rgadded.mkdup.bam"
orig_bam2="../Processed_bams/GRL1693.rgadded.mkdup.bam"
ref_fasta="../Reference_files/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa"

results="Samtools/Results/joint.vcf.gz"
mkdir -p Samtools/Results

# Run variant calling
bcftools mpileup -Ou -f $ref_fasta $orig_bam1 $orig_bam2 | bcftools call --ploidy=1 -vmO z -o $results 2>&1 | tee ${variants_vcf/.vcf/.log}

# Post-process variants
gunzip -f Samtools/Results/joint.vcf.gz
python Utility_scripts/keep_discordant_sites.py Samtools/Results/joint.vcf
java -Xmx4g -jar ../bin/snpEFF/snpEff.jar R64-1-1.86 Samtools/Results/joint.discordant.vcf > Samtools/Results/joint.discordant.annotated.vcf
python Utility_scripts/clean_GATK_annotated_vcf.py Samtools/Results/joint.discordant.annotated.vcf


