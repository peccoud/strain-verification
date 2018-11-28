#!/bin/bash
sample_name=$1
bam_file=../../../Processed_bams/${sample_name}.rgadded.mkdup.bam
ref_folder=../../../Reference_files

mkdir -p Intermediary_files/${sample_name}
cd Intermediary_files/${sample_name}

# Binning
cnvkit.py autobin \
 $bam_file \
 --annotate ${ref_folder}/genes/Saccharomyces_cerevisiae.R64-1-1.92.genes.bed \
 -m wgs \
 -g ../Resources/accessible_regions_R64-1-1.bed

# Coverages
cnvkit.py coverage \
 ${bam_file} \
 ${bam_file.target.bed \
 -o GRL1691.mkdup.rg.targetcoverage.cnn
cnvkit.py coverage \
 /data/Nanopore/Yeast/Illumina/GRL169X_alignments_mkdup/GRL1691.mkdup.rg.bam \
 GRL1691.mkdup.rg.antitarget.bed \
 -o GRL1691.mkdup.rg.antitargetcoverage.cnn

# Flat reference
cnvkit.py reference \
 --haploid-x-reference \
 -o FlatReference.cnn \
 --no-edge \
 -f /projects/organisms/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa \
 -t GRL1691.mkdup.rg.target.bed \
 -a GRL1691.mkdup.rg.antitarget.bed

# Fix Coverages
cnvkit.py fix \
 --no-edge \
 -o GRL1691.mkdup.rg.cnr \
 GRL1691.mkdup.rg.targetcoverage.cnn GRL1691.mkdup.rg.antitargetcoverage.cnn FlatReference.cnn

# Segment
cnvkit.py segment GRL1691.mkdup.rg.cnr -t 0.000006 -o GRL1691.mkdup.rg.cns

# Call
cnvkit.py call GRL1691.mkdup.rg.cns -y -m threshold -t=-1.0000000,0.5849625,1.3219281,1.8073549,2.1699250 --purity 1 -o GRL1691.mkdup.rg.call.cns

# Pics
cnvkit.py scatter GRL1691.mkdup.rg.cnr -s GRL1691.mkdup.rg.cns -o GRL1691-scatter.pdf
cnvkit.py diagram GRL1691.mkdup.rg.cnr -s GRL1691.mkdup.rg.cns -o GRL1691-diagram.pdf
