# import collections
from structures import *


def validate_seq(dna_seq):
    """Valida se a sequencia inserida é de DNA ou não"""
    seq = dna_seq.upper()
    for nuc in seq:
        if nuc not in DNA_Nucleotidos:
            return False
    return seq


def countNucFrequency(seq):
    count = {"A": 0, "T": 0, "C": 0, "G": 0}
    val_seq = validate_seq(seq)
    if val_seq is False:
        print("Not a DNA sequence")
        quit()
    else:
        for nuc in val_seq:
            count[nuc] += 1
        return count
    # return dict(collections.Counter(seq))


def complement(seq):
    return "".join([DNA_reverse_complement[nuc] for nuc in seq])


def transcription(seq):
    """Transcrição de DNA -> RNA, trocando Timina por Uracilo"""
    return seq.upper().replace("T", "U")


def reverse_complement(seq):
    seq = seq.lower()
    seq1 = seq[::-1]
    return seq1.replace("a", "T").replace("t", "A").replace("c", "G").replace("g", "C")


# Com lista por compreensão
def reverse_complement_2(seq):
    return "".join([DNA_reverse_complement[nuc] for nuc in seq])[::-1]
    # mapping = str.maketrans("ATGC", "TACG")
    # return seq.translate(mapping)[::-1]


def cg_content(seq):
    return round((seq.count("C") + seq.count("G")) / len(seq) * 100)


def cg_content_subseq(seq, k=20):
    res = []
    for i in range(0, len(seq) - k + 1, k):
        subseq = seq[i:i + k]
        res.append(cg_content(subseq))
    return res


def translation(seq, init_pos=0, seq_type="RNA"):
    if seq_type == "RNA":
        codoes = []
        for i in range(init_pos, len(seq) - 2, 3):
            cod = seq[i:i + 3]
            codoes.append(cod)
            # print(codoes)
        aa = []
        for c in codoes:
            aa.append(Genetic_Code[c])
        return "".join(aa)
    if seq_type == "DNA":
        RNA_seq = transcription(seq[init_pos:])
        return translation(RNA_seq, seq_type="RNA")


def codon_usage(seq, aminoacid):
    codoes = []
    for i in range(0, len(seq) - 2, 3):
        cod = seq[i:i + 3]
        codoes.append(cod)
    aa = []
    for c in codoes:
        if Genetic_Code[c] == aminoacid:
            aa.append(c)
    # return aa
    count = {}
    for amin in aa:
        count[amin] = count.get(amin, 0) + 1
    # return count
    soma = 0.0
    for value in count.values():
        soma += 1
    resultado = {}
    for cod in count:
        resultado[cod] = round(count[cod] / soma, 2)
    return soma, resultado


def motifs_position(seq, motif):
    pos = []
    for i in range(len(seq) - len(motif)):
        temp = []
        if seq[i] == motif[0]:
            for j in range(len(motif)):
                if seq[i + j] == motif[0 + j]:
                    temp.append(seq[i + j])
                    # if j == len(motif) - 1:
                    #    pos.append(i + 1)
            # print(temp)
            if len(temp) == len(motif):
                pos.append(i + 1)
    pos = [str(p) for p in pos]
    if pos == []:
        return "{} not found in the sequence {}".format(motif, seq)
    else:
        return " ".join(pos)


def open_reading_frames(seq, seq_type="RNA"):
    if seq_type == "RNA":
        orfs = []
        for x in range(3):
            orfs.append(translation(seq, init_pos=x))
            # print(orfs)
        for x in range(3):
            orfs.append(translation(transcription(reverse_complement(seq)), init_pos=x))
        return orfs


def protein(seq):
    seqs = open_reading_frames(seq)
    result = []
    for orf in seqs:
        prot = []
        for x in range(len(orf)):
            if orf[x] == "M":
                prot.append(orf[x])
                for y in range(x + 1, len(orf)):
                    if orf[y] == "_":
                        prot.append(orf[y])
                        break
                    else:
                        prot.append(orf[y])
                # print(prot)
        result.append(prot)
        # print(result)
    for p in result:
        if p != []:
            if p[0] == "M" and p[-1] == "_":
                return "".join(p)
        else:
            return "0 proteins found"
