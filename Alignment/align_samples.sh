#!/bin/bash

trimmed_fastq_dir="../Trimming/Results/Trimmed_fastq_files"
reference_fasta="../Reference_files/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa"

for f in $trimmed_fastq_dir/*val_1.fq.gz
do
    filename=$(basename $f)
    reads2_sub1=${f/val_1/val_2}
    reads2=${reads2_sub1/R1/R2}
    bamname="Results/Alignments/${filename%%_*}.bam"
    bwa mem -t10 $reference_fasta $f $reads2 | samtools sort -@ 10 | samtools view -bS > $bamname
    samtools index $bamname
done

