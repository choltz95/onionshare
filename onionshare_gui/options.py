# -*- coding: utf-8 -*-
"""
OnionShare | https://onionshare.org/

Copyright (C) 2016 Micah Lee <micah@micahflee.com>

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
"""
from PyQt5 import QtCore, QtWidgets

from onionshare import strings, helpers

class Options(QtWidgets.QHBoxLayout):
    """
    The extra onionshare options in the GUI.
    """
    def __init__(self, web, app):
        super(Options, self).__init__()

        self.web = web
        self.app = app
        self.hours = 0

        # close automatically
        self.close_automatically = QtWidgets.QCheckBox()
        self.timer_field = QtWidgets.QLineEdit()
        self.timer_field.setPlaceholderText("leave blank for no limit (hours)")
        self.timer_field.setMaxLength(5)

        if self.web.stay_open:
            self.close_automatically.setCheckState(QtCore.Qt.Unchecked)
            self.timer_field.setReadOnly(True)
        else:
            self.close_automatically.setCheckState(QtCore.Qt.Checked)
            self.timer_field.setReadOnly(False)
        self.close_automatically.setText(strings._("close_on_finish", True))
        self.close_automatically.stateChanged.connect(self.stay_open_changed)
        self.timer_field.textChanged.connect(self.on_text_changed)
        
        # add the widgets
        self.addWidget(self.close_automatically)
        self.addWidget(self.timer_field)
    def stay_open_changed(self, state):
        """
        When the 'close automatically' checkbox is toggled, let the web app know.
        """
        if state > 0:
            self.timer_field.setReadOnly(False)
            self.web.set_stay_open(False)
            self.app.stay_open = False
        else:
            self.timer_field.setReadOnly(True)
            self.web.set_stay_open(True)
            self.app.stay_open = True

    def on_text_changed(self,state):
        h = self.timer_field.text()
        try:
            self.hours = int(h)
            self.web.set_stay_open(True)
            self.app.stay_open = True
        except Exception:
            # warn input here
            # print('Input restricted to integer values')
            pass
