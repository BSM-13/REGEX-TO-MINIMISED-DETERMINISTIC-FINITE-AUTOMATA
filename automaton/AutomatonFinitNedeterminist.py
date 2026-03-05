import queue
from inspect import stack
from queue import Queue
from graphviz import Digraph

from automaton.AutomatonFinitDeterminist import AFD,_frozenset


class AFN:
    def __init__(self, Q, alfabet, relatii, stare_initiala, stare_final):
        self.Q = Q  # setul starlor ce alcatuiesc automatonul
        self.alfabet = alfabet  # alfabetul recunoscut de automaton
        self.relatii = relatii  # dictionar cu caile automatonului
        self.stare_initiala = stare_initiala  # starea de unde incepe automatonul
        self.stare_final = set(stare_final) if isinstance(stare_final, (set, list)) else {stare_final}  # starea in care trebuie sa se termine calculul pentru ca limbajul sa fie regulat

    def accepta(self, cuvant, stare_actuala = None):
        stare = self.stare_initiala if stare_actuala is None else stare_actuala
        if cuvant == "":
            return stare in self.stare_final

        c = cuvant[0]
        if c not in self.alfabet: return False

        stari = set(self.epsilon_closure(stare))

        stari.update(self.relatii.get(stare,{}).get(c,set()))
        for s in stari:
            if self.accepta(cuvant[1:],s):
                return True
        return False

    '''
        Functia accepta verifica daca un cuvant este acceptat de automatonul finit nedeterminist.
        Primeste cuvantul si starea actuala pe care o verifica contra cuvantului, intrucat folosim recursivitate)
        Returnam true daca este acceptat si false in cazul opus.
    '''



    def afiseaza(self):
        for stare in self.relatii:
            for k in self.relatii[stare]:
                for stare_Urm in self.relatii[stare][k]:
                    print(f'{stare}--{k}->{stare_Urm}')



    def epsilon_closure(self,stare):

        l = [stare]
        q = queue.Queue()
        q.put(stare)

        while not q.empty():
            stare_actuala = q.get()
            if "eps" in self.relatii.get(stare_actuala,{}):
                for stare_urm in self.relatii.get(stare_actuala,{}).get("eps"):
                    if stare_urm not in l:
                        l.append(stare_urm)
                        q.put(stare_urm)
        return l
    '''
    Functia epislon_closure primeste o stare si returneaza o lista cu starile in care putem ajunge folosind
    doar epsilon

    Epsilon nu face parte din alfabetul unui automaton.
    '''


    def conversie(self) -> AFD:


        stare_start = frozenset(self.epsilon_closure(self.stare_initiala))
        q = [stare_start]
        stari_DFA = {stare_start}
        relatii_DFA = {}
        stari_finale = set()



        while q:
            stare_actuala = q.pop()
            if any(s in self.stare_final for s in stare_actuala):
                stari_finale.add(stare_actuala)

            dict_relatii = {}


            for litera in self.alfabet:
                set_temp1 = set()
                set_nou = set()
                for s in stare_actuala:
                    set_nou.update(self.relatii.get(s, {}).get(litera, set()))
                for s in set_nou:
                    set_temp1.update(self.epsilon_closure(s))
                set_nou.update(set_temp1)
                set_nou = frozenset(set_nou)
                if set_nou:
                    dict_relatii.update({litera: set_nou})
                    if set_nou not in stari_DFA:
                        stari_DFA.add(set_nou)
                        q.append(set_nou)
            relatii_DFA.update({stare_actuala: dict_relatii})

        existanull = 0
        null = frozenset(["null"])

        for stare in relatii_DFA:
            for l in self.alfabet:
                if l not in relatii_DFA[stare].keys():
                    relatii_DFA[stare][l] = null
                    existanull=1

        if existanull==1:
            stari_DFA.add(null)
            relatii_DFA[null] ={l:null for l in self.alfabet if l != 'eps'}

        return AFD(stari_DFA,self.alfabet, relatii_DFA,stare_start,stari_finale)

    '''
    Functia conversie returneaza un obiect de tip AFD (automaton finit determinist).
    Punem intr-o lista starea initiala a AFN - ului si toate starile in care putem ajunge folosind doar epsilon( folosim algoritmul de epsilon_closure).
    Cream dictionarul relatiilor AFD-ului parcurgem in fucntie de litera starile in care putem ajunge plecand din fiecare stare (BFS).
    Noua stare (lista de stari) care contine starea de start a AFN-ului devine starea de start a AFD - uui.
    Orice stare care contine cel putin o stare finala a AFN-ului devine o stare de final a AFD-ului.
    '''


    def reprezentareGraficaAFN(AFN):
        dot = Digraph(graph_attr={'rankdir':'LR','filename' : 'Automaton finit nedeterminist','label': 'Automaton finit nedeterminist'})
        dot.node('',shape = 'point')
        for stare in AFN.Q:
            if stare in AFN.stare_final:
                dot.node(str(_frozenset([stare])),shape = 'doublecircle')
            else:
                dot.node(str(_frozenset([stare])),shape = 'oval')
        dot.edge('', str(_frozenset([AFN.stare_initiala])))

        for stare in AFN.relatii:
            R= {}
            for litera, stari_urm in AFN.relatii.get(stare,{}).items():

                for destinatie in stari_urm:

                    if destinatie not in R:
                        R[destinatie] = []

                    R[destinatie].append(litera)
            print(R)
            for stare_urm,litera in R.items():
                dot.edge(str(_frozenset([stare])), str(_frozenset([stare_urm])), label = str(R[stare_urm]))

        dot.render('output', format='png', view=True)

    '''
    Folosim graphviz pentru a reprezenta grafic AFN-ul.
    Primim un AFN drept argument.
    Cream cate un nod pentru fiecare stare.
    Parcurgem dictionarul de relatii si desenam muchiile.
    
    '''




