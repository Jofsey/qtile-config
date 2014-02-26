import re
import subprocess
import socket
from libqtile.config import Screen
from libqtile import layout, bar, widget, hook
from libqtile.layout.base import Layout
from keytools import gen_keys, gen_mouse
from grouptools import gen_groups
from mykeyboardlayout import MyKeyboardLayout

qmain = None


def main(qtile):
    """
    @Type qtile: Qtile
    """
    global qmain
    qmain = qtile


keys = gen_keys()
mouse = gen_mouse()
groups = gen_groups()

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True

border = dict(
    border_normal='#808080',
    border_width=2,
    border_focus='#FF0000',
)

layouts = [
    layout.MonadTall(**border),
    # layout.RatioTile(),
    # layout.Stack(stacks=2, **border),
    # layout.Max(**border),
    #MySlice('right', 300, wmclass="skype", fallback=layout.Stack(stacks=1)),
]

layout_name_widget = widget.TextBox(layouts[0].name, name="layout_name")

screen = Screen(bottom=bar.Bar([widget.GroupBox(),
                                widget.Prompt(),
                                widget.WindowName(),
                                widget.Notify(),
                                widget.Systray(),
                                layout_name_widget,
                                MyKeyboardLayout(['us', 'ru']),
                                widget.Volume(),
                                widget.Clock('%I:%M %p')], 30, ))
screens = [screen]


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

    if socket.gethostname() == 'i5':
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

