# Narratologia.py
# Questo file conterrà le funzioni per l'analisi narratologica.
# Luigi Usai: 19 maggio 2025
# sto combinando le potenzialità imparate all'Uni Bologna con quelle apprese in Narratologia
# e nel laboratorio di Usabilità presso Università di Cagliari e Linguistica.

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, scrolledtext
import json
import sqlite3
import itertools # Per le funzioni di Propp

# Variabile globale per graphviz, gestita in StrumentiTestualiUsai.py
graphviz_disponibile = False
try:
    import graphviz
    graphviz_disponibile = True
except ImportError:
    print("Libreria 'graphviz' non trovata. La visualizzazione delle sequenze di Propp non sarà disponibile.")
    print("Installala con: pip install graphviz")
    print("Inoltre, assicurati che il software Graphviz sia installato sul sistema: https://graphviz.org/download/")


# Definizioni delle funzioni di Propp (dal tuo generatore_propp.py)
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

def get_propp_function_description(code):
    """Restituisce la descrizione completa di una funzione dato il suo codice."""
    return FUNZIONI_PROPP.get(code.upper(), f"Funzione Sconosciuta ({code})")


class FunzioniNarratologia:
    def __init__(self, app_ref):
        """
        Inizializza le funzioni di narratologia.
        app_ref: Riferimento all'istanza principale dell'applicazione StrumentiTestualiUsai
                 per accedere, ad esempio, a _display_output o al corpus.
        """
        self.app_ref = app_ref
        self.matrice_greimas_data = None
        self.matrice_propp_data = None
        self.tensori_narrativi_data = None

    def crea_matrice_greimas(self):
        """
        Permette all'utente di definire e visualizzare la Matrice Attanziale di Greimas.
        """
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
            entries[attante] = entry
            if self.matrice_greimas_data and attante in self.matrice_greimas_data:
                entry.insert(0, self.matrice_greimas_data[attante])

        def salva_dati_greimas():
            self.matrice_greimas_data = {attante: entries[attante].get() for attante in attanti}
            output_str = "Matrice Attanziale di Greimas:\n"
            for attante, valore in self.matrice_greimas_data.items():
                output_str += f"  - {attante}: {valore}\n"
            self.app_ref._display_output("Matrice Attanziale (Greimas)", output_str)
            messagebox.showinfo("Matrice Greimas", "Matrice di Greimas aggiornata e visualizzata.", parent=dialog)
            dialog.destroy()

        tk.Button(dialog, text="Salva e Visualizza", command=salva_dati_greimas).pack(pady=20)
        self.app_ref.root.wait_window(dialog)


    def crea_matrice_propp(self):
        """
        Permette all'utente di definire e visualizzare le funzioni di Propp.
        """
        num_funzioni = simpledialog.askinteger("Funzioni di Propp",
                                               "Quante funzioni di Propp vuoi definire (max 31)?",
                                               parent=self.app_ref.root, minvalue=1, maxvalue=31, initialvalue=5)
        if num_funzioni is None:
            return

        self.matrice_propp_data = {}
        # Suggerisci i codici F1, F2, ...
        codici_propp_suggeriti = [f"F{i}" for i in range(1, 32)]

        for i in range(1, num_funzioni + 1):
            desc_sugg = get_propp_function_description(codici_propp_suggeriti[i-1]) if i-1 < len(codici_propp_suggeriti) else ""
            prompt_msg = f"Funzione {i}: Descrivi la funzione (es. {codici_propp_suggeriti[i-1]} - {desc_sugg})"
            
            funzione_desc = simpledialog.askstring(f"Definizione Funzione di Propp {i}", prompt_msg,
                                              parent=self.app_ref.root)
            if funzione_desc is None:
                self.matrice_propp_data = None 
                messagebox.showwarning("Matrice Propp", "Creazione matrice di Propp annullata.", parent=self.app_ref.root)
                return
            # L'utente potrebbe inserire solo la descrizione o codice + descrizione
            self.matrice_propp_data[f"Funzione {i}"] = funzione_desc

        if self.matrice_propp_data:
            output_str = "Matrice delle Funzioni di Propp (Definite dall'Utente):\n"
            for funzione_num, descrizione in self.matrice_propp_data.items():
                output_str += f"  - {funzione_num}: {descrizione}\n"
            self.app_ref._display_output("Matrice di Propp (Utente)", output_str)
            messagebox.showinfo("Matrice Propp", "Matrice di Propp creata e visualizzata.", parent=self.app_ref.root)
        else:
             self.app_ref._display_output("Matrice di Propp (Utente)", "Nessuna funzione di Propp definita.")


    def crea_tensori_narrativi(self):
        """
        Permette all'utente di definire e visualizzare i Tensori Narrativi di Luigi Usai.
        """
        num_dimensioni = simpledialog.askinteger("Tensori Narrativi",
                                                 "Quante dimensioni per i Tensori Narrativi?",
                                                 parent=self.app_ref.root, minvalue=1, initialvalue=3)
        if num_dimensioni is None:
            return

        self.tensori_narrativi_data = {}
        for i in range(1, num_dimensioni + 1):
            dim_nome = simpledialog.askstring(f"Dimensione {i}", f"Nome della Dimensione {i}:",
                                             parent=self.app_ref.root)
            if dim_nome is None:
                self.tensori_narrativi_data = None
                messagebox.showwarning("Tensori Narrativi", "Creazione tensori annullata.", parent=self.app_ref.root)
                return
            
            elementi_str = simpledialog.askstring(f"Elementi Dim. {i}",
                                                  f"Inserisci gli elementi per '{dim_nome}' (separati da virgola):",
                                                  parent=self.app_ref.root)
            if elementi_str is None:
                self.tensori_narrativi_data = None
                messagebox.showwarning("Tensori Narrativi", "Creazione tensori annullata.", parent=self.app_ref.root)
                return
            self.tensori_narrativi_data[dim_nome] = [e.strip() for e in elementi_str.split(',')]

        if self.tensori_narrativi_data:
            output_str = "Tensori Narrativi (Luigi Usai):\n"
            for dimensione, elementi in self.tensori_narrativi_data.items():
                output_str += f"  - Dimensione '{dimensione}': {', '.join(elementi)}\n"
            self.app_ref._display_output("Tensori Narrativi", output_str)
            messagebox.showinfo("Tensori Narrativi", "Tensori Narrativi creati e visualizzati.", parent=self.app_ref.root)
        else:
            self.app_ref._display_output("Tensori Narrativi", "Nessun Tensore Narrativo definito.")

    def _mostra_risultati_generatore_propp(self, titolo, risultati, max_visualizzati=50):
        """Helper per visualizzare risultati potenzialmente lunghi in una nuova finestra."""
        if not risultati:
            self.app_ref._display_output(titolo, "Nessun risultato generato.")
            messagebox.showinfo(titolo, "Nessun risultato da visualizzare.", parent=self.app_ref.root)
            return

        result_window = tk.Toplevel(self.app_ref.root)
        result_window.title(titolo)
        result_window.geometry("700x500")
        result_window.transient(self.app_ref.root)
        result_window.grab_set()

        tk.Label(result_window, text=f"{titolo} (Prime {max_visualizzati} occorrenze se più lunghe):", font=("Arial", 12)).pack(pady=5)
        
        text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=80, height=20)
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
        """
        Genera permutazioni di funzioni di Propp scelte dall'utente.
        """
        codici_input = simpledialog.askstring("Genera Trame Propp (Permutazioni)",
                                               "Inserisci i codici delle funzioni di Propp separati da virgola (es. F1,F8,F11):",
                                               parent=self.app_ref.root)
        if not codici_input:
            return

        lista_codici_funzioni = [cod.strip().upper() for cod in codici_input.split(',')]
        
        try:
            if not all(codice in FUNZIONI_PROPP for codice in lista_codici_funzioni):
                invalid_codes = [c for c in lista_codici_funzioni if c not in FUNZIONI_PROPP]
                messagebox.showerror("Errore Codici", f"Uno o più codici funzione non sono validi: {', '.join(invalid_codes)}", parent=self.app_ref.root)
                return
            if len(lista_codici_funzioni) > 7: # Limite per evitare troppe permutazioni
                 if not messagebox.askyesno("Attenzione", f"Stai per generare permutazioni per {len(lista_codici_funzioni)} funzioni. Questo potrebbe richiedere molto tempo ({math.factorial(len(lista_codici_funzioni))} permutazioni). Continuare?", parent=self.app_ref.root):
                    return


            permutazioni = list(itertools.permutations(lista_codici_funzioni))
            
            trame_generate = []
            for p in permutazioni:
                trama = [get_propp_function_description(codice) for codice in p]
                trame_generate.append(" -> ".join(trama))
            
            titolo_output = f"Trame Generate (Permutazioni di: {', '.join(lista_codici_funzioni)}) - {len(trame_generate)} totali"
            self._mostra_risultati_generatore_propp(titolo_output, trame_generate)

        except ValueError as e:
            messagebox.showerror("Errore Input", str(e), parent=self.app_ref.root)
        except Exception as e:
            messagebox.showerror("Errore Inatteso", f"Si è verificato un errore: {e}", parent=self.app_ref.root)

    def genera_combinazioni_propp(self):
        """
        Genera combinazioni di funzioni di Propp da un set disponibile.
        """
        codici_disponibili_input = simpledialog.askstring("Genera Sottoinsiemi Propp (Combinazioni)",
                                                          "Inserisci i codici delle funzioni DISPONIBILI separati da virgola (es. F1,F2,F3,F8,F11):",
                                                          parent=self.app_ref.root)
        if not codici_disponibili_input:
            return
        
        lista_codici_disponibili = [cod.strip().upper() for cod in codici_disponibili_input.split(',')]

        try:
            if not all(codice in FUNZIONI_PROPP for codice in lista_codici_disponibili):
                invalid_codes = [c for c in lista_codici_disponibili if c not in FUNZIONI_PROPP]
                messagebox.showerror("Errore Codici Disponibili", f"Uno o più codici funzione disponibili non sono validi: {', '.join(invalid_codes)}", parent=self.app_ref.root)
                return

            numero_da_scegliere = simpledialog.askinteger("Numero da Scegliere",
                                                       f"Quante funzioni vuoi scegliere dal set di {len(lista_codici_disponibili)} disponibili?",
                                                       parent=self.app_ref.root, minvalue=1, maxvalue=len(lista_codici_disponibili))
            if numero_da_scegliere is None:
                return

            combinazioni = list(itertools.combinations(lista_codici_disponibili, numero_da_scegliere))
            
            sottoinsiemi_generati = []
            for c in combinazioni:
                sottoinsieme_descr = sorted([get_propp_function_description(codice) for codice in c])
                sottoinsiemi_generati.append(", ".join(sottoinsieme_descr))

            titolo_output = (f"Sottoinsiemi Generati (Combinazioni di {numero_da_scegliere} da: "
                             f"{', '.join(lista_codici_disponibili)}) - {len(sottoinsiemi_generati)} totali")
            self._mostra_risultati_generatore_propp(titolo_output, sottoinsiemi_generati)

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
                                 "La libreria Graphviz è necessaria per questa funzionalità.\n"
                                 "Installala con 'pip install graphviz' e assicurati che il software Graphviz sia nel PATH.",
                                 parent=self.app_ref.root)
            return

        codici_input = simpledialog.askstring("Visualizza Sequenza Funzioni di Propp",
                                               "Inserisci i codici delle funzioni di Propp in sequenza, separati da virgola (es. F8,F11,F14,F16,F18):",
                                               parent=self.app_ref.root)
        if not codici_input:
            return

        propp_codes_sequence = [cod.strip().upper() for cod in codici_input.split(',')]
        
        invalid_codes = [c for c in propp_codes_sequence if c not in FUNZIONI_PROPP]
        if invalid_codes:
            messagebox.showerror("Errore Codici", f"I seguenti codici funzione non sono validi: {', '.join(invalid_codes)}", parent=self.app_ref.root)
            return

        if not propp_codes_sequence:
            messagebox.showwarning("Input Vuoto", "Nessuna sequenza inserita.", parent=self.app_ref.root)
            return

        try:
            import textwrap # Per il testo lungo nei nodi
            dot = graphviz.Digraph(comment="Sequenza Funzioni di Propp (Utente)")
            dot.attr(rankdir='LR') 
            dot.attr('node', shape='box', style='rounded', fontname='Arial', fontsize='10')
            dot.attr('edge', fontname='Arial', fontsize='9')

            previous_node_id = None
            for i, code in enumerate(propp_codes_sequence):
                function_description = get_propp_function_description(code)
                label = f"{code}\n{textwrap.fill(function_description, width=25)}" # width ridotto per nodi più compatti
                node_id = f"node_user_{i}"

                dot.node(node_id, label)
                if previous_node_id is not None:
                    dot.edge(previous_node_id, node_id)
                previous_node_id = node_id
            
            # Chiedi dove salvare
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("File PNG", "*.png"), ("File PDF", "*.pdf"), ("File DOT Source", "*.dot"), ("Tutti i file", "*.*")],
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
                if ext in ['png', 'pdf', 'svg', 'jpeg', 'dot']:
                    save_format = ext
            
            # Rimuovi l'estensione dal nome del file per render, che la aggiunge da solo
            base_file_path = file_path
            if file_path.lower().endswith(f".{save_format}"):
                 base_file_path = file_path[:-len(save_format)-1]


            dot.render(base_file_path, format=save_format, view=True, cleanup=True)
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
        """
        Salva i dati narratologici (Greimas, Propp, Tensori) in un file JSON.
        """
        if not self.matrice_greimas_data and not self.matrice_propp_data and not self.tensori_narrativi_data:
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
        if self.matrice_propp_data:
            dati_da_salvare["matrice_propp_utente"] = self.matrice_propp_data # Aggiornato nome chiave
        if self.tensori_narrativi_data:
            dati_da_salvare["tensori_narrativi"] = self.tensori_narrativi_data
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(dati_da_salvare, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Salvataggio JSON", f"Dati narratologici salvati con successo in:\n{file_path}", parent=self.app_ref.root)
            self.app_ref._display_output("Salvataggio JSON", f"Dati salvati in {file_path}")
        except Exception as e:
            messagebox.showerror("Errore Salvataggio JSON", f"Errore durante il salvataggio del file JSON:\n{e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Salvataggio JSON", f"Errore: {e}")

    def salva_dati_narratologici_db(self):
        """
        Salva i dati narratologici (Greimas, Propp, Tensori) in un database SQLite.
        """
        if not self.matrice_greimas_data and not self.matrice_propp_data and not self.tensori_narrativi_data:
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
            if self.matrice_propp_data:
                cursor.execute("INSERT INTO analisi_narratologica (nome_analisi, dati_json) VALUES (?, ?)",
                               ("Matrice Propp (Utente)", json.dumps(self.matrice_propp_data))) # Aggiornato nome_analisi
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
            self.app_ref._display_output("Salvataggio Database", f"{num_records} record salvati in {db_path}")

        except sqlite3.Error as e:
            messagebox.showerror("Errore Database", f"Errore SQLite: {e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Database", f"Errore SQLite: {e}")
        except Exception as e:
            messagebox.showerror("Errore Salvataggio DB", f"Errore imprevisto durante il salvataggio nel database:\n{e}", parent=self.app_ref.root)
            self.app_ref._display_output("Errore Salvataggio DB", f"Errore: {e}")
    
    # Qui potrebbero essere aggiunte le altre funzioni narratologiche dal file .docx
    # come segment_fabula_syuzhet, detect_narrator_and_focalization, ecc.
    # Ognuna richiederebbe un'interfaccia utente per input specifici e logica di analisi.
