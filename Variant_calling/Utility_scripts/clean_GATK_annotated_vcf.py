import sys

orig_file = sys.argv[1]
res = open(orig_file.replace('.vcf', '.formatted.tsv'), 'w')

ANN_annotation_string = 'Allele | Annotation | Annotation_Impact | Gene_Name | Gene_ID | Feature_Type | Feature_ID | Transcript_BioType | Rank | HGVS.c | HGVS.p | cDNA.pos / cDNA.length | CDS.pos / CDS.length | AA.pos / AA.length | Distance | ERRORS / WARNINGS / INFO'
ANN_fields = ANN_annotation_string.split('|')
ANN_fields = [s.strip() for s in ANN_fields]
n_ANN = len(ANN_fields)
def index_startswith(stringlist, pattern):
    for i, s in enumerate(stringlist):
        if s.startswith(pattern):
            return i

def parse_info_field(info):
    fields = info.split(';')
    ann_index  = index_startswith(fields, 'ANN')
    ann_entries = fields[ann_index].split('|')
    
    # Split entries by transcript
    transcripts = [ann_entries[x:x+15] for x in range(0,len(ann_entries), 15)]    
    
    transcripts = [t for t in transcripts if len(t) == 15]
    # Check severity of mutation if there are multiple annotations
    impact_severity = {'MODIFIER': 1, 'LOW': 2, 'MODERATE': 3, 'HIGH': 4}
    if len(transcripts) > 1:
        severity_index = ANN_fields.index('Annotation_Impact')
        severities = [impact_severity[t[severity_index]] for t in transcripts]
        max_severity = severities.index(max(severities))
        return transcripts[max_severity]
    else:
        return transcripts[0]



format_ind = {
    'GT': 0, 'AD': 1, 'DP': 2, 'GQ': 3, 'PL': 4
}
with open(orig_file) as f:
    for line in f:
        if line.startswith('##'):
            continue
        elif line.startswith('#'):
            header = line[1:].strip().split('\t')
            info_col_ind = header.index('INFO')
            del header[info_col_ind]
            
            # Note the indexing has changed after deleting the info column
            format_col_ind = header.index('FORMAT')
            format_headers = 'GT:AD:DP:GQ:PL'.split(':')
            format_headers1 = [h + ':GRL1691' for h in format_headers]
            format_headers2 = [h + ':GRL1693' for h in format_headers]
            header = header[:format_col_ind] + format_headers1 + format_headers2 + header[(format_col_ind + 3):] + ANN_fields
            res.write('\t'.join(header) + '\n')
        else:
            fields = line.strip().split('\t')
            ann_entries = parse_info_field(fields[info_col_ind])
            del fields[info_col_ind]
            field_format = fields[format_col_ind].split(':')
             
            gt1 = fields[format_col_ind + 1].split(':')
            gt2 = fields[format_col_ind + 2].split(':')
            
            if 'DP' not in field_format:
                gt1.insert(2, '.')
                gt2.insert(2, '.')
            fields = fields[:format_col_ind] + gt1 + gt2 + ann_entries
            res.write('\t'.join(fields) + '\n')

res.close()


