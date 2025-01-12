class Noeud() :
    '''Arbre binaire'''
    
    def __init__(self, valeur=None, gauche=None, droit=None):
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit

    def est_feuille(self) :
        '''Renvoie true si le noeud est une feuille'''
        return self.gauche is None and self.droit is None
    
    def est_vide(self) :
        '''retourne true si l'arbre est vide'''
        return self.valeur is None
    
    def __str__(self):
        return str(self.valeur)
    
    def hauteur(self) :
        '''renvoie la hauteur de l'arbre (la racine est considérée comme une hauteur de 1)'''
        if self is None :
            return -1
        
        h1 = 0
        h2 = 0

        if self.gauche :
            h1 = self.gauche.hauteur()
        if self.droit :
            h2 = self.droit.hauteur()
        return 1+max(h1, h2)
    
            


    

if __name__ == "__main__" :

    racine = Noeud("Racine")
    n1 = Noeud(1)
    n2 = Noeud(2)
    n3 = Noeud(3)
    racine.gauche = n1
    racine.droit = n2
    n1.droit = n3

    ar2 = Noeud()

    print(racine)
    print(racine.hauteur())
    print(ar2)
    print(ar2.est_feuille())
    print(ar2.est_vide())
