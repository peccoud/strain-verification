import os
import subprocess

assembly_dir = 'Results/SPAdes_assembly_series'
quast_dir = 'Results/SPAdes_quast_series'
ref_fasta = '../Reference_files/genome/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa'


def run_quast(assembly_scaffolds, ref_fasta, res_dir):
    cmd = f'quast.py --threads 10 -o {res_dir} -R {ref_fasta} {assembly_scaffolds}'
    print(f'Running {cmd}')
    subprocess.call(cmd, shell=True)


def process_assembly(assembly_res_dir, ref_fasta):
    scaffold_fasta_basename = [f for f in os.listdir(assembly_res_dir)
                               if f == 'scaffolds.fasta']
    scaffold_fasta_basename = scaffold_fasta_basename[0]
    scaffold_fasta = os.path.join(assembly_res_dir, scaffold_fasta_basename)
    sample_name, n_reads, _ = os.path.basename(assembly_res_dir).split('_')
    quast_res_dir = os.path.join(quast_dir, f'{sample_name}_{n_reads}_reads')
    run_quast(scaffold_fasta, ref_fasta, quast_res_dir)


assembly_res_dirs = [os.path.join(assembly_dir, d)
                     for d in os.listdir(assembly_dir)]


for d in assembly_res_dirs:
    process_assembly(d, ref_fasta)

