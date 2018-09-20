import sys

orig_vcf = sys.argv[1]
filtered_vcf = open(orig_vcf.replace('.vcf', '.discordant.vcf'), 'w')

with open(orig_vcf) as f:
    for line in f:
        if line.startswith('#'):
            filtered_vcf.write(line)
        else:
            fields = line.strip().split('\t')
            GT1 = fields[-2].split(':')[0]
            GT2 = fields[-1].split(':')[0]
            if GT1 != GT2:
                filtered_vcf.write(line)
filtered_vcf.close()
