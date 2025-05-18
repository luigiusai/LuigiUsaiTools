import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None
    print("Pillow (PIL) non è installato. L'immagine nell'About non sarà visualizzata. Installa con: pip install Pillow")

class StrumentiTestualiUsai:
    def __init__(self, root):
        self.root = root
        self.root.title("Strumenti Testuali - Progetto di Luigi Usai")
        self.root.geometry("800x700") # Dimensione iniziale finestra
        self.corpus_testuale = [] 
        self.nomi_file_corpus = [] 
        self.stopwords = set([
            "e", "è", "ed", "a", "ad", "al", "allo", "ai", "agli", "alla", "alle",
            "da", "dal", "dallo", "dai", "dagli", "dalla", "dalle",
            "di", "del", "dello", "dei", "degli", "della", "delle",
            "in", "nel", "nello", "nei", "negli", "nella", "nelle",
            "su", "sul", "sullo", "sui", "sugli", "sulla", "sulle",
            "con", "col", "coi", "per", "tra", "fra", "il", "lo", "la", "i", "gli", "le",
            "un", "uno", "una", "ma", "o", "se", "che", "non", "si", "ciò", "cui",
            "come", "dove", "quando", "quale", "quanto", "chi", "perché",
            "questo", "questa", "questi", "queste", "quello", "quella", "quelli", "quelle",
            "essere", "avere", "fare", "dire", "potere", "volere",
            "io", "tu", "lui", "lei", "esso", "essa", "noi", "voi", "essi", "esse",
            "ci", "vi", "li", "ne", "mi", "ti", "si", "lo", "la", "gli", "le",
            "me", "te", "sé", "più", "molto", "mio", "mia", "miei", "mie", "tuo", "tua",
            "tuoi", "tue", "suo", "sua", "suoi", "sue", "nostro", "nostra", "nostri",
            "nostre", "vostro", "vostra", "vostri", "vostre", "loro"
        ])
        self.crea_interfaccia()

    def _get_processed_words(self, remove_stopwords=True, specific_text=None):
        testo_da_processare = ' '.join(self.corpus_testuale) if specific_text is None else specific_text
        if not testo_da_processare:
            return []
        parole = re.findall(r'\b\w+\b', testo_da_processare.lower())
        if remove_stopwords:
            parole = [parola for parola in parole if parola not in self.stopwords]
        return parole

    def crea_interfaccia(self):
        # --- Creazione della Barra dei Menu ---
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # -- Menu File --
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Carica Corpus...", command=self.carica_corpus)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.root.quit)

        # -- Menu Strumenti --
        strumenti_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Strumenti", menu=strumenti_menu)
        strumenti_menu.add_command(label="Gestione Stopword...", command=self.gestione_stopword)
        strumenti_menu.add_separator()
        strumenti_menu.add_command(label="Frequenza Termini...", command=self.frequenza_termini)
        strumenti_menu.add_command(label="Nuvola di Parole...", command=self.nuvola_parole)
        strumenti_menu.add_command(label="Collocazioni (N-grammi)...", command=self.collocazioni)
        strumenti_menu.add_command(label="KWIC (Parole Chiave nel Contesto)...", command=self.kwic)
        strumenti_menu.add_command(label="Andamento Termini...", command=self.andamento)
        strumenti_menu.add_command(label="Rete Co-occorrenze (Testuale)...", command=self.vista_rete)

        # -- Menu About --
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="Informazioni su...", command=self.mostra_about)
        
        # Area di testo per visualizzare il corpus
        corpus_frame = tk.LabelFrame(self.root, text="Corpus Caricato", padx=5, pady=5)
        corpus_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5,5)) # Aggiunto padding
        self.area_testo = scrolledtext.ScrolledText(corpus_frame, wrap=tk.WORD, height=15, width=100, font=("Arial", 10))
        self.area_testo.pack(fill=tk.BOTH, expand=True)
        self.area_testo.insert(tk.END, "Il corpus testuale verrà visualizzato qui dopo il caricamento.\n")
        self.area_testo.config(state=tk.DISABLED) 

        # Area di testo per visualizzare l'output delle analisi
        output_frame = tk.LabelFrame(self.root, text="Risultati Analisi", padx=5, pady=5)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5,10)) # Aggiunto padding
        self.output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10, width=100, font=("Arial", 10))
        self.output_area.pack(fill=tk.BOTH, expand=True)
        self.output_area.insert(tk.END, "L'output delle analisi verrà visualizzato qui.\n")
        self.output_area.config(state=tk.DISABLED)

    def mostra_about(self):
        """Mostra la finestra di About con le informazioni sull'autore."""
        about_window = tk.Toplevel(self.root)
        about_window.title("Informazioni su Strumenti Testuali")
        about_window.geometry("400x450") # Aumentata altezza per foto
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()

        tk.Label(about_window, text="Strumenti Testuali", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        tk.Label(about_window, text="Versione 1.1", font=("Arial", 10)).pack()
        
        info_frame = tk.Frame(about_window, pady=10)
        info_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(info_frame, text="Autore:", font=("Arial", 12, "italic")).pack(pady=(10,0))
        tk.Label(info_frame, text="Luigi Usai", font=("Arial", 14, "bold")).pack()
        tk.Label(info_frame, text="Quartucciu (CA), Italy", font=("Arial", 11)).pack(pady=(0,15))

        # Caricamento e visualizzazione immagine
        if Image and ImageTk: # Verifica se Pillow è stato importato correttamente
            try:
                # Assicurati che 'luigi.jpg' sia nella stessa cartella dello script
                # o fornisci il percorso completo.
                img_path = "luigi.jpg" 
                pil_image = Image.open(img_path)
                
                # Ridimensionamento immagine se necessario per adattarla alla finestra
                base_width = 200 # Larghezza desiderata per l'immagine
                w_percent = (base_width / float(pil_image.size[0]))
                h_size = int((float(pil_image.size[1]) * float(w_percent)))
                pil_image_resized = pil_image.resize((base_width, h_size), Image.LANCZOS) # Usa Image.LANCZOS per Pillow >= 9.1.0
                                                                                        # o Image.ANTIALIAS per versioni precedenti
                
                self.author_photo = ImageTk.PhotoImage(pil_image_resized) # Salva riferimento
                
                img_label = tk.Label(info_frame, image=self.author_photo)
                img_label.pack(pady=10)
            except FileNotFoundError:
                tk.Label(info_frame, text="Immagine 'luigi.jpg' non trovata.", font=("Arial", 9), fg="red").pack(pady=5)
            except Exception as e:
                tk.Label(info_frame, text=f"Errore caricamento immagine: {e}", font=("Arial", 9), fg="red").pack(pady=5)
        else:
            tk.Label(info_frame, text="Libreria Pillow (PIL) non disponibile per visualizzare l'immagine.", font=("Arial", 9), fg="orange").pack(pady=5)

        tk.Label(info_frame, text="Progetto per l'analisi testuale.", font=("Arial", 10)).pack(pady=10)
        
        close_button = tk.Button(about_window, text="Chiudi", command=about_window.destroy, width=10)
        close_button.pack(pady=15)


    def _display_output(self, title, content):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, f"--- {title} ---\n\n{content}")
        self.output_area.config(state=tk.DISABLED)

    def carica_corpus(self):
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
                with open(nome_file, 'r', encoding='utf-8') as f:
                    contenuto = f.read()
                    self.corpus_testuale.append(contenuto)
                    self.nomi_file_corpus.append(nome_file.split('/')[-1]) 
                    self.area_testo.insert(tk.END, f"--- Contenuto di: {self.nomi_file_corpus[-1]} ---\n{contenuto}\n\n")
                    success_count += 1
            except Exception as e:
                problematic_files.append(f"{nome_file.split('/')[-1]}: {e}")
        
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
        sw_window = tk.Toplevel(self.root)
        sw_window.title("Gestione Stopwords")
        sw_window.geometry("500x550") # Leggermente più grande
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
                    items = sorted(list(self.stopwords))
                    sw_listbox.delete(0, tk.END)
                    for item in items:
                        sw_listbox.insert(tk.END, item)
                    sw_entry.delete(0, tk.END)
                    if new_sw in items:
                        idx = items.index(new_sw)
                        sw_listbox.see(idx)
                        sw_listbox.selection_clear(0, tk.END)
                        sw_listbox.selection_set(idx)
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
            for i in reversed(selected_indices): 
                sw_to_remove = sw_listbox.get(i)
                self.stopwords.discard(sw_to_remove) 
                sw_listbox.delete(i)
                removed_sws.append(sw_to_remove)
            if removed_sws:
                messagebox.showinfo("Stopwords Rimosse", f"Rimosse con successo: {', '.join(reversed(removed_sws))}", parent=sw_window)

        def load_default_stopwords():
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
            self.stopwords.update(default_ita_sw)
            items = sorted(list(self.stopwords))
            sw_listbox.delete(0, tk.END)
            for item in items:
                sw_listbox.insert(tk.END, item)
            messagebox.showinfo("Stopwords Caricate", "Lista di stopwords italiane predefinite caricata/aggiornata.", parent=sw_window)

        button_frame_actions = tk.Frame(sw_window)
        button_frame_actions.pack(pady=10)
        tk.Button(button_frame_actions, text="Aggiungi", command=add_sw, width=12, height=1).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame_actions, text="Rimuovi Selez.", command=remove_sw, width=12, height=1).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame_actions, text="Carica Default (ITA)", command=load_default_stopwords, width=18, height=1).pack(side=tk.LEFT, padx=5)
        
        tk.Button(sw_window, text="Chiudi", command=sw_window.destroy, width=10, height=1).pack(pady=15)
        
        self.root.wait_window(sw_window)


    def frequenza_termini(self):
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
            wordcloud = WordCloud(width=800, height=400, background_color='white',
                                  stopwords=None, 
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
        if not self.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.root)
            return
        
        parola_chiave = simpledialog.askstring("Parola Chiave (KWIC)", "Inserisci la parola chiave da cercare:", parent=self.root)
        if not parola_chiave: 
            return
        
        contesto_size = simpledialog.askinteger("Dimensione Contesto", "Quante parole di contesto visualizzare prima e dopo la parola chiave?",
                                                 parent=self.root, minvalue=1, maxvalue=20, initialvalue=5)
        if contesto_size is None: return

        parola_chiave_lower = parola_chiave.lower()
        results_kwic = []
        max_results_display = 200 
        
        testo_completo_originale = ' '.join(self.corpus_testuale)
        tokens_original_case = re.findall(r'\b\w+\b|[\.,;!?()]', testo_completo_originale)
        tokens_lower_case = [t.lower() for t in tokens_original_case]

        found_count = 0
        for i, token_lower in enumerate(tokens_lower_case):
            if token_lower == parola_chiave_lower:
                found_count +=1
                if found_count > max_results_display:
                    results_kwic.append(f"\n--- (Visualizzazione limitata ai primi {max_results_display} risultati) ---")
                    break

                start_idx = max(0, i - contesto_size)
                end_idx = min(len(tokens_original_case), i + contesto_size + 1)
                
                contesto_sx_list = tokens_original_case[start_idx:i]
                parola_target = tokens_original_case[i] 
                contesto_dx_list = tokens_original_case[i+1:end_idx]
                
                contesto_sx_str = ""
                for k_idx, k_tok in enumerate(contesto_sx_list):
                    contesto_sx_str += k_tok
                    if k_idx < len(contesto_sx_list) -1 and not re.match(r'^[\.,;!?]$', contesto_sx_list[k_idx+1]):
                         contesto_sx_str += " "
                    elif k_idx == len(contesto_sx_list) -1 and not re.match(r'^[\.,;!?]$', parola_target): 
                        contesto_sx_str += " "

                contesto_dx_str = ""
                for k_idx, k_tok in enumerate(contesto_dx_list):
                    if k_idx > 0 and not re.match(r'^[\.,;!?]$', k_tok) and not re.match(r'^[\.,;!?]$', contesto_dx_list[k_idx-1]):
                        contesto_dx_str += " "
                    elif k_idx == 0 and not re.match(r'^[\.,;!?]$', k_tok) and not re.match(r'^[\.,;!?]$', parola_target): 
                         contesto_dx_str += " "
                    contesto_dx_str += k_tok

                results_kwic.append(f"...{contesto_sx_str}[{parola_target}]{contesto_dx_str}...")
        
        if results_kwic:
            output_str = f"KWIC per '{parola_chiave}' (contesto: {contesto_size} token, {found_count} occorrenze trovate):\n\n" + "\n".join(results_kwic)
        else:
            output_str = f"Nessuna occorrenza trovata per '{parola_chiave}' nel corpus."
        self._display_output(f"KWIC: {parola_chiave}", output_str)


    def andamento(self):
        if not self.corpus_testuale:
            messagebox.showwarning("Corpus Vuoto", "Per favore, carica prima un corpus testuale.", parent=self.root)
            return
        
        parola_chiave = simpledialog.askstring("Andamento Termine", "Inserisci la parola chiave per l'analisi dell'andamento:", parent=self.root)
        if not parola_chiave: return
        
        parola_chiave_lower = parola_chiave.lower()
        frequencies = []
        segment_labels = []

        if len(self.corpus_testuale) == 1: 
            num_chunks = simpledialog.askinteger("Numero Segmenti", "Dividi il documento in quanti segmenti per l'analisi?",
                                                 parent=self.root, minvalue=2, maxvalue=100, initialvalue=10)
            if num_chunks is None: return

            words_in_doc = self._get_processed_words(remove_stopwords=False, specific_text=self.corpus_testuale[0])

            if not words_in_doc:
                self._display_output("Andamento Termine", "Il documento selezionato è vuoto o non contiene parole.")
                return
            
            if len(words_in_doc) < num_chunks :
                 messagebox.showwarning("Segmenti Eccessivi", f"Il documento contiene solo {len(words_in_doc)} parole. Non può essere diviso in {num_chunks} segmenti. Verrà usato un segmento per parola.", parent=self.root)
                 num_chunks = len(words_in_doc)
                 if num_chunks < 1: 
                     self._display_output("Andamento Termine", "Il documento non ha parole per creare segmenti.")
                     return

            chunk_size = max(1, len(words_in_doc) // num_chunks) 

            for i in range(num_chunks):
                start_idx = i * chunk_size
                end_idx = (i + 1) * chunk_size if i < num_chunks - 1 else len(words_in_doc)
                chunk = words_in_doc[start_idx:end_idx]
                if chunk: 
                    frequencies.append(chunk.count(parola_chiave_lower))
                    segment_labels.append(f"Seg. {i+1}")
            
            if not frequencies: 
                self._display_output("Andamento Termine", f"La parola '{parola_chiave}' non è stata trovata o i segmenti erano vuoti.")
                return

            plot_title = f"Andamento di '{parola_chiave}' (Doc. '{self.nomi_file_corpus[0]}' in {num_chunks} segmenti)"
            plot_xlabel = "Segmento del Testo"
            plot_type = 'line'

        else: 
            for i, testo_doc in enumerate(self.corpus_testuale):
                parole_doc = self._get_processed_words(remove_stopwords=False, specific_text=testo_doc)
                frequencies.append(parole_doc.count(parola_chiave_lower))
                segment_labels.append(self.nomi_file_corpus[i] if self.nomi_file_corpus and i < len(self.nomi_file_corpus) else f"Doc {i+1}")
            
            plot_title = f"Andamento di '{parola_chiave}' attraverso i Documenti Caricati"
            plot_xlabel = "Documento"
            plot_type = 'bar'

        if not frequencies or all(f == 0 for f in frequencies): 
            self._display_output("Andamento Termine", f"Nessuna occorrenza di '{parola_chiave}' trovata nel corpus per il grafico.")
            messagebox.showinfo("Andamento Termine", f"La parola '{parola_chiave}' non è stata trovata nel corpus.", parent=self.root)
            return

        plt.figure(figsize=(12, 7)) 
        if plot_type == 'line':
            plt.plot(segment_labels, frequencies, marker='o', linestyle='-', color='dodgerblue')
        else: 
            plt.bar(segment_labels, frequencies, color='skyblue')
        
        plt.title(plot_title, fontsize=14)
        plt.xlabel(plot_xlabel, fontsize=12)
        plt.ylabel("Frequenza Assoluta", fontsize=12)
        plt.xticks(rotation=45, ha="right", fontsize=10) 
        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='--') 
        plt.tight_layout() 
        plt.show()
        self._display_output("Andamento Termine", f"Grafico dell'andamento di '{parola_chiave}' generato e visualizzato.")


    def vista_rete(self):
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

        parole = self._get_processed_words(remove_stopwords=True) 
        if len(parole) < 2: 
            self._display_output("Rete Co-occorrenze", "Non ci sono abbastanza parole nel corpus (dopo rimozione stopwords) per analizzare le co-occorrenze.")
            messagebox.showinfo("Rete Co-occorrenze", "Testo insufficiente per l'analisi.", parent=self.root)
            return

        co_occurrences = Counter()
        for i in range(len(parole) - window_size + 1):
            window_segment = parole[i : i + window_size]
            parole_nella_finestra_uniche = sorted(list(set(window_segment)))
            
            if len(parole_nella_finestra_uniche) < 2: continue 

            for j in range(len(parole_nella_finestra_uniche)):
                for k in range(j + 1, len(parole_nella_finestra_uniche)):
                    pair = tuple(sorted((parole_nella_finestra_uniche[j], parole_nella_finestra_uniche[k])))
                    co_occurrences[pair] += 1
        
        if not co_occurrences:
            self._display_output("Rete Co-occorrenze", "Nessuna co-occorrenza trovata con i parametri specificati.")
            return

        output_str = f"Le {num_cooc} coppie di termini co-occorrenti più frequenti (finestra: {window_size} parole, stopwords escluse):\n"
        output_str += "--------------------------------------------------------------------------------------\n"
        for (p1, p2), freq in co_occurrences.most_common(num_cooc):
            output_str += f"('{p1}', '{p2}'): {freq}\n"
        
        output_str += "\nNota: Questa è una rappresentazione testuale. Per una visualizzazione grafica della rete, sarebbero necessarie librerie aggiuntive (es. NetworkX, Matplotlib)."
        self._display_output("Rete di Co-occorrenze", output_str)
        messagebox.showinfo("Rete di Co-occorrenze", "Analisi delle co-occorrenze completata. I risultati sono nell'area di output.", parent=self.root)

if __name__ == '__main__':
    radice = tk.Tk()
    app = StrumentiTestualiUsai(radice)
    radice.mainloop()
