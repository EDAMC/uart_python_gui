
from mimetypes import init
from site import getusersitepackages
from struct import pack
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter.filedialog import asksaveasfile

import binascii
import pdb
import sys
import os.path
import sys
import glob
import serial
import threading
import time
import math
import numpy
import csv
_script = sys.argv[0]
_location = os.path.dirname(_script)

#import py_gui_support

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = 'gray40' # X11 color: #666666
_ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
_ana2color = 'beige' # X11 color: #f5f5dc
_tabfg1 = 'black' 
_tabfg2 = 'black' 
_tabbg1 = 'grey75' 
_tabbg2 = 'grey89' 
_bgmode = 'light'

global ser, connected, parameters_checked
ser = ''
connected = 0

_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran:
       return
    style = ttk.Style()
    if sys.platform == "win32":
       style.theme_use('winnative')
    style.configure('.',background=_bgcolor)
    style.configure('.',foreground=_fgcolor)
    style.configure('.',font='TkDefaultFont')
    style.map('.',background =
       [('selected', _compcolor), ('active',_ana2color)])
    if _bgmode == 'dark':
       style.map('.',foreground =
         [('selected', 'white'), ('active','white')])
    else:
       style.map('.',foreground =
         [('selected', 'black'), ('active','black')])
    style.configure('Vertical.TScrollbar',  background=_bgcolor,
        arrowcolor= _fgcolor)
    style.configure('Horizontal.TScrollbar',  background=_bgcolor,
        arrowcolor= _fgcolor)
    _style_code_ran = 1

