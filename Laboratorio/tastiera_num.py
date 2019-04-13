import tkinter as tk
from tkinter import ttk
# import mysql.connector


class Tast_num(tk.Toplevel):
	def __init__(self, parent):
		tk.Toplevel.__init__(self, parent)

		self.value = tk.StringVar()
		self.var = ""

		style = ttk.Style()
		style.configure('Ale.TButton', font=('Verdana', 15))

		self.display = tk.Entry(self, textvariable=self.value, font=('Verdana', 15))
		self.btn1 = ttk.Button(self, text='1', style='Ale.TButton', command=lambda: self._btn_pressed(1))
		self.btn2 = ttk.Button(self, text='2', style='Ale.TButton', command=lambda: self._btn_pressed(2))
		self.btn3 = ttk.Button(self, text='3', style='Ale.TButton', command=lambda: self._btn_pressed(3))

		self.btn4 = ttk.Button(self, text='4', style='Ale.TButton', command=lambda: self._btn_pressed(4))
		self.btn5 = ttk.Button(self, text='5', style='Ale.TButton', command=lambda: self._btn_pressed(5))
		self.btn6 = ttk.Button(self, text='6', style='Ale.TButton', command=lambda: self._btn_pressed(6))

		self.btn7 = ttk.Button(self, text='7', style='Ale.TButton', command=lambda: self._btn_pressed(7))
		self.btn8 = ttk.Button(self, text='8', style='Ale.TButton', command=lambda: self._btn_pressed(8))
		self.btn9 = ttk.Button(self, text='9', style='Ale.TButton', command=lambda: self._btn_pressed(9))

		self.btn0 = ttk.Button(self, text='0', style='Ale.TButton', command=lambda: self._btn_pressed(0))
		self.btndot = ttk.Button(self, text='.', style='Ale.TButton', command=lambda: self._btn_pressed('.'))
		self.canc = ttk.Button(self, text='canc', style='Ale.TButton', command=self.clear)
		self.conferma = ttk.Button(self, text='conferma', style='Ale.TButton', command=self.destroy)

		self.canc_uno = ttk.Button(self, text='<-', style='Ale.TButton', command=self._canc)

		self.display.grid(row=0, column=0, columnspan=3)
		self.btn1.grid(row=1, column=0)
		self.btn2.grid(row=1, column=1)
		self.btn3.grid(row=1, column=2)

		self.btn4.grid(row=2, column=0)
		self.btn5.grid(row=2, column=1)
		self.btn6.grid(row=2, column=2)

		self.btn7.grid(row=3, column=0)
		self.btn8.grid(row=3, column=1)
		self.btn9.grid(row=3, column=2)

		self.btn0.grid(row=4, column=0)
		self.btndot.grid(row=4, column=1)
		self.canc_uno.grid(row=4, column=2)

		self.canc.grid(row=5, column=1)
		self.conferma.grid(row=5, column=2)

		self.wait_window()

	def _btn_pressed(self, val):
		self.var = self.var + str(val)
		if self.var.startswith('0'):
			self.clear()
		else:
			self.value.set(self.var)

	def clear(self):
		self.value.set('')
		self.var = ""

	def _canc(self):
		self.var = self.var[:-1]
		self.value.set(self.var)


if __name__ == '__main__':
	root = tk.Tk()
	new = Tast_num(root)
	new.grid()
	root.mainloop()
