from automaton.AutomatonFinitNedeterminist import regexNFA


REGEX = input("Functia REGEX: ")
CUVANT = input("Cuvant: ")



A = regexNFA(REGEX)
print(A.accepta(CUVANT))
#print(regexNFA("(a|b)*c" ))




