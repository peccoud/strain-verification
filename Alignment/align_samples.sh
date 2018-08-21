#!/bin/bash

trimmed_fastq_dir="../Trimming/Results/Trimmed_fastq_files"

for f in $trimmed_fastq_dir/*val_1.fq.gz
do
    bwa mem -t10 ../
