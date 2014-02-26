from libqtile.command import lazy
from libqtile.config import Group, Match, Screen, Key
from libqtile.window import Window


def gen_groups():
    back = Group("back", [Match(title=["Transmission"])])
    persist = [Group(str(i), init=False, persist=True) for i in range(1, 11)]
    return [back] + persist


def get_side_group(q, toLeft):
    """
        @type q: Qtile
        @type toLeft: bool
        @rtype : _Group
    """
    index = q.groups.index(q.currentGroup)
    return q.groups[(index + (-1 if toLeft else 1)) % len(q.groups)]


def to_left_group(q):
    """ @type q: Qtile """
    get_side_group(q, True).cmd_toscreen()


def to_right_group(q):
    """ @type q: Qtile """
    get_side_group(q, False).cmd_toscreen()

def to_prev_group(q):
    """ @type q: Qtile """
    if q.currentGroup.prev_name in q.groupMap:
        q.groupMap[q.currentGroup.prev_name].cmd_toscreen()


def add_group(q):
    """ @type q: Qtile """
    groups = q.groupMap
    cur_group_name = q.currentGroup.name
    for i in xrange(1, len(groups) + 1):
        name = str(i)
        if not groups.has_key(name):
            q.addGroup(name)
            groups[name].cmd_toscreen()
            groups[name].prev_name = cur_group_name
            return


def move_to_new_group(q):
    """ @type q: Qtile """
    win = q.currentWindow
    add_group(q)
    if win:
        win.togroup(q.currentGroup.name)


def stop_move(q):
    """ @type q: Qtile """
    window = q.currentWindow
    assert isinstance(window, Window)
    if window.in_move:
        window.disablefloating()
        del window.in_move
    q.unmapKey(stop_move_key)


stop_move_key = Key([], "space", lazy.function(stop_move))


def move_to_side_group(q, toLeft):
    """
        @rtype : None
        @type q: Qtile
        @type toLeft: bool
    """
    win = q.currentWindow
    if win is None:
        return
    screen = q.currentScreen
    assert isinstance(win, Window)
    assert isinstance(screen, Screen)
    # Add stop move functionality
    win.in_move = True
    q.mapKey(stop_move_key)

    if not win.floating:
        win.tweak_float(x=screen.width / 4, y=screen.height / 4, w=screen.width / 2, h=screen.height / 2)
    group = get_side_group(q, toLeft)
    win.togroup(group.name)
    group.cmd_toscreen()


def move_to_left_group(q):
    """ @type q: Qtile """
    move_to_side_group(q, True)


def move_to_right_group(q):
    """ @type q: Qtile """
    move_to_side_group(q, False)


def close_group(q):
    """ @type q: Qtile """
    if len(q.groups) <= 1:
        return

    wins = q.currentGroup.windows
    if len(wins) != 0:
        for w in wins:
            w.kill()
    else:
        if q.currentGroup.prev_name in q.groupMap:
            next_index = q.groups.index(q.groupMap[q.currentGroup.prev_name])
        else:
            next_index = max(q.groups.index(q.currentGroup) - 1, 0)
        q.delGroup(q.currentGroup.info()['name'])
        q.groups[next_index].cmd_toscreen()
