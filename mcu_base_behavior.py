import device
import ui
import time
import utils
import mixer
import midi
import transport
import general
import channels

import mcu_constants
import mcu_device
import mcu_track
import mcu_pages
import mcu_knob_mode
import tracknames

class McuBaseClass():
    """ Shared base class for both the extender and the main mackie unit """

    def __init__(self, device: mcu_device.McuDevice):
        pass

    def OnInit(self):
        """ Called when the script has been started """
        pass

    def OnDeInit(self):
        """ Called before the script will be stopped """
        pass

    def OnDirtyMixerTrack(self, SetTrackNum):
        """
        Called on mixer track(s) change, 'SetTrackNum' indicates track index of track that changed or -1 when all tracks changed
        collect info about 'dirty' tracks here but do not handle track(s) refresh, wait for OnRefresh event with HW_Dirty_Mixer_Controls flag
        """
        pass

    def OnUpdateMeters(self):
        """ Called when peak meters have updated values """

    def OnIdle(self):
        """ Called from time to time. Can be used to do some small tasks, mostly UI related """
        pass

    def OnSendTempMsg(Msg, Duration = 1000):
        """ Called when hint message (to be displayed on controller display) is sent to the controller. The duration of message is in ms. """
        pass

    def OnRefresh(self, flags):
        """ Called when something changed that the script might want to respond to. 
            - flags:
            HW_Dirty_Mixer_Sel 	        1 	    mixer selection changed
            HW_Dirty_Mixer_Display 	    2 	    mixer display changed
            HW_Dirty_Mixer_Controls     4 	    mixer controls changed
            HW_Dirty_RemoteLinks 	    16 	    remote links (linked controls) has been added/removed
            HW_Dirty_FocusedWindow 	    32 	    channel selection changed
            HW_Dirty_Performance 	    64 	    performance layout changed
            HW_Dirty_LEDs 	            256     various changes in FL which require update of controller leds
                                                update status leds (play/stop/record/active window/.....) on this flag
            HW_Dirty_RemoteLinkValues 	512 	remote link (linked controls) value is changed
            HW_Dirty_Patterns 	        1024 	pattern changes
            HW_Dirty_Tracks 	        2048 	track changes
            HW_Dirty_ControlValues 	    4096 	plugin cotrol value changes
            HW_Dirty_Colors 	        8192 	plugin colors changes
            HW_Dirty_Names 	            16384 	plugin names changes
            HW_Dirty_ChannelRackGroup 	32768 	Channel rack group changes
            HW_ChannelEvent 	        65536 	channel changes
        """
        pass

    def OnMidiMsg(self):
        """ Called for all MIDI messages. """
        pass

    def OnSysEx(self):
        """ Called for all SysEx messages. """
        pass

    def OnIdle(self):
        """ Called from time to time. Can be used to do some small tasks, mostly UI related. For example: update activity meters. """
        pass

    def OnFirstConnect(self):
        """ Called when device is connected for the first time (ever) """
        pass

    def OnProjectLoad(self, status):
        """ Called when project is loaded """
        pass

    def OnDirtyMixerTrack(self, SetTrackNum):
        """ Called on mixer track(s) change, 'index' indicates track index of track that changed or -1 when all tracks changed
            collect info about 'dirty' tracks here but do not handle track(s) refresh, wait for OnRefresh event with HW_Dirty_Mixer_Controls flag"""
        pass

    def OnUpdateBeatIndicator(self, Value):
        """ Called when the beat indicator has changes - "value" can be off = 0, bar = 1 (on), beat = 2 (on) """
        pass

    def OnUpdateMeters(self):
        """ Called when peak meters needs to be updated """
        pass
