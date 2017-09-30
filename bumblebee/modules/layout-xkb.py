# pylint: disable=C0111,R0903

"""Displays the current keyboard layout using libX11

Requires the following library:
    * libX11.so.6
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

from thirdparty.xkbgroup import *

import logging
log = logging.getLogger(__name__)

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.current_layout)
        )
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=self._next_keymap)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
            cmd=self._prev_keymap)

    def _next_keymap(self, event):
        self._set_keymap(1)

    def _prev_keymap(self, event):
        self._set_keymap(-1)

    def _set_keymap(self, rotation):
        xkb = XKeyboard()
        if xkb.groups_count < 2: return # nothing to doA

        layouts = xkb.groups_symbols[rotation:] + xkb.groups_symbols[:rotation]
        variants = xkb.groups_variants[rotation:] + xkb.groups_variants[:rotation]

        try:
            bumblebee.util.execute("setxkbmap -layout {} -variant {}".format(",".join(layouts), ",".join(variants)))
        except RuntimeError:
            pass

    def current_layout(self, widget):
        try:
            xkb = XKeyboard()
            log.debug("group num: {}".format(xkb.group_num))
            return "{} ({})".format(xkb.group_symbol, xkb.group_variant) if xkb.group_variant else xkb.group_symbol
        except Exception:
            return "n/a"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4