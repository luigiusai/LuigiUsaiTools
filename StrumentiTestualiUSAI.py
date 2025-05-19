# StrumentiTestualiUsai.py
# Progetto Integrato per l'Analisi Testuale e Narratologica
# Autore: Luigi Usai (con assistenza AI)
# Data: 19 Maggio 2025
# Versione: 2.0 (Unificazione e Miglioramenti)
#
# Questo script Tkinter fornisce un'interfaccia grafica per caricare corpora testuali
# ed eseguire varie analisi linguistiche, di usabilità, narratologiche e preliminari Griceane.
#
# Funzionalità incluse:
# - Caricamento di file di testo (.txt) come corpus.
# - Gestione (aggiunta/rimozione) di stopwords.
# - Analisi di frequenza dei termini.
# - Generazione di Nuvole di Parole.
# - Analisi di Collocazioni (N-grammi).
# - KWIC (Parole Chiave nel Contesto).
# - Andamento dei Termini attraverso i documenti o segmenti.
# - Rete di Co-occorrenze testuali.
# - Suddivisione in Frasi e Token (usabilità).
# - Annotazione Morfosintattica (POS Tagging - usabilità).
# - Calcolo Indice di Leggibilità Gulpease (globale e per frase - usabilità, specifico italiano).
# - Creazione e Visualizzazione Matrice Attanziale di Greimas (narratologia).
# - Creazione e Visualizzazione Matrice Funzioni di Propp (narratologia).
# - Creazione e Visualizzazione Tensori Narrativi (Luigi Usai - narratologia).
# - Generazione Permutazioni di Funzioni di Propp (trame possibili).
# - Generazione Combinazioni di Funzioni di Propp (sottoinsiemi di funzioni).
# - Visualizzazione Grafica Sequenza Funzioni di Propp (richiede Graphviz).
# - Analisi Semplificata Indicatori Griceani (Quantità, Modo, Qualità - richiede NLTK).
# - Salvataggio Dati Narratologici (JSON, SQLite).
# - Finestra "About" con informazioni sull'autore.
#
# Dipendenze richieste:
# - tkinter (standard Python)
# - wordcloud (pip install wordcloud)
# - matplotlib (pip install matplotlib)
# - Pillow (PIL) (pip install Pillow) - Per l'immagine nell'About
# - nltk (pip install nltk) - Per tokenizzazione, POS tagging, Gulpease, Grice
# - graphviz (pip install graphviz) - Per visualizzazione sequenze Propp
# - itertools (standard Python)
# - json (standard Python)
# - sqlite3 (standard Python)
# - re (standard Python)
# - collections (standard Python)
# - statistics (standard Python)
# - math (standard Python)
# - textwrap (standard Python)
#
# Assicurati di scaricare i dati NLTK necessari (punkt, averaged_perceptron_tagger)
# Eseguendo in un interprete Python:
# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
#
# Assicurati che il software Graphviz sia installato sul sistema e nel PATH per la visualizzazione grafica di Propp:
# https://graphviz.org/download/
#
# Per una panoramica sui Tensori Narrativi:
# https://www.amazon.it/ARCHITETTURE-INVISIBILI-VIAGGIO-NARRAZIONE-Versione/dp/B0F91P1XBH/
# Riferimento principale delle opere: Harvard Dataverse, DOI:10.7910/DVN/ICOJ19
#

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import json
import sqlite3
import itertools
import re
from collections import Counter
import statistics
import math
import textwrap # Per gestire il testo lungo nei nodi graphviz

# --- Gestione Import Opzionali e Dipendenze ---
# Controlla la disponibilità delle librerie non standard e dei dati NLTK

# Pillow (PIL) per immagine About
pil_disponibile = False
try:
    from PIL import Image, ImageTk
    pil_disponibile = True
except ImportError:
    print("Pillow (PIL) non è installato. L'immagine nell'About non sarà visualizzata. Installa con: pip install Pillow")

# NLTK per analisi linguistiche, usabilità e Grice
nltk_disponibile = False
nltk_punkt_disponibile = False
nltk_tagger_disponibile = False
try:
    import nltk
    nltk_disponibile = True
    # Verifica la presenza dei dati NLTK necessari
    try:
        nltk.data.find('tokenizers/punkt')
        nltk_punkt_disponibile = True
    except nltk.downloader.DownloadError:
        print("Pacchetto NLTK 'punkt' non trovato. Alcune funzionalità (frasi, token, leggibilità, Grice) potrebbero non funzionare.")
        print("Scaricalo eseguendo in Python: nltk.download('punkt')")
    except LookupError:
         print("Pacchetto NLTK 'punkt' non trovato. Alcune funzionalità (frasi, token, leggibilità, Grice) potrebbero non funzionare.")
         print("Scaricalo eseguendo in Python: nltk.download('punkt')")

    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
        nltk_tagger_disponibile = True
    except nltk.downloader.DownloadError:
        print("Pacchetto NLTK 'averaged_perceptron_tagger' non trovato. Il POS tagging potrebbe non funzionare.")
        print("Scaricalo eseguendo in Python: nltk.download('averaged_perceptron_tagger')")
    except LookupError:
        print("Pacchetto NLTK 'averaged_perceptron_tagger' non trovato. Il POS tagging potrebbe non funzionare.")
        print("Scaricalo eseguendo in Python: nltk.download('averaged_perceptron_tagger')")

except ImportError:
    print("Libreria NLTK non trovata. Le funzionalità di usabilità e Grice non saranno disponibili. Installa con: pip install nltk")

# Graphviz per visualizzazione Propp
graphviz_disponibile = False
try:
    import graphviz
    graphviz_disponibile = True
except ImportError:
    print("Libreria 'graphviz' non trovata. La visualizzazione delle sequenze di Propp non sarà disponibile.")
    print("Installala con: pip install graphviz")
    print("Inoltre, assicurati che il software Graphviz sia installato sul sistema e nel PATH: https://graphviz.org/download/")

# WordCloud e Matplotlib per nuvola di parole e andamento termini
wordcloud_disponibile = False
matplotlib_disponibile = False
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    wordcloud_disponibile = True
    matplotlib_disponibile = True
except ImportError:
    print("Librerie 'wordcloud' o 'matplotlib' non trovate. La nuvola di parole e l'andamento termini non saranno disponibili.")
    print("Installale con: pip install wordcloud matplotlib")


# --- Costanti e Definizioni ---

# Definizioni delle 31 funzioni di Propp
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

# Lista (molto limitata) di possibili indicatori di "hedging" (copertura/incertezza) per Grice
HEDGING_TERMS = ["credo", "penso", "forse", "magari", "sembra", "parrebbe", "apparentemente", "in un certo senso", "tipo", "cioè", "insomma"]


# --- Classi per Funzionalità Specifiche ---

