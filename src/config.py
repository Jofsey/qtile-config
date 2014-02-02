from libqtile.config import Key, Screen, Group
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from fn import F

mod = "mod4"
shift = "shift"
ctrl = "control"
space = "space"
ret = "Return"

groups = map(F() >> str >> Group, range(1, 5) + ['u', 'i', 'o', 'p'])

keys = [
    Key(
        [mod], "k",
        lazy.layout.down()  # Switch between windows in current stack pane
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),
    Key(
        [mod, ctrl], "k",
        lazy.layout.shuffle_down()  # Move windows up or down in current stack
    ),
    Key(
        [mod, ctrl], "j",
        lazy.layout.shuffle_up()
    ),
    Key(
        [mod], space,
        lazy.layout.next()  # Switch window focus to other pane(s) of stack
    ),
    Key(
        [mod, shift], space,
        lazy.layout.rotate()  # Swap panes of split stack
    ),

    #Key([mod], "x", lazy.addgroup(Group(str(len(groups))))),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, shift], ret,
        lazy.layout.toggle_split()
    ),

    Key([mod], "Tab", lazy.nextlayout()), # Toggle between different layouts as defined below
    Key([mod], "w", lazy.window.kill()),
    Key([mod, ctrl], "r", lazy.restart()),

    Key([mod], "r", lazy.spawncmd()),

    # Hotkeys
    Key([mod], ret, lazy.spawn("lilyterm")),
    Key([mod], "b", lazy.spawn("chromium")),
]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

dgroups_key_binder = None
dgroups_app_rules = []

layouts = [
    layout.Max(),
    layout.Stack(stacks=2)
]

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.Systray(),
                widget.WindowName(),
                widget.TextBox(str(len(keys)), name="msg"),
                widget.Clock('%I:%M %p'),
            ],
            30,
        ),
    ),
]

main = None
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

mouse = ()
auto_fullscreen = True
widget_defaults = {}


@hook.subscribe.client_new
def java(win):
    try:
        if 'sun-awt-X11-XFramePeer' in win.window.get_wm_class():
            win.java = True
        else:
            win.java = False
    except:
        win.java = False
