"""GUI to commit the mannualy measured throughfall data.
Copyright (C) 2012 Thomas Nauss, Tim Appelhans

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
__version__ = "2012-09-20"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

#TODO(tnauss): Comment

import Tkinter

class GUITFBucketData:
    """Instance for selecting plot by id/color for manual data submission.
    """

    def __init__(self, master, intro=None, question=None, outro=None, \
                  plot_id=None, plot_color=None, buckets_number=None, \
                  marked_buckets=None):
        """GUITFPlotSelection.
        The instance is initialized by a Tkinter.Tk() object and some intro,
        question and outro text. In addition, two lists containing id and
        color information are necessary. The color is used as additional plot
        identification (e.g. plot id xyz is also known as the red plot and 
        so on). 
        
        Args:
            master: Tkinter.Tk() object
            intro: Intro text to be displayed (string)
            question: Question text to be displayed (string)
            outro: Outro text to be displayed (string)
            plot_id: ID of the plot
            plot_color: Color code of the plot
        """
        
        self.plot_id_list = plot_id
        self.plot_color_list = plot_color
        self.buckets_number = buckets_number
        self.text_input = None
       
        self.frame = Tkinter.Frame(master)
        self.frame.pack()
        self.intro = Tkinter.Label(self.frame, \
            font=("Helvetica", 12), \
            text=intro).grid(row=0, column=0, columnspan=8)
       
        self.entry_label = []
        self.entry_widget = []
        
        for i in range(0, self.buckets_number):
            base_row = 10 * (i // 10)
            base_column = 2 * (i // 10)
            if str(i+1) in marked_buckets:
                self.entry_label.append(Tkinter.Label(self.frame, \
                                                      text="Canister " + \
                                                      str(i+1).zfill(2) + "*"))
            else:
                self.entry_label.append(Tkinter.Label(self.frame, \
                                                      text="Canister " + \
                                                      str(i+1).zfill(2) + " "))
            self.entry_label[i].grid(row = 1 + i -base_row, column= base_column + 0)
            self.entry_widget.append(Tkinter.Entry(self.frame, width = 10))
            self.entry_widget[i].grid(row = 1 + i -base_row, column = base_column + 1)        
        self.button_submit = Tkinter.Button(self.frame, text="Submit", \
            fg="black", font=("Helvetica", 12), \
            command=self.submit).grid(row=2+i, column=0, columnspan=8)
        self.outro = Tkinter.Label(self.frame, \
            font=("Helvetica", 12), \
            text=outro).grid(row=3+i, column=0, columnspan=8)
            

    def submit(self):
        self.text_input = [-1.0] * self.buckets_number
        for i in range(0, len(self.entry_widget)):
            if self.entry_widget[i].get() != "":
                self.text_input[i] = self.entry_widget[i].get()
        self.frame.quit()

    def get_values(self):
        return self.text_input
