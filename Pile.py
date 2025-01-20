from ListeChainee import ListeChainee

class Pile() :

    def __init__(self):
        self.contenu = ListeChainee()

    def empiler(self, val) :
        self.contenu.ajouter_debut(val)
    
    def depiler(self) :
        val = self.get_sommet()
        self.contenu.supprimer_debut()
        return val
    
    def est_vide(self) :
        return self.contenu.est_vide()
    
    def get_sommet(self) :
        return self.contenu.get_tete()

    def afficher(self) :
        self.contenu.afficher_liste()

    def renverser(self) :
        p = Pile()
        while not self.est_vide() :
            p.empiler(self.depiler())
        self.contenu = p.contenu


if __name__ == "__main__":
    p = Pile()
    
    print("empilement de 1, 2 et 3")
    p.empiler(1)
    p.empiler(2)
    p.empiler(3)
    p.afficher() 
    
    print("\ndepilement")
    print(p.depiler())  
    p.afficher() 
    
    print(p.depiler()) 
    p.afficher() 
    
    print(p.depiler()) 
    p.afficher()  
    
    print("\npile vide ?")
    print(p.est_vide())  
    
    print("\nempilement de 4, 5, 6")
    p.empiler(4)
    p.empiler(5)
    p.empiler(6)
    p.afficher() 
    
    print("\nrenversement de la pile")
    p.renverser()
    p.afficher() 


    