import tools.gui as gui
import tools.clientinput as ci
import tools.gdlevelclient as glc
import tools.gdleveltools as glt
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


FONT_DOWNLOADING = 'system 70'
FONT_CONSOLE = 'system 20'

MUSIC_KILLBOT = 'killbot.wav'


TIME_DOWNDELAY = 300
TIME_INSTALLWAIT = 6400
TIME_REDFADE = 20
TIME_CONSOLEWAIT = 500
TIME_LINEDELAY = 100
TIME_KILLBOTWAIT = 150


class PageTitle(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.winfo_toplevel().geometry('1280x720')
		tk.Frame.configure(self, bg='black')
		self.winfo_toplevel().configure(bg='black')
		self.winfo_toplevel().title('killbot.exe')
		gui.sound(MUSIC_KILLBOT)

		"""te = tk.Canvas(self, width=1280, height=200, bg='red')
								te.grid(row=4, column=0)
								tl = tk.Label(self, text='Microsoft Windows [Version 10.0.18362.592]', fg='white', bg='black', 
									font=FONT_CONSOLE, anchor='w', justify='left')
								te.create_window(300, 20, window=tl)"""


		self.blank = tk.Label(self, text='', fg='white', bg='black', font=FONT_DOWNLOADING)
		self.blank.grid(row=0, column=0, pady=20)
		self.percentage = 0
		self.inc = 3
		self.l_down = tk.Label(self, text='DOWNLOADING\nKILLBOT.EXE\n0%', fg='white', bg='black', font=FONT_DOWNLOADING)
		self.l_down.grid(row=1, column=0, pady=10)
		self.prog = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=400, mode='determinate')
		self.prog.grid(row=2, column=0)
		self.winfo_toplevel().after(TIME_DOWNDELAY, lambda: self.load(self.percentage, 0, self.inc, 
			self.l_down, self.prog, [self.l_down,
			self.prog], self.blank))

	def clear_wid(self, obj):
		if isinstance(obj, list):
			for b in obj:
				try:
					b.grid_forget()
				except:
					pass
		else:
			obj.grid_forget()

	def load(self, prev_pc, prev_ld, prev_inc, w_down, w_prog, b_list, b_r):
		if prev_pc < 100:
			inc = 3
			if prev_inc == 5:
				inc = 3
			else:
				inc = prev_inc + 1
			perc = prev_pc + inc
			ld = prev_ld + inc
			w_down.config(text='DOWNLOADING\nKILLBOT.EXE\n' + str(perc) + '%')
			w_prog['value'] = ld
			self.winfo_toplevel().update_idletasks()
			self.winfo_toplevel().after(TIME_DOWNDELAY, lambda: self.load(perc, ld, inc, w_down, w_prog, b_list, b_r))
		else:
			self.winfo_toplevel().after(TIME_DOWNDELAY, lambda: self.installing(b_list, b_r))

	def installing(self, b_list, b_r):
		self.l_down.config(text='DOWNLOADING\nKILLBOT.EXE\nINSTALLING...')
		self.winfo_toplevel().after(TIME_INSTALLWAIT, lambda: self.red_fade((255, 0, 0), b_list, b_r))

	def red_fade(self, prev_tup, b_list, b_r):
		self.clear_wid(b_list)
		b_r.config(bg=gui.rgb(prev_tup))
		b_r.grid(row=0, column=0, pady=0)
		self.winfo_toplevel().config(bg=gui.rgb(prev_tup))
		new_tup = (prev_tup[0] - 12, prev_tup[1], prev_tup[2])
		if new_tup[0] > 0:
			self.winfo_toplevel().after(TIME_REDFADE, lambda: self.red_fade(new_tup, [], b_r))
		else:
			cv = tk.Canvas(self, width=1280, height=720, bg='black')
			cv.grid(row=0, column=0)
			self.winfo_toplevel().after(TIME_CONSOLEWAIT, lambda: self.console(0, cv))

	def console(self, step, cv):
		spec_x = [0, 2, 50, 165]
		labels = [
		tk.Label(self, text='Microsoft Windows [Version 10.0.18362.592]', fg='white', bg='black', 
			font=FONT_CONSOLE, anchor='w'),
		tk.Label(self, text='(c) Microsoft Corporation. All rights reserved.', fg='white', bg='black', 
			font=FONT_CONSOLE, anchor='w'),
		tk.Label(self, text='C: \\Users\\Player PC> Run: killbot.exe', fg='white', bg='black', 
			font=FONT_CONSOLE, anchor='w'),
		tk.Label(self, text='Running Program...', fg='white', bg='black', 
			font=FONT_CONSOLE, anchor='w')]
		if step < 4:
			cv.create_window(300 - spec_x[step], 30 + (step * 40), window=labels[step])
			self.winfo_toplevel().after(TIME_LINEDELAY, lambda: self.console(step + 1, cv))
		else:
			self.winfo_toplevel().after(TIME_KILLBOTWAIT, lambda: self.killbot(cv))

	def killbot(self, cv):
		kb = tk.Label(self, text='killbot.exe', fg='red', bg='black', 
			font=FONT_CONSOLE, anchor='w')
		cv.create_window(75, 230, window=kb)

