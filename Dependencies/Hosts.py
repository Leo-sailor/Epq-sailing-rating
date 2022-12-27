import csvcode
import General
csv = csvcode.Csvcode()
base = General.General()
class Hosts:
    def makenewsailor(self):
        first =  # TODO put through cleaner function
        sur =  # TODO put through cleaner function
        champ =  # TODO put through cleaner function
        sailno =  # TODO put through cleaner function
        nat = # TODO put through cleaner function
        region =  # TODO put through cleaner function
        sailorid = base.generatesailorid(nat,sailno,first,sur)
        csv.addsailor()
