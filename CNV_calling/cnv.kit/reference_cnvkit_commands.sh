##############################################################################
# GRL 1691
mkdir -p GRL1691
cd GRL1691

# Binning
cnvkit.py autobin \
  /data/Nanopore/Yeast/Illumina/GRL169X_alignments_mkdup/GRL1691.mkdup.rg.bam \
  --annotate /projects/organisms/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.92.genes.bed \
  -m wgs \
  -g ../accessible_regions_R64-1-1.bed

# Coverages
cnvkit.py coverage \
  /data/Nanopore/Yeast/Illumina/GRL169X_alignments_mkdup/GRL1691.mkdup.rg.bam \
  GRL1691.mkdup.rg.target.bed \
  -o GRL1691.mkdup.rg.targetcoverage.cnn
cnvkit.py coverage \
  /data/Nanopore/Yeast/Illumina/GRL169X_alignments_mkdup/GRL1691.mkdup.rg.bam \
  GRL1691.mkdup.rg.antitarget.bed \
  -o GRL1691.mkdup.rg.antitargetcoverage.cnn

# Flat reference
cnvkit.py reference \
  --haploid-x-reference \
  -o FlatReference.cnn \
  --no-edge \
  -f /projects/organisms/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa \
  -t GRL1691.mkdup.rg.target.bed \
  -a GRL1691.mkdup.rg.antitarget.bed

# Fix Coverages
cnvkit.py fix \
 --no-edge \
 -o GRL1691.mkdup.rg.cnr \
 GRL1691.mkdup.rg.targetcoverage.cnn GRL1691.mkdup.rg.antitargetcoverage.cnn FlatReference.cnn

# Segment
cnvkit.py segment GRL1691.mkdup.rg.cnr -t 0.000006 -o GRL1691.mkdup.rg.cns

# Call
cnvkit.py call GRL1691.mkdup.rg.cns -y -m threshold -t=-1.0000000,0.5849625,1.3219281,1.8073549,2.1699250 --purity 1 -o GRL1691.mkdup.rg.call.cns


# Pics
cnvkit.py scatter GRL1691.mkdup.rg.cnr -s GRL1691.mkdup.rg.cns -o GRL1691-scatter.pdf
cnvkit.py diagram GRL1691.mkdup.rg.cnr -s GRL1691.mkdup.rg.cns -o GRL1691-diagram.pdf

##############################################################################
# GRL 1693
mkdir -p GRL1693
cd GRL1693

# Binning
cnvkit.py autobin \
  /data/Nanopore/Yeast/Illumina/GRL169X_alignments_mkdup/GRL1693.mkdup.rg.bam \
  --annotate /projects/organisms/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.92.genes.bed \
  -m wgs \
  -g ../accessible_regions_R64-1-1.bed

# Coverages
cnvkit.py coverage \
  /data/Nanopore/Yeast/Illumina/GRL169X_alignments_mkdup/GRL1693.mkdup.rg.bam \
  GRL1693.mkdup.rg.target.bed \
  -o GRL1693.mkdup.rg.targetcoverage.cnn
cnvkit.py coverage \
  /data/Nanopore/Yeast/Illumina/GRL169X_alignments_mkdup/GRL1693.mkdup.rg.bam \
  GRL1693.mkdup.rg.antitarget.bed \
  -o GRL1693.mkdup.rg.antitargetcoverage.cnn

# Flat reference
cnvkit.py reference \
  --haploid-x-reference \
  --no-edge \
  -o FlatReference.cnn \
  -f /projects/organisms/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa \
  -t GRL1693.mkdup.rg.target.bed \
  -a GRL1693.mkdup.rg.antitarget.bed

# Fix Coverages
cnvkit.py fix GRL1693.mkdup.rg.targetcoverage.cnn GRL1693.mkdup.rg.antitargetcoverage.cnn FlatReference.cnn \
 -o GRL1693.mkdup.rg.cnr \
 --no-edge

# Segment
cnvkit.py segment GRL1693.mkdup.rg.cnr -t 0.000006 -o GRL1693.mkdup.rg.cns

# Call
cnvkit.py call GRL1693.mkdup.rg.cns -y -m threshold -t=-1.0000000,0.5849625,1.3219281,1.8073549,2.1699250 --purity 1 -o GRL1693.mkdup.rg.call.cns


# Pics
cnvkit.py scatter GRL1693.mkdup.rg.cnr -s GRL1693.mkdup.rg.cns -o GRL1693-scatter.pdf
cnvkit.py diagram GRL1693.mkdup.rg.cnr -s GRL1693.mkdup.rg.cns -o GRL1693-diagram.pdf

##############################################################################
# Joint

