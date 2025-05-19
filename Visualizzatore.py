# visualizzatore_propp_sequence.py
# Luigi Usai, Quartucciu, Sardegna, Italy

import graphviz
import textwrap # Per gestire il testo lungo nei nodi

# Le 31 funzioni di Propp (riprese dal tuo file generatore_propp.py)
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
    "F12": "Messa alla Prova (L'eroe è messo alla Prova dal donatore)",
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

def get_propp_function_description(code):
    """Restituisce la descrizione completa di una funzione dato il suo codice."""
    return FUNZIONI_PROPP.get(code, f"Funzione Sconosciuta ({code})")

def create_propp_sequence_visualization(propp_codes_sequence, title="Sequenza Funzioni di Propp"):
    """
    Crea una visualizzazione grafica di una sequenza di funzioni di Propp
    come un diagramma di flusso.

    Args:
        propp_codes_sequence (list): Una lista di stringhe con i codici delle funzioni di Propp (es. ["F11", "F16", "F18"]).
        title (str): Il titolo per il grafico.

    Returns:
        graphviz.Digraph: L'oggetto grafo creato (può essere salvato o renderizzato).
    """
    if not propp_codes_sequence:
        print("La sequenza di funzioni è vuota.")
        return None

    dot = graphviz.Digraph(comment=title)

    # Impostazioni globali per il grafico (opzionale)
    dot.attr(rankdir='LR') # Layout da Sinistra a Destra (Left to Right)
    dot.attr('node', shape='box') # Forma dei nodi come scatole

    previous_node_id = None

    for i, code in enumerate(propp_codes_sequence):
        function_description = get_propp_function_description(code)
        # Avvolgi il testo per evitare nodi troppo larghi
        label = f"{code}\n{textwrap.fill(function_description, width=30)}"
        node_id = f"node_{i}" # ID univoco per ogni nodo

        dot.node(node_id, label)

        if previous_node_id is not None:
            dot.edge(previous_node_id, node_id) # Aggiungi un arco dal nodo precedente a quello attuale

        previous_node_id = node_id

    return dot

# --- Esempio di Utilizzo ---

if __name__ == "__main__":
    # Esempio di una sequenza classica di Propp (semplificata)
    esempio_sequenza = ["F8", "F9", "F10", "F11", "F14", "F16", "F18", "F19", "F31"]

    print(f"Generazione visualizzazione per la sequenza: {esempio_sequenza}")

    try:
        # Crea l'oggetto grafo
        propp_graph = create_propp_sequence_visualization(esempio_sequenza, title="Esempio Sequenza di Propp")

        if propp_graph:
            # Salva il sorgente .dot del grafico
            propp_graph.save("propp_sequence_example.dot")
            print("Sorgente del grafico salvato come propp_sequence_example.dot")

            # Renderizza il grafico in un file immagine (es. PNG)
            # Assicurati che il software Graphviz sia installato e accessibile nel PATH del sistema
            propp_graph.render("propp_sequence_example", view=True, cleanup=True, format='png')
            print("Grafico renderizzato e salvato come propp_sequence_example.png")
            print("Il file immagine dovrebbe essersi aperto automaticamente (view=True).")

    except FileNotFoundError:
        print("\nERRORE: Il software Graphviz non è stato trovato.")
        print("Assicurati che Graphviz sia installato sul tuo sistema e accessibile nel PATH.")
        print("Puoi scaricarlo da: https://graphviz.org/download/")
    except Exception as e:
        print(f"\nSi è verificato un errore durante la generazione o il rendering del grafico: {e}")

    print("\n--- Fine Esempio ---")
    print("Per visualizzare altre sequenze, modifica la lista 'esempio_sequenza' nello script.")