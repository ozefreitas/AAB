import numpy as np
seq1 = "ATGACGAATCGAATAGAGAC"
seq2 = "ATCGCGAGATCGAGAGATAT"

mat = []
for i in range(len(seq1)):
    linha = []
    for j in range(len(seq2)):
        if seq1[i] == seq2[j]:
            linha.append(1)
        else:
            linha.append(0)
        mat.append(linha)

print(mat)
print(np.array(mat))
