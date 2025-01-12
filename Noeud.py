class Noeud() :
    
    def __init__(self, valeur=None, gauche=None, droit=None):
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit
    
    def __str__(self):
        return str(self.valeur)
    
    def est_feuille(self) :
        return self.gauche is None and self.droit is None
    