class serial_com_top:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("800x480+534+273")
        top.minsize(120, 1)
        top.maxsize(2400, 1100)
        top.resizable(1,  1)
        top.title("Serial_Com")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top
        self.combobox = tk.StringVar()

        self.prmtr_lbl = tk.Label(self.top)
        self.prmtr_lbl.place(relx=0.018, rely=0.046, height=22, width=84)
        self.prmtr_lbl.configure(activebackground="#f9f9f9")
        self.prmtr_lbl.configure(anchor='w')
        self.prmtr_lbl.configure(background="#d9d9d9")
        self.prmtr_lbl.configure(compound='left')
        self.prmtr_lbl.configure(disabledforeground="#a3a3a3")
        self.prmtr_lbl.configure(font="-family {Segoe UI Black} -size 9 -weight bold")
        self.prmtr_lbl.configure(foreground="#000000")
        self.prmtr_lbl.configure(highlightbackground="#d9d9d9")
        self.prmtr_lbl.configure(highlightcolor="black")
        self.prmtr_lbl.configure(text='''Параметр''')

        self.fr_ch_val_lbl = tk.Label(self.top)
        self.fr_ch_val_lbl.place(relx=0.15, rely=0.042, height=24, width=153)
        self.fr_ch_val_lbl.configure(activebackground="#f9f9f9")
        self.fr_ch_val_lbl.configure(anchor='w')
        self.fr_ch_val_lbl.configure(background="#d9d9d9")
        self.fr_ch_val_lbl.configure(compound='left')
        self.fr_ch_val_lbl.configure(disabledforeground="#a3a3a3")
        self.fr_ch_val_lbl.configure(font="-family {Segoe UI Black} -size 9 -weight bold")
        self.fr_ch_val_lbl.configure(foreground="#000000")
        self.fr_ch_val_lbl.configure(highlightbackground="#d9d9d9")
        self.fr_ch_val_lbl.configure(highlightcolor="black")
        self.fr_ch_val_lbl.configure(text='''Значение 1-го канала''')

        self.sec_ch_val_lbl = tk.Label(self.top)
        self.sec_ch_val_lbl.place(relx=0.344, rely=0.046, height=22, width=167)
        self.sec_ch_val_lbl.configure(activebackground="#f9f9f9")
        self.sec_ch_val_lbl.configure(anchor='w')
        self.sec_ch_val_lbl.configure(background="#d9d9d9")
        self.sec_ch_val_lbl.configure(compound='left')
        self.sec_ch_val_lbl.configure(disabledforeground="#a3a3a3")
        self.sec_ch_val_lbl.configure(font="-family {Segoe UI Black} -size 9 -weight bold")
        self.sec_ch_val_lbl.configure(foreground="#000000")
        self.sec_ch_val_lbl.configure(highlightbackground="#d9d9d9")
        self.sec_ch_val_lbl.configure(highlightcolor="black")
        self.sec_ch_val_lbl.configure(text='''''')

        _style_code()
        self.TSeparator1 = ttk.Separator(self.top)
        self.TSeparator1.place(relx=0.143, rely=0.0,  relheight=0.929)
        self.TSeparator1.configure(orient="vertical")

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.menubar.add_command(compound='left', label='Сохранить конфигурацию',command =save_file)

        self.menubar.add_command(compound='left', label='Загрузить конфигурацию',command =load_file)

        # self.menubar.add_command(compound='left',label='Выход', command =exit_programm)

        self.TSeparator2 = ttk.Separator(self.top)
        self.TSeparator2.place(relx=0.0, rely=0.09,  relwidth=0.55)

        self.TSeparator3 = ttk.Separator(self.top)
        self.TSeparator3.place(relx=0.328, rely=0.0,  relheight=0.929)
        self.TSeparator3.configure(orient="vertical")

        self.TSeparator4 = ttk.Separator(self.top)
        self.TSeparator4.place(relx=0.55, rely=0.0,  relheight=0.929)
        self.TSeparator4.configure(orient="vertical")

        self.connection_frm = tk.LabelFrame(self.top)
        self.connection_frm.place(relx=0.568, rely=0.067, relheight=0.279
                , relwidth=0.416)
        self.connection_frm.configure(relief='groove')
        self.connection_frm.configure(font="-family {MS Reference Sans Serif} -size 11 -weight bold")
        self.connection_frm.configure(foreground="#000000")
        self.connection_frm.configure(text='''Подключение''')
        self.connection_frm.configure(background="#d9d9d9")
        self.connection_frm.configure(highlightbackground="#d9d9d9")
        self.connection_frm.configure(highlightcolor="black")

        self.com_lbl = tk.Label(self.connection_frm)
        self.com_lbl.place(relx=0.102, rely=0.224, height=30, width=89
                , bordermode='ignore')
        self.com_lbl.configure(activebackground="#f9f9f9")
        self.com_lbl.configure(anchor='w')
        self.com_lbl.configure(background="#d9d9d9")
        self.com_lbl.configure(compound='left')
        self.com_lbl.configure(disabledforeground="#a3a3a3")
        self.com_lbl.configure(foreground="#000000")
        self.com_lbl.configure(highlightbackground="#d9d9d9")
        self.com_lbl.configure(highlightcolor="black")
        self.com_lbl.configure(text='''COM port:''')

        self.br_lbl = tk.Label(self.connection_frm)
        self.br_lbl.place(relx=0.102, rely=0.672, height=30, width=89
                , bordermode='ignore')
        self.br_lbl.configure(activebackground="#f9f9f9")
        self.br_lbl.configure(anchor='w')
        self.br_lbl.configure(background="#d9d9d9")
        self.br_lbl.configure(compound='left')
        self.br_lbl.configure(disabledforeground="#a3a3a3")
        self.br_lbl.configure(foreground="#000000")
        self.br_lbl.configure(highlightbackground="#d9d9d9")
        self.br_lbl.configure(highlightcolor="black")
        self.br_lbl.configure(text='''Baud Rate:''')

        br = tk.StringVar()
        br_list = ["110", "300", "600", "1200", "2400", "4800",\
                   "9600", "14400", "19200", "38400", "57600",\
                   "115200", "128000","256000"]
        
        self.Br_box = ttk.Combobox(self.connection_frm, values = br_list)
        self.Br_box.place(relx=0.318, rely=0.634, relheight=0.224, relwidth=0.414
                , bordermode='ignore')
        self.Br_box.configure(textvariable=br)
        self.Br_box.configure(takefocus="")

        com = tk.StringVar()
        self.Com_box = ttk.Combobox(self.connection_frm, values = serial_ports())
        self.Com_box.place(relx=0.318, rely=0.209, relheight=0.224
                , relwidth=0.414, bordermode='ignore')
        self.Com_box.configure(textvariable=com)
        self.Com_box.configure(takefocus="")
        self.Com_box.configure(cursor="fleur")

        self.close_p_btn = tk.Button(self.connection_frm)
        self.close_p_btn.place(relx=0.730, rely=0.214, height=24, width=87, bordermode='ignore')
        self.close_p_btn.configure(activebackground="#fd4448")
        self.close_p_btn.configure(activeforeground="black")
        self.close_p_btn.configure(background="#ff4246")
        self.close_p_btn.configure(compound='left')
        self.close_p_btn.configure(cursor="X_cursor")
        self.close_p_btn.configure(disabledforeground="#a3a3a3")
        self.close_p_btn.configure(foreground="#000000")
        self.close_p_btn.configure(highlightbackground="#d9d9d9")
        self.close_p_btn.configure(highlightcolor="black")
        self.close_p_btn.configure(pady="0")
        self.close_p_btn.configure(text='''Закрыть порт''')
        self.close_p_btn.configure(command=close_port)

        self.check_params_btn = tk.Button(self.top)
        self.check_params_btn.place(relx=0.609, rely=0.492, height=24, width=217) #0.609, rely=0.492

        self.check_params_btn.configure(activebackground="#d3ab6d")
        self.check_params_btn.configure(activeforeground="black")
        self.check_params_btn.configure(background="#d3ab6d")
        self.check_params_btn.configure(compound='left')
        self.check_params_btn.configure(cursor="hand2")
        self.check_params_btn.configure(disabledforeground="#d3ab6d")
        self.check_params_btn.configure(font="-family {Terminal_Hex} -size 9 -weight bold")
        self.check_params_btn.configure(foreground="#000000")
        self.check_params_btn.configure(highlightbackground="#ffffff")
        self.check_params_btn.configure(highlightcolor="black")
        self.check_params_btn.configure(pady="0")
        self.check_params_btn.configure(text='''Установка параметров''')
        self.check_params_btn.configure(command=check_parameters)

        self.amp_pos_entry_ch1 = tk.Entry(self.top)
        self.amp_pos_entry_ch1.place(relx=0.158, rely=0.104, height=20
                , relwidth=0.105)
        self.amp_pos_entry_ch1.configure(background="white")
        self.amp_pos_entry_ch1.configure(disabledforeground="#a3a3a3")
        self.amp_pos_entry_ch1.configure(font="TkFixedFont")
        self.amp_pos_entry_ch1.configure(foreground="#000000")
        self.amp_pos_entry_ch1.configure(highlightbackground="#d9d9d9")
        self.amp_pos_entry_ch1.configure(highlightcolor="black")
        self.amp_pos_entry_ch1.configure(insertbackground="black")
        self.amp_pos_entry_ch1.configure(selectbackground="#c4c4c4")
        self.amp_pos_entry_ch1.configure(selectforeground="black")

    
        self.amp_neg_entry_ch1 = tk.Entry(self.top)
        self.amp_neg_entry_ch1.place(relx=0.156, rely=0.204, height=20
                , relwidth=0.105)
        self.amp_neg_entry_ch1.configure(background="white")
        self.amp_neg_entry_ch1.configure(disabledforeground="#a3a3a3")
        self.amp_neg_entry_ch1.configure(font="TkFixedFont")
        self.amp_neg_entry_ch1.configure(foreground="#000000")
        self.amp_neg_entry_ch1.configure(highlightbackground="#d9d9d9")
        self.amp_neg_entry_ch1.configure(highlightcolor="black")
        self.amp_neg_entry_ch1.configure(insertbackground="black")
        self.amp_neg_entry_ch1.configure(selectbackground="#c4c4c4")
        self.amp_neg_entry_ch1.configure(selectforeground="black")

        self.time_pos_entry_ch1 = tk.Entry(self.top)
        self.time_pos_entry_ch1.place(relx=0.156, rely=0.283, height=20
                , relwidth=0.105)
        self.time_pos_entry_ch1.configure(background="white")
        self.time_pos_entry_ch1.configure(disabledforeground="#a3a3a3")
        self.time_pos_entry_ch1.configure(font="TkFixedFont")
        self.time_pos_entry_ch1.configure(foreground="#000000")
        self.time_pos_entry_ch1.configure(highlightbackground="#d9d9d9")
        self.time_pos_entry_ch1.configure(highlightcolor="black")
        self.time_pos_entry_ch1.configure(insertbackground="black")
        self.time_pos_entry_ch1.configure(selectbackground="#c4c4c4")
        self.time_pos_entry_ch1.configure(selectforeground="black")

        self.time_neg_entry_ch1 = tk.Entry(self.top)
        self.time_neg_entry_ch1.place(relx=0.156, rely=0.385, height=20
                , relwidth=0.105)
        self.time_neg_entry_ch1.configure(background="white")
        self.time_neg_entry_ch1.configure(disabledforeground="#a3a3a3")
        self.time_neg_entry_ch1.configure(font="TkFixedFont")
        self.time_neg_entry_ch1.configure(foreground="#000000")
        self.time_neg_entry_ch1.configure(highlightbackground="#d9d9d9")
        self.time_neg_entry_ch1.configure(highlightcolor="black")
        self.time_neg_entry_ch1.configure(insertbackground="black")
        self.time_neg_entry_ch1.configure(selectbackground="#c4c4c4")
        self.time_neg_entry_ch1.configure(selectforeground="black")

        self.TSeparator2_1 = ttk.Separator(self.top)
        self.TSeparator2_1.place(relx=0.0, rely=0.181,  relwidth=0.55)

        self.TSeparator2_1_1 = ttk.Separator(self.top)
        self.TSeparator2_1_1.place(relx=0.0, rely=0.271,  relwidth=0.55)

        self.TSeparator2_1_1_1 = ttk.Separator(self.top)
        self.TSeparator2_1_1_1.place(relx=0.0, rely=0.363,  relwidth=0.55)

        self.TSeparator2_1_1_1_1 = ttk.Separator(self.top)
        self.TSeparator2_1_1_1_1.place(relx=0.0, rely=0.446,  relwidth=0.55)

        self.TSeparator2_1_1_1_1_1 = ttk.Separator(self.top)
        self.TSeparator2_1_1_1_1_1.place(relx=0.0, rely=0.54,  relwidth=0.55)

        self.TSeparator2_1_1_1_1_1_1 = ttk.Separator(self.top)
        self.TSeparator2_1_1_1_1_1_1.place(relx=0.0, rely=0.633, relwidth=0.55)

        self.TSeparator2_1_1_1_1_1_1_1 = ttk.Separator(self.top)
        self.TSeparator2_1_1_1_1_1_1_1.place(relx=0.0, rely=0.721
                ,  relwidth=0.55)

        self.TSeparator2_1_1_1_1_1_1_1_1 = ttk.Separator(self.top)
        self.TSeparator2_1_1_1_1_1_1_1_1.place(relx=0.0, rely=0.825
                ,  relwidth=0.55)

        self.TSeparator2_1_1_1_1_1_1_1_1_1 = ttk.Separator(self.top)
        self.TSeparator2_1_1_1_1_1_1_1_1_1.place(relx=0.0, rely=0.925
                ,  relwidth=0.55)

        self.time_pause_entry_ch1 = tk.Entry(self.top)
        self.time_pause_entry_ch1.place(relx=0.156, rely=0.465, height=20
                , relwidth=0.105)
        self.time_pause_entry_ch1.configure(background="white")
        self.time_pause_entry_ch1.configure(disabledforeground="#a3a3a3")
        self.time_pause_entry_ch1.configure(font="TkFixedFont")
        self.time_pause_entry_ch1.configure(foreground="#000000")
        self.time_pause_entry_ch1.configure(highlightbackground="#d9d9d9")
        self.time_pause_entry_ch1.configure(highlightcolor="black")
        self.time_pause_entry_ch1.configure(insertbackground="black")
        self.time_pause_entry_ch1.configure(selectbackground="#c4c4c4")
        self.time_pause_entry_ch1.configure(selectforeground="black")

        self.period_entry_ch1 = tk.Entry(self.top)
        self.period_entry_ch1.place(relx=0.156, rely=0.567, height=20
                , relwidth=0.105)
        self.period_entry_ch1.configure(background="white")
        self.period_entry_ch1.configure(disabledforeground="#a3a3a3")
        self.period_entry_ch1.configure(font="TkFixedFont")
        self.period_entry_ch1.configure(foreground="#000000")
        self.period_entry_ch1.configure(highlightbackground="#d9d9d9")
        self.period_entry_ch1.configure(highlightcolor="black")
        self.period_entry_ch1.configure(insertbackground="black")
        self.period_entry_ch1.configure(selectbackground="#c4c4c4")
        self.period_entry_ch1.configure(selectforeground="black")

        self.numpack_entry_ch1 = tk.Entry(self.top)
        self.numpack_entry_ch1.place(relx=0.156, rely=0.646, height=20
                , relwidth=0.105)
        self.numpack_entry_ch1.configure(background="white")
        self.numpack_entry_ch1.configure(disabledforeground="#a3a3a3")
        self.numpack_entry_ch1.configure(font="TkFixedFont")
        self.numpack_entry_ch1.configure(foreground="#000000")
        self.numpack_entry_ch1.configure(highlightbackground="#d9d9d9")
        self.numpack_entry_ch1.configure(highlightcolor="black")
        self.numpack_entry_ch1.configure(insertbackground="black")
        self.numpack_entry_ch1.configure(selectbackground="#c4c4c4")
        self.numpack_entry_ch1.configure(selectforeground="black")

        self.time_frame_entry_ch1 = tk.Entry(self.top)
        self.time_frame_entry_ch1.place(relx=0.158, rely=0.75, height=20
                , relwidth=0.105)
        self.time_frame_entry_ch1.configure(background="white")
        self.time_frame_entry_ch1.configure(disabledforeground="#a3a3a3")
        self.time_frame_entry_ch1.configure(font="TkFixedFont")
        self.time_frame_entry_ch1.configure(foreground="#000000")
        self.time_frame_entry_ch1.configure(highlightbackground="#d9d9d9")
        self.time_frame_entry_ch1.configure(highlightcolor="black")
        self.time_frame_entry_ch1.configure(insertbackground="black")
        self.time_frame_entry_ch1.configure(selectbackground="#c4c4c4")
        self.time_frame_entry_ch1.configure(selectforeground="black")


        self.num_of_frames_entry_ch1 = tk.Entry(self.top)
        self.num_of_frames_entry_ch1.place(relx=0.156, rely=0.85, height=20
                , relwidth=0.105)
        self.num_of_frames_entry_ch1.configure(background="white")
        self.num_of_frames_entry_ch1.configure(disabledforeground="#a3a3a3")
        self.num_of_frames_entry_ch1.configure(font="TkFixedFont")
        self.num_of_frames_entry_ch1.configure(foreground="#000000")
        self.num_of_frames_entry_ch1.configure(highlightbackground="#d9d9d9")
        self.num_of_frames_entry_ch1.configure(highlightcolor="black")
        self.num_of_frames_entry_ch1.configure(insertbackground="black")
        self.num_of_frames_entry_ch1.configure(selectbackground="#c4c4c4")
        self.num_of_frames_entry_ch1.configure(selectforeground="black")

        self.amp_pos_lbl = tk.Label(self.top)
        self.amp_pos_lbl.place(relx=0.0, rely=0.102, height=26, width=104)
        self.amp_pos_lbl.configure(activebackground="#f9f9f9")
        self.amp_pos_lbl.configure(anchor='w')
        self.amp_pos_lbl.configure(background="#d9d9d9")
        self.amp_pos_lbl.configure(compound='left')
        self.amp_pos_lbl.configure(disabledforeground="#a3a3a3")
        self.amp_pos_lbl.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.amp_pos_lbl.configure(foreground="#000000")
        self.amp_pos_lbl.configure(highlightbackground="#d9d9d9")
        self.amp_pos_lbl.configure(highlightcolor="black")
        self.amp_pos_lbl.configure(relief="solid")
        self.amp_pos_lbl.configure(text='''AMP_POS, uA''')

        self.amp_neg_lbl = tk.Label(self.top)
        self.amp_neg_lbl.place(relx=0.0, rely=0.204, height=26, width=104)
        self.amp_neg_lbl.configure(activebackground="#f9f9f9")
        self.amp_neg_lbl.configure(anchor='w')
        self.amp_neg_lbl.configure(background="#d9d9d9")
        self.amp_neg_lbl.configure(compound='left')
        self.amp_neg_lbl.configure(disabledforeground="#a3a3a3")
        self.amp_neg_lbl.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.amp_neg_lbl.configure(foreground="#000000")
        self.amp_neg_lbl.configure(highlightbackground="#d9d9d9")
        self.amp_neg_lbl.configure(highlightcolor="black")
        self.amp_neg_lbl.configure(relief="solid")
        self.amp_neg_lbl.configure(text='''AMP_NEG,uA''')

        self.time_pos_lbl = tk.Label(self.top)
        self.time_pos_lbl.place(relx=0.0, rely=0.283, height=26, width=104)
        self.time_pos_lbl.configure(activebackground="#f9f9f9")
        self.time_pos_lbl.configure(anchor='w')
        self.time_pos_lbl.configure(background="#d9d9d9")
        self.time_pos_lbl.configure(compound='left')
        self.time_pos_lbl.configure(disabledforeground="#a3a3a3")
        self.time_pos_lbl.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.time_pos_lbl.configure(foreground="#000000")
        self.time_pos_lbl.configure(highlightbackground="#d9d9d9")
        self.time_pos_lbl.configure(highlightcolor="black")
        self.time_pos_lbl.configure(relief="solid")
        self.time_pos_lbl.configure(text='''TIME_POS, us''')

        self.time_neg_lbl = tk.Label(self.top)
        self.time_neg_lbl.place(relx=0.0, rely=0.385, height=27, width=104)
        self.time_neg_lbl.configure(activebackground="#f9f9f9")
        self.time_neg_lbl.configure(anchor='w')
        self.time_neg_lbl.configure(background="#d9d9d9")
        self.time_neg_lbl.configure(compound='left')
        self.time_neg_lbl.configure(disabledforeground="#a3a3a3")
        self.time_neg_lbl.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.time_neg_lbl.configure(foreground="#000000")
        self.time_neg_lbl.configure(highlightbackground="#d9d9d9")
        self.time_neg_lbl.configure(highlightcolor="black")
        self.time_neg_lbl.configure(relief="solid")
        self.time_neg_lbl.configure(text='''TIME_NEG, us''')

        self.time_pause_lbl = tk.Label(self.top)
        self.time_pause_lbl.place(relx=0.0, rely=0.465, height=26, width=104)
        self.time_pause_lbl.configure(activebackground="#f9f9f9")
        self.time_pause_lbl.configure(anchor='w')
        self.time_pause_lbl.configure(background="#d9d9d9")
        self.time_pause_lbl.configure(compound='left')
        self.time_pause_lbl.configure(disabledforeground="#a3a3a3")
        self.time_pause_lbl.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.time_pause_lbl.configure(foreground="#000000")
        self.time_pause_lbl.configure(highlightbackground="#d9d9d9")
        self.time_pause_lbl.configure(highlightcolor="black")
        self.time_pause_lbl.configure(relief="solid")
        self.time_pause_lbl.configure(text='''TIME_PAUSE, us''')

        self.period_lbl = tk.Label(self.top)
        self.period_lbl.place(relx=0.0, rely=0.563, height=26, width=81)
        self.period_lbl.configure(activebackground="#f9f9f9")
        self.period_lbl.configure(anchor='w')
        self.period_lbl.configure(background="#d9d9d9")
        self.period_lbl.configure(compound='left')
        self.period_lbl.configure(disabledforeground="#a3a3a3")
        self.period_lbl.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.period_lbl.configure(foreground="#000000")
        self.period_lbl.configure(highlightbackground="#d9d9d9")
        self.period_lbl.configure(highlightcolor="black")
        self.period_lbl.configure(relief="solid")
        self.period_lbl.configure(text='''PERIOD, ms''')

        self.numpack_lbl = tk.Label(self.top)
        self.numpack_lbl.place(relx=0.0, rely=0.646, height=26, width=104)
        self.numpack_lbl.configure(activebackground="#f9f9f9")
        self.numpack_lbl.configure(anchor='w')
        self.numpack_lbl.configure(background="#d9d9d9")
        self.numpack_lbl.configure(compound='left')
        self.numpack_lbl.configure(disabledforeground="#a3a3a3")
        self.numpack_lbl.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.numpack_lbl.configure(foreground="#000000")
        self.numpack_lbl.configure(highlightbackground="#d9d9d9")
        self.numpack_lbl.configure(highlightcolor="black")
        self.numpack_lbl.configure(relief="solid")
        self.numpack_lbl.configure(text='''NUMPACK''')

        self.time_frame_lbl = tk.Label(self.top)
        self.time_frame_lbl.place(relx=0.0, rely=0.748, height=26, width=104)
        self.time_frame_lbl.configure(activebackground="#f9f9f9")
        self.time_frame_lbl.configure(anchor='w')
        self.time_frame_lbl.configure(background="#d9d9d9")
        self.time_frame_lbl.configure(compound='left')
        self.time_frame_lbl.configure(disabledforeground="#a3a3a3")
        self.time_frame_lbl.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.time_frame_lbl.configure(foreground="#000000")
        self.time_frame_lbl.configure(highlightbackground="#d9d9d9")
        self.time_frame_lbl.configure(highlightcolor="black")
        self.time_frame_lbl.configure(relief="solid")
        self.time_frame_lbl.configure(text='''TIME_FRAME, ms''')

        self.stimulation_start_btn = tk.Button(self.top)
        self.stimulation_start_btn.place(relx=0.609, rely=0.567, height=24 
                , width=217) #relx=0.609, rely=0.567
        self.stimulation_start_btn.configure(activebackground="#47fa50")
        self.stimulation_start_btn.configure(activeforeground="black")
        self.stimulation_start_btn.configure(background="#47fa50")
        self.stimulation_start_btn.configure(compound='left')
        self.stimulation_start_btn.configure(disabledforeground="#47fa50")
        self.stimulation_start_btn.configure(cursor="hand2")
        self.stimulation_start_btn.configure(font="-family {Terminal_Hex} -size 9 -weight bold")
        self.stimulation_start_btn.configure(foreground="#000000")
        self.stimulation_start_btn.configure(highlightbackground="#ffffff")
        self.stimulation_start_btn.configure(highlightcolor="black")
        self.stimulation_start_btn.configure(pady="0")
        self.stimulation_start_btn.configure(text='''Начало стимуляции''')
        self.stimulation_start_btn.configure(command = start_stimulation )


        self.connect_device_btn = tk.Button(self.top)
        self.connect_device_btn.place(relx=0.609, rely=0.413, height=24, width=217) #relx=0.609, rely=0.413
        self.connect_device_btn.configure(activebackground="#046fba")
        self.connect_device_btn.configure(activeforeground="black")
        self.connect_device_btn.configure(background="#046fba")
        self.connect_device_btn.configure(cursor="hand2")
        self.connect_device_btn.configure(compound='left')
        self.connect_device_btn.configure(disabledforeground="#046fba")
        self.connect_device_btn.configure(font="-family {Terminal_Hex} -size 9 -weight bold")
        self.connect_device_btn.configure(foreground="#000000")
        self.connect_device_btn.configure(highlightbackground="#ffffff")
        self.connect_device_btn.configure(highlightcolor="black")
        self.connect_device_btn.configure(pady="0")
        self.connect_device_btn.configure(text='''Подключение устройства''')
        self.connect_device_btn.configure(command=connect_device)


        self.num_of_frames_lbl = tk.Label(self.top)
        self.num_of_frames_lbl.place(relx=0.0, rely=0.85, height=26, width=115)
        self.num_of_frames_lbl.configure(activebackground="#f9f9f9")
        self.num_of_frames_lbl.configure(anchor='w')
        self.num_of_frames_lbl.configure(background="#d9d9d9")
        self.num_of_frames_lbl.configure(compound='left')
        self.num_of_frames_lbl.configure(disabledforeground="#a3a3a3")
        self.num_of_frames_lbl.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.num_of_frames_lbl.configure(foreground="#000000")
        self.num_of_frames_lbl.configure(highlightbackground="#d9d9d9")
        self.num_of_frames_lbl.configure(highlightcolor="black")
        self.num_of_frames_lbl.configure(relief="solid")
        self.num_of_frames_lbl.configure(text='''NUM_OF_FRAMES''')

        self.Scrolledtext1 = ScrolledText(self.top)
        self.Scrolledtext1.place(relx=0.586, rely=0.646, relheight=0.279
                , relwidth=0.371)
        self.Scrolledtext1.configure(background="white")
        self.Scrolledtext1.configure(font="TkTextFont")
        self.Scrolledtext1.configure(foreground="black")
        self.Scrolledtext1.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext1.configure(highlightcolor="black")
        self.Scrolledtext1.configure(insertbackground="black")
        self.Scrolledtext1.configure(insertborderwidth="3")
        self.Scrolledtext1.configure(selectbackground="#c4c4c4")
        self.Scrolledtext1.configure(selectforeground="black")
        self.Scrolledtext1.configure(wrap="none")

        self.amp_pos_description = tk.Label(self.top)
        self.amp_pos_description.place(relx=0.338, rely=0.095, height=41
                , width=164)
        self.amp_pos_description.configure(anchor='w')
        self.amp_pos_description.configure(background="#d9d9d9")
        self.amp_pos_description.configure(compound='left')
        self.amp_pos_description.configure(disabledforeground="#a3a3a3")
        self.amp_pos_description.configure(foreground="#000000")
        self.amp_pos_description.configure(text='''Значение амплитуды +''')

        self.amp_neg_description = tk.Label(self.top)
        self.amp_neg_description.place(relx=0.338, rely=0.19, height=31
                , width=164)
        self.amp_neg_description.configure(activebackground="#f9f9f9")
        self.amp_neg_description.configure(anchor='w')
        self.amp_neg_description.configure(background="#d9d9d9")
        self.amp_neg_description.configure(compound='left')
        self.amp_neg_description.configure(cursor="fleur")
        self.amp_neg_description.configure(disabledforeground="#a3a3a3")
        self.amp_neg_description.configure(foreground="#000000")
        self.amp_neg_description.configure(highlightbackground="#d9d9d9")
        self.amp_neg_description.configure(highlightcolor="black")
        self.amp_neg_description.configure(text='''Значение амплитуды -''')

        self.time_pos_description = tk.Label(self.top)
        self.time_pos_description.place(relx=0.338, rely=0.28, height=31
                , width=164)
        self.time_pos_description.configure(activebackground="#f9f9f9")
        self.time_pos_description.configure(anchor='w')
        self.time_pos_description.configure(background="#d9d9d9")
        self.time_pos_description.configure(compound='left')
        self.time_pos_description.configure(disabledforeground="#a3a3a3")
        self.time_pos_description.configure(foreground="#000000")
        self.time_pos_description.configure(highlightbackground="#d9d9d9")
        self.time_pos_description.configure(highlightcolor="black")
        self.time_pos_description.configure(text='''Время удержания +''')

        self.time_neg_description = tk.Label(self.top)
        self.time_neg_description.place(relx=0.338, rely=0.38, height=31
                , width=164)
        self.time_neg_description.configure(activebackground="#f9f9f9")
        self.time_neg_description.configure(anchor='w')
        self.time_neg_description.configure(background="#d9d9d9")
        self.time_neg_description.configure(compound='left')
        self.time_neg_description.configure(disabledforeground="#a3a3a3")
        self.time_neg_description.configure(foreground="#000000")
        self.time_neg_description.configure(highlightbackground="#d9d9d9")
        self.time_neg_description.configure(highlightcolor="black")
        self.time_neg_description.configure(text='''Время удержания -''')

        self.time_pause_description = tk.Label(self.top)
        self.time_pause_description.place(relx=0.338, rely=0.46, height=31
                , width=164)
        self.time_pause_description.configure(activebackground="#f9f9f9")
        self.time_pause_description.configure(anchor='w')
        self.time_pause_description.configure(background="#d9d9d9")
        self.time_pause_description.configure(compound='left')
        self.time_pause_description.configure(disabledforeground="#a3a3a3")
        self.time_pause_description.configure(foreground="#000000")
        self.time_pause_description.configure(highlightbackground="#d9d9d9")
        self.time_pause_description.configure(highlightcolor="black")
        self.time_pause_description.configure(text='''Время паузы''')

        self.period_description = tk.Label(self.top)
        self.period_description.place(relx=0.338, rely=0.56, height=31
                , width=164)
        self.period_description.configure(activebackground="#f9f9f9")
        self.period_description.configure(anchor='w')
        self.period_description.configure(background="#d9d9d9")
        self.period_description.configure(compound='left')
        self.period_description.configure(disabledforeground="#a3a3a3")
        self.period_description.configure(foreground="#000000")
        self.period_description.configure(highlightbackground="#d9d9d9")
        self.period_description.configure(highlightcolor="black")
        self.period_description.configure(text='''Период''')

        self.numpack_description = tk.Label(self.top)
        self.numpack_description.place(relx=0.338, rely=0.64, height=31
                , width=164)
        self.numpack_description.configure(activebackground="#f9f9f9")
        self.numpack_description.configure(anchor='w')
        self.numpack_description.configure(background="#d9d9d9")
        self.numpack_description.configure(compound='left')
        self.numpack_description.configure(disabledforeground="#a3a3a3")
        self.numpack_description.configure(foreground="#000000")
        self.numpack_description.configure(highlightbackground="#d9d9d9")
        self.numpack_description.configure(highlightcolor="black")
        self.numpack_description.configure(text='''Число пакетов''')

        self.time_frame_description = tk.Label(self.top)
        self.time_frame_description.place(relx=0.338, rely=0.74, height=31
                , width=164)
        self.time_frame_description.configure(activebackground="#f9f9f9")
        self.time_frame_description.configure(anchor='w')
        self.time_frame_description.configure(background="#d9d9d9")
        self.time_frame_description.configure(compound='left')
        self.time_frame_description.configure(disabledforeground="#a3a3a3")
        self.time_frame_description.configure(foreground="#000000")
        self.time_frame_description.configure(highlightbackground="#d9d9d9")
        self.time_frame_description.configure(highlightcolor="black")
        self.time_frame_description.configure(text='''Время фрейма''')

        self.pause_start_description = tk.Label(self.top)
        self.pause_start_description.place(relx=0.338, rely=0.84, height=31
                , width=164)
        self.pause_start_description.configure(activebackground="#f9f9f9")
        self.pause_start_description.configure(anchor='w')
        self.pause_start_description.configure(background="#d9d9d9")
        self.pause_start_description.configure(compound='left')
        self.pause_start_description.configure(cursor="fleur")
        self.pause_start_description.configure(disabledforeground="#a3a3a3")
        self.pause_start_description.configure(foreground="#000000")
        self.pause_start_description.configure(highlightbackground="#d9d9d9")
        self.pause_start_description.configure(highlightcolor="black")
        self.pause_start_description.configure(text='''Число фреймов''')

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
# def start_up():
    # py_gui_support.main()


