# Analysis of yeast WGS samples

This repository contains all code used for analyzing yeast samples of group Peccoud of Colorado State University. All scripts are tested with software dependencies listed in section `Software dependencies`. The raw data and reference files are delivered separately due to their large size. Scripts in this repository allow full reproduction of all delivered and discussed results. 

Directory structure reflects the types of performed analyses. Scripts for performing each step are placed under analysis-specific directories. Each step has its own `Results`-directory. Some of the steps are independent, while some depend on each other. Dependencies are listed in this `README` document under each section.

# Software dependencies
* FastQC - https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
* Trimgalore! - https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/
* cutadapt - https://cutadapt.readthedocs.io/en/stable/
* bwa - http://bio-bwa.sourceforge.net
* Picard - https://broadinstitute.github.io/picard/

# Analysis steps

Note that instructions for each step assume that working directory in the beginning of the step is the repository's root directory, i.e. the directory where this `README` file is located.

## FastQC before trimming
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

Invoke alignment by running script:
```
cd Aligment
bash align_samples.sh
```

Used bwa parameters:
```
Number of threads (-t): 10
```

Aligned bam files are stored in `Alignment/Results/Alignments`. Downstream steps depending on bam files will look for them in this directory.

## Quality metrics
Alignment of reads produces information for further inspection of sample and sequencing quality. In this step, Picard is used to assess the quality from bam giles. Picard functions will produce multiple result files corresponding to different types of metrics. See Picard documentation for detailed descriptions on each metric.

Invoke quality assessment by running script:
```
cd Quality_metrics
bash run_picard.sh
```

Picard result files will be stored to `Quality_metrics/Picard_results`

## CNV calling

### cn.mops

### CNVnator

### Breakdancer

## De novo assemblies

### SOAP denovo

### SPADes

## Assembly metrics (Quast)

## Subsampling series for 
