import itertools

# Definiamo le 31 funzioni di Propp con un nome sintetico e una breve descrizione
# Fonte: Adattamento da varie risorse sulla morfologia della fiaba di Propp
FUNZIONI_PROPP = {
    "F1": "Allontanamento (Un membro della famiglia si allontana)",
    "F2": "Divieto (All'eroe è imposto un divieto)",
    "F3": "Infrazione (Il divieto è infranto)",
    "F4": "Investigazione (L'antagonista tenta una ricognizione)",
    "F5": "Delazione (L'antagonista riceve informazioni sulla vittima)",
    "F6": "Tranello (L'antagonista tenta di ingannare la vittima)",
    "F7": "Connivenza (La vittima cade nell'inganno)",
    "F8": "Danneggiamento/Mancanza (L'antagonista danneggia o causa una mancanza)",
    "F9": "Mediazione (Il danneggiamento/mancanza è reso noto, l'eroe è sollecitato)",
    "F10": "Consenso dell'Eroe (L'eroe accetta di reagire)",
    "F11": "Partenza dell'Eroe (L'eroe lascia la casa)",
    "F12": "Messa alla Prova (L'eroe è messo alla prova dal donatore)",
    "F13": "Reazione dell'Eroe (L'eroe reagisce alle azioni del donatore)",
    "F14": "Conseguimento Mezzo Magico (L'eroe ottiene un mezzo magico)",
    "F15": "Trasferimento (L'eroe è trasferito vicino all'oggetto della ricerca)",
    "F16": "Lotta (L'eroe e l'antagonista si scontrano)",
    "F17": "Marchiatura (All'eroe è impresso un marchio)",
    "F18": "Vittoria (L'antagonista è sconfitto)",
    "F19": "Rimozione Danno/Mancanza (Il danno/mancanza iniziale è rimosso)",
    "F20": "Ritorno dell'Eroe (L'eroe ritorna)",
    "F21": "Persecuzione (L'eroe è perseguitato)",
    "F22": "Salvataggio (L'eroe è salvato dalla persecuzione)",
    "F23": "Arrivo in Incognito (L'eroe arriva non riconosciuto)",
    "F24": "Pretese Falso Eroe (Un falso eroe avanza pretese)",
    "F25": "Compito Difficile (All'eroe è proposto un compito difficile)",
    "F26": "Adempimento Compito (Il compito è portato a termine)",
    "F27": "Riconoscimento (L'eroe è riconosciuto)",
    "F28": "Smascheramento (Il falso eroe o l'antagonista è smascherato)",
    "F29": "Trasfigurazione (All'eroe è data una nuova apparenza)",
    "F30": "Punizione (L'antagonista è punito)",
    "F31": "Nozze/Ricompensa (L'eroe si sposa o è ricompensato)"
}

def stampa_funzione(codice_funzione):
    """Restituisce la descrizione completa di una funzione dato il suo codice."""
    return FUNZIONI_PROPP.get(codice_funzione, "Funzione sconosciuta")

def genera_permutazioni_funzioni(lista_codici_funzioni):
    """
    Genera tutte le possibili sequenze ordinate (permutazioni)
    di un dato sottoinsieme di funzioni di Propp.
    L'ordine conta.
    """
    if not all(codice in FUNZIONI_PROPP for codice in lista_codici_funzioni):
        raise ValueError("Uno o più codici funzione non sono validi.")
    
    permutazioni = list(itertools.permutations(lista_codici_funzioni))
    
    trame_generate = []
    for p in permutazioni:
        trama = [stampa_funzione(codice) for codice in p]
        trame_generate.append(" -> ".join(trama))
    return trame_generate

def genera_combinazioni_funzioni(lista_codici_funzioni_disponibili, numero_funzioni_da_scegliere):
    """
    Genera tutti i possibili sottoinsiemi non ordinati (combinazioni)
    di funzioni di Propp da una lista più ampia.
    L'ordine NON conta.
    """
    if not all(codice in FUNZIONI_PROPP for codice in lista_codici_funzioni_disponibili):
        raise ValueError("Uno o più codici funzione nella lista dei disponibili non sono validi.")
    if numero_funzioni_da_scegliere > len(lista_codici_funzioni_disponibili):
        raise ValueError("Il numero di funzioni da scegliere non può essere maggiore delle funzioni disponibili.")

    combinazioni = list(itertools.combinations(lista_codici_funzioni_disponibili, numero_funzioni_da_scegliere))
    
    sottoinsiemi_generati = []
    for c in combinazioni:
        sottoinsieme = sorted([stampa_funzione(codice) for codice in c]) # Ordiniamo per coerenza di visualizzazione
        sottoinsiemi_generati.append(", ".join(sottoinsieme))
    return sottoinsiemi_generati

# --- Esempio di Utilizzo ---