def check_parameters():
    global ser, com_selected, br_selected,amp_pos_ch1,amp_neg_ch1,\
    time_pos_ch1,time_neg_ch1,time_pause_ch1,\
    period_ch1,numpack_ch1,time_frame_ch1 ,connected, parameters_checked
    if(connected):
        try:
            com_selected    = gui.Com_box.get()
            br_selected     = gui.Br_box.get()
            amp_pos_ch1     = gui.amp_pos_entry_ch1.get()
            amp_neg_ch1     = gui.amp_neg_entry_ch1.get()
            time_pos_ch1    = gui.time_pos_entry_ch1.get()
            time_neg_ch1    = gui.time_neg_entry_ch1.get()
            time_pause_ch1  = gui.time_pause_entry_ch1.get()
            period_ch1      = gui.period_entry_ch1.get()
            numpack_ch1     = gui.numpack_entry_ch1.get()
            time_frame_ch1  = gui.time_frame_entry_ch1.get()
            num_of_frames_ch1 = gui.num_of_frames_entry_ch1.get()
        except: gui.Scrolledtext1.insert(END,"WRONG PARAMETERS\n")
        gui.Scrolledtext1.insert(END,com_selected +"; BAUD_RATE: " + br_selected+ "\n")
        print(com_selected, br_selected)
        def conversion(value):
            dec_to_hex = (value/1000+1)*8192
            return math.floor(dec_to_hex)
        def bytes(num):
            a = hex(num >> 8), hex(num & 0xFF)
            return [int(a[0],16),int(a[1],16)]
        try:
            time_neg_bytes       = bytes(int(time_neg_ch1))
            time_pause_bytes     = bytes(int(time_pause_ch1))
            time_pos_bytes       = bytes(int(time_pos_ch1))
            init_time_bytes      = bytes(int(period_ch1)*1000 - int(time_neg_ch1) - int(time_pos_ch1) - int(time_pause_ch1))
            numpack_bytes        = bytes(int(numpack_ch1))
            numofframes_bytes    = bytes(int(num_of_frames_ch1))
            amp_pos_val          = bytes(conversion(int(amp_pos_ch1)))
            amp_neg_val          = bytes(conversion(int(amp_neg_ch1)))
            time_relax = int(time_frame_ch1)-int(numpack_ch1)*int(period_ch1)
            if (time_relax < 1):
                time_relax = 1
            else:
                time_relax = math.floor(int(time_frame_ch1)-int(numpack_ch1)*int(period_ch1))
            # time_relax(ms) = time_fram(ms)-(n*T+init_time_bytes)/1000
            time_relax_bytes = bytes(time_relax)
            init_packet   = [0x3C,0x3D,0x3E]
            time_packet   = [time_neg_bytes[0],time_neg_bytes[1], time_pause_bytes[0], time_pause_bytes[1],\
                             time_pos_bytes[0],time_pos_bytes[1], init_time_bytes[0],init_time_bytes[1]]
            amp_packet    = [amp_pos_val[0],amp_pos_val[1],0x00,0x00,amp_neg_val[0],amp_neg_val[1], 0x00, 0x00]
            num_packet    = [time_relax_bytes[0],time_relax_bytes[1], numpack_bytes[0], numpack_bytes[1], numofframes_bytes[0],numofframes_bytes[1]]
            end_packet    = [0x3C,0x3D,0x3E]
            print("//////////")
            print("инициализация:"+str(init_packet))
            print("время-, время паузы, время+, T-sum(t):"        +str(time_packet))
            print("амплитуда+, ноль-пакет, амплитуда-, ноль-пакет:"    +str(amp_packet))
            print("время релаксации, число пакетов, число фреймов"+str(num_packet))
            print("завершение"+str(end_packet))
            print("//////////")
            serial_data = init_packet+time_packet+amp_packet+num_packet+end_packet
            print("Длина пакета", len(serial_data))
            print("Весь пакет:"+str(serial_data))
            ser.write(serial.to_bytes(serial_data))
            my_char = ser.readline()
            print(binascii.hexlify(my_char))
            gui.Scrolledtext1.insert(END,"RECIEVE FROM DEVICE: " + str(binascii.hexlify(my_char))+"\n")
            parameters_checked = 1
        except: 
            gui.Scrolledtext1.insert(END,"WRONG PARAMETERS\n")
            parameters_checked = 0
    else: gui.Scrolledtext1.insert(END,"PLEASE CONNECT DEVICE FIRST\n")
