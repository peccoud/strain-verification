#!/bin/bash
# Runs all stages of cnv.kit for a single sample

sample_name=$1
bam_file=../../../../Processed_bams/${sample_name}.rgadded.mkdup.bam
ref_folder=../../../../Reference_files
ref_fasta=${ref_folder}/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa

mkdir -p Intermediary_files/${sample_name}
mkdir -p Results/${sample_name}
cd Intermediary_files/${sample_name}

# Binning
cnvkit.py autobin \
 $bam_file \
 --annotate ${ref_folder}/genes/Saccharomyces_cerevisiae.R64-1-1.92.genes.bed \
 -m wgs \
 -g ../../Resources/accessible_regions_R64-1-1.bed

target_file=${sample_name}.rgadded.mkdup.target.bed
antitarget_file=${sample_name}.rgadded.mkdup.antitarget.bed

# Coverages
cnvkit.py coverage \
 ${bam_file} \
 ${target_file} \
 -o ${sample_name}.targetcoverage.cnn

cnvkit.py coverage \
 ${bam_file} \
 ${antitarget_file} \
 -o ${sample_name}.antitargetcoverage.cnn

# Flat reference
cnvkit.py reference \
 --haploid-x-reference \
 -o FlatReference.cnn \
 --no-edge \
 -f ${ref_fasta} \
 -t ${target_file} \
 -a ${antitarget_file}

# Fix Coverages
cnvkit.py fix \
 --no-edge \
 -o ${sample_name}.cnr \
 ${sample_name}.targetcoverage.cnn ${sample_name}.antitargetcoverage.cnn FlatReference.cnn

# Segment
cnvkit.py segment ${sample_name}.cnr -t 0.000005 -o ${sample_name}.cns

# Call
cnvkit.py call ${sample_name}.cns -y -m threshold -t=-1.0000000,0.5849625,1.3219281,1.8073549,2.1699250 --purity 1 -o ${sample_name}.call.cns

# Pics
cnvkit.py scatter ${sample_name}.cnr -s ${sample_name}.cns -o ${sample_name}-scatter.pdf
cnvkit.py diagram ${sample_name}.cnr -s ${sample_name}.cns -o ${sample_name}-diagram.pdf


cp ${sample_name}.call.cns ../../Results/${sample_name}
cp *pdf ../../Results/${sample_name}
