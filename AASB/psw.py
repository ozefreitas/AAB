def criaMatZeros(nl,nc):
    res = []
    for i in range(0,nl):
        res.append([0]*nc)
    return res


def criaPWM(seqs, alfabeto):   #seqs é uma lista de sequencias   #slide de geração de PWM - exemplo
    conts = criaMatZeros(len(alfabeto), len(seqs[0]))
    for seq in seqs:
        for x in range(len(seq)):
            linha = alfabeto.index(seq[x])    #linha que corresponde à letra
            conts[linha][x] += 1
    pwm = criaMatZeros(len(conts), len(conts[0]))
    for a in range(len(conts)):
        for b in range(len(conts[0])):
            pwm[a][b] = conts[a][b]/len(seqs)
    return pwm


def probabSeq (pwm, alfabeto, seq):   #slide de probabilidades de geração de sequencias
    res = 1
    for i in range(len(seq)):
        linha = alfabeto.index(seq[i])
        res = res*pwm[linha][i]
    return res


def posMaisProvavel (pwm, alfabeto, seq):   #slide sequencia mais provavel de p
    maximo = -1.0
    maxind = -1
    for k in range(len(seq)-len(pwm[0])):    #k posição inicial, tamanho da seq menos tamanho do motif
        p = probabSeq(pwm, alfabeto, seq[k:k+len(pwm[0])])   #
        if(p > maximo):
            maximo = p   #maior probabilidade 
            maxind = k   #indice que corresponde há maior probabilidade 
    return maxind
#se quiser saber todas as probabilidades fazer uma lista com todos os p

#valor esperado é 1/len(alfabeto 