#!/bin/bash
# Command fastqc must be in PATH
mkdir -p Results/FastQC_before_trimming
for f in ../Raw_data/*fastq.gz
do
    fastqc $f
done

# Move results to correct folder
mv ../Raw_data/*html Results/FastQC_before_trimming
mv ../Raw_data/*zip Results/FastQC_before_trimming
