#!/bin/bash
orig_bam1="../Processed_bams/GRL1691.rgadded.mkdup.bam"
orig_bam2="Processed_bams/GRL1693.rgadded.mkdup.bam"
ref_fasta="../Reference_files/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa"
gatk_jar="../bin/GATK-4.jar"
gatk_jar_38="../bin/GATK-3.8.jar"

bam1_name=$(basename $orig_bam1)
bam2_name=$(basename $orig_bam2)

java -jar $gatk_jar HaplotypeCaller\
     -R $ref_fasta \
     -I $orig_bam1 \
     -ERC GVCF \
     -O GATK/Results/${bam1_name}.raw.snps.indels.g.vcf \
     -G StandardAnnotation \
     -G AS_StandardAnnotation \
     --sample_ploidy 1

java -jar $gatk_jar HaplotypeCaller\
     -R $ref_fasta \
     -I $orig_bam2 \
     -ERC GVCF \
     -O GATK/Results/${bam2_name}.raw.snps.indels.g.vcf \
     -G StandardAnnotation \
     -G AS_StandardAnnotation \
     --sample_ploidy 1 

java -jar $gatk_jar_38 \
   -T CombineGVCFs \
   -R $ref_fasta \
   --variant GATK/Results/${bam1_name}.raw.snps.indels.g.vcf \
   --variant GATK/Results/${bam2_name}.raw.snps.indels.g.vcf \
   -o GATK/Results/joint.g.vcf \
   -G Standard \
   -G AS_StandardAnnotation

java -Xmx4g -jar $gatk_jar GenotypeGVCFs \
   -R $ref_fasta \
   -V GATK/Results/joint.g.vcf \
   -O GATK/Results/joint.vcf.gz \
   -G StandardAnnotation \
   -G AS_StandardAnnotation

gunzip -f GATK/Results/joint.vcf.gz
python Utility_scripts/keep_discordant_sites.py GATK/Results/joint.vcf
java -Xmx4g -jar ../bin/snpEFF/snpEff.jar R64-1-1.86 GATK/Results/joint.discordant.vcf > GATK/Results/joint.discordant.annotated.vcf
python Utility_scripts/clean_GATK_annotated_vcf.py GATK/Results/joint.discordant.annotated.vcf

