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
    # file.afficher()
    # print(file.est_vide())
    file.enfiler(1)
    file.enfiler(2)
    file.enfiler(3)
    file.afficher()
    print(file.est_vide())
    # print(file.est_vide())
    print("elt suppr : ", file.defiler())
    file.afficher()