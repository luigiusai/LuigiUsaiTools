# usability.py
# Contiene funzioni per l'analisi di usabilità e leggibilità del testo.
# Luigi Usai, Quartucciu, Italia, Maggio 2025

import tkinter as tk
from tkinter import simpledialog, messagebox
import math

# Dipendenze NLTK (verranno controllate nel file principale)
nltk_disponibile = False
nltk_punkt_disponibile = False
nltk_tagger_disponibile = False
try:
    import nltk
    nltk_disponibile = True
    # La disponibilità di punkt e tagger viene verificata in StrumentiTestualiUsai.py
    # e propagata qui se necessario, o le funzioni falliranno con grazia.
except ImportError:
    pass


class FunzioniUsability:
    def __init__(self, app_ref):
        """
        Inizializza le funzioni di usabilità e leggibilità.
        app_ref: Riferimento all'istanza principale dell'applicazione.
        """
        self.app_ref = app_ref
        self.lingua_analisi = "italian" # Default
        # Propaga lo stato delle dipendenze NLTK dal modulo principale
        global nltk_punkt_disponibile, nltk_tagger_disponibile
        if hasattr(app_ref, 'nltk_punkt_disponibile'): # Verifica se l'attributo esiste
            nltk_punkt_disponibile = app_ref.nltk_punkt_disponibile
        if hasattr(app_ref, 'nltk_tagger_disponibile'):
            nltk_tagger_disponibile = app_ref.nltk_tagger_disponibile


    def imposta_lingua_analisi(self):
        """
        Permette all'utente di impostare la lingua per le analisi che la supportano.
        """
        lingua_scelta = simpledialog.askstring("Imposta Lingua Analisi", 
                                               "Scegli la lingua per l'analisi (es. 'italian', 'english'):",
                                               initialvalue=self.lingua_analisi,
                                               parent=self.app_ref.root)
        if lingua_scelta and lingua_scelta.lower() in ['italian', 'english']:
            self.lingua_analisi = lingua_scelta.lower()
            messagebox.showinfo("Lingua Impostata", f"Lingua per l'analisi impostata a: {self.lingua_analisi}", parent=self.app_ref.root)
            self.app_ref._display_output("Impostazione Lingua", f"Lingua analisi: {self.lingua_analisi}")
        elif lingua_scelta:
            messagebox.showwarning("Lingua non Supportata", "Lingua non riconosciuta. Mantengo: " + self.lingua_analisi, parent=self.app_ref.root)

    def _check_corpus_e_nltk(self, check_punkt=False, check_tagger=False):
        """Controlla se il corpus è caricato e se NLTK e i suoi componenti sono disponibili."""
        if not self.app_ref.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.app_ref.root)
            return False
        if not nltk_disponibile:
            messagebox.showerror("NLTK Mancante", "La libreria NLTK è necessaria per questa funzionalità.", parent=self.app_ref.root)
            return False
        if check_punkt and not nltk_punkt_disponibile:
            messagebox.showerror("NLTK (Punkt) Mancante", "Il pacchetto 'punkt' di NLTK è necessario.", parent=self.app_ref.root)
            return False
        if check_tagger and not nltk_tagger_disponibile:
            messagebox.showerror("NLTK (Tagger) Mancante", "Il pacchetto 'averaged_perceptron_tagger' di NLTK è necessario.", parent=self.app_ref.root)
            return False
        return True

    def subdividi_in_frasi(self):
        """
        Suddivide il corpus in frasi e le visualizza.
        """
        if not self._check_corpus_e_nltk(check_punkt=True):
            return

        testo_completo = ' '.join(self.app_ref.corpus_testuale)
        try:
            frasi = nltk.sent_tokenize(testo_completo, language=self.lingua_analisi)
            output_str = f"Suddivisione in Frasi (Lingua: {self.lingua_analisi}):\n"
            output_str += "-------------------------------------------------\n"
            if not frasi:
                output_str += "Nessuna frase trovata."
            for i, frase in enumerate(frasi):
                output_str += f"Frase {i+1}: {frase}\n"
            self.app_ref._display_output("Suddivisione in Frasi", output_str)
        except Exception as e:
            messagebox.showerror("Errore Suddivisione Frasi", f"Errore: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Suddivisione Frasi", f"Errore: {e}")

    def subdividi_in_token(self):
        """
        Suddivide il corpus in token e li visualizza.
        """
        if not self._check_corpus_e_nltk(check_punkt=True): # Punkt è usato da word_tokenize per alcune lingue
            return

        testo_completo = ' '.join(self.app_ref.corpus_testuale)
        try:
            # word_tokenize usa 'punkt' internamente per la gestione delle abbreviazioni ecc.
            # e può prendere un argomento 'language'.
            tokens = nltk.word_tokenize(testo_completo, language=self.lingua_analisi)
            output_str = f"Suddivisione in Token (Lingua: {self.lingua_analisi}):\n"
            output_str += "--------------------------------------------------\n"
            if not tokens:
                output_str += "Nessun token trovato."
            else:
                output_str += ", ".join(tokens)
            self.app_ref._display_output("Suddivisione in Token", output_str)
        except Exception as e:
            messagebox.showerror("Errore Suddivisione Token", f"Errore: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Suddivisione Token", f"Errore: {e}")

    def annotazione_pos(self):
        """
        Esegue il Part-of-Speech tagging sul corpus e visualizza i risultati.
        """
        if not self._check_corpus_e_nltk(check_punkt=True, check_tagger=True):
            return

        testo_completo = ' '.join(self.app_ref.corpus_testuale)
        try:
            tokens = nltk.word_tokenize(testo_completo, language=self.lingua_analisi)
            # nltk.pos_tag per l'italiano usa il tagger 'averaged_perceptron_tagger', 
            # che è addestrato principalmente su inglese ma ha una certa generalità.
            # Per risultati migliori in italiano, sarebbe necessario un tagger specifico per l'italiano.
            # Tuttavia, per questa implementazione, usiamo quello di default.
            # L'argomento 'lang' in pos_tag può essere usato per specificare set di tag diversi (es. 'universal')
            # ma il tagger sottostante rimane lo stesso a meno di configurazioni avanzate.
            tagged_tokens = nltk.pos_tag(tokens) # Non c'è un argomento 'language' diretto per il tagger qui

            output_str = f"Annotazione Morfosintattica (POS Tagging - Lingua: {self.lingua_analisi}):\n"
            output_str += "-------------------------------------------------------------------\n"
            if not tagged_tokens:
                output_str += "Nessun token da annotare."
            for token, tag in tagged_tokens:
                output_str += f"{token} [{tag}]\n"
            
            output_str += "\nNota: Il tagger predefinito di NLTK ('averaged_perceptron_tagger') è ottimizzato per l'inglese."
            output_str += "\nPer l'italiano, i risultati potrebbero non essere ottimali senza un modello specifico."
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
            parole_raw = nltk.word_tokenize(testo_completo.lower(), language='italian') # Forziamo italiano per Gulpease
            parole = [p for p in parole_raw if p.isalpha()]
            
            num_parole = len(parole)
            if num_parole == 0:
                self.app_ref._display_output("Indice Gulpease", "Nessuna parola valida trovata per il calcolo.")
                return

            # Tokenizzazione frasi
            frasi = nltk.sent_tokenize(testo_completo, language='italian') # Forziamo italiano
            num_frasi = len(frasi)
            if num_frasi == 0:
                self.app_ref._display_output("Indice Gulpease", "Nessuna frase trovata per il calcolo.")
                return
            
            num_lettere = sum(len(p) for p in parole)

            # Formula Gulpease: G = 89 + ( ( (Frasi * 100) / Parole * 3 ) - ( (Lettere * 100) / Parole * 10 ) ) / 100
            # Semplificata: G = 89 + (Frasi * 300 / Parole) - (Lettere * 10 / Parole)
            # G = 89 + ( (Frasi * 300) - (Lettere * 10) ) / Parole
            
            gulpease_index = 89 + ( (num_frasi * 300) - (num_lettere * 10) ) / num_parole
            
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
                return

            output_str = f"Analisi Leggibilità per Frase (Indice Gulpease - per l'italiano):\n"
            output_str += "-----------------------------------------------------------------\n"
            
            risultati_frasi = []
            for i, frase_txt in enumerate(frasi_originali):
                parole_raw_frase = nltk.word_tokenize(frase_txt.lower(), language='italian')
                parole_frase = [p for p in parole_raw_frase if p.isalpha()]
                
                num_parole_frase = len(parole_frase)
                if num_parole_frase == 0:
                    risultati_frasi.append(f"Frase {i+1}: \"{frase_txt[:70]}...\" - Indice Gulpease: N/A (0 parole)")
                    continue

                num_lettere_frase = sum(len(p) for p in parole_frase)
                
                # Gulpease per una singola frase (num_frasi = 1)
                gulpease_frase = 89 + ( (1 * 300) - (num_lettere_frase * 10) ) / num_parole_frase
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