def start_stimulation():
    global ser, connected, parameters_checked
    if(connected):
        if(parameters_checked):
            com_selected = gui.Com_box.get()
            br_selected  = gui.Br_box.get()
            start_data = [0x22,0x21,0x22,0x01,0x22,0x21,0x22]
            gui.Scrolledtext1.insert(END,"START STIMULATION\n")
            print(com_selected, br_selected)
            ser.write(serial.to_bytes(start_data))
            my_char = ser.readline()
            print(my_char)
        else: gui.Scrolledtext1.insert(END,"CHECK PARAMETERS FIRST\n")
    else: gui.Scrolledtext1.insert(END,"PLEASE CONNECT DEVICE FIRST\n")
def connect_device():
    global ser, connected, com_selected, br_selected
    gui.Scrolledtext1.insert(END,"CONNECT DEVICE...\n")
    if(not connected):
        try:
            com_selected = gui.Com_box.get()
            br_selected  = gui.Br_box.get()
            init_data = [0xac] * 5
            print(com_selected, br_selected)
            if(not connected):
                ser = serial.Serial(port = com_selected, baudrate=br_selected, timeout = 2.5)
                connected = 1
            ser.write(serial.to_bytes(init_data))
            my_char = ser.readline()
            print(binascii.hexlify(my_char))
            gui.Scrolledtext1.delete(1.0,END)
            gui.Scrolledtext1.insert(END,"CONNECTING, WAIT...\n")
            if (my_char != init_data):
                gui.Scrolledtext1.insert(END,"WRONG ANSWER FROM DEVICE (not ECHO)\n")
            else: 
                gui.Scrolledtext1.insert(END,"DEVICE CONNECTED\n")
        except: 
            gui.Scrolledtext1.insert(END,"WRONG DEVICE OR BAUD RATE...\n")
    else: gui.Scrolledtext1.insert(END,"ALREADY CONNECTED...\n")
