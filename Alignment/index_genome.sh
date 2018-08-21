#!/bin/bash

reference_fasta="../Reference_files/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa"
bwa index $reference_fasta
samtools faidx $reference_fasta
