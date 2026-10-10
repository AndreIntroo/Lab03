from operator import attrgetter
class Prestito:
    def __init__(self, codp, data, cods, cognome_a):
        self.codp = codp
        self.data = data
        self.cods = cods
        self.cognome_a = cognome_a
    def __str__(self):
        return f"codice prestito:{self.codp} data: {self.data} codice strumento:{self.cods} cognome allievo effettuante prestito:{self.cognome_a}"
class Strumento:
    def __init__(self,codice,tipo, marca, anno_acq, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.__anno_acq = int(anno_acq)
        self.__valore = float(valore)
    #scrivo i getter e i setter per tutti gli attrivuti che ho messo privati
    @property
    def anno_acq (self):
        return self.__anno_acq
    @property
    def valore(self):
        return self.__valore
    @anno_acq.setter
    def anno_acq(self, anno_acq):
        anno_num = int(anno_acq)
        if anno_num>2026:
            raise Exception("ERRORE: non puoi inserire un anno del futuro per uno strumento")
        self.__anno_acq = anno_num
    @valore.setter
    def valore(self,valore):
        valore_num = float(valore)
        if valore_num < 0:
            raise Exception("ERRORE:non puoi inserire un valore negativo di un oggetto.")
        self.__valore = valore_num
    def __str__(self):
        return f"codice strumento:{self.codice}, tipo:{self.tipo} , marca: {self.marca}, anno: {self.anno_acq} valore(euro): {self.valore:.2f}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile,):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = {}
        self.prestiti = {}
    #scrivo i getter e i setter per gli atrributi che ho messo privati


    def __str__(self):
        return f"{self.nome} {self.responsabile} "





    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, 'r', encoding ='utf_8') as file:
                for line in file:
                    campi = line.strip().split(',')
                    new_strumento = Strumento(campi[0],campi[1], campi[2], campi[3],float(campi[4]))
                    self.strumenti[campi[0]] = new_strumento
        except FileNotFoundError:
            print("non è stato trovato nessun file con quel nome")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        lista_identificativi = []
        if  not self.strumenti:
            identificativo_numero = 1
        else:
            for k in self.strumenti.keys():
                lista_identificativi.append(int(k[1:]))
            identificativo_numero =  1+ max(lista_identificativi)
        codice = f"S{identificativo_numero}"
        new_strumento = Strumento(codice, tipo,marca, anno_acquisto, valore)
        self.strumenti[codice] = new_strumento
        return new_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        lista = list(self.strumenti.values())
        return sorted(lista, key=attrgetter("marca"))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception(f"il codice {id_strumento} non è presente nella lista degli identificativi degli strumenti")

        for p in self.prestiti.values():
            if p.cods== id_strumento:
                raise Exception(f"è gia stato effettuato un prestito dello strumento {id_strumento}")
        if not self.prestiti:
            id_numero= 1
        else:
            lista_id = []
            for k in self.prestiti.keys():
                lista_id.append(int(k[1:]))
            id_numero = 1+ max(lista_id)
        codp = f"P{id_numero}"
        new_prestito = Prestito(codp, data,id_strumento, cognome_allievo)
        self.prestiti[codp] = new_prestito
        return new_prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception(f"errore: non esiste nessun prestito con questo codice")
        del self.prestiti[id_prestito]
