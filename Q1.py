'''
Description: This is a SNPs data treatment program for vcf file.
'''


def main():

    # Create chrnames_to_chrs dictionary, parse the input file
    chrnames_to_chrs = dict()
    filename = "trio.sample.vcf"
    with open(filename, "r") as fh:
        for line in fh:
            # Skip header lines, which starts with #
            if not line.startswith("#"):
                fields = line.strip().split("\t")
                chrname = fields[0]
                pos = int(fields[1])
                snpid = fields[2]
                ref = fields[3]
                alt = fields[4]
                
                # Put the data to the dictionary
                if chrname not in chrnames_to_chrs:
                    chrnames_to_chrs[chrname] = Chromosome(chrname)
                chrnames_to_chrs[chrname].add_snp(chrname, pos, snpid, ref, alt)




    with open("transitions.txt","w") as outfile:
        #Specify size of regions.
        region = 1000000
        outfile.write("chromosome\t\tregion\t\t percent_transitions\t\tnum_snps\n")
        for chrname in chrnames_to_chrs:
            chr_obj = chrnames_to_chrs[chrname]
            #Initiate variables.
            start = 1
            last_snp = max(chr_obj.locations_to_snps.keys())
            #Use a while loop to scan regions in each chromosome.
            while start < last_snp:
                end = start + region - 1                
                percent_trs = chr_obj.percent_trs(start,end)
                num_snps = chr_obj.count_snps(start,end)
                outfile.write(f"{chrname}"+f"\t\t{start}..{end}".ljust(20, ' ')+f"\t\t{percent_trs}\t\t\t{num_snps}\n")
                #Renew new start value for next loop.
                start = start + region


# A class representing simple SNPs
class SNP:
    def __init__(self, chrname, pos, snpid, ref_allele, alt_allele):
        assert ref_allele != alt_allele, f"Error: ref == alt at pos {pos}"
        self.chrname = chrname
        self.pos = pos
        self.snpid = snpid
        self.ref_allele = ref_allele
        self.alt_allele = alt_allele

    # Returns True if ref_allele/alt_allele is A/G, G/A, C/T, or T/C
    def is_transition(self):
        is_AG = (self.ref_allele == "A" and self.alt_allele == "G")
        is_GA = (self.ref_allele == "G" and self.alt_allele == "A")
        if is_AG or is_GA:
            return True  
        
        is_CT = (self.ref_allele == "C" and self.alt_allele == "T")
        is_TC = (self.ref_allele == "T" and self.alt_allele == "C")
        if is_CT or is_TC:
            return True

        return False

    # Returns True if the snp is a transversion (ie, not a transition)
    def is_transversion(self):
        if self.is_transition():
            return False
        return True

    # For nice print
    def __str__(self):
        return f"chrname = {self.chrname}\n" + \
                   f"pos = {self.pos}\n" + \
                   f"snpid = {self.snpid}\n" + \
                   f"ref = {self.ref_allele}\n" + \
                   f"alt_allele = {self.alt_allele}\n" + \
                   f"is_transition = {self.is_transition()}\n" + \
                   f"is_transversion = {self.is_transversion()}\n"

'''
# Transition test; should not result in "Test failed!"
snp1 = SNP("1", 12351, "rs11345", "C", "T")
assert snp1.is_transition(), "Test failed!"
print(snp1)
print()

# Transversion test; should not result in "Test failed!"
snp2 = SNP("1", 36642, "rs22541", "A", "T")
assert snp2.is_transversion(), "Test failed!"
print(snp2)
print()

# Error test; should result in "Error: ref == alt at position 69835"
snp3 = SNP("1", 69835, "rs53461", "A", "A")   # Program aborted here

'''


# A class representing a chromosome, which has a collection of SNPs
class Chromosome:
    def __init__(self, chrname):
        self.chrname = chrname
        self.locations_to_snps = dict()

    def get_name(self):
        return self.name
   
    # Given all necessary information to add a new SNP, create
    # a new SNP object and add it to the SNPs dictionary.
    def add_snp(self, chrname, pos, snpid, ref_allele, alt_allele):        
        newsnp = SNP(chrname, pos, snpid, ref_allele, alt_allele)
        self.locations_to_snps[pos] = newsnp

    # Returns the number of transition snps stored in this chromosome
    def count_transitions(self):
        count = 0
        for snp in self.locations_to_snps.values():
            if snp.is_transition():
                count = count + 1
        return count

    # Returns the number of transversion snps stored in this chromosome
    def count_transversions(self):
        return len(self.locations_to_snps) - self.count_transitions()

    #Returns the percentage of transition SNPs.
    def percent_trs(self,start,end):
        trs_count = 0
        trv_count = 0
        for pos,snp in self.locations_to_snps.items():
            if pos >= start and pos <= end:
                if snp.is_transition():
                    trs_count += 1
                else:
                    trv_count += 1
                                
        if (trs_count+trv_count) == 0:
            return 0
        else:
            return round(trs_count/(trs_count+trv_count),3)

    
    #Returns the number of SNPs in a region.
    def count_snps(self,start,end):
        count = 0
        for snp in self.locations_to_snps:
            if snp >= start and snp <= end:
                count += 1
        return count



    # (Inside Chromosome class ...)

    # Returns the number of snps between l and m, divided by region size
    def density_region(self, l, m):
        count = 0
        for location in self.locations_to_snps:
            if location >= l and location <= m:
                count += 1
        return 1000*count/float(m-l+1)


    # Given a region size, looks at non-overlapping windows
    # of that size and returns a list of three elements for
    # the region with the highest density:
    # [density of region, start of region, end of region]
    def max_density(self, region_size):
        region_start = 1
        last_snp_position = max(self.locations_to_snps.keys())        
        best_answer = [0.0, 1, region_size-1]
        
        while region_start < last_snp_position:
            region_end = region_start + region_size - 1
            region_density = self.density_region(region_start, region_end)
            if region_density > best_answer[0]:
                best_answer = [region_density, region_start, region_end]            
            region_start = region_start + region_size
        
        return best_answer


    
'''
# Test chromosome class
chr1 = Chromosome("testChr")
chr1.add_snp("testChr", 24524, "rs15926", "G", "T")
chr1.add_snp("testChr", 62464, "rs61532", "C", "T")

# These should not fail:
assert chr1.count_transitions() == 1, "Test Failed!"
assert chr1.count_transversions() == 1, "Test Failed!"
'''


if __name__ == "__main__":
    main()



