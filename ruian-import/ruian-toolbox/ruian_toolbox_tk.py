# -*- coding: utf-8 -*-
# Hlavní ovládání aplikací. Používá framework Tk. Nehodí se k dockerizaci

import tkFont
import ttk
from Tkinter import *
from idlelib import ToolTip

from ruian_services.services import config as ruian_services_config
from shared_tools import ruian_importer_config, ruian_download_config, GIS_LAYERS


class SetupForm(Frame):
    tab_frames_border = 10

    def _get_frame(self, a_name):
        return Frame(self, name=a_name, bd=5)

    def _get_top_label(self, frame, description):
        # lbl = Label(frame, wraplength='4i', justify=LEFT, anchor=N, text=description)
        lbl = Text(frame, height=3, bd=0, wrap=WORD, font=self.customFont, bg="slate gray")
        lbl.insert(INSERT, description)
        lbl.config(state=DISABLED)
        # lbl.pack()
        lbl.grid(row=0, column=0, columnspan=2, sticky=W + E, pady=5)

    def __init__(self, root_element):
        self.customFont = tkFont.Font(family="Helvetica", size=9)

        Frame.__init__(self, root_element)
        self.pack(expand=Y, fill=BOTH)

        self.master.title('RÚIAN Toolbox - nastavení')
        self.editsRow = 0
        self.create_widgets()

    def create_widgets(self):
        nb = ttk.Notebook(self, name='notebook')
        nb.enable_traversal()
        nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)

        self.create_description_tab(nb)
        self.create_downloader_tab(nb)
        self.create_import_tab(nb)
        self.create_services_tab(nb)

        buttonsFrame = Frame(self, bd=5)
        btn = Button(buttonsFrame, text='Uložit konfiguraci a zavřít', underline=0)
        btn.pack(side=RIGHT, fill=BOTH)
        buttonsFrame.pack(side=BOTTOM, fill=BOTH)

    def create_description_tab(self, nb):
        frame = self._get_frame('descrip')

        self._get_top_label(frame, "Tato aplikace umožňuje nastavit parametry komponent RÚIAN Toolbox.")

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure((0, 1), weight=1, uniform=1)

        nb.add(frame, text='Úvod ', underline=0, padding=2)

    def _say_neat(self, v):
        v.set('Yeah, I know...')
        self.update()
        self.after(500, v.set(''))

    def add_control(self, control, a_column=0, a_sticky=W):
        control.grid(row=self.editsRow, column=a_column, sticky=a_sticky)
        self.editsRow = self.editsRow + 1
        return control

    def add_control_with_label(self, frame, control, caption, edit_value=""):
        label = Label(frame, wraplength='4i', justify=LEFT, anchor=N, text=caption)
        label.grid(row=self.editsRow, column=0, sticky=E)
        control.grid(row=self.editsRow, column=1, sticky=W + E + N + S)
        if edit_value is not None:
            if edit_value != "":
                control.insert(0, edit_value)
        self.editsRow += 1
        return control

    def create_downloader_tab(self, nb):
        frame = self._get_frame("download")

        config = ruian_download_config()

        self._get_top_label(frame, "RÚIAN Downloader umožňuje stáhnout aktuální databázi včetně stahování aktualizací.")
        self.editsRow = 1

        self.add_control(Label(frame, wraplength='4i', justify=LEFT, anchor=N, text="  Konfigurace:"))
        edit = self.add_control(Entry(frame, bd=1), a_sticky=W + E)
        edit.insert(0, config.fileName)

        self.add_control(Label(frame, wraplength='4i', justify=LEFT, anchor=N, text="  Adresář se staženými daty:"))
        edit = self.add_control(Entry(frame, bd=1), a_sticky=W + E)
        edit.insert(0, config.dataDir)

        CheckVar1 = IntVar()
        self.add_control(
            Checkbutton(frame, text="Rozbalit stažené soubory", variable=CheckVar1, onvalue=1, offvalue=0))

        CheckVar2 = IntVar()
        self.add_control(
            Checkbutton(frame, text="Spustit importér po stažení dat", variable=CheckVar2, onvalue=1, offvalue=0))

        check_var4 = IntVar()
        check_var4.set(1)  # int(config.ignoreHistoricalData))
        self.add_control(
            Checkbutton(frame, text="Ignorovat historická data", variable=check_var4, onvalue=1, offvalue=0))

        check_var3 = IntVar()
        self.add_control(Checkbutton(frame, text="Stahovat automaticky každý den", variable=check_var3, onvalue=1))

        self.add_control(Label(frame, wraplength='4i', justify=LEFT, anchor=N, text="  Čas stahování:"))
        b = self.add_control(Entry(frame, bd=1), a_sticky=W)
        b.insert(0, config.automaticDownloadTime)
        ToolTip.ToolTip(b, 'Čas, ve který se mají stahovat denní aktualizace')

        self.editsRow += 1

        neatVar = StringVar()
        self.add_control(Button(frame, text='Stáhni data ', underline=0, command=lambda v=neatVar: self._say_neat(v)),
                         a_sticky=E)

        frame.columnconfigure(0, weight=1, uniform=1)
        nb.add(frame, text='Downloader ')

    def create_import_tab(self, nb):
        frame = self._get_frame("importTabFrame")
        config = ruian_importer_config()

        self._get_top_label(
            frame,
            "RÚIAN Importer umožňuje importovat stažený stav do databáze včetně načtení aktualizačních balíčků."
        )
        self.editsRow = 1

        self.add_control_with_label(frame, Entry(frame, bd=1), "Konfigurace:", edit_value=config.fileName)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Data:", edit_value=config.dataDir)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Jméno databáze:", edit_value=config.dbname)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Host:", edit_value=config.host)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Port:", edit_value=config.port)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Uživatel:", edit_value=config.user)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Heslo:", edit_value=config.password)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Načítej pouze tyto vrstvy:", edit_value=config.layers)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Cesta k OS4Geo:", edit_value=config.os4GeoPath)

        self.editsRow += 1
        neatVar = StringVar()
        self.add_control(Button(frame, text='Importuj ', underline=0, command=lambda v=neatVar: self._say_neat(v)),
                         a_column=1, a_sticky=E)

        frame.columnconfigure(1, weight=1, uniform=1)
        nb.add(frame, text='Importer ', underline=0)

    def create_services_tab(self, nb):
        frame = self._get_frame("servicesTabFrame")
        config = ruian_services_config.config

        self._get_top_label(
            frame,
            "RÚIAN Services umožňuje využívat repliku databáze RÚIAN pomocí standardizovaných služeb."
        )
        self.editsRow = 1

        self.add_control_with_label(frame, Entry(frame, bd=1), "Jméno serveru:", edit_value=config.serverHTTP)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Port:", edit_value=config.portNumber)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Cesta na server:", edit_value=config.servicesWebPath)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Database host:", edit_value=config.databaseHost)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Database port:", edit_value=config.databasePort)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Database name:", edit_value=config.databaseName)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Database user name:",
                                    edit_value=config.databaseUserName)
        self.add_control_with_label(frame, Entry(frame, bd=1), "Database password:", edit_value=config.databasePassword)
        self.add_control_with_label(frame, Entry(frame, bd=1), "noCGIAppServerHTTP:",
                                    edit_value=config.noCGIAppServerHTTP)
        self.add_control_with_label(frame, Entry(frame, bd=1), "noCGIAppPortNumber:",
                                    edit_value=config.noCGIAppPortNumber)

        frame.columnconfigure(1, weight=1, uniform=1)
        nb.add(frame, text='Services ', underline=0)


def center_window(window, w=300, h=200):
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


if __name__ == '__main__':
    root = Tk()
    setup_form = SetupForm(root)
    center_window(root, 600, 350)
    root.mainloop()
