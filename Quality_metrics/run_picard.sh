#!/bin/bash
in_bam=$1
bam_basename=$(basename $in_bam)
sample_name=${bam_basename/.bam/}
REF_FASTA="../Reference_files/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa"
PICARD="../bin/picard-2.9.jar"

# Set read groups
java -jar $PICARD AddOrReplaceReadGroups \
    I=$in_bam \
    O=../Processed_bams/${sample_name}.rgadded.bam \
    RGID=${sample_name} \
    RGLB=${sample_name} \
    RGPL=illumina \
    RGPU=unit1 \
    RGSM=${sample_name}

samtools index ../Processed_bams/${sample_name}.rgadded.bam

# Mark duplicates
java -jar $PICARD MarkDuplicates \
    I=../Processed_bams/${sample_name}.rgadded.bam \
    O=../Processed_bams/${sample_name}.rgadded.mkdup.bam \
    M=Results/${sample_name}_duplicate_metrics.txt

samtools index ../Processed_bams/${sample_name}.rgadded.mkdup.bam
processed_bam="../Processed_bams/${sample_name}.rgadded.mkdup.bam"

# Calculate WGS metrics
java -jar $PICARD CollectWgsMetrics \
    I=$processed_bam \
    O=Results/${sample_name}_collect_wgs_metrics.txt \
    R=$REF_FASTA

# Collect yield metrics
java -jar $PICARD CollectQualityYieldMetrics \
    I=$processed_bam \
    O=Results/${sample_bam}_collect_quality_yield_metrics.txt
