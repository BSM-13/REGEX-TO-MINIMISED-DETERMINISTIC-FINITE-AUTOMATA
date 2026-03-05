from graphviz import Digraph
class _frozenset(frozenset):
    def __repr__(self):
        return super().__repr__().replace('_frozenset','')


def formatareFrozenset(stare):
    if isinstance(stare, str):return stare
    if isinstance(stare, (frozenset)):
        elemente = [str(e) for e in stare]
        return "{" + ",".join(elemente) + "}"

class AFD:

    def __init__(self , Q, alfabet, relatii, stare_start, stare_final):

        self.Q = Q                       #setul starlor ce alcatuiesc automatonul
        self.alfabet = alfabet           #alfabetul recunoscut de automaton
        self.relatii = relatii           #dictionar cu caile automatonului
        self.stare_initiala = stare_start   #starea de unde incepe automatonul
        self.stare_final = set(stare_final) if isinstance(stare_final,(set,list)) else {stare_final}   #starea in care trebuie sa se termine calculul pentru ca limbajul sa fie regulat


    def accepta(self, cuvant):
        stare = self.stare_initiala
        for caracter in cuvant:
            if caracter not in self.alfabet:
                return False
            stare = self.relatii.get(stare,{}).get(caracter)
            if stare is None:
                return False

        return stare in self.stare_final

    def afiseaza(self):
        for stare, rel in self.relatii.items():

            stare = _frozenset(stare) if isinstance(stare,(set,frozenset)) else {stare}

            for l,stare_urm in rel.items():

                stare_urm = frozenset(stare_urm) if isinstance(stare_urm,(set,frozenset)) else {stare_urm}

                print(f'{stare} --{l}-> {stare_urm} ')



    def Hopcroft_minimizare(self):
        Pcomp = [self.stare_final,set(self.Q) - self.stare_final]
        X = Pcomp.copy()
        while X:
            A = X.pop(0)
            for litera in self.alfabet:
                split = 0
                P1 = set()
                for stare in self.relatii:
                    if self.relatii.get(stare,{}).get(litera,None) in A:
                       P1.add(stare)
                Pnou = []
                for P2 in Pcomp:
                    P2_intersectie = P1.intersection(P2)
                    P2_diferenta = P2.difference(P1)
                    if P2_diferenta and P2_intersectie:
                        Pnou.append(P2_diferenta)
                        Pnou.append(P2_intersectie)
                        split = 1
                        if P2 in X:
                            X.remove(P2)
                            X.append(P2_diferenta)
                            X.append(P2_intersectie)
                        else:
                            if len(P2_intersectie) <= len(P2_diferenta):
                                X.append(P2_intersectie)
                            else:

                                X.append(P2_diferenta)

                    else: Pnou.append(P2)

                if split == 1:
                    Pcomp = Pnou

        return Pcomp
    '''
    Functia Hopcroft_minimizare grupeaza starile care au acelasi comportament.
    Plecam de la partitiile initiale Pcomp = [starile finale, starile care nu sunt finale]
    Parcurgem Pcomp de cate ori este nevoie pana cand nu mai este modificat.
    Returnam Pcomp.

    '''

    def reconstruireAFD(self):
        H = [frozenset(partitie) for partitie in self.Hopcroft_minimizare()]
        relatii_nou = {}
        for stare in self.relatii:
            relatii_stare = {}
            for litera in self.alfabet:
                stare_urm = self.relatii.get(stare,{}).get(litera)

                for partitie_finala in H:
                    partitie_finala =frozenset(partitie_finala)
                    if stare_urm in partitie_finala:
                        relatii_stare.update({litera:partitie_finala})

            for partitie_initiala in H:
                partitie_initiala = frozenset(partitie_initiala)
                if stare in partitie_initiala:
                    relatii_nou.update({partitie_initiala:relatii_stare})
        self.relatii = relatii_nou
        self.Q = frozenset(H)
        i = 1
        sf = set()
        for stare in self.Q:
            if self.stare_initiala in stare and i == 1:
                self.stare_initiala = stare
                i = 0
            if not self.stare_final.isdisjoint(stare):
                sf.add(stare)
        self.stare_final = frozenset(sf)


    def reprezentareGraficaAFD(AFD):
        dot = Digraph(graph_attr={'rankdir':'LR','filename' : 'Automaton finit determinist','label': 'Automaton finit determinist'})
        dot.node('',shape = 'point')
        for stare in AFD.Q:
            if stare in AFD.stare_final:
                stare = formatareFrozenset(stare)
                dot.node(stare,shape = 'doublecircle')
            else:
                stare = formatareFrozenset(stare)
                dot.node(stare,shape = 'oval')
        stare = formatareFrozenset(AFD.stare_initiala)
        dot.edge('', stare)

        for stare in AFD.relatii:
            R= {}
            for litera, stare_urm in AFD.relatii.get(stare,{}).items():

                if stare_urm not in R:
                    R[stare_urm] = []

                R[stare_urm].append(litera)

            for stare_urm,litera in R.items():

                si = formatareFrozenset(stare)
                sf = formatareFrozenset(stare_urm)
                dot.edge(si, sf, label = str(litera))

        dot.render('output', format='png', view=True)