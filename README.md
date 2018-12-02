# Analysis of yeast WGS samples

This repository contains all code used for analyzing yeast samples of group Peccoud of Colorado State University. All scripts are tested with software dependencies listed in section `Software dependencies`. The raw data and reference files are delivered separately due to their large size. Scripts in this repository allow full reproduction of all delivered and discussed results. 

Directory structure reflects the types of performed analyses. Scripts for performing each step are placed under analysis-specific directories. Each step has its own `Results`-directory. Some of the steps are independent, while some depend on each other. Dependencies are listed in this `README` document under each section.

# Software dependencies
* FastQC - https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
* Trimgalore! - https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/
* cutadapt - https://cutadapt.readthedocs.io/en/stable/
* bwa - http://bio-bwa.sourceforge.net
* Picard - https://broadinstitute.github.io/picard/
* CNVnator - https://github.com/abyzovlab/CNVnator
* Breakdancer - http://breakdancer.sourceforge.net/
* Samtools - http://www.htslib.org/doc/samtools.html
* BCFtools - https://samtools.github.io/bcftools//bcftools.html
* Genome Analysis Toolkit (GATK) - https://software.broadinstitute.org/gatk/
* snpEFF - http://snpeff.sourceforge.net/
* SOAPdenovo2 - http://soap.genomics.org.cn/soapdenovo.html
* SPAdes - http://cab.spbu.ru/software/spades/
* QUAST - http://bioinf.spbau.ru/quast

# Analysis steps

Note that instructions for each step assume that working directory in the beginning of the step is the repository's root directory, i.e. the directory where this `README` file is located.

## FastQC (v0.11.7) before trimming
FastQC calculates and visualizes sequencing quality metrics, e.g. GC content distribution and sequencing adapter contamination. FastQC metrics can be used to identify issues in sequencing. Comparing metrics befor and after trimming step helps to determine if trimming was successful.
 
Run FastQC by invoking script:
```
cd FastQC
bash run_fastqc_before_trimming.sh
```
Results of FastQC run will be placed in `FastQC/Results/FastQC_before_trimming`. See example reports on FastQC website for interpretation.

## Trimming reads
Adaptive trimming removes possible adapter contamination and low-quality tales of reads. Trimming produces new set of fastq files to be used in downstream analyses. Trimming is performed with Trimgalore!. Trimgalore! also runs FastQC on trimmed files and stores FastQC results along with trimmed fastq files.

Run trimming by invoking script:
```
cd Trimming
bash trim_reads.sh
```

Trimmed set of fastq files will be stored in `Trimming/Results/Trimmed_fastq_files`. Downstream steps depending on fastq files will look for them in this directory.

## Aligning reads

Reads are aligned to reference sequence using bwa.

Build BWA index from reference fasta by running script:
```
cd Alignment
bash index_genome.sh
```
Index is stored along with the reference fasta file in `Reference_files/genome`

Alignment is performed using BWA (v. 0.7.15) with default parameters. Invoke alignment by running script:
```
cd Aligment
bash align_samples.sh
```


Aligned bam files and their indices are stored in `Alignment/Results/Alignments`. Downstream steps depending on bam files will look for them in this directory.

## Quality metrics
Alignment of reads produces information for further inspection of sample and sequencing quality. In this step, Picard is used to assess the quality from bam giles. Picard functions will produce multiple result files corresponding to different types of metrics. See Picard documentation for detailed descriptions on each metric.

In this step, we we also mark duplicate reads with Picard and produce duplicate marked bam files. These bam files will be used for downstream analyses.

Invoke quality assessment by running script:
```
cd Quality_metrics
bash process_samples.sh
```

Picard result files will be stored to `Quality_metrics/Results`. Processed bam files for downstream analysis will be stored to `Processed_bams`

## CNV calling

### CNVnator (v0.3.3)
Invoke CNVnator analysis by running
```
cd CNV_calling
bash CNVnator/call_samples.sh
```

CNVnator is run with bin size of 20. Bin size variable is set in the beginning of script `CNVnator/run_CNVnator.sh`. Using larger bin sizes leads to missing deletions known to be in the sample and clearly visible by manual inspection.

Results will be stored to `CNV_calling/CNVnator/Results`


### Breakdancer v. 1.3.6
For running Breakdancer, you need to set paths and permissions for Breakdancer:
* Add Breakdancer *perl* directory, located in your breakdance installation root folder, to `PATH` environment variable.
* Set execution rights for perl script `bam2cfg.pl` in that directory: `chmod gu+x breakdancer/perl/bam2fcfg.pl`. Give the actual path to Breakdancer installation directory.

After setting up, invoke Breakdancer, including automatic configuration, by running:
```
cd CNV_calling
bash breakdancer/call_samples.sh
```
Results are stored in `CNV_calling/breakdancer/Results`.

