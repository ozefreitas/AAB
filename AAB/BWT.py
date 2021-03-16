# -*- coding: utf-8 -*-

class BWT:
    
    def __init__(self, seq = "", buildsufarray = False):
        self.bwt = self.build_bwt(seq, buildsufarray) 
        self.matrix = self.get_full_matrix(seq)


    def set_bwt(self, bw): 
        self.bwt = bw

     ######        
    def get_full_matrix(self, text):
        ls = []
        for n in range(len(text)):
            ls.append(text[n:]+text[:n])  # dependende o valor de i, ele vai buscar 
            # a parte que esta para lá desse indice e depois junta a parte que esta antes
        ls.sort()
        return ls

    ######
    def print_matrix(self):
         for c in self.matrix:
             print(c)


    def build_bwt(self, text, buildsufarray = False):
        m = self.get_full_matrix(text)  ######
        res = ""
        for l in m:  # l toma cada uma das strings de sequencias dentro da lista
            res += l[-1]  # e concatena-se o ultimo simbolo de cada sequencia nessa lista em res
        if buildsufarray:  # contruir um array de sufixos ao mesmo tempo
            self.sa = []  # vai guardar na variável sa
            for i in range(len(m)):  # o iterador toma todos os valores num range do tamanho da lista que contem todas as sequencias
                stpos = m[i].index("$")  # em cada uma dessas sequencias vê em que indice aparece o simbolo "$"
                self.sa.append(len(text)-stpos-1)  # e adiciona a posição a contar do fim da sequencia orifinal
        return res    


    def inverse_bwt(self):
        firstcol = self.get_first_col()
        res = ""
        c = "$" 
        occ = 1
        for i in range(len(self.bwt)):
            s = find_ith_occ(self.bwt, c, occ)
            nuc = firstcol[s]
            occ = 1 
            k = s - 1
            while firstcol[k] == nuc and k >= 0: # ve quantas vezes ocorre um simbolo para podermos depois ir buscar essa ocorrencia na bwt
                occ += 1                           # e firstcol[k], vai vendo o que tem para tras, uma vez que esta por ordem alfabetica
                # e se for um aunica ocorrencia, nao continua
                k -= 1
            res += nuc
            return res        


    def get_first_col (self):
        firstcol = []
        m = self.bwt
        for s in m:
            firstcol.append(s)
        firstcol.sort()
        return firstcol


    def last_to_first(self):
        res = []
        fc = self.get_first_col()
        for x in range(len(fc)):
            nuc = self.bwt[x]  # vai buscar o simbolo da bwt correspondente ao numero do iterador
            occ = self.bwt[:x].count(nuc) + 1  # vai contar o numero de vezes qeu esse simbolo aparece até a posição do iterador
            res.append(find_ith_occ(fc, nuc, occ))  # vai ver em que indice aparece essa ocorrencia na primeira coluna
        return res


    def bw_matching(self, patt):
        lf = self.last_to_first()
        res = []
        top = 0
        bottom = len(self.bwt)-1
        flag = True
        while flag and top <= bottom:
            if patt != "":
                symbol = patt[-1]
                patt = patt[:-1]
                lmat = self.bwt[top:(bottom+1)]
                if symbol in lmat:
                    topIndex = lmat.index(symbol) + top
                    bottomIndex = bottom - lmat[::-1].index(symbol)
                    top = lf[topIndex]
                    bottom = lf[bottomIndex]
                else: 
                    flag = False
            else: 
                for i in range(top, bottom+1): 
                    res.append(i)
                flag = False            
        return res        


    def bw_matching_pos(self, patt):
        res = []
        match = self.bw_matching(patt)
        for m in match:
            res.append(self.sa[m])
        res.sort()
        return res


# auxiliary

def find_ith_occ(l, elem, index):
    for x in range(len(l)):
        k = 0
        if l[x] == elem:
            k += 1
            if k == index:
                return x
    return -1 

     
def test():
    seq = "TAGACAGAGA$"
    bw = BWT(seq)
    # bw.print_matrix()
    print (bw.bwt)
#    print (bw.last_to_first())
#    print (bw.bw_matching("AGA"))


def test2():
    bw = BWT("")
    bw.set_bwt("ACG$GTAAAAC")
    print (bw.inverse_bwt())

def test3():
    seq = "TAGACAGAGA$"
    bw = BWT(seq, True)
    print("Suffix array:", bw.sa)
#    print(bw.bw_matching_pos("AGA"))

test()
#test2()
#test3()

