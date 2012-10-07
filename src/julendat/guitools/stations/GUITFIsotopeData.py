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

class GUITFIsotopeData:
    """Instance for selecting plot by id/color for manual data submission.
    """

    def __init__(self, master, header, intro, bucket_id, bucket_amount, outro, \
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
            font=("Helvetica", 12), \
            text=header).grid(row=0, column=0, columnspan=8)
        self.question = Tkinter.Label(self.frame, \
            font=("Helvetica", 16), \
            text=intro).grid(row=1, column=0, columnspan=8)
       
        self.id = []
        self.amount = []
        self.checkbutton = []
        self.check = []
        for i in range(0, len(bucket_id)/2):
            self.id.append(Tkinter.Label(self.frame, \
                                         font=("Helvetica", 14), \
                                         text="Bucket " + str(bucket_id[i]) + ": "))
            self.id[i].grid(row=2+i,column=0)
            self.amount.append(Tkinter.Label(self.frame, \
                                         font=("Helvetica", 14), \
                                         text=str(bucket_amount[i])))
            self.amount[i].grid(row=2+i,column=1)
            self.check.append(i)
            self.check[i] = Tkinter.Variable(0)
            self.checkbutton.append(Tkinter.Checkbutton(self.frame, \
                                            variable=self.check[i], \
                                            command=self.enable_done, \
                                            offvalue=False))
            self.checkbutton[i].deselect()
            self.checkbutton[i].grid(row=2+i,column=2)
        for i in range(len(bucket_id)/2, len(bucket_id)):
            self.id.append(Tkinter.Label(self.frame, \
                                         font=("Helvetica", 14), \
                                         text="Bucket " + str(bucket_id[i]) + ": "))
            self.id[i].grid(row=2+i-len(bucket_id)/2,column=4)
            self.amount.append(Tkinter.Label(self.frame, \
                                         font=("Helvetica", 14), \
                                         text=str(bucket_amount[i])))
            self.amount[i].grid(row=2+i-len(bucket_id)/2,column=5)
            self.check.append(i)
            self.check[i] = Tkinter.Variable(0)
            self.checkbutton.append(Tkinter.Checkbutton(self.frame, \
                                            variable=self.check[i], \
                                            command=self.enable_done, \
                                            offvalue=False))
            self.checkbutton[i].deselect()
            self.checkbutton[i].grid(row=2+i-len(bucket_id)/2,column=6)
            self.button_done = Tkinter.Button(self.frame, text="Done", \
                                          fg="grey", font=("Helvetica", 12), \
                                          command=None)
            self.button_done.grid(row=13, column=0, columnspan=8)

            
    def enable_done(self):
        enable = True
        for i in range(0, len(self.check)):
            if self.check[i].get() == False:
                enable = False
        if enable == True:
            self.button_done = Tkinter.Button(self.frame, text="Done", \
                                          fg="black", font=("Helvetica", 12), \
                                          command=self.done)
            self.button_done.grid(row=13, column=0, columnspan=8)
        


    def done(self):
        self.frame.quit()
