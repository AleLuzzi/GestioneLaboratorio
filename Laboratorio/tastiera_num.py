import tkinter as tk
from tkinter import ttk
# import mysql.connector


class Tast_num(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.value = tk.StringVar()
		self.var = ""

		self.btn1 = ttk.Button(self, text='1', command=lambda: self._btn_pressed(1))
		self.btn2 = ttk.Button(self, text='2', command=lambda: self._btn_pressed(2))
		self.btn3 = ttk.Button(self, text='3', command=lambda: self._btn_pressed(3))

		self.btn4 = ttk.Button(self, text='4', command=lambda: self._btn_pressed(4))
		self.btn5 = ttk.Button(self, text='5', command=lambda: self._btn_pressed(5))
		self.btn6 = ttk.Button(self, text='6', command=lambda: self._btn_pressed(6))

		self.btn7 = ttk.Button(self, text='7', command=lambda: self._btn_pressed(7))
		self.btn8 = ttk.Button(self, text='8', command=lambda: self._btn_pressed(8))
		self.btn9 = ttk.Button(self, text='9', command=lambda: self._btn_pressed(9))

		self.btn0 = ttk.Button(self, text='0', command=lambda: self._btn_pressed(0))
		self.btndot = ttk.Button(self, text='.', command=lambda: self._btn_pressed('.'))
		self.canc = ttk.Button(self, text='canc', command=self._canc)

		self.btn1.grid(row=0, column=0)
		self.btn2.grid(row=0, column=1)
		self.btn3.grid(row=0, column=2)

		self.btn4.grid(row=1, column=0)
		self.btn5.grid(row=1, column=1)
		self.btn6.grid(row=1, column=2)

		self.btn7.grid(row=2, column=0)
		self.btn8.grid(row=2, column=1)
		self.btn9.grid(row=2, column=2)

		self.btn0.grid(row=3, column=0)
		self.btndot.grid(row=3, column=1)
		self.canc.grid(row=3, column=2)

	def _btn_pressed(self, val):
			self.var = self.var + str(val)
			self.value.set(self.var)
			print(self.value.get())

	def _canc(self):
		self.value.set('')
		self.var = ""


if __name__ == '__main__':
	root = tk.Tk()
	new = Tast_num(root)
	new.grid()
	root.mainloop()
