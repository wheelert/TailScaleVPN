import threading
import time
import gi
import subprocess
import dbus
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio
from gi.repository import GLib
gi.require_version('Handy', '1')
from gi.repository import Handy
import tailscaleDB
import os
import requests

class TailScaleVPN(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="TailScaleVPN")

        Handy.init()
        _cwd = os.getcwd()
        # load CSS
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_path(_cwd+"/TailScaleVPN.css")
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        hb = Handy.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "TailScale-VPN"
        self.set_titlebar(hb)
        self.set_border_width(0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        ip = self.get_ip()
        self.label = Gtk.Label(ip)
        vbox.add(self.label)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.connect("row-activated", self.on_row_click);
        box_outer.pack_start(self.listbox, True, True, 0)

        self.pop_nodes()

        vbox.add(box_outer)

        # disconnect button
        button3 = Gtk.Button(label="Disconnect")
        button3.connect("clicked", self.disconnectAll)
        vbox.add(button3)

        # exit button
        self.button2 = Gtk.Button(label="Exit")
        self.button2.connect("clicked", self.AppClose)
        vbox.add(self.button2)

        self.add(vbox)

    def pop_nodes(self):
        for _node in self.getNodes():
            # row
            row = Gtk.ListBoxRow()

            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)

            row.add(hbox)
            vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            hbox.pack_start(vbox2, True, True, 0)

            label1 = Gtk.Label(label=_node["Title"], xalign=0)
            label1.set_name("title")
            label2 = Gtk.Label(label=_node["Body"][0:100], xalign=0)
            if _node["Body"] == "active":
                label2.set_name("status-active")
            else:
                label2.set_name("status")

            vbox2.pack_start(label1, True, True, 0)
            vbox2.pack_start(label2, True, True, 0)

            row.set_name("list_row")

            self.listbox.add(row)
            # end row

    def get_ip(self):
        _url = "http://ifconfig.me"
        response = requests.get(_url)
        ip = "IP: "+response.text
        return ip

    def on_row_click(self, listbox, listboxrow):
        _node = tailscaleDB.getNode(listboxrow.get_index())

        watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
        win.get_window().set_cursor(watch_cursor)

        tailscaleDB.set_exit_node(_node["IP"])
        self.repopListbox()
        self.label.set_text(self.get_ip())
        win.get_window().set_cursor(None)
        return GLib.SOURCE_CONTINUE

    def repopListbox(self):
        tailscaleDB.clear_listnodes()
        for _row in self.listbox.get_children():
            self.listbox.remove(_row)
        time.sleep(5)
        self.pop_nodes()
        self.listbox.show_all()


    def disconnectAll(self, widget):
        tailscaleDB.disconnect_all()
        self.repopListbox()
        self.label.set_text(self.get_ip())
        return GLib.SOURCE_CONTINUE

    def AppClose(self, widget):
        exit()

    def getNodes(self):
        _notes = tailscaleDB.localdb_con()
        return _notes



win = TailScaleVPN()
win.connect("destroy", Gtk.main_quit)
win.set_icon_from_file("/usr/share/TailScaleVPN/TailScaleVPN.png")
win.show_all()
Gtk.main()
