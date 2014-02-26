from itertools import chain
from libqtile.command import lazy
from libqtile.config import Key, Drag, Click
from grouptools import to_left_group, to_right_group, add_group, close_group, move_to_left_group, move_to_right_group, \
    move_to_new_group
from wintools import focus_left, focus_right, focus_down, focus_up, unminimize

mod = "mod4"
shift = "shift"
ctrl = "control"
space = "space"
ret = "Return"
alt = "mod1"


class MultiKey:
    up = "up_placeholder"
    down = "down_placeholder"
    left = "left_placeholder"
    right = "right_placeholder"

    replaces = {
        up: ['Up', 'k'],
        down: ['Down', 'j'],
        left: ['Left', 'h'],
        right: ['Right', 'l']
    }

    def __init__(self, modifiers, key, *commands):
        if key not in [MultiKey.up, MultiKey.down, MultiKey.left, MultiKey.right]:
            raise Exception('illegal key param')
        self.modifiers = modifiers
        self.key = key
        self.commands = commands

    def expand(self):
        """
        @rtype: list
        """
        return [Key(self.modifiers, to, *self.commands) for to in self.replaces[self.key]]


def expand_placeholders(keys):
    """
    @type keys: list
    @rtype: list
    """
    return list(chain(*[
        key.expand() if isinstance(key, MultiKey) else [key] for key in keys
    ]))


def gen_keys():
    return expand_placeholders([
        #  Change window focus
        MultiKey([mod], MultiKey.left, lazy.function(focus_left)),
        MultiKey([mod], MultiKey.right, lazy.function(focus_right)),
        MultiKey([mod], MultiKey.down, lazy.function(focus_down)),
        MultiKey([mod], MultiKey.up, lazy.function(focus_up)),
        Key([alt], "Tab", lazy.group.next_window()),
        Key([alt, shift], "Tab", lazy.group.prev_window()),

        #  Move window to group
        MultiKey([mod, ctrl, shift], MultiKey.left, lazy.function(move_to_left_group)),
        MultiKey([mod, ctrl, shift], MultiKey.right, lazy.function(move_to_right_group)),

        #  Change group
        MultiKey([mod, ctrl], MultiKey.left, lazy.function(to_left_group)),
        MultiKey([mod, ctrl], MultiKey.right, lazy.function(to_right_group)),
        MultiKey([alt, ctrl], MultiKey.left, lazy.function(to_left_group)),    #duplicate
        MultiKey([alt, ctrl], MultiKey.right, lazy.function(to_right_group)),  #duplicate

        #  Add/delete group
        Key([mod], space, lazy.function(add_group)),
        Key([mod, shift], space, lazy.function(move_to_new_group)),
        Key([mod, ctrl], 'w', lazy.function(close_group)),
        Key([mod], 'p', lazy.function(close_group)),            #duplicate

        #  Run program
        Key([mod], ret, lazy.spawn("mlterm")),
        Key([mod], "b", lazy.spawn("chromium")),
        Key([mod], "t", lazy.spawn("dolphin")),

        #  Window management
        Key([mod], "e", lazy.window.disable_floating()),
        Key([mod], "w", lazy.window.kill()),
        Key([alt], "F4", lazy.window.kill()),
        Key([mod], "m", lazy.window.toggle_maximize()),
        Key([mod], "f", lazy.window.toggle_maximize()),     #duplicate
        Key([mod], "n", lazy.window.toggle_minimize()),
        Key([mod], "u", lazy.function(unminimize)),

        #  Set layout
        Key([mod], 's', lazy.group.setlayout('stack')),
        Key([mod], 'a', lazy.group.setlayout('max')),
        Key([mod], 'r', lazy.group.setlayout('ratiotile')),

        #  Qtile
        Key([mod, shift], ret, lazy.spawncmd()),
        Key([mod, ctrl], "r", lazy.restart()),
    ])


def gen_mouse():
    return [
        Drag([mod], "Button1", lazy.window.set_position_floating(),
             start=lazy.window.get_position()),
        Drag([mod], "Button3", lazy.window.set_size_floating(),
             start=lazy.window.get_size()),
        Click([mod], "Button2", lazy.window.bring_to_front())
    ]
