class MaListe() :

    def __init__(self):
        self.liste = []

    def ajouter(self, elt) :
        self.liste.append(elt);

    def supprimer(self, elt) :
        if len(self.liste)==0 :
            print("La liste est vide")

        if elt in self.liste :
            self.liste.remove(elt)

        else :
            print("L'élément", elt, "n'est pas dans la liste")

    def obtenir(self, index) :
        if len(self.liste)==0 :
            print("La liste est vide")
        if index > len(self.liste) :
            print("L'indice est trop grand")
        else :
            return self.liste[index]
    
    def trouver_indice(self, elt) :
        if elt in self.liste :
            return self.liste.index(elt)
        else :
            return("L'element n'est pas dans la liste")

    def afficher(self) :
        if len(self.liste)==0 :
            print("La liste est vide")
            quit()

        for elt in self.liste :
            print(elt, " ", end="")
        print()

    def taille(self) :
        return len(self.liste)
    
    def inverser(self) :
        self.liste.reverse()

    def vider(self) :
        self.liste.clear()

    def contient(self, elt, cle=None) :
        for item in self.liste:
            if isinstance(item, dict):
                if cle in item and item[cle] == elt:
                    return True
            elif item == elt:
                return True
        return False

    def compter(self, elt, cle=None) :
        cpt=0
        for item in self.liste:
            if isinstance(item, dict):
                if cle in item and item[cle]==elt :
                    cpt+=1
            elif item  == elt :
                cpt += 1
        return cpt
    
    def trier(self, cle=None) :
        if cle :
            self.liste.sort(key=lambda x : x[cle])
        else :
            self.liste.sort()

    
    def trouver_doublons(self, cle=None) :
        vu = set()
        doublons = set()

        for e in self.liste :
            if isinstance(e, dict) :
                if e[cle] in vu :
                    doublons.add(e[cle])
                else :
                    vu.add(e[cle])
            else :
                if e in vu:
                    doublons.add(e)
                else:
                    vu.add(e)
        return doublons
    
    def filtrer_uniques(self, cle=None) :
        vu = set()
        uniques = set()

        for e in self.liste :
            if isinstance(e, dict) :
                if e[cle] not in vu :
                    uniques.add(e[cle])
                    vu.add(e[cle])
                else :
                    uniques.remove(e[cle])
            else :
                if e not in vu:
                    uniques.add(e)
                    vu.add(e)
                else :
                    uniques.remove(e)
        return uniques
    
    def k_plus_grand(self, k=0, cle=None) :
        # à refaire 
        liste_triee = sorted(self.liste, reverse=True)
        if k == 0 :
            return liste_triee[0]
        else :
            return liste_triee[k-1]
    
    def fusionner(self, liste2, cle=None) :
        # prend en paramètre une autre liste triée et fusionne les deux listes en une seule liste triée
        self.liste.extend(liste2.liste)
        self.trier(cle)
    
    def rearranger_pairs_impairs(self, cle=None) :
        # à faire
        pass

    def intercaler(self, liste2, cle=None) :
        # à faire
        pass


li = MaListe()
li.ajouter("cc")
li.ajouter("ee")
li.ajouter("ee")
li.ajouter("dd")
li.ajouter("dd")
# li.afficher()
li.inverser()
# li.afficher()
# print(li.contient("d"))

l2 = MaListe()
l2.ajouter({"age" : 32, "prenom" : "chunchu"})
l2.ajouter({"age" : 30, "prenom" : "hanjoo"})
# l2.ajouter(3)
l2.ajouter({"age" : 32, "prenom" : "woonghee"})

l5 = MaListe()
l5.ajouter({"age" : 34, "prenom" : "geonjae"})
l5.ajouter({"age" : 28, "prenom" : "jungkook"})
# l2.ajouter(2)
# print(l2.contient(80, "age"))
# print(l2.contient('woongee', "prenom"))
# print(l2.contient(6))
# print(l2.compter("hanjoo", "prenom"))
# print(l2.compter(2))
# print(l2.compter(32, "age"))
# l2.afficher()

l3 = MaListe()
l3.ajouter(1)
l3.ajouter(8)
l3.ajouter(1)
l3.ajouter(3)
l3.ajouter(4)
l3.ajouter(6)
l3.ajouter(6)
l3.ajouter(5)

l4 = MaListe()
l4.ajouter(2)
l4.ajouter(7)
l4.ajouter(9)
l4.ajouter(10)
l4.ajouter(11)
l4.ajouter(-7)
# print(l3.contient(7))
# print(l3.compter(6))
# print(l3.compter(1))

# l2.trier("age")
# l2.afficher()
# print(l2.trouver_doublons("age"))
# print(l2.filtrer_uniques("age"))
# print(li.trouver_doublons())
# print(l2.filtrer_uniques("age"))
print(l3.k_plus_grand())
l2.fusionner(l5, "age");
l2.afficher()
