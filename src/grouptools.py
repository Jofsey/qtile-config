from libqtile.config import Group, Match


def gen_groups():
    back = Group("back", [Match(wm_class=["transmission", "transmission-qt"]),
                          Match(title=["tail -f .qtile.log - LilyTerm"])])
    return [back, Group("1")]

def change_group(q, toLeft):
    """
        @type q: Qtile
        @type toLeft: bool
    """
    index = q.groups.index(q.currentGroup)
    q.groups[(index + (-1 if toLeft else 1)) % len(q.groups)].cmd_toscreen()


def to_left_group(q):
    change_group(q, True)


def to_right_group(q):
    change_group(q, False)

def add_group(q):
    """ @type q: Qtile """
    groups = q.groupMap
    for i in xrange(1, len(groups) + 1):
        name = str(i)
        if not groups.has_key(name):
            q.addGroup(name)
            groups[name].cmd_toscreen()
            return


def close_group(q):
    """ @type q: Qtile """
    if len(q.groups) < 2:
        return

    wins = q.currentGroup.windows
    if len(wins) != 0:
        for w in wins:
            w.kill()
    else:
        next_index = max(q.groups.index(q.currentGroup) - 1, 0)
        q.delGroup(q.currentGroup.info()['name'])
        q.groups[next_index].cmd_toscreen()
