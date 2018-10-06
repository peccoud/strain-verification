import os
import pandas as pd

quast_results = 'Results/SPAdes_quast_series'

# Function for listing file paths in a tree
def get_files_in_tree(dir_, ext=None):
    file_paths = list()
    for root, _, filenames in os.walk(dir_):
        for filename in filenames: 
            if not ext or (ext and filename.endswith(ext)):
                file_paths.append(os.path.join(root, filename))
            else:
                continue
    return file_paths


def read_report(quast_dir):
    print(f'Processing folder {quast_dir}')
    sample_name, n_reads = get_sample_name_and_reads(quast_dir)
    report_file = get_files_in_tree(quast_dir, 
                                    ext='transposed_report.tsv')[0]
    df = pd.read_csv(report_file, sep='\t')
    df['sample_name'] = [sample_name]
    df['reads'] = [int(n_reads)]
    return df


def get_sample_name_and_reads(quast_dir):
    return os.path.basename(quast_dir).split('_')[:2]


def process_reports(report_list):
    return pd.concat(report_list)


quast_res_dirs = [os.path.join(quast_results, f) for f
                  in os.listdir(quast_results)]
report_list = [read_report(r) for r in quast_res_dirs]

quast_df =  process_reports(report_list)

# Write out for analysis with R
csv_path = 'Results/Summarized_results/Combined_Quast_reports.tsv'
quast_df.to_csv(csv_path, sep='\t', index=False)
