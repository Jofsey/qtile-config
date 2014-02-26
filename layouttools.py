from libqtile.layout import MonadTall


def grow_main(q):
    """ :type q: Qtile """
    layout = q.currentLayout
    if not isinstance(layout, MonadTall):
        q.log.error('unexpected layout')
        return
    if layout.focused == 0:
        layout.cmd_grow()
    else:
        layout._grow_main(layout.change_ratio)
        q.currentGroup.layoutAll()


def shrink_main(q):
    """ :type q: Qtile """
    layout = q.currentLayout
    if not isinstance(layout, MonadTall):
        q.log.error('unexpected layout')
        return
    if not isinstance(layout, MonadTall): return
    if layout.focused == 0:
        layout.cmd_shrink()
    else:
        layout._shrink_main(layout.change_ratio)
        q.currentGroup.layoutAll()
