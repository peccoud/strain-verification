import os
import subprocess
import sys

# Downsample fastq files
fastq_dir = sys.argv[1]
sample_name = sys.argv[2]


fastqs = [f for f in os.listdir(fastq_dir)
          if f.endswith(".fq.gz") and f.startswith(sample_name)]
fastqs_1 = sorted([os.path.join(fastq_dir, f)
                  for f in fastqs if "_R1_" in f])
fastqs_2 = sorted([os.path.join(fastq_dir, f) 
                   for f in fastqs if "_R2_" in f])

downsampling_res_dir = f'{sample_name}_subsampling_series'
os.makedirs(downsampling_res_dir, exist_ok=True)

# Number of reads to downsample to
downsampling_targets = [10000, 30000, 60000, 90000, 120000, 150000,
                        180000, 210000, 240000, 260000, 300000, 400000,
                        500000, 600000, 700000, 800000, 900000, 1000000,
                        1200000, 1400000, 1600000, 1800000, 2000000,
                        2500000, 3000000, 3500000]

def downsample_fastq(reads1, reads2, target_dir, downsampling_target):
    res_dir = os.path.join(target_dir,
                           f'fastq_{downsampling_target}_reads')
    os.makedirs(res_dir, exist_ok=True)
    cmd = 'seqtk sample -s123 {fasta_file} {downsampling_target} | gzip  > {out_file}'
    cmd_reads_1 = cmd.format(
                    fasta_file=reads1,
                    downsampling_target=downsampling_target,
                    out_file=os.path.join(res_dir,
                                          os.path.basename(reads1).replace('.fq', f'.{downsampling_target}_reads.fq.gz'))
    )
    print(cmd_reads_1)
    subprocess.call(cmd_reads_1, shell=True)
    subprocess.call(
        cmd.format(
            fasta_file=reads2,
            downsampling_target=downsampling_target,
            out_file=os.path.join(res_dir,
                                  os.path.basename(reads2).replace('.fq', f'.{downsampling_target}_reads.fq.gz'))
            ),
        shell=True
    )

for reads1, reads2 in zip(fastqs_1, fastqs_2):
    for dt in downsampling_targets:
        downsample_fastq(reads1, reads2, downsampling_res_dir, dt)

