from DNAtoolkit import *
import random

randomDNAseq = "".join([random.choice(DNA_Nucleotidos)
                        for nuc in range(51)])
DNAstr = "TGGTCGGTCATCGGCTCTGTTCTCACGGAAGATACATGCTTGACGGTCCAG"  # validate_seq(randomDNAseq)

# Testes para função validate_seq
# print(validate_seq(randomDNAseq))
# print(validate_seq("AGCTGH"))
# print(validate_seq("ATCGATCGATTA"))
# print(validate_seq("AtgCCAAgaC"))
# Testes para funçao countNucFrequency
# print(countNucFrequency("TAGCTAGAACATG"))
# print(countNucFrequency("TAGCTAHSGAACATG"))

# Teste para complementar
# print(complement(DNAstr))

# Teste para transcrição
# print(transcription("ATAAGAGCTTTTAGA"))

# Teste para complementar reverso
# print(reverse_complement("ATAGACTAGATCG"))

# Teste para tradução
# print(translation("ATGGCCATGGCGCCCAGAACTGAGATCAATAGTACCCGTATTAACGGGTGA", seq_type="DNA"))
# print(translation("AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA"))

# Teste para codon usage
# print(codon_usage("AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA", "R"))

# Teste para open_reading_frames
# print(open_reading_frames(transcription(DNAstr)))

print("Sequence: {}\n".format(DNAstr))
print(f"Sequence: {DNAstr}\n")
print(f"[1] + Sequence and Complement: \n5' {DNAstr} 3'")
print("   {}".format("".join(['|' for x in range(len(DNAstr))])))
print(f"3' {complement(DNAstr)} 5'\n")
print(f"[2] + Sequence Length: {len(DNAstr)}\n")
print(f"[3] + Nucleotid Frequency: {countNucFrequency(DNAstr)}\n")
print(f"[4] + DNA -> RNA: {transcription(DNAstr)}\n")
print(f"[5] + Reverse complement: 5' {reverse_complement_2(DNAstr)} 3'\n")
print(f"[6] + CG Content: {cg_content(DNAstr)}%\n")
print(f"[7] + CG Content in each Subseq k = 5: {cg_content_subseq(DNAstr, k=5)}%\n")
print(f"[8] + Translation DNA -> Protein: {translation(DNAstr, seq_type='DNA')}\n")
print(f"[9] + Translation RNAm -> Protein: {translation(transcription(DNAstr))}\n")
print(f"[10] + Codon Usage for aminoacid R (Total codons + Frequency): {codon_usage(transcription(DNAstr), 'R')}\n")
print(f"[11] + Motif ATAGA position: {motifs_position(DNAstr, 'ATAGA')}\n")
print(f"[12] + Open Reading Frames: {open_reading_frames(transcription(DNAstr))}\n")
print(f"[13] + Proteins: {protein(transcription(DNAstr))}\n")