class FunzioniUsability:
    """Contiene funzioni per l'analisi di usabilità e leggibilità del testo."""
    def __init__(self, app_ref):
        self.app_ref = app_ref
        self.lingua_analisi = "italian" # Default per funzioni come Gulpease

    def imposta_lingua_analisi(self):
        """Permette all'utente di impostare la lingua per le analisi che la supportano."""
        lingua_scelta = simpledialog.askstring("Imposta Lingua Analisi",
                                               "Scegli la lingua per l'analisi (es. 'italian', 'english').\n"
                                               "Nota: Gulpease funziona solo per l'italiano.",
                                               initialvalue=self.lingua_analisi,
                                               parent=self.app_ref.root)
        if lingua_scelta:
            lingua_scelta_lower = lingua_scelta.strip().lower()
            # Aggiungere altre lingue supportate da NLTK se necessario
            if lingua_scelta_lower in ['italian', 'english']:
                self.lingua_analisi = lingua_scelta_lower
                messagebox.showinfo("Lingua Impostata", f"Lingua per l'analisi impostata a: {self.lingua_analisi}", parent=self.app_ref.root)
                self.app_ref._display_output("Impostazione Lingua", f"Lingua analisi: {self.lingua_analisi}")
            else:
                messagebox.showwarning("Lingua non Supportata", f"Lingua '{lingua_scelta}' non supportata o riconosciuta.\nMantengo: {self.lingua_analisi}", parent=self.app_ref.root)

    def _check_corpus_e_nltk(self, check_punkt=False, check_tagger=False):
        """Controlla se il corpus è caricato e se NLTK e i suoi componenti sono disponibili."""
        if not self.app_ref.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.app_ref.root)
            return False
        if not nltk_disponibile:
            messagebox.showerror("NLTK Mancante", "La libreria NLTK è necessaria per questa funzionalità.", parent=self.app_ref.root)
            return False
        if check_punkt and not nltk_punkt_disponibile:
            messagebox.showerror("Dipendenza NLTK Mancante", "Il pacchetto 'punkt' di NLTK è necessario per questa funzionalità.\nScaricalo eseguendo in Python: nltk.download('punkt')", parent=self.app_ref.root)
            return False
        if check_tagger and not nltk_tagger_disponibile:
            messagebox.showerror("Dipendenza NLTK Mancante", "Il pacchetto 'averaged_perceptron_tagger' di NLTK è necessario per questa funzionalità.\nScaricalo eseguendo in Python: nltk.download('averaged_perceptron_tagger')", parent=self.app_ref.root)
            return False
        return True

    def subdividi_in_frasi(self):
        """Suddivide il corpus in frasi e le visualizza."""
        if not self._check_corpus_e_nltk(check_punkt=True):
            return

        testo_completo = ' '.join(self.app_ref.corpus_testuale)
        try:
            frasi = nltk.sent_tokenize(testo_completo, language=self.lingua_analisi)
            output_str = f"Suddivisione in Frasi (Lingua: {self.lingua_analisi}):\n"
            output_str += "-------------------------------------------------\n"
            if not frasi:
                output_str += "Nessuna frase trovata."
            else:
                 # Limita la visualizzazione per testi molto lunghi
                 max_frasi_visualizzate = 500
                 for i, frase in enumerate(frasi):
                     if i >= max_frasi_visualizzate:
                         output_str += f"\n... e altre {len(frasi) - max_frasi_visualizzate} frasi non visualizzate."
                         break
                     output_str += f"Frase {i+1}: {frase}\n"

            self.app_ref._display_output("Suddivisione in Frasi", output_str)
        except Exception as e:
            messagebox.showerror("Errore Suddivisione Frasi", f"Errore: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Suddivisione Frasi", f"Errore: {e}")

    def subdividi_in_token(self):
        """Suddivide il corpus in token e li visualizza."""
        if not self._check_corpus_e_nltk(check_punkt=True):
            return

        testo_completo = ' '.join(self.app_ref.corpus_testuale)
        try:
            # word_tokenize usa 'punkt' internamente e può prendere un argomento 'language'.
            tokens = nltk.word_tokenize(testo_completo, language=self.lingua_analisi)
            output_str = f"Suddivisione in Token (Lingua: {self.lingua_analisi}):\n"
            output_str += "--------------------------------------------------\n"
            if not tokens:
                output_str += "Nessun token trovato."
            else:
                 # Limita la visualizzazione per testi molto lunghi
                 max_tokens_visualizzati = 1000
                 display_tokens = tokens[:max_tokens_visualizzati]
                 output_str += ", ".join(display_tokens)
                 if len(tokens) > max_tokens_visualizzati:
                     output_str += f"\n... e altri {len(tokens) - max_tokens_visualizzati} token non visualizzati."

            self.app_ref._display_output("Suddivisione in Token", output_str)
        except Exception as e:
            messagebox.showerror("Errore Suddivisione Token", f"Errore: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Suddivisione Token", f"Errore: {e}")

    def annotazione_pos(self):
        """Esegue il Part-of-Speech tagging sul corpus e visualizza i risultati."""
        if not self._check_corpus_e_nltk(check_punkt=True, check_tagger=True):
            return

        testo_completo = ' '.join(self.app_ref.corpus_testuale)
        try:
            tokens = nltk.word_tokenize(testo_completo, language=self.lingua_analisi)
            # nltk.pos_tag usa il tagger 'averaged_perceptron_tagger'.
            # Per l'italiano, i risultati potrebbero non essere ottimali senza un modello specifico.
            # Usiamo quello di default e avvisiamo l'utente.
            tagged_tokens = nltk.pos_tag(tokens) # Non c'è un argomento 'language' diretto per il tagger qui

            output_str = f"Annotazione Morfosintattica (POS Tagging - Lingua: {self.lingua_analisi}):\n"
            output_str += "-------------------------------------------------------------------\n"
            if not tagged_tokens:
                output_str += "Nessun token da annotare."
            else:
                # Limita la visualizzazione
                max_tagged_visualizzati = 500
                for i, (token, tag) in enumerate(tagged_tokens):
                    if i >= max_tagged_visualizzati:
                        output_str += f"\n... e altri {len(tagged_tokens) - max_tagged_visualizzati} token non visualizzati."
                        break
                    output_str += f"{token} [{tag}]\n"

            output_str += "\nNota: Il tagger predefinito di NLTK ('averaged_perceptron_tagger') è ottimizzato per l'inglese."
            output_str += "\nPer l'italiano, i risultati potrebbero non essere ottimali senza un modello specifico addestrato."
            self.app_ref._display_output("Annotazione POS", output_str)
        except Exception as e:
            messagebox.showerror("Errore Annotazione POS", f"Errore: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Annotazione POS", f"Errore: {e}")

    def calcola_gulpease_globale(self):
        """
        Calcola l'indice di leggibilità Gulpease per l'intero corpus.
        Questa funzione è specifica per la lingua ITALIANA.
        """
        if self.lingua_analisi != "italian":
            messagebox.showwarning("Lingua non Adatta", "L'indice Gulpease è calibrato per la lingua italiana. "
                                   f"La lingua attualmente impostata è '{self.lingua_analisi}'. "
                                   "Il risultato potrebbe non essere attendibile.", parent=self.app_ref.root)

        if not self._check_corpus_e_nltk(check_punkt=True): # Necessario per frasi e parole
            return

        testo_completo = ' '.join(self.app_ref.corpus_testuale)
        try:
            # Tokenizzazione parole (solo alfabetiche)
            # Forziamo italiano per la tokenizzazione specifica per Gulpease
            parole_raw = nltk.word_tokenize(testo_completo.lower(), language='italian')
            parole = [p for p in parole_raw if p.isalpha()]

            num_parole = len(parole)
            if num_parole == 0:
                self.app_ref._display_output("Indice Gulpease", "Nessuna parola alfabetica valida trovata per il calcolo.")
                messagebox.showwarning("Indice Gulpease", "Nessuna parola valida trovata per il calcolo.", parent=self.app_ref.root)
                return

            # Tokenizzazione frasi
            # Forziamo italiano per la tokenizzazione specifica per Gulpease
            frasi = nltk.sent_tokenize(testo_completo, language='italian')
            num_frasi = len(frasi)
            if num_frasi == 0:
                self.app_ref._display_output("Indice Gulpease", "Nessuna frase trovata per il calcolo.")
                messagebox.showwarning("Indice Gulpease", "Nessuna frase trovata per il calcolo.", parent=self.app_ref.root)
                return

            num_lettere = sum(len(p) for p in parole)

            # Formula Gulpease: G = 89 + ( ( (Frasi * 100) / Parole * 3 ) - ( (Lettere * 100) / Parole * 10 ) ) / 100
            # Semplificata: G = 89 + (Frasi * 300 / Parole) - (Lettere * 10 / Parole)
            # G = 89 + ( (Frasi * 300) - (Lettere * 10) ) / Parole

            # Evita divisione per zero, anche se num_parole > 0 è già stato controllato
            if num_parole > 0:
                gulpease_index = 89 + ( (num_frasi * 300) - (num_lettere * 10) ) / num_parole
            else:
                 gulpease_index = 0 # O altro valore indicativo

            # Cap e Floor dell'indice
            gulpease_index = max(0, min(100, gulpease_index))

            interpretazione = ""
            if gulpease_index >= 80: interpretazione = "Molto facile (lettori con licenza elementare)"
            elif gulpease_index >= 60: interpretazione = "Facile (lettori con licenza media inferiore)"
            elif gulpease_index >= 40: interpretazione = "Abbastanza difficile (lettori con licenza media superiore)"
            else: interpretazione = "Difficile (lettori con laurea)"

            output_str = f"Indice di Leggibilità Globale Gulpease (per l'italiano):\n"
            output_str += "-------------------------------------------------------\n"
            output_str += f"Numero di Lettere (alfabetiche): {num_lettere}\n"
            output_str += f"Numero di Parole (alfabetiche): {num_parole}\n"
            output_str += f"Numero di Frasi: {num_frasi}\n"
            output_str += f"Indice Gulpease: {gulpease_index:.2f}\n"
            output_str += f"Interpretazione: {interpretazione}\n\n"
            output_str += "Scala di riferimento Gulpease:\n"
            output_str += "  > 80: Molto facile\n  60-80: Facile\n  40-60: Abbastanza difficile\n  < 40: Difficile\n"
            if self.lingua_analisi != "italian":
                 output_str += f"\nATTENZIONE: Calcolato usando metriche italiane su testo potenzialmente non italiano ('{self.lingua_analisi}')."


            self.app_ref._display_output("Indice Gulpease Globale", output_str)

        except Exception as e:
            messagebox.showerror("Errore Gulpease", f"Errore durante il calcolo dell'indice Gulpease: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Gulpease", f"Errore: {e}")

    def analisi_leggibilita_per_frase(self):
        """
        Calcola l'indice Gulpease per ogni frase del testo.
        Utile per la "proiezione della leggibilità sul testo".
        Specifico per ITALIANO.
        """
        if self.lingua_analisi != "italian":
            messagebox.showwarning("Lingua non Adatta", "L'indice Gulpease è calibrato per la lingua italiana. "
                                   f"La lingua attualmente impostata è '{self.lingua_analisi}'. "
                                   "I risultati per frase potrebbero non essere attendibili.", parent=self.app_ref.root)

        if not self._check_corpus_e_nltk(check_punkt=True):
            return

        testo_completo = ' '.join(self.app_ref.corpus_testuale)
        try:
            frasi_originali = nltk.sent_tokenize(testo_completo, language='italian') # Forziamo italiano
            if not frasi_originali:
                self.app_ref._display_output("Leggibilità per Frase", "Nessuna frase trovata.")
                messagebox.showwarning("Leggibilità per Frase", "Nessuna frase trovata.", parent=self.app_ref.root)
                return

            output_str = f"Analisi Leggibilità per Frase (Indice Gulpease - per l'italiano):\n"
            output_str += "-----------------------------------------------------------------\n"

            risultati_frasi = []
            # Limita la visualizzazione per evitare output eccessivi
            max_frasi_visualizzate = 300
            for i, frase_txt in enumerate(frasi_originali):
                if i >= max_frasi_visualizzate:
                    risultati_frasi.append(f"\n--- (Visualizzazione limitata alle prime {max_frasi_visualizzate} frasi) ---")
                    break

                parole_raw_frase = nltk.word_tokenize(frase_txt.lower(), language='italian')
                parole_frase = [p for p in parole_raw_frase if p.isalpha()]

                num_parole_frase = len(parole_frase)
                if num_parole_frase == 0:
                    risultati_frasi.append(f"Frase {i+1}: \"{frase_txt[:70]}...\" - Indice Gulpease: N/A (0 parole)")
                    continue

                num_lettere_frase = sum(len(p) for p in parole_frase)

                # Gulpease per una singola frase (num_frasi = 1)
                # Evita divisione per zero, anche se num_parole_frase > 0 è già stato controllato
                if num_parole_frase > 0:
                    gulpease_frase = 89 + ( (1 * 300) - (num_lettere_frase * 10) ) / num_parole_frase
                else:
                    gulpease_frase = 0 # O altro valore indicativo

                gulpease_frase = max(0, min(100, gulpease_frase))

                interpretazione_frase = ""
                if gulpease_frase >= 80: interpretazione_frase = "Molto facile"
                elif gulpease_frase >= 60: interpretazione_frase = "Facile"
                elif gulpease_frase >= 40: interpretazione_frase = "Abb. difficile"
                else: interpretazione_frase = "Difficile"

                risultati_frasi.append(f"Frase {i+1}: \"{frase_txt[:70]}...\"\n  Indice Gulpease: {gulpease_frase:.2f} ({interpretazione_frase}) "
                                       f"[L:{num_lettere_frase}, P:{num_parole_frase}]")

            output_str += "\n\n".join(risultati_frasi)
            if self.lingua_analisi != "italian":
                 output_str += f"\n\nATTENZIONE: Calcolato usando metriche italiane su testo potenzialmente non italiano ('{self.lingua_analisi}')."

            self.app_ref._display_output("Leggibilità per Frase (Gulpease)", output_str)

        except Exception as e:
            messagebox.showerror("Errore Leggibilità per Frase", f"Errore: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Leggibilità per Frase", f"Errore: {e}")