def shuntingYard(s):
    stack = []
    rez = []


    operatori = {
        '('  : 0,
        ')' : 0,
        '|' : 1,
        '.' : 2,
        '*' : 3,
        '?' : 3,
        '+' : 3
    }


    while s:
        if not s:
            stack.append(rez)
            return s

        c = s.pop(0)
        if c in operatori and c not in ['(',')']:
            while stack and operatori[stack[-1]] >= operatori[c] and stack[-1] !='(':
                rez.append(stack.pop())
            stack.append(c)

        elif c == '(':
            stack.append(c)
        elif c == ')':
            x = stack.pop()
            while x != '(' and stack:
                rez.append(x)
                x = stack.pop()

            if not stack and x !='(':
                print("Ordine eronata a parantezelor")
                return
        else:
            rez.append(c)
    while stack:
        rez.append(stack.pop())
    return rez

'''
Folosim algorimtul de Shunting Yard pentru a lista post-fixata, pornind de la un string cu functia regex.
Ne folosim de un dictionar ce contine toti operatorii cu un sistem de prioritati.
'''


stiva_AFN = []
id_stare = 0


def initializare_stari():
    global id_stare
    id_stare +=1
    return id_stare

'''
Folosim functia de initializare stari pentru genera o noua stare de fiecare data cand avem nevoie.
'''

def Thompsonlitera(l):
    qi = str(initializare_stari())
    qf = str(initializare_stari())
    A = AFN([qi,qf],[l],{qi:{l:[qf]}},qi,{qf})
    return A


def Thompsonpunct(stivaAFN):
    af = stivaAFN.pop()
    ai = stivaAFN.pop()

    Q = af.Q + ai.Q

    alfabet = list(set(af.alfabet + ai.alfabet))

    relatii_final = ai.relatii | af.relatii


    for sf in ai.stare_final:
        if sf not in relatii_final:
            relatii_final[sf] = {}
        relatii_final[sf].setdefault('eps',[])
        relatii_final[sf]['eps'].append(af.stare_initiala)

    A = AFN(Q,alfabet,relatii_final,ai.stare_initiala,af.stare_final)

    return A


def Thompsonreuniune(stivaAFN):
    stare_initiala = str(initializare_stari())
    stare_finala = str(initializare_stari())

    af = stivaAFN.pop()
    ai = stivaAFN.pop()

    Q = ai.Q + af.Q
    Q.append(stare_initiala)
    Q.append(stare_finala)

    alfabet = list(set(af.alfabet + ai.alfabet))

    relatii_final = ai.relatii | af.relatii

    relatii_final[stare_initiala] = {}
    relatii_final[stare_initiala].setdefault('eps',[])
    relatii_final[stare_initiala]['eps'].append(af.stare_initiala)
    relatii_final[stare_initiala]['eps'].append(ai.stare_initiala)

    for sf in ai.stare_final:
        if sf not in relatii_final:
            relatii_final[sf] = {}
        relatii_final[sf].setdefault('eps',[])
        relatii_final[sf]['eps'].append(stare_finala)

    for sf in af.stare_final:
        if sf not in relatii_final:
            relatii_final[sf] = {}
        relatii_final[sf].setdefault('eps',[])
        relatii_final[sf]['eps'].append(stare_finala)

    A = AFN(Q,alfabet,relatii_final,stare_initiala,stare_finala)
    return A



