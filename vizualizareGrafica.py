from graphviz import Digraph
from automaton.AutomatonFinitDeterminist import AFD


def reprezentareGraficaAFD(AFD):
    dot = Digraph(comment='AUTOMATON FINIT DETERMINIST')
    dot.node('',shape = 'point')
    for stare in AFD.Q:
        dot.node(str(stare),shape = 'circle')

    dot.render('output', format='png', view=True)

'''
    for stare in AFD.relatii:
        for litera in AFD.relatii.get(stare,{}):
            for stare_urm in AFD.relatii.get(stare,{}).get(litera,None):
                dot.edge(str(stare),str(stare_urm))
'''
