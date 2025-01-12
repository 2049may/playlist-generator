from ListeChainee import ListeChainee

class Pile() :

    def __init__(self):
        self.contenu = ListeChainee()

    def empiler(self, val) :
        self.contenu.ajouter_fin(val)
    
    def depiler(self) :
        val = self.get_sommet()
        self.contenu.supprimer_fin()
        return val
    
    def get_sommet(self) :
        return self.contenu.get_dernier_maillon()

    def afficher(self) :
        self.contenu.afficher_liste()

if __name__ == "__main__" :
    p = Pile()
    p.depiler()
    p.afficher()
    p.empiler(2)
    p.afficher()
    p.empiler(6)
    p.afficher()
    # p.depiler()
    p.afficher()
    p.empiler(9)
    p.empiler(6)
    p.empiler(181)
    p.afficher()
    print(p.depiler())
    p.afficher()
