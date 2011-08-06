'''
GUI to manually select the plot ID from a list.
Copyright (C) 2011 Thomas Nauss, Tim Appelhans

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Please send any comments, suggestions, criticism, or (for our sake) bug
reports to nausst@googlemail.com

This GUI has been constructed using PAGE (see http://page.sourceforge.net/).

@author: Thomas Nauss, Tim Appelhans
@license: GNU General Public License
'''

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2010-08-04    "
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import sys

py2 = py30 = py31 = False
version = sys.hexversion
if version >= 0x020600F0 and version < 0x03000000 :
    py2 = True    # Python 2.6 or 2.7
    from Tkinter import *
    import ttk
elif version >= 0x03000000 and version < 0x03010000 :
    py30 = True
    from tkinter import *
    import ttk
elif version >= 0x03010000:
    py31 = True
    from tkinter import *
    import tkinter.ttk as ttk
else:
    print ("""
    You do not have a version of python supporting ttk widgets..
    You need a version >= 2.6 to execute PAGE modules.
    """)
    sys.exit()

'''

    If you use the following functions, change the names 'w' and
    'w_win'.  Use as a template for creating a new Top-level window.

    w = None
    def create_New_Toplevel_1 ()
    global w
    global w_win
    if w: # So we have only one instance of window.
        return
    w = Toplevel (root)
    w.title('New Toplevel 1')
    w.geometry('600x350+409+452')
    w_win = New_Toplevel_1 (w)

   Template for routine to destroy a top level window.

def destroy():
    global w
    w.destroy()
    w = None
'''

class GUIManualPlotSelection:
    def __init__(self, master=None,plotID_list=None):
        # Set background of toplevel window to match
        # current style
        self.master = Frame(master)
        self.master.pack()
        style = ttk.Style()
        theme = style.theme_use()
        default = style.lookup(theme, 'background')
        master.configure(background=default)

        self.scr33 = ScrolledListBox (master)
        self.scr33.place(relx=0.02,rely=0.03,relheight=0.96,relwidth=0.45)
        self.scr33.configure(height="3")
        self.scr33.configure(selectbackground="#c4c4c4")
        self.scr33.configure(width="10")
        self.scr33.configure(font=("Helvetica", 16))
        for plotID in plotID_list:
            self.scr33.insert(END, plotID)

        self.tBu35 = Button (master)
        self.tBu35.place(relx=0.5,rely=0.86)
        self.tBu35.configure(takefocus="")
        self.tBu35.configure(font=("Helvetica", 16))
        self.tBu35.configure(fg="darkgreen")
        self.tBu35.configure(text="OK")
        self.tBu35.configure(command=self.button_ok)

        self.tBu36 = Button (master)
        self.tBu36.place(relx=0.8,rely=0.86)
        self.tBu36.configure(takefocus="")
        self.tBu36.configure(font=("Helvetica", 16))
        self.tBu36.configure(fg="red")
        self.tBu36.configure(text="Cancel")
        self.tBu36.configure(command=self.button_canel)

        self.m32 = Menu(master,font=("Helvetica", 16))
        master.configure(menu = self.m32)


        self.mes33 = Message (master)
        self.mes33.place(relx=0.52,rely=0.03,relheight=0.78,relwidth=0.42)
        self.mes33.configure(text="ARE YOU SURE?")
        self.mes33.configure(width="251")

    def button_ok(self):
        self.correct_plotID = self.scr33.get(map(int, self.scr33.curselection())[0])
        self.master.quit()

    def button_canel(self):
        print "This is not good."
        self.master.quit()

    def get_correct_plotID(self):
        return self.correct_plotID
    
# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        self.configure(yscrollcommand=self._autoscroll(vsb),
            xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (took from ScrolledText.py)
        methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

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
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
