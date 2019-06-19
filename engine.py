#
# Copyright (c) 2013 Shotgun Software, Inc
# ----------------------------------------------------
#
"""
A Katana engine for Tank.
"""
import os
import sys
import ctypes
import shutil
import logging
import traceback

import tank

from Katana import Configuration
from Katana import Callbacks


class KatanaEngine(tank.platform.Engine):
    """
    An engine that supports Katana.
    """

    def __init__(self, *args, **kwargs):
        self._ui_enabled = bool(Configuration.get('KATANA_UI_MODE'))
        super(KatanaEngine, self).__init__(*args, **kwargs)
        

    @property
    def has_ui(self):
        """
        Whether Katana is running as a GUI/interactive session.
        """
        return self._ui_enabled

    def init_engine(self):
        self.log_debug("%s: Initializing..." % self)
        os.environ["TANK_KATANA_ENGINE_INIT_NAME"] = self.instance_name

    

    def add_katana_menu(self, **kwargs):
        self.log_info("Start creating Shotgun menu.")

        menu_name = "Shotgun"
        if self.get_setting("use_sgtk_as_menu_name", False):
            menu_name = "Sgtk"

        tk_katana = self.import_module("tk_katana")
        self._menu_generator = tk_katana.MenuGenerator(self, menu_name)

    def pre_app_init(self):
        """
        Called at startup.
        """
        tk_katana = self.import_module("tk_katana")

        # Make sure callbacks tracking the context switching are active.
        tk_katana.tank_ensure_callbacks_registered()

    def post_app_init(self):
        if self.has_ui:
            try:
                self.add_katana_menu()
            except AttributeError:
                # Katana is probably not fully started and the main menu is not available yet
                Callbacks.addCallback(Callbacks.Type.onStartupComplete, self.add_katana_menu)
            except:
                traceback.print_exc()

    def destroy_engine(self):
        self.log_debug("%s: Destroying..." % self)
        if self.has_ui:
            try:
                self._menu_generator.destroy_menu()
            except:
                traceback.print_exc()

    def launch_command(self, cmd_id):
        callback = self._callback_map.get(cmd_id)
        if callback is None:
            self.log_error("No callback found for id: %s" % cmd_id)
            return
        callback()

    
    def _define_qt_base(self):
        
        try:
            from PySide2 import QtGui
        except:
            # fine, we don't expect PySide2 to be present just yet
            self.logger.debug("PySide2 not detected - trying for PySide now...")
        else:
            # looks like pyside2 is already working! No need to do anything
            self.logger.debug("PySide2 detected - the existing version will be used.")

            return super(KatanaEngine, self)._define_qt_base()
        
        class QTProxy(object):
            def __getattr__(self,name):
                raise tank.TankError("LOOKS")
        
            
        base = {"qt_core" : QTProxy(),"qt_gui": QTProxy(),"dialog_base":None}

        
        try:
            from PyQt4 import QtCore, QtGui
            import PyQt4
            QtCore.Signal = QtCore.pyqtSignal
            QtCore.Slot = QtCore.pyqtSlot
            QtCore.Property = QtCore.pyqtProperty
            QtCore.__version__ = QtCore.QT_VERSION_STR
            base["qt_core"] = QtCore
            base["qt_gui"] = QtGui
            base["dialog_base"] = QtGui.QDialog
            self.log_debug("Successfully initialized PyQt '%s' located in %s."
                            % (QtCore.PYQT_VERSION_STR, PyQt4.__file__))
        except ImportError:
            print "PyQt import error"
        except Exception, e:
            import traceback
            self.log_warning("Error setting up PyQt. PyQt based UI support "
                             "will not be available: %s" % e)
            self.log_debug(traceback.format_exc())    
        print base
        return base



    #####################################################################################
    # Logging

    def log_debug(self, msg):
        if self.get_setting("debug_logging", False):
            print "Shotgun Debug: %s" % msg

    def log_info(self, msg):
        print "Shotgun Info: %s" % msg

    def log_warning(self, msg):
        print "Shotgun Warning: %s" % msg

    def log_error(self, msg):
        print "Shotgun Error: %s" % msg


