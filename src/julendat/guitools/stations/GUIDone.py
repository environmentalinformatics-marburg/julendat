"""GUI to notice the user of something.
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
__version__ = "2012-10-27"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

#TODO(tnauss): Comment

import Tkinter

class GUIDone:
    """Instance for notifying the user of something.
    """

    def __init__(self, master, header, intro, comment, outro):
        """GUITFPlotSelection.
        The instance is initialized by a Tkinter.Tk() object and some intro,
        comment and outro text. 
        
        Args:
            master: Tkinter.Tk() object
            intro: Intro text to be displayed (string)
            comment: Comment text to be displayed (string)
            outro: Outro text to be displayed (string)
        """
        
        self.frame = Tkinter.Frame(master)
        self.frame.pack()
        self.header = Tkinter.Label(self.frame, \
            font=("Helvetica", 12), \
            text=header).grid(row=0, column=0, columnspan=8)
        self.intro = Tkinter.Label(self.frame, \
            font=("Helvetica", 16), \
            text=intro).grid(row=1, column=0, columnspan=8)
        self.comment = Tkinter.Label(self.frame, \
            font=("Helvetica", 16), \
            text=comment).grid(row=2, column=0, columnspan=8)
        self.outro = Tkinter.Label(self.frame, \
            font=("Helvetica", 16), \
            text=outro).grid(row=3, column=0, columnspan=8)
        self.button_done = Tkinter.Button(self.frame, text="Done", \
                                      fg="black", font=("Helvetica", 12), \
                                      command=self.done)
        self.button_done.grid(row=13, column=0, columnspan=8)

    def done(self):
        self.frame.quit()
