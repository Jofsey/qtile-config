from libqtile.command import lazy
from libqtile.config import Key, Drag, Click
from grouptools import to_left_group, to_right_group, add_group, close_group, move_to_left_group, move_to_right_group

mod = "mod4"
shift = "shift"
ctrl = "control"
space = "space"
ret = "Return"
alt = "mod1"
left = "Left"
right = "Right"


def gen_keys():
    return [
        #  Groups
        Key([mod, ctrl], "h", lazy.function(to_left_group)),
        Key([mod, ctrl], left, lazy.function(to_left_group)),

        Key([mod, ctrl], "l", lazy.function(to_right_group)),
        Key([mod, ctrl], right, lazy.function(to_right_group)),

        Key([mod, ctrl, shift], "h", lazy.function(move_to_left_group)),
        Key([mod, ctrl, shift], left, lazy.function(move_to_left_group)),

        Key([mod, ctrl, shift], "l", lazy.function(move_to_right_group)),
        Key([mod, ctrl, shift], right, lazy.function(move_to_right_group)),

        Key([mod], "o", lazy.function(add_group)),
        Key([mod], "p", lazy.function(close_group)),

        #  Program running
        Key([mod], ret, lazy.spawn("lilyterm")),
        Key([mod], "b", lazy.spawn("chromium")),
        Key([mod], "t", lazy.spawn("dolphin")),

        #  Layout
        Key([mod], "k", lazy.layout.down()),
        Key([mod], "j", lazy.layout.up()),
        Key([mod], "e", lazy.window.disable_floating()),
        Key([mod, ctrl], "k",
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
        Key([mod], "n", lazy.layout.client_to_next()),
        Key([alt], "Tab", lazy.group.next_window()),
        Key([alt, shift], "Tab", lazy.group.prev_window()),
        Key([mod], "m", lazy.window.toggle_maximize()),

        Key([mod, shift], "Return", lazy.layout.toggle_split()),

        Key([mod], "Tab", lazy.nextlayout()), # Toggle between different layouts as defined below
        Key([mod], "w", lazy.window.kill()),
        Key([mod, ctrl], "r", lazy.restart()),

        Key([mod], "r", lazy.spawncmd()),
    ]


def gen_mouse():
    return [
        Drag([mod], "Button1", lazy.window.set_position_floating(),
             start=lazy.window.get_position()),
        Drag([mod], "Button3", lazy.window.set_size_floating(),
             start=lazy.window.get_size()),
        Click([mod], "Button2", lazy.window.bring_to_front())
    ]
