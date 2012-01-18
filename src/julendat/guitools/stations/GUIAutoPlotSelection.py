"""GUI to verify if the correct plot ID has been selected automatically.
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
"""

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2012-01-08"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

#TODO(tnauss): Comment

import Tkinter

class GUIAutoPlotSelection:

    def __init__(self,master,intro,question,outro):
        
        self.frame = Tkinter.Frame(master)
        self.frame.pack()
        self.intro = Tkinter.Label(self.frame, font=("Helvetica", 16), text=intro).grid(row=0, column=0, columnspan=2)
        self.question = Tkinter.Label(self.frame, font=("Helvetica", 22, "bold"), text=question).grid(row=1, column=0, columnspan=2)
        self.outro = Tkinter.Label(self.frame, font=("Helvetica", 16), text=outro).grid(row=2, column=0, columnspan=2)
        self.button_yes = Tkinter.Button(self.frame, text="Yes", fg="darkgreen", font=("Helvetica", 16), command=self.yes).grid(row=3, column=0)
        self.button_no = Tkinter.Button(self.frame, text="No", fg="red", font=("Helvetica", 16), command=self.no).grid(row=3, column=1)
        self.finito = Tkinter.Label(self.frame, font=("Helvetica", 16), text="\n").grid(row=4, column=0, columnspan=2)

    def yes(self):
        self.correct_plot_id = True
        self.frame.quit()

    def no(self):
        self.correct_plot_id = False
        self.frame.quit()

    def get_correct_plot_id(self):
        return self.correct_plot_id