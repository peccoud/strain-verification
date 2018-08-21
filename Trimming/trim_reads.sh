#!/bin/bash
fastq_dir="../Raw_data"
output_dir="Results/Trimmed_fastq_files"


for f in ${fastq_dir}/*R1_001.fastq.gz
do
    trim_galore -o $output_dir --fastqc --paired $f ${f/R1/R2}
done