def load_file ():
    filepath = tk.filedialog.askopenfilename()
    file = open(filepath, "r")
    data = list(csv.reader(file, delimiter=","))
    file.close()
    print(data)
    print("load_file")
    gui.Com_box.delete              (0,END)
    gui.Br_box.delete               (0,END)
    gui.amp_pos_entry_ch1.delete    (0,END)
    # gui.amp_pos_entry_ch2.delete    (0,END)
    gui.amp_neg_entry_ch1.delete    (0,END)
    # gui.amp_neg_entry_ch2.delete    (0,END)
    gui.time_pos_entry_ch1.delete   (0,END)
    # gui.time_pos_entry_ch2.delete   (0,END)
    gui.time_neg_entry_ch1.delete   (0,END)
    # gui.time_neg_entry_ch2.delete   (0,END)
    gui.time_pause_entry_ch1.delete (0,END)
    # gui.time_pause_entry_ch2.delete (0,END)
    gui.period_entry_ch1.delete     (0,END)
    # gui.period_entry_ch2.delete     (0,END)
    gui.numpack_entry_ch1.delete    (0,END)
    # gui.numpack_entry_ch2.delete    (0,END)
    gui.time_frame_entry_ch1.delete (0,END)
    # gui.time_frame_entry_ch2.delete (0,END)
    gui.num_of_frames_entry_ch1.delete(0,END)

    gui.Com_box.insert              (0,data[0][1])
    gui.Br_box.insert               (0,data[1][1])
    gui.amp_pos_entry_ch1.insert    (0,data[2][1])
    # gui.amp_pos_entry_ch2.insert    (0,data[3][1])
    gui.amp_neg_entry_ch1.insert    (0,data[3][1])
    # gui.amp_neg_entry_ch2.insert    (0,data[5][1])
    gui.time_pos_entry_ch1.insert   (0,data[4][1])
    # gui.time_pos_entry_ch2.insert   (0,data[7][1])
    gui.time_neg_entry_ch1.insert   (0,data[5][1])
    # gui.time_neg_entry_ch2.insert   (0,data[9][1])
    gui.time_pause_entry_ch1.insert (0,data[6][1])
    # gui.time_pause_entry_ch2.insert (0,data[11][1])
    gui.period_entry_ch1.insert     (0,data[7][1])
    # gui.period_entry_ch2.insert     (0,data[13][1])
    gui.numpack_entry_ch1.insert    (0,data[8][1])
    # gui.numpack_entry_ch2.insert    (0,data[15][1])
    gui.time_frame_entry_ch1.insert (0,data[9][1])
    # gui.time_frame_entry_ch2.insert (0,data[17][1])
    gui.num_of_frames_entry_ch1.insert(0,data[10][1])