class FunzioniNarratologia:
    """Contiene funzioni per l'analisi e la generazione basata su modelli narratologici (Greimas, Propp, Tensori)."""
    def __init__(self, app_ref):
        self.app_ref = app_ref
        self.matrice_greimas_data = None
        self.matrice_propp_data_utente = None # Dati Propp definiti dall'utente
        self.tensori_narrativi_data = None

    def get_propp_function_description(self, code):
        """Restituisce la descrizione completa di una funzione di Propp dato il suo codice."""
        # Usa le funzioni utente se definite, altrimenti le standard
        funzioni_di_riferimento = self.matrice_propp_data_utente if self.matrice_propp_data_utente is not None else FUNZIONI_PROPP
        return funzioni_di_riferimento.get(code.upper(), f"Funzione Sconosciuta ({code})")


    def crea_matrice_greimas(self):
        """Permette all'utente di definire e visualizzare la Matrice Attanziale di Greimas."""
        messagebox.showinfo("Matrice Attanziale di Greimas",
                             "Definisci i ruoli attanziali (Soggetto, Oggetto, Destinante, Destinatario, Aiutante, Oppositore) per la tua analisi.",
                             parent=self.app_ref.root)

        dialog = tk.Toplevel(self.app_ref.root)
        dialog.title("Matrice Attanziale di Greimas")
        dialog.geometry("400x350")
        dialog.transient(self.app_ref.root)
        dialog.grab_set()

        tk.Label(dialog, text="Definisci gli attanti:", font=("Arial", 12, "bold")).pack(pady=10)

        attanti = ["Soggetto", "Oggetto", "Destinante", "Destinatario", "Aiutante", "Oppositore"]
        entries = {}

        for attante in attanti:
            frame = tk.Frame(dialog)
            frame.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame, text=f"{attante}:", width=15, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            # Pre-popola se ci sono dati salvati
            if self.matrice_greimas_data and attante in self.matrice_greimas_data:
                entry.insert(0, self.matrice_greimas_data[attante])

        def salva_dati_greimas():
            self.matrice_greimas_data = {attante: entries[attante].get().strip() for attante in attanti}
            output_str = "Matrice Attanziale di Greimas:\n"
            output_str += "-----------------------------\n"
            for attante, valore in self.matrice_greimas_data.items():
                output_str += f"  - {attante}: {valore if valore else '[Non definito]'}\n"
            self.app_ref._display_output("Matrice Attanziale (Greimas)", output_str)
            messagebox.showinfo("Matrice Greimas", "Matrice di Greimas aggiornata e visualizzata.", parent=dialog)
            dialog.destroy()

        tk.Button(dialog, text="Salva e Visualizza", command=salva_dati_greimas).pack(pady=20)
        tk.Button(dialog, text="Annulla", command=dialog.destroy).pack(pady=5)

        self.app_ref.root.wait_window(dialog)

    def crea_matrice_propp(self):
        """Permette all'utente di definire e visualizzare le funzioni di Propp personalizzate."""
        # L'utente può definire un sottoinsieme o ridefinire le descrizioni
        messagebox.showinfo("Matrice Funzioni di Propp",
                             "Qui puoi definire un sottoinsieme o personalizzare le descrizioni delle Funzioni di Propp.\n"
                             "Inserisci le funzioni nel formato 'Codice: Descrizione' (una per riga).\n"
                             "Se vuoi usare le 31 funzioni standard, puoi saltare questo passaggio o cliccare 'Usa Standard'.",
                             parent=self.app_ref.root)

        dialog = tk.Toplevel(self.app_ref.root)
        dialog.title("Definisci Funzioni di Propp Personalizzate")
        dialog.geometry("500x600")
        dialog.transient(self.app_ref.root)
        dialog.grab_set()

        tk.Label(dialog, text="Definisci/Modifica Funzioni di Propp:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="Formato: Codice (es. F1): Descrizione", font=("Arial", 10, "italic")).pack()

        # Usiamo un Text widget per permettere l'editing di più funzioni
        text_area = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=50, height=15, font=("Arial", 10))
        text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Popola con le funzioni standard o i dati utente salvati
        if self.matrice_propp_data_utente:
             for codice, desc in self.matrice_propp_data_utente.items():
                 text_area.insert(tk.END, f"{codice}: {desc}\n")
        else:
            # Popola con le funzioni standard come suggerimento
            for codice, desc in FUNZIONI_PROPP.items():
                text_area.insert(tk.END, f"{codice}: {desc}\n")


        def salva_dati_propp():
            input_text = text_area.get(1.0, tk.END).strip()
            lines = input_text.split('\n')
            new_propp_data = {}
            errors = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'): continue # Salta righe vuote o commenti
                if ':' in line:
                    codice, desc = line.split(':', 1)
                    codice = codice.strip().upper()
                    desc = desc.strip()
                    if codice and desc:
                         # Opzionale: validare che il codice inizi con 'F' e sia seguito da numeri
                         if re.match(r'^F\d+$', codice):
                            new_propp_data[codice] = desc
                         else:
                             errors.append(f"Codice non valido: '{codice}' (deve iniziare con 'F' seguito da numeri)")
                    else:
                        errors.append(f"Formato riga non valido: '{line}' (deve essere Codice: Descrizione)")
                else:
                    errors.append(f"Formato riga non valido: '{line}' (deve contenere ':')")

            if errors:
                error_msg = "Errori nel formato delle funzioni:\n" + "\n".join(errors)
                messagebox.showerror("Errore Formato", error_msg, parent=dialog)
                return

            self.matrice_propp_data_utente = new_propp_data
            output_str = "Matrice Funzioni di Propp (Personalizzata):\n"
            output_str += "------------------------------------------\n"
            if not self.matrice_propp_data_utente:
                output_str += "[Nessuna funzione definita dall'utente. Verranno usate le 31 standard per le operazioni.]\n"
            else:
                for codice, descrizione in self.matrice_propp_data_utente.items():
                    output_str += f"  - {codice}: {descrizione}\n"

            self.app_ref._display_output("Matrice di Propp (Utente)", output_str)
            messagebox.showinfo("Matrice Propp", "Matrice di Propp personalizzata aggiornata e visualizzata.", parent=dialog)
            dialog.destroy()

        tk.Button(dialog, text="Salva e Visualizza", command=salva_dati_propp).pack(pady=10)
        tk.Button(dialog, text="Usa Standard (31 Funzioni)", command=lambda: [setattr(self, 'matrice_propp_data_utente', None), messagebox.showinfo("Matrice Propp", "Verranno usate le 31 funzioni standard di Propp.", parent=dialog), dialog.destroy()]).pack(pady=5)
        tk.Button(dialog, text="Annulla", command=dialog.destroy).pack(pady=5)

        self.app_ref.root.wait_window(dialog)


    def crea_tensori_narrativi(self):
        """Permette all'utente di definire e visualizzare i Tensori Narrativi di Luigi Usai."""
        messagebox.showinfo("Tensori Narrativi",
                             "Definisci le dimensioni e gli elementi per i tuoi Tensori Narrativi.\n"
                             "Esempio: Dimensione 'Personaggi', Elementi 'Eroe, Antagonista, Aiutante'.\n"
                             "Formato: NomeDimensione: Elemento1, Elemento2, Elemento3... (una dimensione per riga)",
                             parent=self.app_ref.root)

        dialog = tk.Toplevel(self.app_ref.root)
        dialog.title("Definisci Tensori Narrativi")
        dialog.geometry("500x400")
        dialog.transient(self.app_ref.root)
        dialog.grab_set()

        tk.Label(dialog, text="Definisci Dimensioni e Elementi per i Tensori:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(dialog, text="Formato: NomeDimensione: Elemento1, Elemento2, Elemento3...", font=("Arial", 10, "italic")).pack()
        tk.Label(dialog, text="(Una dimensione per riga)", font=("Arial", 10, "italic")).pack()


        text_area = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=50, height=10, font=("Arial", 10))
        text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Popola con dati utente salvati se esistono
        if self.tensori_narrativi_data:
             for dim_name, elements in self.tensori_narrativi_data.items():
                 text_area.insert(tk.END, f"{dim_name}: {', '.join(elements)}\n")
        else:
            # Esempio suggerito
            text_area.insert(tk.END, "Personaggi: Eroe, Antagonista, Aiutante\n")
            text_area.insert(tk.END, "Temi: Amore, Odio, Vendetta\n")
            text_area.insert(tk.END, "Emozioni: Gioia, Tristezza, Paura\n")


        def salva_dati_tensori():
            input_text = text_area.get(1.0, tk.END).strip()
            lines = input_text.split('\n')
            new_tensori_data = {}
            errors = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'): continue # Salta righe vuote o commenti
                if ':' in line:
                    dim_name, elements_str = line.split(':', 1)
                    dim_name = dim_name.strip()
                    elements = [e.strip() for e in elements_str.split(',') if e.strip()] # Filtra elementi vuoti
                    if dim_name and elements:
                         new_tensori_data[dim_name] = elements
                    else:
                        errors.append(f"Formato riga non valido: '{line}' (deve essere NomeDimensione: Elemento1, Elemento2...)")
                else:
                    errors.append(f"Formato riga non valido: '{line}' (deve contenere ':')")

            if errors:
                error_msg = "Errori nel formato delle dimensioni/elementi:\n" + "\n".join(errors)
                messagebox.showerror("Errore Formato", error_msg, parent=dialog)
                return

            self.tensori_narrativi_data = new_tensori_data
            output_str = "Tensori Narrativi (Luigi Usai - Definiti dall'Utente):\n"
            output_str += "-------------------------------------------------------\n"
            if not self.tensori_narrativi_data:
                output_str += "[Nessun Tensore Narrativo definito dall'utente.]\n"
            else:
                for dimensione, elementi in self.tensori_narrativi_data.items():
                    output_str += f"  - Dimensione '{dimensione}': {', '.join(elementi)}\n"

            self.app_ref._display_output("Tensori Narrativi", output_str)
            messagebox.showinfo("Tensori Narrativi", "Tensori Narrativi aggiornati e visualizzati.", parent=dialog)
            dialog.destroy()


        tk.Button(dialog, text="Salva e Visualizza", command=salva_dati_tensori).pack(pady=10)
        tk.Button(dialog, text="Annulla", command=dialog.destroy).pack(pady=5)

        self.app_ref.root.wait_window(dialog)


    # --- Funzioni Core di Generazione Propp (Spostate qui o chiamate da qui) ---
    # Queste funzioni non dipendono direttamente dalla GUI, ma usano le definizioni FUNZIONI_PROPP

    def genera_permutazioni_funzioni(self, lista_codici_funzioni):
        """
        Genera tutte le possibili sequenze ordinate (permutazioni)
        di un dato sottoinsieme di funzioni di Propp. L'ordine conta.
        Usa le funzioni standard o quelle utente se definite.
        """
        # Usa le funzioni utente se definite, altrimenti le standard
        funzioni_di_riferimento = self.matrice_propp_data_utente if self.matrice_propp_data_utente is not None else FUNZIONI_PROPP

        if not all(codice.upper() in funzioni_di_riferimento for codice in lista_codici_funzioni):
            invalid_codes = [c.upper() for c in lista_codici_funzioni if c.upper() not in funzioni_di_riferimento]
            raise ValueError(f"Uno o più codici funzione non sono validi nel set di riferimento: {', '.join(invalid_codes)}")

        permutazioni = list(itertools.permutations([cod.upper() for cod in lista_codici_funzioni]))

        trame_generate = []
        for p in permutazioni:
            # Usa la descrizione dal set di riferimento
            trama = [funzioni_di_riferimento.get(codice, f"Sconosciuta ({codice})") for codice in p]
            trame_generate.append(" -> ".join(trama))
        return trame_generate

    def genera_combinazioni_funzioni(self, lista_codici_funzioni_disponibili, numero_funzioni_da_scegliere):
        """
        Genera tutti i possibili sottoinsiemi non ordinati (combinazioni)
        di funzioni di Propp da una lista più ampia. L'ordine NON conta.
        Usa le funzioni standard o quelle utente se definite.
        """
        # Usa le funzioni utente se definite, altrimenti le standard
        funzioni_di_riferimento = self.matrice_propp_data_utente if self.matrice_propp_data_utente is not None else FUNZIONI_PROPP


        if not all(codice.upper() in funzioni_di_riferimento for codice in lista_codici_funzioni_disponibili):
             invalid_codes = [c.upper() for c in lista_codici_funzioni_disponibili if c.upper() not in funzioni_di_riferimento]
             raise ValueError(f"Uno o più codici funzione nella lista dei disponibili non sono validi nel set di riferimento: {', '.join(invalid_codes)}")

        if numero_funzioni_da_scegliere > len(lista_codici_funzioni_disponibili):
            raise ValueError("Il numero di funzioni da scegliere non può essere maggiore delle funzioni disponibili.")

        combinazioni = list(itertools.combinations([cod.upper() for cod in lista_codici_funzioni_disponibili], numero_funzioni_da_scegliere))

        sottoinsiemi_generati = []
        for c in combinazioni:
            # Usa la descrizione dal set di riferimento e ordina per coerenza di visualizzazione
            sottoinsieme = sorted([funzioni_di_riferimento.get(codice, f"Sconosciuta ({codice})") for codice in c])
            sottoinsiemi_generati.append(", ".join(sottoinsieme))
        return sottoinsiemi_generati

    # --- Interfacce GUI per Generatori Propp ---

    def _mostra_risultati_generatore_propp(self, titolo, risultati, max_visualizzati=200):
        """Helper per visualizzare risultati potenzialmente lunghi in una nuova finestra."""
        if not risultati:
            self.app_ref._display_output(titolo, "Nessun risultato generato.")
            messagebox.showinfo(titolo, "Nessun risultato da visualizzare.", parent=self.app_ref.root)
            return

        result_window = tk.Toplevel(self.app_ref.root)
        result_window.title(titolo)
        result_window.geometry("800x600")
        result_window.transient(self.app_ref.root)
        result_window.grab_set()

        tk.Label(result_window, text=f"{titolo} (Prime {max_visualizzati} occorrenze se più lunghe):", font=("Arial", 12)).pack(pady=5)

        text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=90, height=25)
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        output_str = ""
        for i, item in enumerate(risultati):
            if i >= max_visualizzati:
                output_str += f"\n... e altri {len(risultati) - max_visualizzati} risultati."
                break
            output_str += f"{i+1}. {item}\n"

        text_area.insert(tk.END, output_str)
        text_area.config(state=tk.DISABLED)

        tk.Button(result_window, text="Chiudi", command=result_window.destroy).pack(pady=10)
        self.app_ref._display_output(titolo, f"Visualizzati {min(len(risultati), max_visualizzati)} risultati su {len(risultati)} totali.")


    def genera_permutazioni_propp(self):
        """Genera permutazioni di funzioni di Propp scelte dall'utente (GUI)."""
        codici_input = simpledialog.askstring("Genera Trame Propp (Permutazioni)",
                                               "Inserisci i codici delle funzioni di Propp separati da virgola (es. F1,F8,F11).\n"
                                               "Attenzione: il numero di permutazioni cresce MOLTO velocemente!",
                                               parent=self.app_ref.root)
        if not codici_input:
            return

        lista_codici_funzioni = [cod.strip().upper() for cod in codici_input.split(',')]

        try:
            if len(lista_codici_funzioni) > 8: # Limite consigliato per evitare troppe permutazioni (8! = 40320)
                 if not messagebox.askyesno("Attenzione", f"Stai per generare permutazioni per {len(lista_codici_funzioni)} funzioni. Questo potrebbe richiedere molto tempo e memoria ({math.factorial(len(lista_codici_funzioni)):,} permutazioni stimate). Continuare?", parent=self.app_ref.root):
                    return

            trame_generate = self.genera_permutazioni_funzioni(lista_codici_funzioni)

            titolo_output = f"Trame Generate (Permutazioni di: {', '.join(lista_codici_funzioni)}) - {len(trame_generate)} totali"
            self._mostra_risultati_generatore_propp(titolo_output, trame_generate)

        except ValueError as e:
            messagebox.showerror("Errore Input", str(e), parent=self.app_ref.root)
        except Exception as e:
            messagebox.showerror("Errore Inatteso", f"Si è verificato un errore: {e}", parent=self.app_ref.root)

    def genera_combinazioni_propp(self):
        """Genera combinazioni di funzioni di Propp da un set disponibile (GUI)."""
        codici_disponibili_input = simpledialog.askstring("Genera Sottoinsiemi Propp (Combinazioni)",
                                                          "Inserisci i codici delle funzioni DISPONIBILI separati da virgola (es. F1,F2,F3,F8,F11):",
                                                          parent=self.app_ref.root)
        if not codici_disponibili_input:
            return

        lista_codici_disponibili = [cod.strip().upper() for cod in codici_disponibili_input.split(',')]

        try:
            if not lista_codici_disponibili:
                 messagebox.showwarning("Input Vuoto", "Nessun codice disponibile inserito.", parent=self.app_ref.root)
                 return

            numero_da_scegliere = simpledialog.askinteger("Numero da Scegliere",
                                                       f"Quante funzioni vuoi scegliere dal set di {len(lista_codici_disponibili)} disponibili?",
                                                       parent=self.app_ref.root, minvalue=1, maxvalue=len(lista_codici_disponibili))
            if numero_da_scegliere is None:
                return

            combinazioni = self.genera_combinazioni_funzioni(lista_codici_disponibili, numero_da_scegliere)


            titolo_output = (f"Sottoinsiemi Generati (Combinazioni di {numero_da_scegliere} da: "
                             f"{', '.join(lista_codici_disponibili)}) - {len(combinazioni)} totali")
            self._mostra_risultati_generatore_propp(titolo_output, combinazioni)

        except ValueError as e:
            messagebox.showerror("Errore Input", str(e), parent=self.app_ref.root)
        except Exception as e:
            messagebox.showerror("Errore Inatteso", f"Si è verificato un errore: {e}", parent=self.app_ref.root)


    def visualizza_sequenza_propp_input(self):
        """
        Permette all'utente di inserire una sequenza di funzioni di Propp
        e la visualizza graficamente usando Graphviz.
        """
        if not graphviz_disponibile:
            messagebox.showerror("Graphviz non disponibile",
                                 "La libreria Graphviz e il software 'dot' sono necessari per questa funzionalità.\n"
                                 "Installali e assicurati che 'dot' sia nel PATH di sistema.",
                                 parent=self.app_ref.root)
            return

        codici_input = simpledialog.askstring("Visualizza Sequenza Funzioni di Propp",
                                               "Inserisci i codici delle funzioni di Propp in sequenza, separati da virgola (es. F8,F11,F14,F16,F18):",
                                               parent=self.app_ref.root)
        if not codici_input:
            return

        propp_codes_sequence = [cod.strip().upper() for cod in codici_input.split(',')]

        # Usa le funzioni utente se definite, altrimenti le standard per la validazione e descrizione
        funzioni_di_riferimento = self.matrice_propp_data_utente if self.matrice_propp_data_utente is not None else FUNZIONI_PROPP

        invalid_codes = [c for c in propp_codes_sequence if c not in funzioni_di_riferimento]
        if invalid_codes:
            messagebox.showerror("Errore Codici", f"I seguenti codici funzione non sono validi nel set di riferimento: {', '.join(invalid_codes)}", parent=self.app_ref.root)
            return

        if not propp_codes_sequence:
            messagebox.showwarning("Input Vuoto", "Nessuna sequenza inserita.", parent=self.app_ref.root)
            return

        try:
            dot = graphviz.Digraph(comment="Sequenza Funzioni di Propp (Utente)")
            dot.attr(rankdir='LR') # Layout da Sinistra a Destra
            dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Arial', fontsize='10')
            dot.attr('edge', fontname='Arial', fontsize='9', color='gray')

            previous_node_id = None
            for i, code in enumerate(propp_codes_sequence):
                # Usa la descrizione dal set di riferimento
                function_description = funzioni_di_riferimento.get(code, f"Sconosciuta ({code})")
                label = f"{code}\n{textwrap.fill(function_description, width=25)}" # width ridotto per nodi più compatti
                node_id = f"node_user_{i}"

                dot.node(node_id, label)
                if previous_node_id is not None:
                    dot.edge(previous_node_id, node_id)
                previous_node_id = node_id

            # Chiedi dove salvare
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("File PNG", "*.png"), ("File PDF", "*.pdf"), ("File SVG", "*.svg"), ("File DOT Source", "*.dot"), ("Tutti i file", "*.*")],
                title="Salva Visualizzazione Sequenza Propp",
                initialfile="sequenza_propp_utente",
                parent=self.app_ref.root
            )
            if not file_path:
                return

            # Estrai formato ed estensione
            save_format = 'png' # default
            if '.' in file_path:
                ext = file_path.split('.')[-1].lower()
                if ext in ['png', 'pdf', 'svg', 'jpeg', 'jpg', 'dot']: # Aggiunto jpg
                    save_format = ext
                else:
                     # Se l'estensione non è riconosciuta, usa png e aggiungila al nome file
                     file_path += ".png"
                     save_format = 'png'

            # Rimuovi l'estensione dal nome del file per render, che la aggiunge da solo
            base_file_path = file_path
            if file_path.lower().endswith(f".{save_format}"):
                 base_file_path = file_path[:-len(save_format)-1]


            dot.render(base_file_path, format=save_format, view=True, cleanup=True) # cleanup=True rimuove il .dot dopo il render
            messagebox.showinfo("Visualizzazione Creata",
                                f"Visualizzazione della sequenza di Propp salvata come '{file_path}' e aperta.",
                                parent=self.app_ref.root)
            self.app_ref._display_output("Visualizzazione Sequenza Propp", f"Grafico generato e salvato in {file_path}")

        except graphviz.backend.execute.ExecutableNotFound:
             messagebox.showerror("Errore Graphviz",
                                 "Eseguibile Graphviz (dot) non trovato.\n"
                                 "Assicurati che Graphviz sia installato e che la directory 'bin' sia nel PATH di sistema.",
                                 parent=self.app_ref.root)
             self.app_ref._display_output("Errore Visualizzazione Propp", "Graphviz (dot) non trovato nel PATH.")
        except Exception as e:
            messagebox.showerror("Errore Visualizzazione", f"Si è verificato un errore: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Visualizzazione Propp", f"Errore: {e}")


    def salva_dati_narratologici_json(self):
        """Salva i dati narratologici (Greimas, Propp Utente, Tensori) in un file JSON."""
        if not self.matrice_greimas_data and not self.matrice_propp_data_utente and not self.tensori_narrativi_data:
            messagebox.showwarning("Nessun Dato", "Non ci sono dati narratologici da salvare.", parent=self.app_ref.root)
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")],
            title="Salva Dati Narratologici come JSON",
            parent=self.app_ref.root
        )

        if not file_path:
            return

        dati_da_salvare = {}
        if self.matrice_greimas_data:
            dati_da_salvare["matrice_greimas"] = self.matrice_greimas_data
        if self.matrice_propp_data_utente:
            dati_da_salvare["matrice_propp_utente"] = self.matrice_propp_data_utente
        if self.tensori_narrativi_data:
            dati_da_salvare["tensori_narrativi"] = self.tensori_narrativi_data

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(dati_da_salvare, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Salvataggio JSON", f"Dati narratologici salvati con successo in:\n{file_path}", parent=self.app_ref.root)
            self.app_ref._display_output("Salvataggio JSON", f"Dati narratologici salvati in {file_path}")
        except Exception as e:
            messagebox.showerror("Errore Salvataggio JSON", f"Errore durante il salvataggio del file JSON:\n{e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Salvataggio JSON", f"Errore: {e}")

    def carica_dati_narratologici_json(self):
        """Carica i dati narratologici (Greimas, Propp Utente, Tensori) da un file JSON."""
        file_path = filedialog.askopenfilename(
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")],
            title="Carica Dati Narratologici da JSON",
            parent=self.app_ref.root
        )

        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                dati_caricati = json.load(f)

            caricati = []
            if "matrice_greimas" in dati_caricati:
                self.matrice_greimas_data = dati_caricati["matrice_greimas"]
                caricati.append("Matrice Greimas")
            if "matrice_propp_utente" in dati_caricati:
                self.matrice_propp_data_utente = dati_caricati["matrice_propp_utente"]
                caricati.append("Matrice Propp (Utente)")
            if "tensori_narrativi" in dati_caricati:
                self.tensori_narrativi_data = dati_caricati["tensori_narrativi"]
                caricati.append("Tensori Narrativi")

            if caricati:
                messagebox.showinfo("Caricamento JSON", f"Dati narratologici caricati con successo da:\n{file_path}\nCaricati: {', '.join(caricati)}", parent=self.app_ref.root)
                self.app_ref._display_output("Caricamento JSON", f"Dati narratologici caricati da {file_path}: {', '.join(caricati)}")
                # Opzionale: visualizzare i dati caricati nell'area di output
                output_str = "Dati Narratologici Caricati:\n"
                if self.matrice_greimas_data:
                     output_str += "\nMatrice Greimas:\n" + "\n".join([f"  - {k}: {v}" for k,v in self.matrice_greimas_data.items()])
                if self.matrice_propp_data_utente:
                     output_str += "\nMatrice Propp (Utente):\n" + "\n".join([f"  - {k}: {v}" for k,v in self.matrice_propp_data_utente.items()])
                if self.tensori_narrativi_data:
                     output_str += "\nTensori Narrativi:\n" + "\n".join([f"  - {k}: {', '.join(v)}" for k,v in self.tensori_narrativi_data.items()])
                self.app_ref._display_output("Dati Narratologici Caricati", output_str)

            else:
                 messagebox.showwarning("Caricamento JSON", f"Nessun dato narratologico riconosciuto nel file:\n{file_path}", parent=self.app_ref.root)
                 self.app_ref._display_output("Caricamento JSON", f"Nessun dato riconosciuto nel file {file_path}")


        except json.JSONDecodeError:
            messagebox.showerror("Errore Caricamento JSON", f"Errore nel decodificare il file JSON.\nAssicurati che il file sia un JSON valido.", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Caricamento JSON", "Erro: Formato JSON non valido.")
        except Exception as e:
            messagebox.showerror("Errore Caricamento JSON", f"Errore durante il caricamento del file JSON:\n{e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Caricamento JSON", f"Errore: {e}")


    def salva_dati_narratologici_db(self):
        """Salva i dati narratologici (Greimas, Propp Utente, Tensori) in un database SQLite."""
        if not self.matrice_greimas_data and not self.matrice_propp_data_utente and not self.tensori_narrativi_data:
            messagebox.showwarning("Nessun Dato", "Non ci sono dati narratologici da salvare nel database.", parent=self.app_ref.root)
            return

        db_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("File Database SQLite", "*.db"), ("Tutti i file", "*.*")],
            title="Salva Dati Narratologici in Database SQLite",
            parent=self.app_ref.root
        )

        if not db_path:
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analisi_narratologica (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    nome_analisi TEXT,
                    dati_json TEXT
                )
            ''')

            num_records = 0
            if self.matrice_greimas_data:
                cursor.execute("INSERT INTO analisi_narratologica (nome_analisi, dati_json) VALUES (?, ?)",
                               ("Matrice Greimas", json.dumps(self.matrice_greimas_data)))
                num_records +=1
            if self.matrice_propp_data_utente:
                cursor.execute("INSERT INTO analisi_narratologica (nome_analisi, dati_json) VALUES (?, ?)",
                               ("Matrice Propp (Utente)", json.dumps(self.matrice_propp_data_utente)))
                num_records +=1
            if self.tensori_narrativi_data:
                cursor.execute("INSERT INTO analisi_narratologica (nome_analisi, dati_json) VALUES (?, ?)",
                               ("Tensori Narrativi", json.dumps(self.tensori_narrativi_data)))
                num_records +=1

            conn.commit()
            conn.close()
            messagebox.showinfo("Salvataggio Database",
                                f"{num_records} record narratologici salvati con successo nel database:\n{db_path}",
                                parent=self.app_ref.root)
            self.app_ref._display_output("Salvataggio Database", f"{num_records} record narratologici salvati in {db_path}")

        except sqlite3.Error as e:
            messagebox.showerror("Errore Database", f"Errore SQLite: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Database", f"Errore SQLite: {e}")
        except Exception as e:
            messagebox.showerror("Errore Salvataggio DB", f"Erro imprevisto durante il salvataggio nel database:\n{e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Salvataggio DB", f"Erro: {e}")

    def carica_dati_narratologici_db(self):
        """Carica i dati narratologici (Greimas, Propp Utente, Tensori) da un database SQLite."""
        db_path = filedialog.askopenfilename(
            filetypes=[("File Database SQLite", "*.db"), ("Tutti i file", "*.*")],
            title="Carica Dati Narratologici da Database SQLite",
            parent=self.app_ref.root
        )

        if not db_path:
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Verifica se la tabella esiste
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analisi_narratologica';")
            if not cursor.fetchone():
                 messagebox.showwarning("Errore Caricamento Database", f"Il database '{db_path}' non contiene la tabella 'analisi_narratologica'.", parent=self.app_ref.root)
                 conn.close()
                 return

            cursor.execute("SELECT nome_analisi, dati_json FROM analisi_narratologica ORDER BY timestamp DESC") # Carica i più recenti per tipo
            records = cursor.fetchall()
            conn.close()

            if not records:
                 messagebox.showwarning("Caricamento Database", f"Nessun record trovato nella tabella 'analisi_narratologica' del database:\n{db_path}", parent=self.app_ref.root)
                 self.app_ref._display_output("Caricamento Database", f"Nessun record trovato in {db_path}")
                 return

            # Carica i dati, prendendo il più recente per ogni tipo di analisi
            dati_caricati = {}
            for nome_analisi, dati_json in records:
                 if nome_analisi not in dati_caricati: # Prende solo il primo (il più recente per nome_analisi)
                     try:
                         dati_caricati[nome_analisi] = json.loads(dati_json)
                     except json.JSONDecodeError:
                         print(f"Erro nel decodificare JSON per record '{nome_analisi}'. Saltato.") # Stampa in console per debug
                         continue # Salta record corrotto

            caricati = []
            if "Matrice Greimas" in dati_caricati:
                self.matrice_greimas_data = dati_caricati["Matrice Greimas"]
                caricati.append("Matrice Greimas")
            if "Matrice Propp (Utente)" in dati_caricati:
                self.matrice_propp_data_utente = dati_caricati["Matrice Propp (Utente)"]
                caricati.append("Matrice Propp (Utente)")
            if "Tensori Narrativi" in dati_caricati:
                self.tensori_narrativi_data = dati_caricati["Tensori Narrativi"]
                caricati.append("Tensori Narrativi")

            if caricati:
                messagebox.showinfo("Caricamento Database", f"Dati narratologici caricati con successo dal database:\n{db_path}\nCaricati: {', '.join(caricati)}", parent=self.app_ref.root)
                self.app_ref._display_output("Caricamento Database", f"Dati narratologici caricati da {db_path}: {', '.join(caricati)}")
                 # Visualizza i dati caricati nell'area di output
                output_str = "Dati Narratologici Caricati dal Database:\n"
                if self.matrice_greimas_data:
                     output_str += "\nMatrice Greimas:\n" + "\n".join([f"  - {k}: {v}" for k,v in self.matrice_greimas_data.items()])
                if self.matrice_propp_data_utente:
                     output_str += "\nMatrice Propp (Utente):\n" + "\n".join([f"  - {k}: {v}" for k,v in self.matrice_propp_data_utente.items()])
                if self.tensori_narrativi_data:
                     output_str += "\nTensori Narrativi:\n" + "\n".join([f"  - {k}: {', '.join(v)}" for k,v in self.tensori_narrativi_data.items()])
                self.app_ref._display_output("Dati Narratologici Caricati", output_str)

            else:
                 messagebox.showwarning("Caricamento Database", f"Nessun dato narratologico riconosciuto o valido nel database:\n{db_path}", parent=self.app_ref.root)
                 self.app_ref._display_output("Caricamento Database", f"Nessun dato riconosciuto o valido in {db_path}")


        except sqlite3.Error as e:
            messagebox.showerror("Errore Database", f"Errore SQLite durante il caricamento: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Database", f"Errore SQLite: {e}")
        except Exception as e:
            messagebox.showerror("Errore Caricamento DB", f"Erro imprevisto durante il caricamento dal database:\n{e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Caricamento DB", f"Erro: {e}")


class FunzioniGrice:
    """Contiene funzioni per l'analisi preliminare basata sulle Massime Conversazionali di Grice."""
    def __init__(self, app_ref):
        self.app_ref = app_ref
        # HEDGING_TERMS è definito globalmente all'inizio del file

    def _check_corpus_e_nltk(self, check_punkt=False):
        """Controlla se il corpus è caricato e se NLTK e i suoi componenti sono disponibili."""
        if not self.app_ref.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.app_ref.root)
            return False
        if not nltk_disponibile:
            messagebox.showerror("NLTK Mancante", "La libreria NLTK è necessaria per questa funzionalità.", parent=self.app_ref.root)
            return False
        if check_punkt and not nltk_punkt_disponibile:
            messagebox.showerror("Dipendenza NLTK Mancante", "Il pacchetto 'punkt' di NLTK è necessario per questa funzionalità.\nScaricalo eseguendo in Python: nltk.download('punkt')", parent=self.app_ref.root)
            return False
        return True

    def analyze_gricean_indicators(self):
        """
        Analizza il corpus caricato per potenziali indicatori superficiali
        di violazioni delle massime di Grice (Quantità, Modo, Qualità).
        """
        if not self._check_corpus_e_nltk(check_punkt=True):
             return

        testo_completo = ' '.join(self.app_ref.corpus_testuale)

        self.app_ref._display_output("Analisi Griceana Semplificata", "Esecuzione analisi Griceana semplificata...")
        output_str = "--- Analisi Griceana Semplificata ---\n"
        output_str += f"Testo analizzato (primi 100 caratteri): \"{testo_completo[:100]}...\"" if len(testo_completo) > 100 else f"Testo analizzato: \"{testo_completo}\""
        output_str += "\n(Nota: Questa analisi è MOLTO semplificata e basata su indicatori superficiali. Non è un'analisi pragmatica completa.)\n"
        output_str += "----------------------------------------------------------------------------------------------------\n"


        try:
            # Usa la lingua impostata nelle funzioni di usabilità
            sentences = nltk.sent_tokenize(testo_completo, language=self.app_ref.funzioni_usability.lingua_analisi)
            num_sentences = len(sentences)
            output_str += f"\nNumero di frasi: {num_sentences}"

            if num_sentences == 0:
                output_str += "\nNessuna frase trovata per l'analisi."
                self.app_ref._display_output("Analisi Griceana Semplificata", output_str)
                return

            # Usa la lingua impostata per la tokenizzazione
            all_words = nltk.word_tokenize(testo_completo, language=self.app_ref.funzioni_usability.lingua_analisi)
            num_words = len(all_words)
            output_str += f"\nNumero totale di token (parole e punteggiatura): {num_words}"

            # Indicatori per la Massima della Quantità e del Modo (Concisezza/Prolissità)
            # Consideriamo solo le parole alfabetiche per la lunghezza media delle frasi
            sentence_word_lengths = []
            for s in sentences:
                words_in_sentence = [w for w in nltk.word_tokenize(s, language=self.app_ref.funzioni_usability.lingua_analisi) if w.isalpha()]
                sentence_word_lengths.append(len(words_in_sentence))


            if sentence_word_lengths and sum(sentence_word_lengths) > 0: # Assicura che ci siano parole in totale
                avg_sentence_length = sum(sentence_word_lengths) / len(sentence_word_lengths)
                output_str += f"\nLunghezza media delle frasi (solo parole alfabetiche): {avg_sentence_length:.2f}"

                # Semplici soglie per identificare frasi "troppo lunghe" o "troppo corte"
                # Queste soglie sono arbitrarie e dipendono dal tipo di testo!
                long_sentence_threshold = avg_sentence_length * 1.5
                short_sentence_threshold = avg_sentence_length * 0.5

                potential_quantity_manner_issues = []
                for i, s_len in enumerate(sentence_word_lengths):
                    original_sentence = sentences[i]
                    if s_len > long_sentence_threshold and s_len > 15: # Soglia minima per evitare frasi corte "lunghe" rispetto alla media bassa
                         potential_quantity_manner_issues.append(f"Frase {i+1} ({s_len} parole): Potrebbe essere troppo lunga o prolissa. \"{original_sentence[:70]}...\"")
                    elif s_len < short_sentence_threshold and s_len > 0 and s_len < 4: # Soglia massima per evitare frasi vuote/cortissime
                         potential_quantity_manner_issues.append(f"Frase {i+1} ({s_len} parole): Potrebbe essere troppo breve o poco informativa. \"{original_sentence[:70]}...\"")
                    elif s_len == 0 and original_sentence.strip(): # Frase non vuota ma senza parole alfabetiche (es. solo punteggiatura)
                         potential_quantity_manner_issues.append(f"Frase {i+1} (0 parole): Contiene solo punteggiatura o simboli. \"{original_sentence[:70]}...\"")


                if potential_quantity_manner_issues:
                    output_str += "\n\nPotenziali problemi di Quantità o Modo (basati sulla lunghezza delle frasi):"
                    for issue in potential_quantity_manner_issues:
                        output_str += f"\n- {issue}"
                else:
                    output_str += "\n\nLunghezza delle frasi nella norma (secondo questo semplice indicatore)."
            else:
                 output_str += "\n\nNon è stato possibile calcolare la lunghezza media delle frasi (nessuna parola alfabetica trovata)."


            # Ripetizioni semplici (potenziale violazione Quantità: Eccessivamente informativo? o Modo: Non conciso?)
            # Qui cerchiamo solo parole alfabetiche ripetute immediatamente vicine, un indicatore molto grossolano
            alpha_words_lower = [w.lower() for w in all_words if w.isalpha()]
            repeated_words = [alpha_words_lower[i] for i in range(len(alpha_words_lower)-1) if alpha_words_lower[i] == alpha_words_lower[i+1]]
            if repeated_words:
                output_str += f"\n\nPotenziali ripetizioni consecutive di parole (indicatore grezzo di Modo/Quantità): {set(repeated_words)}"
                output_str += "\n(Nota: Un'analisi vera richiederebbe il confronto tra frasi e una comprensione della retorica e del contesto.)"
            else:
                output_str += "\n\nNessuna ripetizione consecutiva di parole alfabetiche trovata."


            # Indicatori per la Massima della Qualità (Incertezza/Hedging - MOLTO LIMITATO)
            hedging_indicators_found = []
            words_lower = [w.lower() for w in all_words]
            for term in HEDGING_TERMS:
                if term in words_lower:
                    hedging_indicators_found.append(term)

            if hedging_indicators_found:
                output_str += f"\n\nPotenziali indicatori di incertezza/hedging (potenziale rilevanza per la Massima di Qualità): {set(hedging_indicators_found)}"
                output_str += "\n(Nota: La presenza di questi termini non significa necessariamente falsità, ma esitazione, mancanza di certezza o strategia retorica.)"
            else:
                output_str += "\n\nNessun indicatore superficiale di incertezza/hedging trovato."

            output_str += "\n\n--- Analisi Completata (Ricorda le Grandi Limitazioni) ---"
            output_str += "\nUna vera analisi Griceana richiede comprensione del contesto, intenzione, common sense e modelli linguistici molto avanzati."


        except Exception as e:
            output_str += f"\n\nSi è verificato un errore durante l'analisi Griceana: {e}"
            messagebox.showerror("Errore Analisi Griceana", f"Si è verificato un errore: {e}", parent=self.app_ref.root)

        self.app_ref._display_output("Analisi Griceana Semplificata", output_str)


# --- Classe Principale dell'Applicazione GUI ---

class StrumentiTestualiUsai:
    """Applicazione GUI principale per l'analisi testuale e narratologica."""
    def __init__(self, root):
        self.root = root
        self.root.title("Strumenti Testuali e Narratologici - Progetto di Luigi Usai")
        self.root.geometry("900x750") # Dimensione iniziale finestra leggermente più grande
        self.corpus_testuale = []
        self.nomi_file_corpus = []
        self.stopwords = set([ # Stopwords italiane di default (ampliate)
            "a", "ad", "al", "allo", "ai", "agli", "alla", "alle", "anche", "ancora", "aveva", "avevano",
            "avevo", "avrà", "avrai", "avranno", "avrebbe", "avrebbero", "avrei", "avremmo", "avremo",
            "avreste", "avresti", "avrete", "avevamo", "avevate", "c", "che", "chi", "ci", "ciò", "coi",
            "col", "come", "con", "contro", "cui", "da", "dal", "dallo", "dai", "dagli", "dalla",
            "dalle", "dei", "degli", "del", "dell", "della", "delle", "dello", "dentro", "di", "dice", "dietro",
            "dire", "disse", "dopo", "dove", "dovrà", "dovrebbe", "dovrei", "dovremmo", "dovremo", "dovreste",
            "dovresti", "dovrete", "dunque", "e", "è", "ebbe", "ebbero", "ed", "ecco", "era", "erano",
            "eravamo", "eravate", "ero", "esempio", "esse", "essendo", "essere", "essi", "esso", "faccia",
            "facciamo", "facciano", "faccio", "facemmo", "facendo", "facesse", "facessero", "facessi",
            "facessimo", "faceste", "facesti", "faceva", "facevamo", "facevano", "facevate", "fai", "fanno",
            "farà", "farai", "faranno", "fare", "farebbe", "farebbero", "farei", "faremmo", "faremo",
            "fareste", "faresti", "farete", "fece", "fecero", "fino", "fosse", "fossero", "fossi", "fossimo",
            "foste", "fosti", "fra", "fu", "furono", "già", "gli", "ha", "hai", "hanno", "ho", "i", "il",
            "in", "infatti", "inoltre", "invece", "io", "l", "la", "le", "lei", "li", "lo", "loro", "lui",
            "ma", "me", "mentre", "mi", "mia", "mie", "miei", "mio", "modo", "molto", "ne", "negli", "nei",
            "nel", "nell", "nella", "nelle", "nello", "nessuno", "noi", "non", "nostra", "nostre",
            "nostri", "nostro", "o", "ogni", "oppure", "ora", "per", "perché", "perciò", "però", "più",
            "poco", "possa", "possano", "posso", "potrebbe", "potrebbero", "potrei", "potremmo", "potremo",
            "potreste", "potresti", "potrete", "prima", "può", "pure", "qualsiasi", "quando", "quanta",
            "quante", "quanti", "quanto", "quella", "quelle", "quelli", "quello", "questa", "queste",
            "questi", "questo", "qui", "quindi", "sarà", "sarai", "saranno", "sarebbe", "sarebbero",
            "sarei", "saremmo", "saremo", "sareste", "saresti", "sarete", "se", "sé", "secondo", "sembra",
            "sembrava", "senza", "sette", "sia", "siamo", "siano", "siate", "siete", "significa", "solo",
            "sono", "sopra", "sotto", "sta", "stai", "stando", "stanno", "starà", "starai", "staranno",
            "starebbe", "starebbero", "starei", "staremmo", "staremo", "stareste", "staresti", "starete",
            "stata", "state", "stati", "stato", "stava", "stavamo", "stavano", "stavate", "stessa",
            "stesse", "stessi", "stesso", "stette", "stettero", "stetti", "stia", "stiamo", "stiano",
            "stiate", "sto", "su", "sua", "sue", "sugli", "sui", "sul", "sull", "sulla", "sulle", "sullo",
            "suoi", "suo", "t", "tale", "tali", "tanto", "te", "tempo", "ti", "tra", "tre", "tripla",
            "triplo", "troppo", "tu", "tua", "tue", "tuoi", "tuo", "tutta", "tuttavia", "tutte", "tutti",
            "tutto", "un", "una", "uno", "uomo", "va", "vai", "vale", "varie", "verso", "vi", "via", "voi",
            "volta", "volte", "vostra", "vostre", "vostri", "vostro"
        ])

        # Inizializza le classi per le funzionalità specifiche, passando il riferimento alla finestra principale
        self.funzioni_usability = FunzioniUsability(self)
        self.funzioni_narratologia = FunzioniNarratologia(self)
        self.funzioni_grice = FunzioniGrice(self)

        self.crea_interfaccia()

    def _get_processed_words(self, remove_stopwords=True, specific_text=None):
        """Ottiene una lista di parole dal corpus o da un testo specifico, opzionalmente rimuovendo le stopwords."""
        testo_da_processare = ' '.join(self.corpus_testuale) if specific_text is None else specific_text
        if not testo_da_processare:
            return []
        # Usa re per trovare sequenze alfabetiche, più robusto della semplice split
        parole = re.findall(r'\b\w+\b', testo_da_processare.lower())
        if remove_stopwords:
            parole = [parola for parola in parole if parola not in self.stopwords]
        return parole

    def crea_interfaccia(self):
        """Crea l'interfaccia grafica principale dell'applicazione."""
        # --- Creazione della Barra dei Menu ---
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # -- Menu File --
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Carica Corpus Testuale (.txt)...", command=self.carica_corpus)
        file_menu.add_separator()
        # Sottomenu per Salvataggio Dati Narratologici
        salva_dati_narr_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Salva Dati Narratologici", menu=salva_dati_narr_menu)
        salva_dati_narr_menu.add_command(label="Salva come JSON...", command=self.funzioni_narratologia.salva_dati_narratologici_json)
        salva_dati_narr_menu.add_command(label="Salva in Database SQLite...", command=self.funzioni_narratologia.salva_dati_narratologici_db)
        # Sottomenu per Caricamento Dati Narratologici
        carica_dati_narr_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Carica Dati Narratologici", menu=carica_dati_narr_menu)
        carica_dati_narr_menu.add_command(label="Carica da JSON...", command=self.funzioni_narratologia.carica_dati_narratologici_json)
        carica_dati_narr_menu.add_command(label="Carica da Database SQLite...", command=self.funzioni_narratologia.carica_dati_narratologici_db)

        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.root.quit)

        # -- Menu Strumenti Linguistici --
        strumenti_linguistici_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Strumenti Linguistici", menu=strumenti_linguistici_menu)
        strumenti_linguistici_menu.add_command(label="Gestione Stopword...", command=self.gestione_stopword)
        strumenti_linguistici_menu.add_separator()
        strumenti_linguistici_menu.add_command(label="Frequenza Termini...", command=self.frequenza_termini)
        # Controlla disponibilità WordCloud/Matplotlib prima di aggiungere
        if wordcloud_disponibile and matplotlib_disponibile:
             strumenti_linguistici_menu.add_command(label="Nuvola di Parole...", command=self.nuvola_parole)
             strumenti_linguistici_menu.add_command(label="Andamento Termini...", command=self.andamento)

        strumenti_linguistici_menu.add_command(label="Collocazioni (N-grammi)...", command=self.collocazioni)
        strumenti_linguistici_menu.add_command(label="KWIC (Parole Chiave nel Contesto)...", command=self.kwic)
        strumenti_linguistici_menu.add_command(label="Rete Co-occorrenze (Testuale)...", command=self.vista_rete)


        # -- Menu Usabilità e Leggibilità --
        usability_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Usabilità e Leggibilità", menu=usability_menu)
        # La lingua è usata da diverse funzioni NLTK
        if nltk_disponibile:
             usability_menu.add_command(label="Imposta Lingua Analisi...", command=self.funzioni_usability.imposta_lingua_analisi)
             usability_menu.add_separator()

        # Controlla disponibilità NLTK Punkt prima di aggiungere
        if nltk_disponibile and nltk_punkt_disponibile:
            usability_menu.add_command(label="Suddivisione in Frasi...", command=self.funzioni_usability.subdividi_in_frasi)
            usability_menu.add_command(label="Suddivisione in Token...", command=self.funzioni_usability.subdividi_in_token)
            # Gulpease è specifico italiano, ma richiede punkt
            usability_menu.add_command(label="Indice Leggibilità Gulpease (Globale)...", command=self.funzioni_usability.calcola_gulpease_globale)
            usability_menu.add_command(label="Analisi Leggibilità per Frase (Gulpease)...", command=self.funzioni_usability.analisi_leggibilita_per_frase)
        # Controlla disponibilità NLTK Tagger prima di aggiungere (richiede anche punkt)
        if nltk_disponibile and nltk_punkt_disponibile and nltk_tagger_disponibile:
             usability_menu.add_command(label="Annotazione Morfosintattica (POS)...", command=self.funzioni_usability.annotazione_pos)

        # -- Menu Narratologia --
        narratologia_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Narratologia", menu=narratologia_menu)
        narratologia_menu.add_command(label="Definisci Matrice Greimas...", command=self.funzioni_narratologia.crea_matrice_greimas)
        narratologia_menu.add_command(label="Definisci Funzioni di Propp (Personalizzate)...", command=self.funzioni_narratologia.crea_matrice_propp)
        narratologia_menu.add_command(label="Definisci Tensori Narrativi (Luigi Usai)...", command=self.funzioni_narratologia.crea_tensori_narrativi)
        narratologia_menu.add_separator()
        narratologia_menu.add_command(label="Genera Trame (Permutazioni Propp)...", command=self.funzioni_narratologia.genera_permutazioni_propp)
        narratologia_menu.add_command(label="Genera Sottoinsiemi (Combinazioni Propp)...", command=self.funzioni_narratologia.genera_combinazioni_propp)
        # Controlla disponibilità Graphviz prima di aggiungere
        if graphviz_disponibile:
             narratologia_menu.add_command(label="Visualizza Sequenza Propp (Grafico)...", command=self.funzioni_narratologia.visualizza_sequenza_propp_input)


        # -- Menu Analisi Avanzate --
        analisi_avanzate_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analisi Avanzate", menu=analisi_avanzate_menu)
        # Controlla disponibilità NLTK Punkt prima di aggiungere Grice
        if nltk_disponibile and nltk_punkt_disponibile:
             analisi_avanzate_menu.add_command(label="Indicatori Griceani (Semplificato)...", command=self.funzioni_grice.analyze_gricean_indicators)


        # -- Menu About --
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="Informazioni su...", command=self.mostra_about)

        # Area di testo per visualizzare il corpus
        corpus_frame = tk.LabelFrame(self.root, text="Corpus Caricato", padx=5, pady=5)
        corpus_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5,5))
        self.area_testo = scrolledtext.ScrolledText(corpus_frame, wrap=tk.WORD, height=15, width=100, font=("Arial", 10))
        self.area_testo.pack(fill=tk.BOTH, expand=True)
        self.area_testo.insert(tk.END, "Il corpus testuale verrà visualizzato qui dopo il caricamento.\n")
        self.area_testo.config(state=tk.DISABLED)

        # Area di testo per visualizzare l'output delle analisi
        output_frame = tk.LabelFrame(self.root, text="Risultati Analisi", padx=5, pady=5)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5,10))
        self.output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10, width=100, font=("Arial", 10))
        self.output_area.pack(fill=tk.BOTH, expand=True)
        self.output_area.insert(tk.END, "L'output delle analisi verrà visualizzato qui.\n")
        self.output_area.config(state=tk.DISABLED)

    def mostra_about(self):
        """Mostra la finestra di About con le informazioni sull'autore e il progetto."""
        about_window = tk.Toplevel(self.root)
        about_window.title("Informazioni su Strumenti Testuali")
        about_window.geometry("450x500") # Aumentata altezza per foto e testo
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()

        tk.Label(about_window, text="Strumenti Testuali e Narratologici", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        tk.Label(about_window, text="Versione 2.0", font=("Arial", 10)).pack()

        info_frame = tk.Frame(about_window, pady=10)
        info_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(info_frame, text="Autore:", font=("Arial", 12, "italic")).pack(pady=(10,0))
        tk.Label(info_frame, text="Luigi Usai", font=("Arial", 14, "bold")).pack()
        tk.Label(info_frame, text="Quartucciu (CA), Italia", font=("Arial", 11)).pack(pady=(0,15))

        # Caricamento e visualizzazione immagine solo se Pillow è disponibile
        if pil_disponibile:
            try:
                # Assicurati che 'luigi.jpg' sia nella stessa cartella dello script
                # o fornisci il percorso completo.
                img_path = "luigi.jpg"
                pil_image = Image.open(img_path)

                # Ridimensionamento immagine se necessario
                base_width = 200
                w_percent = (base_width / float(pil_image.size[0]))
                h_size = int((float(pil_image.size[1]) * float(w_percent)))
                # Usa Image.Resampling.LANCZOS per Pillow >= 9.1.0, altrimenti Image.ANTIALIAS (deprecato)
                try:
                    pil_image_resized = pil_image.resize((base_width, h_size), Image.Resampling.LANCZOS)
                except AttributeError: # Per compatibilità con vecchie versioni Pillow
                    try:
                         pil_image_resized = pil_image.resize((base_width, h_size), Image.ANTIALIAS)
                    except AttributeError: # Se ANTIALIAS non esiste più
                         pil_image_resized = pil_image.resize((base_width, h_size)) # Ridimensionamento base


                self.author_photo = ImageTk.PhotoImage(pil_image_resized) # Salva riferimento
                img_label = tk.Label(info_frame, image=self.author_photo)
                img_label.pack(pady=10)
            except FileNotFoundError:
                tk.Label(info_frame, text="Immagine 'luigi.jpg' non trovata.", font=("Arial", 9), fg="red").pack(pady=5)
            except Exception as e:
                tk.Label(info_frame, text=f"Erro caricamento immagine: {e}", font=("Arial", 9), fg="red").pack(pady=5)
        else:
            tk.Label(info_frame, text="Libreria Pillow (PIL) non disponibile per visualizzare l'immagine.", font=("Arial", 9), fg="orange").pack(pady=5)


        tk.Label(info_frame, text="Progetto per l'analisi testuale, linguistica e narratologica.", font=("Arial", 10)).pack(pady=(10,0))
        tk.Label(info_frame, text="Include strumenti basati su modelli classici (Propp, Greimas) e concetti innovativi (Tensori Narrativi).", font=("Arial", 9)).pack()
        tk.Label(info_frame, text="Riferimenti: Harvard Dataverse (DOI:10.7910/DVN/ICOJ19) e pubblicazioni correlate.", font=("Arial", 9)).pack()
        tk.Label(info_frame, text="GitHub: https://github.com/luigiusai/LuigiUsaiTools", font=("Arial", 9)).pack()


        close_button = tk.Button(about_window, text="Chiudi", command=about_window.destroy, width=10)
        close_button.pack(pady=15)


    def _display_output(self, title, content):
        """Visualizza l'output formattato nell'area di testo dedicata."""
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, f"--- {title} ---\n\n{content}")
        self.output_area.config(state=tk.DISABLED)

    def carica_corpus(self):
        """Permette all'utente di selezionare e caricare uno o più file di testo nel corpus."""
        nomi_file = filedialog.askopenfilenames(
            title="Seleziona file di testo (.txt)",
            filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")]
        )
        if not nomi_file:
            return

        self.corpus_testuale = []
        self.nomi_file_corpus = []
        self.area_testo.config(state=tk.NORMAL)
        self.area_testo.delete(1.0, tk.END)

        problematic_files = []
        success_count = 0

        for nome_file in nomi_file:
            try:
                # Tenta di leggere con codifica UTF-8, poi ISO-8859-1 se fallisce
                try:
                    with open(nome_file, 'r', encoding='utf-8') as f:
                        contenuto = f.read()
                except UnicodeDecodeError:
                     with open(nome_file, 'r', encoding='iso-8859-1') as f:
                        contenuto = f.read()

                self.corpus_testuale.append(contenuto)
                # Estrai solo il nome del file dal percorso completo
                nome_semplice = nome_file.split('/')[-1].split('\\')[-1] # Gestisce sia / che \
                self.nomi_file_corpus.append(nome_semplice)
                # Mostra solo i primi N caratteri del contenuto nell'area di testo del corpus per non sovraccaricare la GUI
                anteprima_contenuto = contenuto[:2000] + '...' if len(contenuto) > 2000 else contenuto
                self.area_testo.insert(tk.END, f"--- Contenuto di: {self.nomi_file_corpus[-1]} ---\n{anteprima_contenuto}\n\n")
                success_count += 1
            except Exception as e:
                nome_semplice = nome_file.split('/')[-1].split('\\')[-1]
                problematic_files.append(f"{nome_semplice}: {e}")

        self.area_testo.config(state=tk.DISABLED)

        if success_count > 0:
            messagebox.showinfo("Corpus Caricato", f"{success_count} file caricati con successo nel corpus.", parent=self.root)
            self._display_output("Corpus Caricato", f"{success_count} file caricati.\nNomi: {', '.join(self.nomi_file_corpus)}")

        if problematic_files:
            messagebox.showwarning("Problemi nel Caricamento",
                                   f"Alcuni file non sono stati caricati o hanno causato errori:\n" +
                                   "\n".join(problematic_files), parent=self.root)
            if success_count == 0:
                 self._display_output("Errore Caricamento Corpus", "Nessun file è stato caricato correttamente.")


    def gestione_stopword(self):
        """Gestisce l'aggiunta, rimozione e caricamento di stopwords."""
        sw_window = tk.Toplevel(self.root)
        sw_window.title("Gestione Stopwords")
        sw_window.geometry("500x550")
        sw_window.resizable(False, False)
        sw_window.transient(self.root)
        sw_window.grab_set()

        tk.Label(sw_window, text="Stopwords Correnti:", font=("Arial", 11, "bold")).pack(pady=(10,2))

        sw_listbox_frame = tk.Frame(sw_window)
        sw_listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        sw_scrollbar = tk.Scrollbar(sw_listbox_frame, orient=tk.VERTICAL)
        sw_listbox = tk.Listbox(sw_listbox_frame, yscrollcommand=sw_scrollbar.set, selectmode=tk.EXTENDED, font=("Arial", 10))
        sw_scrollbar.config(command=sw_listbox.yview)
        sw_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        sw_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Popola la listbox con le stopwords correnti
        for sw in sorted(list(self.stopwords)):
            sw_listbox.insert(tk.END, sw)

        entry_frame = tk.Frame(sw_window)
        entry_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(entry_frame, text="Nuova Stopword:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0,5))
        sw_entry = tk.Entry(entry_frame, width=35, font=("Arial", 10))
        sw_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        def add_sw():
            new_sw = sw_entry.get().strip().lower()
            if new_sw:
                if new_sw not in self.stopwords:
                    self.stopwords.add(new_sw)
                    # Aggiorna la listbox mantenendo l'ordine alfabetico
                    items = sorted(list(self.stopwords))
                    sw_listbox.delete(0, tk.END)
                    for item in items:
                        sw_listbox.insert(tk.END, item)
                    sw_entry.delete(0, tk.END)
                    # Seleziona e mostra la nuova stopword aggiunta
                    if new_sw in items:
                        idx = items.index(new_sw)
                        sw_listbox.see(idx)
                        sw_listbox.selection_clear(0, tk.END)
                        sw_listbox.selection_set(idx)
                    self._display_output("Stopwords Aggiornate", f"Aggiunta: '{new_sw}'. Lista attuale ({len(self.stopwords)}): {', '.join(sorted(list(self.stopwords)))[:500]}...")
                else:
                    messagebox.showinfo("Duplicato", f"'{new_sw}' è già presente nella lista delle stopwords.", parent=sw_window)
            else:
                messagebox.showwarning("Input Vuoto", "Inserisci una parola da aggiungere come stopword.", parent=sw_window)

        def remove_sw():
            selected_indices = sw_listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Nessuna Selezione", "Seleziona una o più stopwords da rimuovere.", parent=sw_window)
                return
            removed_sws = []
            # Rimuovi partendo dall'ultimo indice per evitare problemi con l'aggiornamento degli indici
            for i in reversed(selected_indices):
                sw_to_remove = sw_listbox.get(i)
                self.stopwords.discard(sw_to_remove)
                sw_listbox.delete(i)
                removed_sws.append(sw_to_remove)
            if removed_sws:
                messagebox.showinfo("Stopwords Rimosse", f"Rimosse con successo: {', '.join(reversed(removed_sws))}", parent=sw_window)
            # Aggiorna l'output per mostrare le stopwords attuali
            self._display_output("Stopwords Aggiornate", f"Rimosse: {', '.join(reversed(removed_sws))}. Lista attuale ({len(self.stopwords)}): {', '.join(sorted(list(self.stopwords)))[:500]}...")


        def load_default_stopwords():
            # Lista di stopwords italiane predefinite (può essere caricata da un file esterno in futuro)
            default_ita_sw = set([
                "a", "ad", "al", "allo", "ai", "agli", "alla", "alle", "anche", "ancora", "aveva", "avevano",
                "avevo", "avrà", "avrai", "avranno", "avrebbe", "avrebbero", "avrei", "avremmo", "avremo",
                "avreste", "avresti", "avrete", "avevamo", "avevate", "c", "che", "chi", "ci", "ciò", "coi",
                "col", "come", "con", "contro", "cui", "da", "dal", "dallo", "dai", "dagli", "dalla",
                "dalle", "dei", "degli", "del", "dell", "della", "delle", "dello", "dentro", "di", "dice", "dietro",
                "dire", "disse", "dopo", "dove", "dovrà", "dovrebbe", "dovrei", "dovremmo", "dovremo", "dovreste",
                "dovresti", "dovrete", "dunque", "e", "è", "ebbe", "ebbero", "ed", "ecco", "era", "erano",
                "eravamo", "eravate", "ero", "esempio", "esse", "essendo", "essere", "essi", "esso", "faccia",
                "facciamo", "facciano", "faccio", "facemmo", "facendo", "facesse", "facessero", "facessi",
                "facessimo", "faceste", "facesti", "faceva", "facevamo", "facevano", "facevate", "fai", "fanno",
                "farà", "farai", "faranno", "fare", "farebbe", "farebbero", "farei", "faremmo", "faremo",
                "fareste", "faresti", "farete", "fece", "fecero", "fino", "fosse", "fossero", "fossi", "fossimo",
                "foste", "fosti", "fra", "fu", "furono", "già", "gli", "ha", "hai", "hanno", "ho", "i", "il",
                "in", "infatti", "inoltre", "invece", "io", "l", "la", "le", "lei", "li", "lo", "loro", "lui",
                "ma", "me", "mentre", "mi", "mia", "mie", "miei", "mio", "modo", "molto", "ne", "negli", "nei",
                "nel", "nell", "nella", "nelle", "nello", "nessuno", "noi", "non", "nostra", "nostre",
                "nostri", "nostro", "o", "ogni", "oppure", "ora", "per", "perché", "perciò", "però", "più",
                "poco", "possa", "possano", "posso", "potrebbe", "potrebbero", "potrei", "potremmo", "potremo",
                "potreste", "potresti", "potrete", "prima", "può", "pure", "qualsiasi", "quando", "quanta",
                "quante", "quanti", "quanto", "quella", "quelle", "quelli", "quello", "questa", "queste",
                "questi", "questo", "qui", "quindi", "sarà", "sarai", "saranno", "sarebbe", "sarebbero",
                "sarei", "saremmo", "saremo", "sareste", "saresti", "sarete", "se", "sé", "secondo", "sembra",
                "sembrava", "senza", "sette", "sia", "siamo", "siano", "siate", "siete", "significa", "solo",
                "sono", "sopra", "sotto", "sta", "stai", "stando", "stanno", "starà", "starai", "staranno",
                "starebbe", "starebbero", "starei", "staremmo", "staremo", "stareste", "staresti", "starete",
                "stata", "state", "stati", "stato", "stava", "stavamo", "stavano", "stavate", "stessa",
                "stesse", "stessi", "stesso", "stette", "stettero", "stetti", "stia", "stiamo", "stiano",
                "stiate", "sto", "su", "sua", "sue", "sugli", "sui", "sul", "sull", "sulla", "sulle", "sullo",
                "suoi", "suo", "t", "tale", "tali", "tanto", "te", "tempo", "ti", "tra", "tre", "tripla",
                "triplo", "troppo", "tu", "tua", "tue", "tuoi", "tuo", "tutta", "tuttavia", "tutte", "tutti",
                "tutto", "un", "una", "uno", "uomo", "va", "vai", "vale", "varie", "verso", "vi", "via", "voi",
                "volta", "volte", "vostra", "vostre", "vostri", "vostro"
            ])
            self.stopwords.update(default_ita_sw) # Aggiunge le default senza rimuovere quelle esistenti
            # Aggiorna la listbox
            items = sorted(list(self.stopwords))
            sw_listbox.delete(0, tk.END)
            for item in items:
                sw_listbox.insert(tk.END, item)
            messagebox.showinfo("Stopwords Caricate", f"Lista di stopwords italiane predefinite ({len(default_ita_sw)} termini) caricata/aggiornata.", parent=sw_window)
            self._display_output("Stopwords Aggiornate", f"Lista stopwords attuale ({len(self.stopwords)}): {', '.join(sorted(list(self.stopwords)))[:500]}...") # Mostra solo i primi 500 caratteri


        button_frame_actions = tk.Frame(sw_window)
        button_frame_actions.pack(pady=10)
        tk.Button(button_frame_actions, text="Aggiungi", command=add_sw, width=12, height=1).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame_actions, text="Rimuovi Selez.", command=remove_sw, width=12, height=1).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame_actions, text="Carica Default (ITA)", command=load_default_stopwords, width=18, height=1).pack(side=tk.LEFT, padx=5)

        tk.Button(sw_window, text="Chiudi", command=sw_window.destroy, width=10, height=1).pack(pady=15)

        self.root.wait_window(sw_window)


    def frequenza_termini(self):
        """Calcola e visualizza la frequenza dei termini nel corpus (stopwords escluse)."""
        if not self.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.root)
            return

        parole = self._get_processed_words(remove_stopwords=True)
        if not parole:
            self._display_output("Frequenza Termini", "Il corpus non contiene parole valide dopo il filtraggio delle stopwords.")
            messagebox.showinfo("Frequenza Termini", "Nessuna parola da analizzare dopo la rimozione delle stopwords.", parent=self.root)
            return

        frequenze = Counter(parole)
        num_termini = simpledialog.askinteger("Numero Termini", "Quanti termini più frequenti vuoi visualizzare?",
                                              parent=self.root, minvalue=1, initialvalue=20)
        if num_termini is None:
            return

        output_str = f"I {num_termini} termini più frequenti (stopwords escluse):\n"
        output_str += "--------------------------------------------------\n"
        for parola, freq in frequenze.most_common(num_termini):
            output_str += f"{parola}: {freq}\n"
        self._display_output("Frequenza Termini", output_str)

    def nuvola_parole(self):
        """Genera e visualizza una nuvola di parole dal corpus (stopwords escluse)."""
        if not wordcloud_disponibile or not matplotlib_disponibile:
             messagebox.showerror("Librerie Mancanti", "Le librerie 'wordcloud' e 'matplotlib' sono necessarie per questa funzionalità.", parent=self.root)
             return

        if not self.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.root)
            return

        parole = self._get_processed_words(remove_stopwords=True)
        if not parole:
            self._display_output("Nuvola di Parole", "Nessuna parola da visualizzare (corpus vuoto o solo stopwords).")
            messagebox.showwarning("Attenzione", "Il corpus è vuoto o non contiene parole valide dopo la rimozione delle stopwords.", parent=self.root)
            return

        frequenze = Counter(parole)
        if not frequenze:
            messagebox.showwarning("Attenzione", "Nessuna frequenza da visualizzare per la nuvola di parole.", parent=self.root)
            return

        try:
            # Generate word cloud from frequencies
            wordcloud = WordCloud(width=800, height=400, background_color='white',
                                  stopwords=None, # Le stopwords sono già state rimosse prima
                                  colormap='viridis',
                                  max_words=150
                                 ).generate_from_frequencies(frequenze)

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title("Nuvola di Parole (Senza Stopwords) - Progetto di Luigi Usai", fontsize=14)
            plt.tight_layout(pad=0)
            plt.show()
            self._display_output("Nuvola di Parole", "Nuvola di parole generata e visualizzata con successo.")
        except Exception as e:
            messagebox.showerror("Errore WordCloud", f"Errore durante la generazione della nuvola di parole: {e}", parent=self.root)
            self._display_output("Nuvola di Parole", f"Errore durante la generazione: {e}")


    def collocazioni(self):
        """Calcola e visualizza le collocazioni (N-grammi) più frequenti nel corpus (stopwords escluse)."""
        if not self.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.root)
            return

        n_gram_size = simpledialog.askinteger("Dimensione N-gram", "Inserisci la dimensione per le collocazioni (es. 2 per bigrammi, 3 per trigrammi):",
                                              parent=self.root, minvalue=2, maxvalue=5, initialvalue=2)
        if n_gram_size is None: return

        num_colloc = simpledialog.askinteger("Numero Collocazioni", "Quante collocazioni più frequenti vuoi visualizzare?",
                                             parent=self.root, minvalue=1, initialvalue=10)
        if num_colloc is None: return

        parole = self._get_processed_words(remove_stopwords=True)
        if len(parole) < n_gram_size:
            self._display_output("Collocazioni", f"Testo insufficiente per formare {n_gram_size}-grammi dopo la rimozione delle stopwords.")
            messagebox.showinfo("Collocazioni", f"Non ci sono abbastanza parole ({len(parole)}) per creare {n_gram_size}-grammi.", parent=self.root)
            return

        # Genera gli N-grammi
        ngrams_list = [" ".join(parole[i:i+n_gram_size]) for i in range(len(parole)-n_gram_size+1)]

        if not ngrams_list:
            self._display_output("Collocazioni", "Nessuna collocazione trovata (possibile dopo filtraggio).")
            return

        frequenze_colloc = Counter(ngrams_list)

        output_str = f"Le {num_colloc} {n_gram_size}-grammi più frequenti (stopwords escluse):\n"
        output_str += "--------------------------------------------------\n"
        for colloc, freq in frequenze_colloc.most_common(num_colloc):
            output_str += f"'{colloc}': {freq}\n"
        self._display_output("Collocazioni", output_str)


    def kwic(self):
        """Esegue l'analisi KWIC (Keyword In Context) per una parola chiave."""
        if not self.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.root)
            return

        parola_chiave = simpledialog.askstring("Parola Chiave (KWIC)", "Inserisci la parola chiave da cercare:", parent=self.root)
        if not parola_chiave:
            return

        contesto_size = simpledialog.askinteger("Dimensione Contesto", "Quante parole di contesto visualizzare prima e dopo la parola chiave?",
                                                 parent=self.root, minvalue=1, maxvalue=20, initialvalue=5)
        if contesto_size is None: return

        parola_chiave_lower = parola_chiave.strip().lower()
        results_kwic = []
        max_results_display = 200 # Limita il numero di risultati visualizzati

        testo_completo_originale = ' '.join(self.corpus_testuale)
        # Tokenizza mantenendo la punteggiatura per un contesto più fedele
        tokens_original_case = re.findall(r'\b\w+\b|[\.,;!?\'"\(\)]', testo_completo_originale) # Aggiunti altri segni di punteggiatura/simboli comuni
        tokens_lower_case = [t.lower() for t in tokens_original_case]

        found_count = 0
        for i, token_lower in enumerate(tokens_lower_case):
            if token_lower == parola_chiave_lower:
                found_count +=1
                if found_count > max_results_display:
                    results_kwic.append(f"\n--- (Visualizzazione limitata ai primi {max_results_display} risultati su {found_count-1} trovati) ---")
                    break

                start_idx = max(0, i - contesto_size)
                end_idx = min(len(tokens_original_case), i + contesto_size + 1)

                contesto_sx_list = tokens_original_case[start_idx:i]
                parola_target = tokens_original_case[i]
                contesto_dx_list = tokens_original_case[i+1:end_idx]

                # Ricostruisci le stringhe di contesto gestendo spazi e punteggiatura
                contesto_sx_str = ""
                for k_idx, k_tok in enumerate(contesto_sx_list):
                    contesto_sx_str += k_tok
                    # Aggiungi spazio solo se non è l'ultimo token e il token successivo non è punteggiatura
                    if k_idx < len(contesto_sx_list) -1 and not re.match(r'^[\.,;!?\'"\(\)]$', contesto_sx_list[k_idx+1]):
                         contesto_sx_str += " "
                    # Aggiungi spazio se è l'ultimo token SX e la parola target non è punteggiatura
                    elif k_idx == len(contesto_sx_list) -1 and not re.match(r'^[\.,;!?\'"\(\)]$', parola_target):
                        contesto_sx_str += " "

                contesto_dx_str = ""
                for k_idx, k_tok in enumerate(contesto_dx_list):
                     # Aggiungi spazio prima del token DX solo se non è il primo token DX e il token precedente non è punteggiatura
                    if k_idx > 0 and not re.match(r'^[\.,;!?\'"\(\)]$', k_tok) and not re.match(r'^[\.,;!?\'"\(\)]$', contesto_dx_list[k_idx-1]):
                        contesto_dx_str += " "
                    # Aggiungi spazio prima del primo token DX se la parola target non è punteggiatura
                    elif k_idx == 0 and not re.match(r'^[\.,;!?\'"\(\)]$', k_tok) and not re.match(r'^[\.,;!?\'"\(\)]$', parola_target):
                         contesto_dx_str += " "
                    contesto_dx_str += k_tok


                results_kwic.append(f"...{contesto_sx_str}[{parola_target}]{contesto_dx_str}...")

        if results_kwic:
            output_str = f"KWIC per '{parola_chiave}' (contesto: {contesto_size} token, {found_count} occorrenze trovate):\n\n" + "\n".join(results_kwic)
        else:
            output_str = f"Nessuna occorrenza trovata per '{parola_chiave}' nel corpus."
        self._display_output(f"KWIC: {parola_chiave}", output_str)


    def andamento(self):
        """Visualizza l'andamento della frequenza di un termine attraverso i documenti o segmenti di un singolo documento."""
        if not matplotlib_disponibile:
             messagebox.showerror("Libreria Mancante", "La libreria 'matplotlib' è necessaria per questa funzionalità.", parent=self.root)
             return

        if not self.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.root)
            return

        parola_chiave = simpledialog.askstring("Andamento Termine", "Inserisci la parola chiave per l'analisi dell'andamento:", parent=self.root)
        if not parola_chiave: return

        parola_chiave_lower = parola_chiave.strip().lower()
        frequencies = []
        segment_labels = []

        if len(self.corpus_testuale) == 1:
            # Analisi per segmenti all'interno di un singolo documento
            num_chunks = simpledialog.askinteger("Numero Segmenti", "Dividi il documento in quanti segmenti per l'analisi?",
                                                 parent=self.root, minvalue=2, maxvalue=100, initialvalue=10)
            if num_chunks is None: return

            # Ottieni tutte le parole del documento (senza rimuovere stopwords per mantenere la lunghezza originale)
            words_in_doc = re.findall(r'\b\w+\b', self.corpus_testuale[0].lower())

            if not words_in_doc:
                self._display_output("Andamento Termine", "Il documento selezionato è vuoto o non contiene parole.")
                messagebox.showwarning("Andamento Termine", "Il documento selezionato è vuoto o non contiene parole.", parent=self.root)
                return

            if len(words_in_doc) < num_chunks :
                 # Se il numero di parole è inferiore al numero di segmenti richiesti, adatta il numero di segmenti
                 messagebox.showwarning("Segmenti Eccessivi", f"Il documento contiene solo {len(words_in_doc)} parole. Non può essere diviso in {num_chunks} segmenti. Verrà usato un segmento per parola (max {len(words_in_doc)} segmenti).", parent=self.root)
                 num_chunks = len(words_in_doc)
                 if num_chunks < 1:
                     self._display_output("Andamento Termine", "Il documento non ha parole per creare segmenti.")
                     return

            # Calcola la dimensione approssimativa di ogni segmento
            chunk_size = max(1, len(words_in_doc) // num_chunks)

            for i in range(num_chunks):
                # Definisci gli indici di inizio e fine per il segmento corrente
                start_idx = i * chunk_size
                # L'ultimo segmento prende tutte le parole rimanenti
                end_idx = (i + 1) * chunk_size if i < num_chunks - 1 else len(words_in_doc)
                chunk = words_in_doc[start_idx:end_idx]

                if chunk: # Assicurati che il segmento non sia vuoto
                    frequencies.append(chunk.count(parola_chiave_lower))
                    segment_labels.append(f"Seg. {i+1}")

            if not frequencies:
                self._display_output("Andamento Termine", f"La parola '{parola_chiave}' non è stata trovata o i segmenti erano vuoti.")
                messagebox.showinfo("Andamento Termine", f"La parola '{parola_chiave}' non è stata trovata o i segmenti erano vuoti.", parent=self.root)
                return

            plot_title = f"Andamento di '{parola_chiave}' (Doc. '{self.nomi_file_corpus[0]}' in {num_chunks} segmenti)"
            plot_xlabel = "Segmento del Testo"
            plot_type = 'line' # Grafico a linea per l'andamento sequenziale

        else:
            # Analisi attraverso documenti multipli
            for i, testo_doc in enumerate(self.corpus_testuale):
                # Ottieni tutte le parole del documento (senza rimuovere stopwords per contare su base totale)
                parole_doc = re.findall(r'\b\w+\b', testo_doc.lower())
                frequencies.append(parole_doc.count(parola_chiave_lower))
                segment_labels.append(self.nomi_file_corpus[i] if self.nomi_file_corpus and i < len(self.nomi_file_corpus) else f"Doc {i+1}")

            plot_title = f"Andamento di '{parola_chiave}' attraverso i Documenti Caricati"
            plot_xlabel = "Documento"
            plot_type = 'bar' # Grafico a barre per confronto tra documenti

        # Controlla se la parola chiave è stata trovata almeno una volta in tutto il corpus
        if not frequencies or all(f == 0 for f in frequencies):
            self._display_output("Andamento Termine", f"Nessuna occorrenza di '{parola_chiave}' trovata nel corpus per il grafico.")
            messagebox.showinfo("Andamento Termine", f"La parola '{parola_chiave}' non è stata trovata nel corpus.", parent=self.root)
            return

        # Genera il grafico
        plt.figure(figsize=(12, 7))
        if plot_type == 'line':
            plt.plot(segment_labels, frequencies, marker='o', linestyle='-', color='dodgerblue')
        else: # plot_type == 'bar'
            plt.bar(segment_labels, frequencies, color='skyblue')

        plt.title(plot_title, fontsize=14)
        plt.xlabel(plot_xlabel, fontsize=12)
        plt.ylabel("Frequenza Assoluta", fontsize=12)
        # Ruota le etichette sull'asse x se sono molte per evitare sovrapposizioni
        if len(segment_labels) > 10:
             plt.xticks(rotation=45, ha="right", fontsize=10)
        else:
             plt.xticks(fontsize=10)

        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='--')
        plt.tight_layout() # Adatta il layout per evitare tagli
        plt.show()
        self._display_output("Andamento Termine", f"Grafico dell'andamento di '{parola_chiave}' generato e visualizzato.")


    def vista_rete(self):
        """Calcola e visualizza le co-occorrenze più frequenti tra termini (stopwords escluse) in una finestra di contesto."""
        if not self.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.root)
            return

        window_size = simpledialog.askinteger("Finestra di Contesto (Co-occorrenze)",
                                              "Inserisci la dimensione della finestra di contesto (numero di parole vicine da considerare):",
                                              parent=self.root, minvalue=2, maxvalue=10, initialvalue=3)
        if window_size is None: return

        num_cooc = simpledialog.askinteger("Numero Co-occorrenze",
                                           "Quante coppie di co-occorrenze più frequenti vuoi visualizzare?",
                                           parent=self.root, minvalue=1, initialvalue=15)
        if num_cooc is None: return

        # Ottieni le parole processate (minuscolo, senza stopwords)
        parole = self._get_processed_words(remove_stopwords=True)
        if len(parole) < window_size:
            self._display_output("Rete Co-occorrenze", f"Non ci sono abbastanza parole nel corpus (dopo rimozione stopwords) per analizzare le co-occorrenze con una finestra di dimensione {window_size}.")
            messagebox.showinfo("Rete Co-occorrenze", "Testo insufficiente per l'analisi delle co-occorrenze.", parent=self.root)
            return

        co_occurrences = Counter()
        # Itera attraverso le parole per creare finestre di contesto
        for i in range(len(parole) - window_size + 1):
            window_segment = parole[i : i + window_size]
            # Considera solo le parole uniche all'interno della finestra e ordinale per creare coppie consistenti
            parole_nella_finestra_uniche = sorted(list(set(window_segment)))

            # Se ci sono almeno due parole uniche nella finestra, genera tutte le coppie possibili
            if len(parole_nella_finestra_uniche) < 2: continue

            # Genera tutte le coppie non ordinate di parole uniche nella finestra
            for j in range(len(parole_nella_finestra_uniche)):
                for k in range(j + 1, len(parole_nella_finestra_uniche)):
                    pair = tuple(sorted((parole_nella_finestra_uniche[j], parole_nella_finestra_uniche[k])))
                    co_occurrences[pair] += 1

        if not co_occurrences:
            self._display_output("Rete Co-occorrenze", "Nessuna co-occorrenza trovata con i parametri specificati.")
            messagebox.showinfo("Rete Co-occorrenze", "Nessuna co-occorrenza trovata.", parent=self.root)
            return

        output_str = f"Le {num_cooc} coppie di termini co-occorrenti più frequenti (finestra: {window_size} parole, stopwords escluse):\n"
        output_str += "--------------------------------------------------------------------------------------\n"
        for (p1, p2), freq in co_occurrences.most_common(num_cooc):
            output_str += f"('{p1}', '{p2}'): {freq}\n"

        output_str += "\nNota: Questa è una rappresentazione testuale. Per una visualizzazione grafica della rete, sarebbero necessarie librerie aggiuntive (es. NetworkX, Matplotlib)."
        self._display_output("Rete di Co-occorrenze", output_str)
        messagebox.showinfo("Rete di Co-occorrenze", "Analisi delle co-occorrenze completata. I risultati sono nell'area di output.", parent=self.root)


# --- Blocco Principale per l'Esecuzione dell'Applicazione ---

if __name__ == '__main__':
    # Inizializza la finestra principale di Tkinter
    radice = tk.Tk()
    # Crea un'istanza della classe principale dell'applicazione
    app = StrumentiTestualiUsai(radice)
    # Avvia il loop principale dell'interfaccia grafica
    radice.mainloop()