Breakdancer calls all samples at the same time. Results of all samples are in the same table.

### CNVkit v0.9.3

Provided scripts assume that CNVkit is installed according to its [installation instructions](https://github.com/etal/cnvkit). After installation, invoke CNVkit pipeline using samples GRL1691 and GRL1693 by running:

```
cd CNV_calling
bash cnv.kit/run_cnvkit.sh
```

Intermediary files produced by CNVkit pipeline will be stored in directory `CNV_calling/cnv.kit/Intermediary_files`. Copy number variants called by the pipeline will be stored in directory `CNV_calling/cnv.kit/Results/<sample_name>`.

## Variant calling

Variant calling was run both with GATK pipeline and a pipeline consisting of Samtools and bcftools.

In both cases, variant calling was run jointly on both samples of interest, GRL1691 and GRL1693. Variant calling was run against yeast reference genome R64-1-1, corresponding to strain 288C. Called variants were filtered to contain only discordantly called variants between GRL1691 and GRL1693, annotated with snpEFF, and annotated vcf file was formatted further with a custom script. 

### GATK (v3.8 and v4.beta.5)

GATK pipeline consists of calling GATK HaplotypeCaller separately on each sample with `--sample-ploidy` set to 1, combining resulting GVCF files with GATK CombineGVCFs, and running GATK GenotypeVCFs on the combined GVC. GATK tools were run with GATK version, except for CombineGVCFs, which was run with GATK version 3.8, as there was no working version of it in GATK 4 at the time of setting up the analyses. 

The main difference in approach to variant calling between GATK HaplotypeCaller and Bcftools is that GATK HaplotypeCaller does local reassembly in the regions with genomic variation. This leads to better accuracy in case of e.g. indels that might affect alignment rate or quality. Documentation of GATK contains a more detailed explanation of the main steps taken by HaplotypeCaller: [https://software.broadinstitute.org/gatk/documentation/tooldocs/3.8-0/org_broadinstitute_gatk_tools_walkers_haplotypecaller_HaplotypeCaller.php].

Execute GATK pipeline by running
```
cd Variant_calling
bash GATK/run_GATK_pipeline.sh
```

Results will be stored in `GATK/Results`. Script keeps all intermediate files. Annotated and formatted discordant variants are in a tab-separated file `joint.discordant.annotated.formatted.tsv`.


### Bcftools (v.1.8) of SAMtools software suite

Execute Bcftools pipeline by running

```
cd Variant_calling
bash Samtools/run_Samtools_pipeline.sh
```
Results will be stored in `Samtools/Results`. As with GATK, intermediate files are kept, and annotated and formatted discordant variants are in a tab-separated file `joint.discordant.annotated.formatted.tsv`.

## De novo assemblies

De novo assemblies were performed with two tools, with SPAdes used for downstream analyses.

### SOAPdenovo (v. 2.04)

SOAPdenovo2 is a short read de novo assembler based on Hamiltonian de Bruijin graphs. SOAPdenovo2 builds contigs using overlapping reads, and joints contigs to form scaffolds based on read pairness and insert size information.

Setup SOAPdenovo assembler by adding the folder with its executables to `PATH` and setting execution rights to for file `SOAPdenovo-63mer`, located in the root folder of SOAPDenovo. In addition, SOAPdenovo requires creation of configuration files. Configuration files were created manually and are located in folder `SOAPdenovo/configs`.

Setup QUAST for calculating assembly quality metrics by adding the root folder of Quast to `PATH` and setting execution rights for file `quast.py` inside of it.

Execute SOAPdenovo assembly and calculate metrics with Quast by running:
```
cd Denovo_assembly
python SOAPdenovo/run_SOAPdenovo_assembly.py
```
Results, both assemblies and QUAST results, will be stored to `Denovo_assembly/SOAPdenovo/results`. Quast was run two times for each sample - once on scaffolds and once on contigs. Results for each sample are stored in folders `quast_results_scaffolds` and `quast_results_contigs`. Metrics are stored in a tabular format in files `report.tsv` and `transposed_report.tsv`. In addition, Quast creates a visual report as an html file, `report.html`, which can be viewed in a web browser.


### SPADes (v. 3.9.0)
SPAdes is another de novo assembler for short reads, based on Eulerian de Bruijin graphs. Outline of the complex algorithm is presented in SPAdes' publication.

Setup SPAdes assembler by adding directory `bin` in SPAdes directory to your `PATH`.

Execute SPAdes assembly and calculate metrics with Quast by running:
```
cd Denovo_assembly
python SPAdes/run_SPAdes_assembly.py
```

## Annotation by blasting
TBD.

## Assembly metrics (Quast)

Quast is run as part of assembly pipelines, so there is no need to run it separately. Various metrics reported by Quast are explained in [http://quast.bioinf.spbau.ru/manual.html#sec3](its manual).

## Subsampling series 
Subsampling series were performed to assess the effect of depth of sequencing on variant calling and assembly quality. Variant calling in subsamplling series was performed with Samtools and assemblies were made with SPAdes. In each round of subsampling, following steps were performed:

* Subsampling itself
* Variant calling with Samtools
* Variant annotation with snpEFF
* Assembly with SPAdes
* Assessment of the assembly with Quast

### Running subsampling analyses

Run subsampling:
```
cd Subsampling
bash run_subsampling.sh
```
Samples are subsampled using a default random seed value of X to make subsampling reproducible. Sampling procedure produces one sample for each of the following target number of read pairs: 10 000, 30 000, 60 000, 90 000, 120 000, 150 000, 180 000, 210 000, 240 000, 260 000, 300 000, 400 000, 500 000, 600 000, 700 000, 800 000, 900 000, 1 000 000, 1 200 000, 1 400 000, 1 600 000, 1 800 000, 2 000 000, 2 500 000, 3 000 000, 3 500 000.

After subsampling is complete, run SPAdes assemblies and assessment of their qualities. Note that both subsampling and performing tens of assemblies is time-consuming.

```
bash run_spades_assemblies.sh
bash run_quast_series.sh
```

### Result files

Results are summarized and visualized using an R Notebook. Render a pdf summary report by running

```
bash summarize_results.sh
```


## References
References
* FASTQC: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
* TRIMGALORE: https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/
* BWA: Li, H. (2013). Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM, 00(00), 1–3. http://doi.org/arXiv:1303.3997 [q-bio.GN]
* ENSEMBL: Zerbino, D. R., Achuthan, P., Akanni, W., Amode, M. R., Barrell, D., Bhai, J., … Flicek, P. (2018). Ensembl 2018. Nucleic Acids Research, 46(D1), D754–D761. http://doi.org/10.1093/nar/gkx1098
* PICARD: https://broadinstitute.github.io/picard/
* CNVKIT: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004873
* CNVnator: Abyzov, A., Urban, A. E., Snyder, M., & Gerstein, M. (2011). CNVnator: An approach to discover, genotype, and characterize typical and atypical CNVs from family and population genome sequencing. Genome Research, 21(6), 974–984. http://doi.org/10.1101/gr.114876.110
* BREAKDANCER: Chen, K., Wallis, J. W., Mclellan, M. D., Larson, D. E., Kalicki, J. M., Pohl, C. S., … Elaine, R. (2013). BreaDancer - An algorithm for high resolution mapping of genomic structure variation. Nature Methods, 6(9), 677–681. http://doi.org/10.1038/nmeth.1363.BreakDancer
* GATK: Van der Auwera, G. A., Carneiro, M. O., Hartl, C., Poplin, R., del Angel, G., Levy-Moonshine, A., … DePristo, M. A. (2013). From fastQ data to high-confidence variant calls: The genome analysis toolkit best practices pipeline. Current Protocols in Bioinformatics. http://doi.org/10.1002/0471250953.bi1110s43
* SAMTOOLS: Li, H. (2011). A statistical framework for SNP calling, mutation discovery, association mapping and population genetical parameter estimation from sequencing data. Bioinformatics, 27(21), 2987–2993. http://doi.org/10.1093/bioinformatics/btr509
* BCFTOOLS: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3198575/
* SNPEFF: Cingolani, P., Platts, A., Wang, L. L., Coon, M., Nguyen, T., Wang, L., … Ruden, D. M. (2012). A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff. Fly, 6(2), 80–92. http://doi.org/10.4161/fly.19695
* SPADES: Bankevich, A., Nurk, S., Antipov, D., Gurevich, A. A., Dvorkin, M., Kulikov, A. S., … Pevzner, P. A. (2012). SPAdes: A New Genome Assembly Algorithm and Its Applications to Single-Cell Sequencing. Journal of Computational Biology, 19(5), 455–477. http://doi.org/10.1089/cmb.2012.0021
* SOAPDENOVO2: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004873# 
* QUAST: Gurevich, A., Saveliev, V., Vyahhi, N., & Tesler, G. (2013). QUAST: Quality assessment tool for genome assemblies. Bioinformatics, 29(8), 1072–1075. http://doi.org/10.1093/bioinformatics/btt086 
* BLAST: Camacho, C., Coulouris, G., Avagyan, V., Ma, N., Papadopoulos, J., Bealer, K., & Madden, T. L. (2009). BLAST+: Architecture and applications. BMC Bioinformatics, 10, 1–9. http://doi.org/10.1186/1471-2105-10-421
