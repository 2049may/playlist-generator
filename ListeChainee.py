class Maillon() :
    '''
    Un maillon est un élément d'une liste chaînée. Il contient une valeur et un pointeur vers le maillon suivant.
    '''

    def __init__(self, valeur=None):
        self.valeur = valeur
        self.suivant = None

class ListeChainee() :

    def __init__(self, tete=None):
        self.tete = tete

    def est_vide(self) :
        '''renvoie True si la liste est vide'''
        return self.tete is None

    def taille(self) :
        '''renvoie la taille de la liste'''
        if self.tete is None :
            return 0
        
        t = 1
        ptr = self.tete
        while ptr.suivant is not None :
            t += 1
            ptr = ptr.suivant
        return t
    
    def get_tete(self) :
        '''renvoie la valeur du premier maillon (la tete)'''
        return self.tete.valeur
    
    def get_dernier_maillon(self) :
        '''renvoie la valeur du dernier maillon'''
        if self.tete is None :
            return None
        
        ptr = self.tete
        while ptr.suivant is not None :
            ptr = ptr.suivant

        return ptr.valeur
    
    def ajouter_debut(self, val) :
        '''ajoute un maillon au début de la liste'''
        m = Maillon(val)
        if self.tete is None :
            self.tete = m
        else :
            ptr = self.tete
            self.tete = m
            self.tete.suivant = ptr
    
    def ajouter_fin(self, val) :
        '''ajoute un maillon de valeur val à la fin de la liste (operation couteuse)'''
        m = Maillon(val)
        if self.tete is None :
            self.tete = m
        else :
            ptr = self.tete
            while ptr.suivant is not None :
                ptr = ptr.suivant
            ptr.suivant = m

    # def inserer(self, val)
    
    def get_maillon_indice(self, i) :
        '''renvoie le maillon à l'indice i'''
        if i >= self.taille() :
            return None
        else :
            if self.tete is not None :
                ptr = self.tete
                for _ in range(i) :
                    ptr = ptr.suivant
                return ptr.valeur


    def supprimer_debut(self) :
        '''supprime la tete de la chaine'''
        if self.tete is not None :
            self.tete = self.tete.suivant

    def supprimer_fin(self) :
        '''supprime le dernier element de la liste'''
        if self.tete is not None :
            if self.tete.suivant is None:
                self.tete = None
            else:
                ptr = self.tete
                ptr2 = ptr.suivant
                while ptr2.suivant is not None :
                    ptr = ptr.suivant
                    ptr2 = ptr.suivant
                ptr.suivant = None
            


    def afficher_liste(self) :
        if self.tete is None :
            print("Aucun élément")
        else :
            ptr = self.tete
            while ptr is not None :
                print(ptr.valeur, " ", end="")
                ptr = ptr.suivant
            print()



if __name__ == "__main__" :

    m1 = Maillon(3)
    m2 = Maillon(4)

    m1.suivant = m2

    liste = ListeChainee(m1)
    liste2 = ListeChainee()

    print("m1 = ", m1.valeur)
    print("m2 = ", m2.valeur)

    print("taille : ", liste.taille())
    print(liste.est_vide())
    print("taille : ", liste2.taille())
    print(liste2.est_vide())
    print(liste.get_dernier_maillon())
    print("--liste 1--")
    liste.afficher_liste()
    liste.ajouter_fin(2)
    liste.afficher_liste()
    liste.ajouter_debut(6)
    liste.afficher_liste()
    liste.supprimer_debut()
    liste.afficher_liste()
    liste.supprimer_fin()
    liste.afficher_liste()
    print(liste.get_maillon_indice(2))

    print()
    print("--liste 2--")
    
    liste2.afficher_liste()
    liste2.ajouter_debut(3)
    liste2.ajouter_debut(3)
    liste2.ajouter_debut(3)
    liste2.afficher_liste()
    liste2.supprimer_fin()
    liste2.ajouter_fin(2)
    liste2.afficher_liste()
    liste2.supprimer_debut()
    liste2.afficher_liste()
    print(liste2.get_maillon_indice(2))
    