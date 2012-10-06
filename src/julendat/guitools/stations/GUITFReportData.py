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

class GUITFReportData:
    """Instance for selecting plot by id/color for manual data submission.
    """

    def __init__(self, master, intro, question, outro, \
                  plot_id, plot_color):
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
       
        self.frame = Tkinter.Frame(master)
        self.frame.pack()
        self.intro = Tkinter.Label(self.frame, \
            font=("Helvetica", 16), \
            text=intro).grid(row=0, column=0, columnspan=8)
        self.entry_label = Tkinter.Label(self.frame, \
                                         text="Enter here").grid(row=1,column=0)
        self.entry_widget = Tkinter.Entry(self.frame)
        self.entry_widget.grid(row=1,column = 1)
        self.entry_widget.get()
        self.button_submit = Tkinter.Button(self.frame, text="Submit", \
            fg="black", font=("Helvetica", 16), \
            command=self.submit).grid(row=5, column=0, columnspan=8)
       
    def submit(self):
        self.text_input = self.entry_widget.get()
        self.frame.quit()

    def get_values(self):
        return self.text_input

        '''
        
        
        self.question = Tkinter.Label(self.frame, \
            font=("Helvetica", 22, "bold"), \
            text=question).grid(row=1, column=0, columnspan=8)
        self.outro = Tkinter.Label(self.frame, \
            font=("Helvetica", 16), \
            text=outro).grid(row=2, column=0, columnspan=8)
        self.button_color = []
        for i in range(0, len(plot_id_list)):
            self.button_color.append(Tkinter.Button( \
                self.frame, text=plot_id_list[i], bg=plot_color_list[i], \
                fg="LightGrey", font=("Helvetica", 16), \
                command=lambda i=i:self.plot(plot_id_index=i)))
            self.button_color[i].grid(row=4, column=i)
        self.button_cancel = Tkinter.Button(self.frame, text="Cancel", \
            fg="black", font=("Helvetica", 16), \
            command=self.cancel).grid(row=5, column=0, columnspan=8)
        self.finito = Tkinter.Label(self.frame, \
            font=("Helvetica", 16), \
            text="\n").grid(row=4, column=0, columnspan=2)

    def plot(self, plot_id_index):
        """Sets plot id and color depending on user selection.
        
        Args:
            plot_id_index: ID of the plot
        """

        self.plot_id = self.plot_id_list[plot_id_index]
        self.plot_color = self.plot_color_list[plot_id_index]
        self.frame.quit()

    def cancel(self):
        self.plot_id = False
        self.plot_color = False
        self.frame.quit()

    def get_plot_id(self):
        return self.plot_id
    
    def get_plot_color(self):
        return self.plot_color
        '''