def save_file ():
    parameters_list_str = ''
    com_selected    = gui.Com_box.get()
    br_selected     = gui.Br_box.get()
    amp_pos_ch1     = gui.amp_pos_entry_ch1.get()
    # amp_pos_ch2     = gui.amp_pos_entry_ch2.get()
    amp_neg_ch1     = gui.amp_neg_entry_ch1.get()
    # amp_neg_ch2     = gui.amp_neg_entry_ch2.get()
    time_pos_ch1    = gui.time_pos_entry_ch1.get()
    # time_pos_ch2    = gui.time_pos_entry_ch2.get()
    time_neg_ch1    = gui.time_neg_entry_ch1.get()
    # time_neg_ch2    = gui.time_neg_entry_ch2.get()
    time_pause_ch1  = gui.time_pause_entry_ch1.get()
    # time_pause_ch2  = gui.time_pause_entry_ch2.get()
    period_ch1      = gui.period_entry_ch1.get()
    # period_ch2      = gui.period_entry_ch2.get()
    numpack_ch1     = gui.numpack_entry_ch1.get()
    # numpack_ch2     = gui.numpack_entry_ch2.get()
    time_frame_ch1  = gui.time_frame_entry_ch1.get()
    # time_frame_ch2  = gui.time_frame_entry_ch2.get()
    num_of_frames_ch1 = gui.num_of_frames_entry_ch1.get()

    parameters_list_str = "com_selected,"    + com_selected+"\n"+\
                          "br_selected,"     + br_selected+"\n"+\
                          "amp_pos_ch1,"     + amp_pos_ch1+"\n"+\
                          "amp_neg_ch1,"     + amp_neg_ch1+"\n"+\
                          "time_pos_ch1,"    + time_pos_ch1+"\n"+\
                          "time_neg_ch1,"    + time_neg_ch1+"\n"+\
                          "time_pause_ch1,"  + time_pause_ch1+"\n"+\
                          "period_ch1,"      + period_ch1+"\n"+\
                          "numpack_ch1,"     + numpack_ch1+"\n"+\
                          "time_frame_ch1,"  + time_frame_ch1+"\n"+\
                          "num_of_frames_ch1," + num_of_frames_ch1
    f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".csv")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = parameters_list_str # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.
    print("save_file")

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
def close_port():
  global connected, parameters_checked, ser, com_selected, br_selected
  if connected:
    ser.close()
    gui.Scrolledtext1.insert(END,"PORT IS CLOSED.\n")
    connected = 0
    parameters_checked = 0
  else:
    gui.Scrolledtext1.insert(END,"PORT IS NOT OPENED\n")
if __name__ == '__main__':
    # py_gui_support.main()
    global root, gui , t1, t2
    root = tk.Tk()
    gui = serial_com_top(root)
    t1 = threading.Thread(target = serial_ports)
    t1.daemon = True
    root.mainloop()
    while True:
        time.sleep(1)
        gui.Com_box = ttk.Combobox(gui.connection_frm, values = serial_ports())
