
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


def find_read_files(fastq_dir, samplename):
    files = [os.path.join(fastq_dir, f)
             for f in os.listdir(fastq_dir)]
    r1_ = [f for f in files 
           if samplename in f and 'val_1' in f]
    r2_ = [f for f in files 
           if samplename in f and 'val_2' in f]
    return r1_[0], r2_[0]


# Set paths
fastq_dir = '../Trimming/Results/Trimmed_fastq_files'
yeast_index = '../Reference_files/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa'
alignments_dir = '../Alignment/Results/Alignments'
results_dir = 'SPAdes/Results'
os.makedirs(alignments_dir, exist_ok=True)

# Tool paths
PICARD_JAR = '../bin/picard-2.9/picard.jar'

# Directory for yeast assemblies
assembly_dir = results_dir
os.makedirs(assembly_dir, exist_ok=True)

# Directory with config files


def run_SPAdes(reads1, reads2, out_prefix, trusted_contigs=None,
               cpu=10, memory=16):
    """Run SPAdes."""
    # Build command
    cmd = ('spades.py -1 {reads1} -2 {reads2} -t {cpu} '
           '-m {memory} -o {out_prefix}').format(
            reads1=reads1,
            reads2=reads2,
            cpu=cpu,
            memory=memory,    
            out_prefix=out_prefix
    )

    if trusted_contigs:
        cmd += '--trusted-contigs ' + trusted_contigs

    # Execute assembly
    print('Running assembly\n%s' % cmd)
    p = subprocess.call(cmd, shell=True)

    if p:
        return False
    else:
        return True


# Run assemblies
def run_assembly(samplename, fastq_dir, assembly_dir, trusted_contigs=None):
    r1, r2 = find_read_files(fastq_dir, samplename)
    out_folder = os.path.join(assembly_dir, samplename)
    os.makedirs(out_folder, exist_ok=True)
    run_SPAdes(r1, r2, out_folder, trusted_contigs)

# Assemblies without the reference
assembly_dir_without_reference = os.path.join(assembly_dir, 'without_reference')
run_assembly('GRL1691', fastq_dir, assembly_dir_without_reference)
run_assembly('GRL1693', fastq_dir, assembly_dir_without_reference)
run_assembly('GRL1694', fastq_dir, assembly_dir_without_reference)

# ...and with reference
assembly_dir_with_reference = os.path.join(assembly_dir, 'with_reference')
run_assembly('GRL1691', fastq_dir, assembly_dir_with_reference, yeast_index)
run_assembly('GRL1693', fastq_dir, assembly_dir_with_reference, yeast_index)
run_assembly('GRL1694', fastq_dir, assembly_dir_with_reference, yeast_index)




# Collect genome assembly metrics with QUAST

# Set up functions
def run_quast(contigs, reference_fasta, output_dir, scaffolds=False):
    cmd = 'quast.py {contigs} -R {ref} -o {output_dir}'.format(
                        output_dir=output_dir,
                        contigs=contigs,
                        ref=reference_fasta
        )
    if scaffolds:
        cmd += ' --scaffolds'
    print(cmd)
    p_ = subprocess.call(cmd, shell=True)


def quast_wrapper(samplename, assembly_dir, reference_fasta, scaffolds=False):

    sample_assembly_dir = os.path.join(assembly_dir, samplename)
    if scaffolds:
        contigs_fasta = find_file(sample_assembly_dir, 'scaffolds.fasta')
        quast_out = os.path.join(assembly_dir, 'quast_results_scaffolds', samplename)
    else:
        contigs_fasta = find_file(sample_assembly_dir, 'contigs.fasta')
        quast_out = os.path.join(assembly_dir, 'quast_results_contigs', samplename)

    os.makedirs(os.path.dirname(quast_out), exist_ok=True)

    run_quast(contigs_fasta, reference_fasta, quast_out)


samplenames = ['GRL1691', 'GRL1693', 'GRL1694']

for s in samplenames:
    
    # Assemblies made with no reference for scaffolding
    quast_wrapper(s, assembly_dir_without_reference, yeast_index)
    quast_wrapper(s, assembly_dir_with_reference, yeast_index)
    

    # Assemblies with reference used for scaffolding
    quast_wrapper(s, assembly_dir_without_reference, yeast_index, True)
    quast_wrapper(s, assembly_dir_with_reference, yeast_index, True)


