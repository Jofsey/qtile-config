from libqtile.layout import Max, Stack
from libqtile.layout.base import Delegate, Layout
from libqtile.layout.slice import Single


class MySlice(Delegate):
    """Slice layout

    This layout cuts piece of screen and places a single window on that piece,
    and delegates other window placement to other layout
    """

    defaults = [
        ("width", 256, "Slice width"),
        ("side", "left", "Side of the slice (left, right, top, bottom)"),
        ("name", "max", "Name of this layout."),
    ]

    def __init__(self, side, width,
                 wname=None, wmclass=None, role=None,
                 fallback=Stack(stacks=1), **config):
        if wname is None and wmclass is None and role is None:
            wname = 'slice'
        self.match = {
            'wname': wname,
            'wmclass': wmclass,
            'role': role,
        }
        Delegate.__init__(self, width=width, side=side, **config)
        self.add_defaults(MySlice.defaults)
        self._slice = Max()
        self._fallback = fallback

    def clone(self, group):
        res = Layout.clone(self, group)
        res._slice = self._slice.clone(group)
        res._fallback = self._fallback.clone(group)
        res._window = None
        return res

    def layout(self, windows, screen):
        if self._slice not in self.layouts.values():
            self.delegate_layout(windows, {self._fallback: screen})
        else:
            if self.side == 'left':
                win, sub = screen.hsplit(self.width)
            elif self.side == 'right':
                sub, win = screen.hsplit(screen.width - self.width)
            elif self.side == 'top':
                win, sub = screen.vsplit(self.width)
            elif self.side == 'bottom':
                sub, win = screen.vsplit(screen.height - self.width)
            else:
                raise NotImplementedError(self.side)
            self.delegate_layout(
                windows,
                {
                    self._slice: win,
                    self._fallback: sub,
                }
            )

    def configure(self, win, screen):
        raise NotImplementedError("Should not be called")

    def _get_layouts(self):
        return (self._slice, self._fallback)

    def _get_active_layout(self):
        return self._fallback  # always

    def add(self, win):
        if win.match(**self.match):
            self._slice.add(win)
            self.layouts[win] = self._slice
        else:
            self._fallback.add(win)
            self.layouts[win] = self._fallback