if __name__ == "__main__":
    print("--- Esempio di Generatore di Varianti Narrative (Funzioni di Propp) ---")

    # 1. Permutazioni: Creiamo storie con un piccolo set di funzioni dove l'ordine conta.
    # Usiamo i nomi sintetici del suo esempio per le funzioni chiave:
    # F1: Allontanamento, F2: Divieto, F3: Infrazione, F8: Mancanza, 
    # F11: Partenza, F14: Dono magico, F16: Lotta, F18: Vittoria, F31: Ricompensa
    
    # Esempio con 3 funzioni chiave dove l'ordine è importante
    funzioni_per_permutazioni_esempio = ["F11", "F16", "F18"] # Partenza, Lotta, Vittoria
    print(f"\n--- Permutazioni di {len(funzioni_per_permutazioni_esempio)} funzioni ({[stampa_funzione(f) for f in funzioni_per_permutazioni_esempio]}) ---")
    try:
        trame_permutate = genera_permutazioni_funzioni(funzioni_per_permutazioni_esempio)
        print(f"Numero di trame possibili (permutazioni): {len(trame_permutate)}")
        for i, trama in enumerate(trame_permutate):
            print(f"Trama {i+1}: {trama}")
        if not trame_permutate:
            print("Nessuna trama generata (controllare input).")
    except ValueError as e:
        print(f"Errore: {e}")

    # Esempio con un numero maggiore di funzioni (ATTENZIONE: n! cresce molto velocemente)
    # Se si usano 8 funzioni, 8! = 40,320. Stampare tutto potrebbe essere eccessivo.
    # Qui ne usiamo 4 per dimostrazione.
    funzioni_per_permutazioni_ridotte = ["F8", "F11", "F14", "F16"] # Mancanza, Partenza, Dono, Lotta
    print(f"\n--- Permutazioni di {len(funzioni_per_permutazioni_ridotte)} funzioni ({[stampa_funzione(f) for f in funzioni_per_permutazioni_ridotte]}) ---")
    try:
        trame_permutate_ridotte = genera_permutazioni_funzioni(funzioni_per_permutazioni_ridotte)
        print(f"Numero di trame possibili (permutazioni): {len(trame_permutate_ridotte)}")
        # Stampiamo solo le prime 5 per brevità
        for i, trama in enumerate(trame_permutate_ridotte[:5]):
            print(f"Trama {i+1}: {trama}")
        if len(trame_permutate_ridotte) > 5:
            print("... e altre.")
        if not trame_permutate_ridotte:
            print("Nessuna trama generata.")
            
    except ValueError as e:
        print(f"Errore: {e}")

    # 2. Combinazioni: Selezioniamo un sottoinsieme di funzioni da un set più ampio, l'ordine non conta.
    # Supponiamo di voler scegliere 3 funzioni da un set di 5 funzioni disponibili.
    funzioni_disponibili_esempio = ["F1", "F2", "F3", "F8", "F11"]
    numero_da_scegliere = 3
    print(f"\n--- Combinazioni: Scegliere {numero_da_scegliere} funzioni da un set di {len(funzioni_disponibili_esempio)} ({[stampa_funzione(f) for f in funzioni_disponibili_esempio]}) ---")
    try:
        sottoinsiemi_combinati = genera_combinazioni_funzioni(funzioni_disponibili_esempio, numero_da_scegliere)
        print(f"Numero di sottoinsiemi possibili (combinazioni): {len(sottoinsiemi_combinati)}")
        for i, sottoinsieme in enumerate(sottoinsiemi_combinati):
            print(f"Sottoinsieme {i+1}: [{sottoinsieme}]")
        if not sottoinsiemi_combinati:
            print("Nessun sottoinsieme generato.")
    except ValueError as e:
        print(f"Errore: {e}")

    # Esempio più grande: Scegliere 7 funzioni dalle 31 totali (C(31,7))
    # Questo genererebbe un numero molto grande di combinazioni (2,629,575 secondo la sua formula C(31,7) = 2.629.575, non 62 milioni), 
    # quindi non le stamperemo tutte.
    # Calcoliamo solo il numero per dimostrazione.
    tutte_le_funzioni_codici = list(FUNZIONI_PROPP.keys())
    numero_da_scegliere_grande = 7
    
    print(f"\n--- Combinazioni: Scegliere {numero_da_scegliere_grande} funzioni dalle {len(tutte_le_funzioni_codici)} totali ---")
    try:
        # Calcoliamo il numero di combinazioni senza generarle tutte per evitare problemi di memoria/tempo
        num_combinazioni_grandi = len(list(itertools.combinations(tutte_le_funzioni_codici, numero_da_scegliere_grande)))
        print(f"Numero teorico di sottoinsiemi possibili (combinazioni) C({len(tutte_le_funzioni_codici)}, {numero_da_scegliere_grande}): {num_combinazioni_grandi:,}") # Formattato con separatore migliaia
        print("(La generazione e stampa di tutte queste combinazioni richiederebbe molto tempo e memoria).")
    except ValueError as e:
        print(f"Errore: {e}")
        
    print("\n--- Fine Esempio ---")

