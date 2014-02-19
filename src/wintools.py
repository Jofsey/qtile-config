from libqtile.window import Window


def focus_to_side(q, to_min, horizontal):
    """
        @type q: Qtile
        @type to_min: bool
        @type horizontal: bool
    """
    cur_win = q.currentWindow
    if cur_win is None:
        return

    main_size = lambda win: win.width if horizontal else win.height
    sec_size  = lambda win: win.height if horizontal else win.width
    inverter = lambda val, size: val if to_min else 3000 - (val + size)
    main_val  = lambda win: inverter(win.x if horizontal else win.y, main_size(win))
    sec_val   = lambda win: inverter(win.y if horizontal else win.x, sec_size(win))
    main_center = lambda win: main_val(win) + main_size(win) / 2
    sec_center  = lambda win: sec_val(win) + sec_size(win) / 2


    def is_same_level(w):
        return not sec_val(w) >= sec_val(cur_win) + sec_size(cur_win)\
            and not sec_val(w) + sec_size(w) <= sec_val(cur_win)

    def is_lefter_by_center(w):
        return main_center(w) < main_center(cur_win)

    def ranger(w):
        return abs(main_center(w) - main_center(cur_win)) * 10000 + abs(sec_center(w) - sec_center(cur_win))

    wins = q.currentGroup.windows.copy()
    wins = filter(lambda w: not w.minimized, wins)
    wins = filter(is_same_level, wins)
    wins = filter(is_lefter_by_center, wins)
    if not any(wins):
        return
    target = min(wins, key=ranger)
    assert isinstance(target, Window)
    q.currentGroup.focus(target, False)


def focus_left(q):
    """ @type q: Qtile """
    focus_to_side(q, True, True)


def focus_right(q):
    """ @type q: Qtile """
    focus_to_side(q, False, True)


def focus_up(q):
    """ @type q: Qtile """
    focus_to_side(q, True, False)


def focus_down(q):
    """ @type q: Qtile """
    focus_to_side(q, False, False)
