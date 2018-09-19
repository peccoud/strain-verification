
# coding: utf-8

# Load libraries
import os
import subprocess
import sys

# Helper functions
def find_file(dir_, ending):
    files_ = [f for f in os.listdir(dir_) if f.endswith(ending)]
    if len(files_) > 1:
        print('Found more than one match!')
        return None
    elif not files_:
        print('Did not find any matches!')
        return None
    else:
        return os.path.join(dir_, files_[0])


# In[95]:


# Set paths
fastq_dir = '../Trimming/Results/Trimmed_fastq_files'
yeast_index = '../Reference_files/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa'
alignments_dir = '../Alignment/Results/Alignments'
results_dir = 'SOAPdenovo/Results'
os.makedirs(alignments_dir, exist_ok=True)

# Tool paths
PICARD_JAR = '../bin/picard-2.9/picard.jar'

# Directory for yeast assemblies
assembly_dir = results_dir
os.makedirs(assembly_dir, exist_ok=True)

# Directory with config files
soap_config_dir = 'SOAPdenovo/configs'


def run_soapdenovo2(config, out_prefix):
    """Run SOAPdenovo2."""
    log_file = os.path.join(os.path.dirname(out_prefix), 'ass.log')
    err_file = os.path.join(os.path.dirname(out_prefix), 'ass.err')

    # Build command
    cmd = ('SOAPdenovo-63mer all -s {config} -K 63 -R -o {out_prefix} '
           '1>{log_file} 2>{err_file}').format(
                config=config,
                out_prefix=out_prefix,
                log_file=log_file,
                err_file=err_file
    )

    # Execute assembly
    print('Running assembly\n%s' % cmd)
    p = subprocess.call(cmd, shell=True)

    if p:
        return False
    else:
        return True


# Run assemblies

# Assembly for GRL1691:

# Set paths and create result directory
GRL1691_config = os.path.join(soap_config_dir, 'GRL1691.config')
out_GRL1691 = os.path.join(assembly_dir, 'GRL1691_assembly/GRL1691')
os.makedirs(os.path.dirname(out_GRL1691), exist_ok=True)

# Run assembly
status = run_soapdenovo2(GRL1691_config, out_GRL1691)

# Same for other samples:

# Assembly for GRL1693
GRL1693_config = os.path.join(soap_config_dir, 'GRL1693.config')
out_GRL1693 = os.path.join(assembly_dir, 'GRL1693_assembly/GRL1693')
os.makedirs(os.path.dirname(out_GRL1693), exist_ok=True)
status = run_soapdenovo2(GRL1693_config, out_GRL1693)

# Assembly for GRL1694
GRL1694_config = os.path.join(soap_config_dir, 'GRL1694.config')
out_GRL1694 = os.path.join(assembly_dir, 'GRL1694_assembly/GRL1694')
os.makedirs(os.path.dirname(out_GRL1694), exist_ok=True)
status = run_soapdenovo2(GRL1694_config, out_GRL1694)


# Collect genome assembly metrics with QUAST

# Set up functions
def run_quast(contigs, reference_fasta, output_dir, scaffolds=False):
    cmd = 'quast.py {contigs} -R {ref} -o {output_dir}'.format(
                        output_dir=output_dir,
                        contigs=' '.join(contigs),
                        ref=reference_fasta
        )
    if scaffolds:
        cmd += ' --scaffolds'
    print(cmd)
    p_ = subprocess.call(cmd, shell=True)


# Run comparison for GRL1691
GRL1691_assembly_dir = os.path.dirname(out_GRL1691)
GRL1691_contigs_fasta = find_file(GRL1691_assembly_dir, '.contig')
quast_out_GRL1691 = os.path.join(assembly_dir, 'quast_results_contigs', 'GRL1691')
os.makedirs(os.path.dirname(quast_out_GRL1691), exist_ok=True)

status = run_quast([GRL1691_contigs_fasta], yeast_index, quast_out_GRL1691)

# Run comparison for GRL1693
GRL1693_assembly_dir = os.path.dirname(out_GRL1693)
GRL1693_contigs_fasta = find_file(GRL1693_assembly_dir, '.contig')
quast_out_GRL1693 = os.path.join(assembly_dir, 'quast_results_contigs', 'GRL1693')
os.makedirs(os.path.dirname(quast_out_GRL1693), exist_ok=True)

status = run_quast([GRL1693_contigs_fasta], yeast_index, quast_out_GRL1693)

# Run comparison for GRL1694
GRL1694_assembly_dir = os.path.dirname(out_GRL1694)
GRL1694_contigs_fasta = find_file(GRL1694_assembly_dir, '.contig')
quast_out_GRL1694 = os.path.join(assembly_dir, 'quast_results_contigs', 'GRL1694')
os.makedirs(os.path.dirname(quast_out_GRL1694), exist_ok=True)

status = run_quast([GRL1694_contigs_fasta], yeast_index, quast_out_GRL1694)


# Run Quast comparisons on scaffolds
# Run comparison for GRL1691
GRL1691_assembly_dir = os.path.dirname(out_GRL1691)
GRL1691_scaffolds_fasta = find_file(GRL1691_assembly_dir, '.scafSeq')
quast_out_GRL1691 = os.path.join(assembly_dir, 'quast_results_scaffolds', 'GRL1691')
os.makedirs(os.path.dirname(quast_out_GRL1691), exist_ok=True)

status = run_quast([GRL1691_scaffolds_fasta], yeast_index,
                   quast_out_GRL1691, scaffolds=True)

# Run comparison for GRL1693
GRL1693_assembly_dir = os.path.dirname(out_GRL1693)
GRL1693_scaffolds_fasta = find_file(GRL1693_assembly_dir, '.scafSeq')
quast_out_GRL1693 = os.path.join(assembly_dir, 'quast_results_scaffolds', 'GRL1693')
os.makedirs(os.path.dirname(quast_out_GRL1693), exist_ok=True)

status = run_quast([GRL1693_scaffolds_fasta], yeast_index,
                   quast_out_GRL1693, scaffolds=True)

# Run comparison for GRL1694
GRL1694_assembly_dir = os.path.dirname(out_GRL1694)
GRL1694_scaffolds_fasta = find_file(GRL1694_assembly_dir, '.scafSeq')
quast_out_GRL1694 = os.path.join(assembly_dir, 'quast_results_scaffolds', 'GRL1694')
os.makedirs(os.path.dirname(quast_out_GRL1694), exist_ok=True)

status = run_quast([GRL1694_scaffolds_fasta], yeast_index,
                   quast_out_GRL1694, scaffolds=True)

