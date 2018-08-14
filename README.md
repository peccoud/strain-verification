# Analysis of yeast WGS samples

This repository contains all code used for analyzing yeast samples of group Peccoud of Colorado State University. All scripts are tested with software dependencies listed in section `Software dependencies`. The raw data and reference files are delivered separately due to their large size. Scripts in this repository allow full reproduction of all delivered and discussed results. 

Directory structure reflects the types of performed analyses. Scripts for performing each step are placed under analysis-specific directories. Each step has its own `Results`-directory. Some of the steps are independent, while some depend on each other. Dependencies are listed in this `README` document under each section.

# Software dependencies
* FastQC - https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
* Trimgalore! 

# Analysis steps

## FastQC before trimming
FastQC calculates and visualizes sequencing quality metrics, e.g. GC content distribution and sequencing adapter contamination. FastQC metrics can be used to identify issues in sequencing. Comparing metrics befor and after trimming step helps to determine if trimming was successful.
 
Run FastQC by invoking script:
```
cd FastQC
bash run_fastqc_before_trimming.sh
```
Results of FastQC run will be placed in `FastQC/Results/FastQC_before_trimming`. See example reports on FastQC website for interpretation.

## Trimming reads
Adaptive trimming removes possible adapter contamination and low-quality tales of reads. Trimming produces new set of fastq files to be used in downstream analyses. Trimming is performed with Trimgalore!

Run trimming by invoking script:
```
cd Trimming
bash trim_reads.sh
```
