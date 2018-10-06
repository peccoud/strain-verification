import os
import subprocess
import sys

subsampled_sample_dir = sys.argv[1]

SPADES = 'spades.py'


ref_fasta = '../Reference_files/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa'
downsampling_dirs = [os.path.join(subsampled_sample_dir, f) 
                     for f in os.listdir(subsampled_sample_dir)]
assembly_results_dir = 'Results/SPAdes_assembly_series'
os.makedirs(assembly_results_dir, exist_ok=True)

def run_spades(reads1, reads2, ref_fasta, res_dir):
    cmd = f'{SPADES} -1 {reads1} -2 {reads2} -t 6 -m 16 --trusted-contigs {ref_fasta} -o {res_dir}'
    print(f'Running {cmd}')
    subprocess.call(cmd, shell=True)


def run_quast(assembly_scaffolds, ref_fasta, res_dir):
    cmd = f'quast.py -o {res_dir} -R {ref_fasta} {assembly_scaffolds}'
    print(f'Running {cmd}')
    subprocess.call(cmd, shell=True)


def process_downsampled_read_pair(assembly_results_dir,
                                  reads1,
                                  ref_fasta):
    reads2 = reads1.replace('val_1', 'val_2').replace('_R1', '_R2')
    downsampling_target = int(os.path.basename(reads1).split('.')[1].split('_')[0])
    sample_name = os.path.basename(reads1).split('_')[0]
    res_dir = os.path.join(assembly_results_dir, f'{sample_name}_{downsampling_target}_reads')
    os.makedirs(res_dir, exist_ok=True)
    run_spades(reads1, reads2, ref_fasta, res_dir)


def assemble_downsampled_folder(downsampling_dir,
                                assembly_results_dir,
                                ref_fasta):
    print(downsampling_dir)
    print(os.listdir(downsampling_dir))
    reads1_list = [os.path.join(downsampling_dir, f) for f in os.listdir(downsampling_dir)
                   if 'val_1' in f]
    for r in reads1_list:
        process_downsampled_read_pair(assembly_results_dir, r, ref_fasta)


for d in downsampling_dirs:
    assemble_downsampled_folder(d, assembly_results_dir, ref_fasta)

