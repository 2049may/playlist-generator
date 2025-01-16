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

    def recherche(self, valeur, dict=False):
        '''recherche une valeur dans l'arbre et renvoie le noeud correspondant'''
        print(f"Searching for {valeur} in node with value {self.valeur}")

        if dict:
            if self.valeur['name'] == valeur:
                print(f"Noeud trouvé : {self.valeur}")
                return self
            if self.gauche:
                result = self.gauche.recherche(valeur, True)
                if result:
                    return result
            if self.droit:
                return self.droit.recherche(valeur, True)
        else:
            if self.valeur == valeur:
                print(f"Noeud trouvé : {self.valeur}")
                return self
            if self.gauche:
                result = self.gauche.recherche(valeur)
                if result:
                    return result
            if self.droit:
                return self.droit.recherche(valeur)
        # print(f"Node with value {valeur} not found")
        return None
    
    def supprimer(self, valeur):
        '''supprime un noeud de l'arbre et le remplace par la feuille la plus à droite'''
        noeud = self.recherche(valeur, dict=True)
        if noeud is not None:
            parent = self.parent(valeur)
            if parent:
                if noeud == parent.gauche:
                    parent.gauche = None
                else:
                    parent.droit = None
        else:
            print(f"Nooeud {valeur} non trouvé.")
    
    def parent(self, valeur) :
        '''renvoie le parent d'un noeud'''
        if self.droit is None and self.gauche is None :
            return None
        
        if self.gauche is not None and self.gauche.valeur == valeur or self.droit is not None and self.droit.valeur == valeur :
            return self
        else :
            fd = None
            fg = None
            if self.droit :
                fd = self.droit.parent(valeur)

            if self.gauche :
                fg = self.gauche.parent(valeur)
            
            return fd or fg
        
    def recherche_feuille(self) :
        '''
        renvoie la feuille la plus à droite de l'arbre
        '''
        if self is None :
            return -1
        if self.gauche is None and self.droit is None :
            return self
        if self.droit :
            return self.droit.recherche_feuille()
        if self.gauche :
            return self.gauche.recherche_feuille()
    
            


    

if __name__ == "__main__" :

    racine = Noeud("Racine")
    n1 = Noeud(1)
    n2 = Noeud(2)
    n3 = Noeud(3)
    n4 = Noeud(4)
    n5 = Noeud(5)
    n5.gauche = Noeud(6)
    racine.gauche = n1
    racine.droit = n2
    n1.droit = n3
    n2.gauche = n4
    n4.droit = n5

    ar2 = Noeud()

    # print(racine)
    # print(racine.hauteur())
    # print(ar2)
    # print(ar2.est_feuille())
    # print(ar2.est_vide())
    print(racine.recherche(3))
    print(racine.parent(5))
    print(racine.recherche_feuille())

    racine2 = Noeud({'name': 'Racine', 'uri': 'http://www.racine.com'})
    n1 = Noeud({'name': '1', 'uri': 'http://www.1.com'})
    n2 = Noeud({'name': '2', 'uri': 'http://www.2.com'})
    n3 = Noeud({'name': '3', 'uri': 'http://www.3.com'})
    n4 = Noeud({'name': 'Tabber', 'uri': 'spotify:artist:4CYjITN8Au3K5CWFeex7fU'})

    racine2.gauche = n1
    racine2.droit = n2
    n1.gauche = n3
    n3.droit = n4
    
    print(racine2.recherche('2', True))
    print(racine2.recherche('Tabber', True))