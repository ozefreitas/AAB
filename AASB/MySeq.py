# -*- coding: utf-8 -*-

def translate_codon (cod):
    """Translates a codon into an aminoacid using an internal dictionary with the standard genetic code."""
    tc = {"GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
          "TGT": "C", "TGC": "C",
          "GAT": "D", "GAC": "D",
          "GAA": "E", "GAG": "E",
          "TTT": "F", "TTC": "F",
          "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
          "CAT": "H", "CAC": "H",
          "ATA": "I", "ATT": "I", "ATC": "I",
          "AAA": "K", "AAG": "K",
          "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
          "ATG": "M", "AAT": "N", "AAC": "N",
          "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
          "CAA": "Q", "CAG": "Q",
          "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
          "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
          "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
          "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
          "TGG": "W",
          "TAT": "Y", "TAC": "Y",
          "TAA": "_", "TAG": "_", "TGA": "_"}
    if cod in tc:
        return tc[cod]
    else:
        return None


class MySeq: 
    """ Class for biological sequences. """
    
    def __init__(self, seq, seq_type="DNA"):
        self.seq = seq.upper()
        self.seq_type = seq_type

    def __len__(self):
        return len(self.seq)
    
    def __getitem__(self, n):
        return self.seq[n]

    def __getslice__(self, i, j):
        return self.seq[i:j]

    def __str__(self):
        return self.seq
        
    def get_seq_biotype(self):
        return self.seq_type
        
    def show_info_seq (self):
        print ("Sequence: " + self.seq + " biotype: " + self.seq_type)
        
    def alphabet(self):
        if self.seq_type == "DNA": return "ACGT"
        elif self.seq_type == "RNA": return "ACGU"
        elif self.seq_type == "PROTEIN": return "ACDEFGHIKLMNPQRSTVWY"
        else: return None
        
    def validate (self):
        alp = self.alphabet()
        res = True
        i = 0
        while i < len(self.seq) and res:
            if self.seq[i] not in alp: 
                res = False
            else: 
                i += 1
        return res 
        
    def transcription (self):
        if self.seq_type == "DNA":
            return MySeq(self.seq.replace("T","U"), "RNA")
        else:
            return None
        
    def translate (self, iniPos= 0):
        if self.seq_type != "DNA":
            return None
        seq_aa = ""
        for pos in range(iniPos,len(self.seq)-2,3):
            cod = self.seq[pos:pos+3]
            seq_aa += translate_codon(cod)
        return MySeq(seq_aa, "PROTEIN")     
    
    def reverse_comp(self):
        if self.seq_type == "PROTEIN":
            return None
        elif self.seq_type == "DNA":
            inv = self.seq[::-1]
            invrep = inv.replace("A","t").replace("T","a").replace("C","g").replace("G","c")
            return MySeq(invrep, self.seq_type)
        else:
            inv = self.seq[::-1]
            invrep = inv.replace("A","t").replace("T","u").replace("C","g").replace("G","c")
            return MySeq(invrep, self.seq_type)


# if __name__ == "__main__":
#     s1 = MySeq("ATGTGATAAGAATAGAATGCTGAATAAATAGAATGACAT")
#     s2 = MySeq("MKVVLSVQERSVVSLL", "PROTEIN")
#     print(s1.validate(), s2.validate())
#     print(s1)
#     s3 = s1.transcription()
#     s5 = s1.reverse_comp()
#     s5.show_info_seq()
#     s3.show_info_seq()
#     s4 = s1.reverse_comp().translate()
#     s4.show_info_seq()


class Enzyme:

    def __init__(self, iub):
        self.enzima = iub
        self.iub = {"R": ["G", "A"], "Y": ["C", "T"], "M": ["A", "C"], "K": ["G", "T"],
                    "S": ["G", "C"], "W": ["A", "T"], "B": ["C", "G", "T"], "D": ["G", "A", "T"],
                    "H": ["C", "A", "T"], "V": ["G", "A", "C"], "N": ["G", "A", "C", "T"]}

    def __len__(self):
        return len(self.enzima)

    def __getitem__(self, n):
        return self.enzima[n]

    def __getslice__(self, i, j):
        return self.enzima[i:j]

    def __str__(self):
        return self.enzima

    def iubToRE(self):
        regexp = ""
        for cod in self.enzima:
            if cod == "^":
                regexp += cod
            elif cod in self.iub:
                regexp += "["+str("".join(self.iub[cod]))+"]"
            elif cod in ["A", "G", "T", "C"]:
                regexp += cod
        return regexp

    def cutPositions(self, seq):
        import re
        regexp = self.iubToRE()
        indice = regexp.index("^")
        regexp = regexp.replace("^", "")
        # res = re.search(regexp, seq)
        res2 = re.findall(regexp, seq)
        result = []
        for i in res2:
            result.append(seq.index(i))
        # return res.group()
        # return res.span()
        return result

    def cutSubsequences(self, locs, seq):
        for i in locs:
            if i >= len(seq):
                return None
        result = [seq[0:locs[0]]]
        for i in range(len(locs)):
            if locs[i] == locs[-1]:
                result.append(seq[locs[i]:len(seq)])
            else:
                result.append(seq[locs[i]:locs[i+1]])
        return result


if __name__ == "__main__":
    X = Enzyme(iub="G^AMTV")
    print(X.__str__())
    print(X.iubToRE())
    print(X.cutPositions(seq="GACTGTAGCTAGAATA"))
    print(X.cutSubsequences([3, 8, 15], "GACTGTAGCTAGAATAATCGGATA"))
