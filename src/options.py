# options.py
#
# Copyright 2025 Diego Povliuk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later


import gi
from typing import cast
from gettext import gettext as _

from .utils import ASPECT_RATIOS
from .preferences import settings

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


@Gtk.Template(resource_path="/io/github/diegopvlk/Cine/options.ui")
class OptionsMenuButton(Gtk.MenuButton):
    __gtype_name__ = "OptionsMenuButton"

    flip_box: Gtk.Box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("realize", self._on_realize)
        self.connect("notify::active", self._on_active)
        self.aspect_index: int = 0

    def _on_realize(self, *arg):
        from .window import CineWindow

        self.win = cast(CineWindow, self.get_root())

    def _on_active(self, *arg):
        hwdec_on = settings.get_boolean("hwdec")
        hwdec = str(self.win.mpv.hwdec_current)
        self.flip_box.props.sensitive = not (hwdec_on and "-copy" not in hwdec)

    # --- RESET VIDEO OPTIONS ---
    @Gtk.Template.Callback()
    def _on_reset_all_options(self, _btn):
        self.win.mpv.command_async("set", "video-aspect-override", "-1")
        self.win.mpv.command_async("set", "video-rotate", 0)
        self.win.mpv.command_async("vf", "remove", "@hflip")
        self.win.mpv.command_async("vf", "remove", "@vflip")
        self.win.mpv.command_async("set", "video-zoom", 0)
        self.win.mpv.command_async("set", "contrast", 0)
        self.win.mpv.command_async("set", "brightness", 0)
        self.win.mpv.command_async("set", "gamma", 0)
        self.win.mpv.command_async("set", "saturation", 0)
        self.win.mpv.command_async("set", "sub-delay", 0)
        self.win.mpv.command_async("set", "audio-delay", 0)
        self.win.mpv.command_async("set", "speed", 1.0)

    # --- ASPECT RATIO ---
    @Gtk.Template.Callback()
    def _on_aspect_next(self, _btn):
        self.aspect_index = (self.aspect_index + 1) % len(ASPECT_RATIOS)
        val = ASPECT_RATIOS[self.aspect_index]
        self.win.mpv.command("set", "video-aspect-override", val)
        label = _("Original") if val == "-1" else val
        self.win.mpv.show_text(_("Aspect Ratio") + f": {label}")

    @Gtk.Template.Callback()
    def _on_aspect_prev(self, _btn):
        self.aspect_index = (self.aspect_index - 1) % len(ASPECT_RATIOS)
        val = ASPECT_RATIOS[self.aspect_index]
        self.win.mpv.command("set", "video-aspect-override", val)
        label = _("Original") if val == "-1" else val
        self.win.mpv.show_text(_("Aspect Ratio") + f": {label}")

    @Gtk.Template.Callback()
    def _on_aspect_reset(self, _btn):
        self.aspect_index = 0
        self.win.mpv.command("set", "video-aspect-override", "-1")
        self.win.mpv.show_text(_("Aspect Ratio") + ": " + _("Original"))

    # --- ROTATE ---
    @Gtk.Template.Callback()
    def _on_rotate_right(self, _btn):
        curr = cast(int, self.win.mpv["video-rotate"])
        new_val = (curr + 90) % 360
        self.win.mpv.command("set", "video-rotate", new_val)
        self.win.mpv.show_text(_("Rotate") + f": {new_val}°")

    @Gtk.Template.Callback()
    def _on_rotate_left(self, _btn):
        curr = cast(int, self.win.mpv["video-rotate"])
        new_val = (curr - 90) % 360
        self.win.mpv.command("set", "video-rotate", new_val)
        self.win.mpv.show_text(_("Rotate") + f": {new_val}°")

    @Gtk.Template.Callback()
    def _on_rotate_reset(self, _btn):
        self.win.mpv.command("set", "video-rotate", 0)
        self.win.mpv.show_text(_("Rotate") + f": 0°")

    # --- FLIP ---
    @Gtk.Template.Callback()
    def _on_flip_horiz(self, _btn):
        self.win.mpv.command("vf", "toggle", "@hflip:hflip")
        self.win.mpv.show_text(_("Flip: Horizontal"))

    @Gtk.Template.Callback()
    def _on_flip_vert(self, _btn):
        self.win.mpv.command("vf", "toggle", "@vflip:vflip")
        self.win.mpv.show_text(_("Flip: Vertical"))

    @Gtk.Template.Callback()
    def _on_flip_reset(self, _btn):
        self.win.mpv.command("vf", "remove", "@hflip")
        self.win.mpv.command("vf", "remove", "@vflip")
        self.win.mpv.show_text(_("Flip: Reset"))

    # --- ZOOM ---
    @Gtk.Template.Callback()
    def _on_zoom_inc(self, _btn):
        self.win.mpv.command("add", "video-zoom", 0.1)
        val = self.win.mpv["video-zoom"]
        self.win.mpv.show_text(_("Zoom") + f": {val:.1f}x")

    @Gtk.Template.Callback()
    def _on_zoom_dec(self, _btn):
        self.win.mpv.command("add", "video-zoom", -0.1)
        val = self.win.mpv["video-zoom"]
        self.win.mpv.show_text(_("Zoom") + f": {val:.1f}x")

    @Gtk.Template.Callback()
    def _on_zoom_reset(self, _btn):
        self.win.mpv.command("set", "video-zoom", 0)
        self.win.mpv.show_text(_("Zoom") + ": 0x")

    # --- CONTRAST ---
    @Gtk.Template.Callback()
    def _on_contrast_inc(self, _btn):
        self.win.mpv.command("add", "contrast", 1)
        self.win.mpv.show_text(_("Contrast") + f": {self.win.mpv.contrast}")

    @Gtk.Template.Callback()
    def _on_contrast_dec(self, _btn):
        self.win.mpv.command("add", "contrast", -1)
        self.win.mpv.show_text(_("Contrast") + f": {self.win.mpv.contrast}")

    @Gtk.Template.Callback()
    def _on_contrast_reset(self, _btn):
        self.win.mpv.command("set", "contrast", 0)
        self.win.mpv.show_text(_("Contrast") + ": 0")

    # --- BRIGHTNESS ---
    @Gtk.Template.Callback()
    def _on_brightness_inc(self, _btn):
        self.win.mpv.command("add", "brightness", 1)
        self.win.mpv.show_text(_("Brightness") + f": {self.win.mpv.brightness}")

    @Gtk.Template.Callback()
    def _on_brightness_dec(self, _btn):
        self.win.mpv.command("add", "brightness", -1)
        self.win.mpv.show_text(_("Brightness") + f": {self.win.mpv.brightness}")

    @Gtk.Template.Callback()
    def _on_brightness_reset(self, _btn):
        self.win.mpv.command("set", "brightness", 0)
        self.win.mpv.show_text(_("Brightness") + ": 0")

    # --- GAMMA ---
    @Gtk.Template.Callback()
    def _on_gamma_inc(self, _btn):
        self.win.mpv.command("add", "gamma", 1)
        self.win.mpv.show_text(_("Gamma") + f": {self.win.mpv.gamma}")

    @Gtk.Template.Callback()
    def _on_gamma_dec(self, _btn):
        self.win.mpv.command("add", "gamma", -1)
        self.win.mpv.show_text(_("Gamma") + f": {self.win.mpv.gamma}")

    @Gtk.Template.Callback()
    def _on_gamma_reset(self, _btn):
        self.win.mpv.command("set", "gamma", 0)
        self.win.mpv.show_text(_("Gamma") + ": 0")

    # --- SATURATION ---
    @Gtk.Template.Callback()
    def _on_saturation_inc(self, _btn):
        self.win.mpv.command("add", "saturation", 1)
        self.win.mpv.show_text(_("Saturation") + f": {self.win.mpv.saturation}")

    @Gtk.Template.Callback()
    def _on_saturation_dec(self, _btn):
        self.win.mpv.command("add", "saturation", -1)
        self.win.mpv.show_text(_("Saturation") + f": {self.win.mpv.saturation}")

    @Gtk.Template.Callback()
    def _on_saturation_reset(self, _btn):
        self.win.mpv.command("set", "saturation", 0)
        self.win.mpv.show_text(_("Saturation") + ": 0")

    # --- SUBTITLE DELAY ---
    @Gtk.Template.Callback()
    def _on_sub_delay_up(self, _btn):
        self.win.mpv.command("add", "sub-delay", 0.1)
        val = cast(float, self.win.mpv["sub-delay"])
        self.win.mpv.show_text(_("Subtitle Delay") + f": {round(val * 1000)} ms")

    @Gtk.Template.Callback()
    def _on_sub_delay_down(self, _btn):
        self.win.mpv.command("add", "sub-delay", -0.1)
        val = cast(float, self.win.mpv["sub-delay"])
        self.win.mpv.show_text(_("Subtitle Delay") + f": {round(val * 1000)} ms")

    @Gtk.Template.Callback()
    def _on_sub_delay_reset(self, _btn):
        self.win.mpv.command("set", "sub-delay", 0)
        self.win.mpv.show_text(_("Subtitle Delay") + ": 0ms")

    # --- AUDIO DELAY ---
    @Gtk.Template.Callback()
    def _on_audio_delay_up(self, _btn):
        self.win.mpv.command("add", "audio-delay", 0.1)
        val = cast(float, self.win.mpv["audio-delay"])
        self.win.mpv.show_text(_("Audio Delay") + f": {round(val * 1000)} ms")

    @Gtk.Template.Callback()
    def _on_audio_delay_down(self, _btn):
        self.win.mpv.command("add", "audio-delay", -0.1)
        val = cast(float, self.win.mpv["audio-delay"])
        self.win.mpv.show_text(_("Audio Delay") + f": {round(val * 1000)} ms")

    @Gtk.Template.Callback()
    def _on_audio_delay_reset(self, _btn):
        self.win.mpv.command("set", "audio-delay", 0)
        self.win.mpv.show_text(_("Audio Delay") + f": 0ms")

    # --- PLAYBACK SPEED ---
    @Gtk.Template.Callback()
    def _on_speed_inc(self, _btn):
        self.win.mpv.command("add", "speed", 0.1)
        self.win.mpv.show_text(_("Speed") + f": {self.win.mpv.speed:.1f}x")

    @Gtk.Template.Callback()
    def _on_speed_dec(self, _btn):
        self.win.mpv.command("add", "speed", -0.1)
        self.win.mpv.show_text(_("Speed") + f": {self.win.mpv.speed:.1f}x")

    @Gtk.Template.Callback()
    def _on_speed_reset(self, _btn):
        self.win.mpv.command("set", "speed", 1.0)
        self.win.mpv.show_text(_("Speed") + f": 1.0x")
