#!/bin/bash
GENOMEDIR="../Reference_files/genome"
REF_FASTA="${GENOMEDIR}/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa"
chrfastadir="${GENOMEDIR}/R64_chromosomes"
in_bam=$1
bam_filename=$(basename $in_bam)
sample_name=${bam_filename/.bam/}
bin_size=20

# CNVnator needs chromosome level fasta files. Create them if they don't exist
if [ ! -d "$chrfastadir" ];
then
  workdir=$(pwd)
  mkdir -p $chrfastadir
  cd $chrfastadir
  faidx -x $REF_FASTA
  cd $workdir
fi


# Initialize sample
cnvnator -root ${sample_name}.root -tree $in_bam

# Generate histogram
cnvnator -genome name R64.1.1 -root ${sample_name}.root -his $bin_size -d $chrfastadir

# Calculate statistics
cnvnator -root ${sample_name}.root -stat $bin_size

# RD signal partitioning
cnvnator -root ${sample_name}.root -partition $bin_size

# Run CNV calling
cnvnator -root ${sample_name}.root -call $bin_size \
    > CNVnator/Results/CNVnator_${sample_name}_calls.tsv

# Add header
cat CNVnator/header CNVnator/Results/CNVnator_${sample_name}_calls.tsv \
    > CNVnator/Results/CNVnator_${sample_name}_calls_with_header.tsv

# Clean up
rm ${sample_name}.root
