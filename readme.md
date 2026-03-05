Acest proiect converteste expresii regulate (REGEX) in automatoane finitie deterministe.

Proces:
1.Proiectul primeste de la tastatura o functie REGEX si un cuvant.
2.Transforma functia REGEX intr-un automaton finit nedetermminist folosind algoritmul Shunting Yard si Regulile lui Thompson pentru simbolurile: [. , | , * , ? , +]. Printeaza reprezentarea grafica a AFN-ului.
3.Conversia AFN-ului intr-un automaton finit determinist utilizand algoritmii de epsilon closure si Breadth First Search. Printarea reprezentarii grafice a AFD-ului.
4. Minimizarea AFD-ului utilizand algorimtul lui Hopcroft. Afisarea reprezentarii grafice a AFD- ului minimizat.
5. Verifica cuvantul. Returneaza True daca este acceptat si False in caz contrar.

Instalare:

```bash
 pip install -r requirements.txt
 python main.py

