import tkinter as tk


class Controllo(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Controllo Versione")
        self.attributes("-topmost", True)

        update = False

        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        self.geometry("+%d+%d" % (x, y))

        # Gets downloaded version
        versionsource = open('version.txt', 'r')
        versioncontents = versionsource.read()
        print(versioncontents)

        # gets newest version
        updatesource = open('z:\\Laboratorio\\version.txt')
        updatecontents = updatesource.read()
        print(updatecontents)

        # checks for updates
        for i in range(0, 21):
            if updatecontents[i] != versioncontents[i]:
                datalabel = tk.Label(self,
                                     text="\n\nCi sono aggiornamenti disponibili.\n\n")
                datalabel.grid()
                update = True
                break
        if not update:
            versionlabel = tk.Label(self,
                                    text="\n\nNon ci sono aggiornamenti disponibili.\n\n")
            versionlabel.grid()

if __name__ == "__main__":
    root = tk.Tk()
    new = Controllo()
    root.mainloop()