def Thompsonrepetare(stivaAFN):
    stare_initiala = str(initializare_stari())
    stare_finala = str(initializare_stari())
    a = stivaAFN.pop()

    Q = a.Q.copy()
    Q.append(stare_initiala)
    Q.append(stare_finala)

    alfabet = a.alfabet

    relatii_final = {}

    for stari,relatii in a.relatii.items():
        relatii_final[stari] = {}
        for litera, sf in relatii.items():
            relatii_final[stari][litera] = sf.copy()



    relatii_final[stare_initiala] = {}
    relatii_final[stare_initiala].setdefault('eps',[])
    relatii_final[stare_initiala]['eps'].append(stare_finala)
    relatii_final[stare_initiala]['eps'].append(a.stare_initiala)

    for sf in a.stare_final:
        if sf not in relatii_final:
            relatii_final[sf] = {}
        relatii_final[sf].setdefault('eps',[])
        relatii_final[sf]['eps'].append(stare_finala)
        relatii_final[sf]['eps'].append(a.stare_initiala)


    A = AFN(Q,alfabet,relatii_final,stare_initiala,stare_finala)
    return A


def Thompsonplus(stivaAFN):
    stare_initiala = str(initializare_stari())
    stare_finala = str(initializare_stari())
    a = stivaAFN.pop()

    Q = a.Q.copy()
    Q.append(stare_initiala)
    Q.append(stare_finala)

    alfabet = a.alfabet

    relatii_final = {}

    for stari,relatii in a.relatii.items():
        relatii_final[stari] = {}
        for litera, sf in relatii.items():
            relatii_final[stari][litera] = sf.copy()



    relatii_final[stare_initiala] = {}
    relatii_final[stare_initiala].setdefault('eps',[])
    relatii_final[stare_initiala]['eps'].append(a.stare_initiala)

    for sf in a.stare_final:
        if sf not in relatii_final:
            relatii_final[sf] = {}
        relatii_final[sf].setdefault('eps',[])
        relatii_final[sf]['eps'].append(stare_finala)
        relatii_final[sf]['eps'].append(a.stare_initiala)


    A = AFN(Q,alfabet,relatii_final,stare_initiala,stare_finala)
    return A

def Thompsonintrebare(stivaAFN):
    stare_initiala = str(initializare_stari())
    stare_finala = str(initializare_stari())
    a = stivaAFN.pop()

    Q = a.Q.copy()
    Q.append(stare_initiala)
    Q.append(stare_finala)

    alfabet = a.alfabet

    relatii_final = {}

    for stari,relatii in a.relatii.items():
        relatii_final[stari] = {}
        for litera, sf in relatii.items():
            relatii_final[stari][litera] = sf.copy()



    relatii_final[stare_initiala] = {}
    relatii_final[stare_initiala].setdefault('eps',[])
    relatii_final[stare_initiala]['eps'].append(stare_finala)
    relatii_final[stare_initiala]['eps'].append(a.stare_initiala)

    for sf in a.stare_final:
        if sf not in relatii_final:
            relatii_final[sf] = {}
        relatii_final[sf].setdefault('eps',[])
        relatii_final[sf]['eps'].append(stare_finala)


    A = AFN(Q,alfabet,relatii_final,stare_initiala,stare_finala)
    return A



'''
Functiile Thompson se folosesc pentru a parcurge functia REGEX utilizand regulile Thopsom
'''

def regexNFA(s):


    s = list(s)
    rez = []
    for i in range(len(s)-1):
        if s[i] not in ['(','|','.'] and s[i+1] not in ['*',')','|','?','+']:
            rez.append(s[i])
            rez.append('.')
        else: rez.append(s[i])
    rez.append(s[i+1])
    sY = shuntingYard(rez)

    stiva_AFN = []
    for caracter in sY:
        if caracter == '.':
            A = Thompsonpunct(stiva_AFN)
            stiva_AFN.append(A)
        elif caracter == '|':
            A = Thompsonreuniune(stiva_AFN)
            stiva_AFN.append(A)
        elif caracter == '*':
            A = Thompsonrepetare(stiva_AFN)
            stiva_AFN.append(A)
        elif caracter == '+':
            A = Thompsonplus(stiva_AFN)
            stiva_AFN.append(A)
        elif caracter == '?':
            A = Thompsonintrebare(stiva_AFN)
            stiva_AFN.append(A)
        else:
            A = Thompsonlitera(caracter)
            stiva_AFN.append(A)

    A = stiva_AFN.pop()
    #A.afiseaza()
    A.reprezentareGraficaAFN()
    Adeterminist = A.conversie()
    Adeterminist.reprezentareGraficaAFD()
    Adeterminist.reconstruireAFD()
    Adeterminist.reprezentareGraficaAFD()
    return Adeterminist



'''
Functia REGEXNFA primeste ca argument un string ce contine functia regex.
O parcurgem. Introducem operatorul . acolo unde este nevoie.
Ii aplicam algoritmul de Shunting Yard.
Ii aplicam regulile Thompson pentru a o converti intr-un automaton finit nedeterminist.
Reprezentam grafic AFN-ul.
Il convertim intr-un AFD.
Reprezentam grafic AFD-ul.
Il minimizam daca este posibil folosind algoritmul lui Hopcroft.
Reprezentam grafic AFD-ul minimizat.
'''