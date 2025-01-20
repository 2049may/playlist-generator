import ListeChainee

class File() :

    def __init__(self):
        self.contenu = ListeChainee.ListeChainee()
    
    def est_vide(self) :
        return self.contenu.est_vide()

    def enfiler(self, valeur) :
        self.contenu.ajouter_debut(valeur)
    
    def defiler(self) :
        val = self.get_tete()
        self.contenu.supprimer_fin()
        return val
    
    def get_tete(self) :
        return self.contenu.get_dernier_maillon()
    
    def afficher(self) :
        self.contenu.afficher_liste()
    
    

if __name__ == "__main__" :

    file = File()
    file.enfiler(1)
    file.enfiler(2)
    file.enfiler(3)
    print("file après enfilement de 1, 2et 3:")
    file.afficher()

    print("defilement de la file:")
    print(file.defiler())
    print("file apres défilement:")
    file.afficher()
