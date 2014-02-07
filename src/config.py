import re
import subprocess
from libqtile.config import Key, Screen, Group, Match, Drag, Click
from libqtile.command import lazy, Client
from libqtile import layout, bar, widget, hook
from fn import F
from libqtile.layout.base import Layout
from keytools import gen_keys, gen_mouse

qmain = None


def main(qtile):
    """
    @Type qtile: Qtile
    """
    global qmain
    qmain = qtile


keys = gen_keys()
mouse = gen_mouse()

g1 = [Group("back", [Match(wm_class=["transmission", "transmission-qt"]), Match(title=["tail -f .qtile.log - LilyTerm"])])]
groups = g1 + map(F() >> str >> Group, range(1, 3))

dgroups_key_binder = None
dgroups_app_rules = []

layouts = [
    layout.RatioTile(),
    layout.Stack(stacks=2, name="stack"),
    layout.Max(name="max"),
]

layout_name_widget = widget.TextBox(layouts[0]._name(), name="layout_name")
screen = Screen(bottom=bar.Bar([widget.GroupBox(),
                                widget.Prompt(),
                                widget.WindowName(),
                                widget.Notify(),
                                widget.Systray(),
                                layout_name_widget,
                                widget.Volume(),
                                widget.Clock('%I:%M %p'), ], 30, ), )
screens = [screen]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    auto_float_types=[
        'utility',
        'notification',
        'toolbar',
        'splash',
        'dialog',
    ],
    float_rules=[
        {'wmclass': 'sun-awt-X11-XDialogPeer'}, #vue
        {'wmclass': 'sun-awt-X11-XWindowPeer'}, #vue
    ],
)

auto_fullscreen = True
widget_defaults = {}






@hook.subscribe.startup
def startup():
    def is_running(process):
        s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
        for x in s.stdout:
            if re.search(process, x) and not re.search("defunct", x):
                return True
        return False

    def is_window_exist(name):
        for w in qmain.cmd_windows():
            if w['name'] == name:
                return True
        return False

    def execute_once(process):
        if not is_running(process):
            return subprocess.Popen(process.split())

    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])
    execute_once("transmission-qt")


@hook.subscribe.layout_change
def update_layout_name(lay, group):
    """
        @type lay: Layout
        @type group: _Group
    """
    layout_name_widget.update(lay.name)


@hook.subscribe.client_new
def java(win):
    try:
        if 'sun-awt-X11-XFramePeer' in win.window.get_wm_class():
            win.java = True
        else:
            win.java = False
    except:
        win.java = False

