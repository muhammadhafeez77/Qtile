from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess
from libqtile import hook

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(['picom', '--config', os.path.expanduser('~/.config/picom/picom.conf')])
    subprocess.Popen(['xset', 's', '120'])  # Timeout in seconds
    subprocess.Popen(['xss-lock', '--', os.path.expanduser('~/.config/qtile/lock.sh')])


mod = "mod4"
keys = []
terminal = guess_terminal()

myTerm = "alacritty" 

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
   Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"],"Return",lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key(["shift"], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "b", lazy.spawn("google-chrome"), desc = "Spawn Firefox"),
    Key([mod], "e", lazy.spawn("thunar"), desc = "Spawn Thunar"),
    Key([mod], "d", lazy.spawn("rofi -show drun -show-icons"), desc='Run Launcher'),

    Key([], "print",lazy.spawn('sh -c "xfce4-screenshooter -w"'),desc="Screenshot"),
    Key([ "shift"],"print",lazy.spawn('sh -c "xfce4-screenshooter "'),desc="Screenshot Region"),
   
    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),    
    Key([], "XF86AudioRaiseVolume", 
        lazy.spawn("bash -c 'vol=$(pactl get-sink-volume @DEFAULT_SINK@ | grep -oP \"\\d+(?=%)\" |head -1); [ $vol -lt 150 ] && pactl set-sink-volume @DEFAULT_SINK@ +5%'")     ),

    # Mic mute (check xkeysyms for exact name)
    Key([], "XF86AudioMicMute", lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle")),
    
    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    Key(["mod1"], "l", lazy.spawn("sh -c '~/.config/qtile/lock.sh'"),desc="Lock screen with horizontal password bar"),
    Key(["mod1", "control"], "l", lazy.spawn("sh -c '~/.config/qtile/lock.sh ; systemctl sleep' "),desc="Lock screen and put computer to sleep"),
]



# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]
#groups = [Group(i) for i in "󰊯󱘶󰧮"]
#groups = [Group(i) for i in "" "" "󰊯" "" "" "" "" "󱘶" "󰧮"] 
for i in groups:
    keys.extend(
        [
           #  mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            # Key(
            #     [mod, "shift"],
            #     i.name,
            #     lazy.window.togroup(i.name, switch_group=True),
            #     desc=f"Switch to & move focused window to group {i.name}",
            # ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name)),
        ]
    )

colors = [
    ["#44362F", "#44362F"],  # bg          (primary.background)
    ["#a9b1d6", "#a9b1d6"],  # fg          (primary.foreground)
    ["#32344a", "#32344a"],  # color[2]    (normal.black)
    ["#f7768e", "#f7768e"],  # color[3]    (normal.red)
    ["#9ece6a", "#9ece6a"],  # color[4]    (normal.green)
    ["#e0af68", "#e0af68"],  # color[5]    (normal.yellow)
    ["#7aa2f7", "#7aa2f7"],  # color[6]    (normal.blue)
    ["#ad8ee6", "#ad8ee6"],  # color[7]    (normal.magenta)
    ["#0db9d7", "#0db9d7"],  # color[8]    (bright.cyan)
    ["#444b6a", "#444b6a"],  # color[9]    (bright.black)
    ["#9683EC", "#9683EC"]   # color[10]   (purplish.periwinkle)
]
   

# helper in case your colors are ["#hex", "#hex"]
def C(x): return x[0] if isinstance(x, (list, tuple)) else x

layout_theme = {
    "border_width" : 3,
    "margin" : 0,
    "border_focus" : colors[10],
    "border_normal" : colors[1],
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
     layout.TreeTab(**layout_theme),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font ",
    fontsize=16,
    padding=0,
    background=colors[0],
)


extension_defaults = widget_defaults.copy()

sep = widget.Sep(linewidth=1, padding=8, foreground=colors[9])

screens = [
    Screen(
        top=bar.Bar(
            widgets = [
                widget.Spacer(length = 8),
                widget.Image(
                    filename = "~/.config/qtile/icons/emblem-kali.png", # Make a folder name 'icons' and put your image in it
                  scale = "False",
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("qtilekeys-yad")},
                ),
                widget.Prompt(
                    font = "Iosevka Nerd Font",
                    fontsize=14,
                    foreground = colors[0]
                ),
                sep,
                widget.GroupBox(
                    fontsize = 18,
                    margin_y = 5,
                    margin_x = 5,
                    padding_y = 0,
                    padding_x = 2,
                    borderwidth = 3,
                    active = colors[8],
                    inactive = colors[9],
                    rounded = False,
                    highlight_color = colors[0],
                    highlight_method = "line",
                    this_current_screen_border = colors[7],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[7],
                    other_screen_border = colors[4],
                ),
                  
                widget.TextBox(
                    text = '|',
                    font = "JetBrainsMono Nerd Font Propo Bold",
                    foreground = colors[9],
                    padding = 2,
                    fontsize = 14
                ),
                widget.CurrentLayout(
                    foreground = colors[1],
                    padding = 5
                ),
                widget.TextBox(
                    text = '|',
                    font = "JetBrainsMono Nerd Font Propo Bold",
                    foreground = colors[9],
                    padding = 2,
                    fontsize = 14
                ),              
                widget.WindowName(
                    foreground = colors[6],
                    padding = 8,
                    max_chars = 40
                ),
                widget.GenPollText(
                    update_interval = 300,
                    func = lambda: subprocess.check_output("printf $(uname -r)", shell=True, text=True),
                    foreground = colors[3],
                    padding = 8, 
                    fmt = '{}',
                ),
                sep,
                widget.CPU(
                    foreground = colors[4],
                    padding = 8, 
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e btop')},
                    format="CPU: {load_percent}%",
                ),
                sep,
                widget.Memory(
                    foreground = colors[8],
                    padding = 8, 
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e btop')},
                    measure_mem = 'G',                       # Turn 'G' to 'M' to see in MiB
                    format = 'Mem: {MemUsed:.2f} {mm}iB',
                ),
                #sep,
                #widget.DF(
                #    update_interval = 60,
                #    foreground = colors[5],
                #    padding = 8, 
                #    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('notify-disk')},
                #    partition = '/',
                #    format = '{uf}{m} free',
                #    fmt = 'Disk: {}',
                #    visible_on_warn = False,
                #),
      
                sep,
               widget.Volume(
                  foreground=colors[7],
                  padding=8,
                  fmt='Vol: {}',   # M is Mute
                  get_volume_command='pactl get-sink-volume @DEFAULT_SINK@',
                  check_mute_command='pactl get-sink-mute @DEFAULT_SINK@',
                  check_mute_string='yes',
                  limit_max_volume=True,
                ),
                sep,
                widget.Battery(
                    foreground=colors[6],           # pick a palette slot you like
                    padding=8,
                    update_interval=5,
                    format='{percent:2.0%} {char}',       # e.g. "73% ⚡"
                    fmt='Battery: {}',
                    charge_char='',               # shown while charging
                    discharge_char='',            # Nerd icon; use '-' if you prefer plain ascii
                    full_char='✔',                 # when at/near 100%
                    unknown_char='?',
                    empty_char='!', 
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e upower -i $(upower -e | grep BAT)'),
                    },
                ), 
                sep,
                widget.Clock(
                    foreground = colors[3],
                    padding = 8, 
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('notify-date')},
                    format = "%a, %b %d - %I:%M %p",
                ),
                widget.Systray(padding = 6),
                widget.Spacer(length = 8),
            ],
            margin=[0, 0, 0, 0], 
            size=30
        ),
        wallpaper= "/home/miya/Pictures/peace.jpg",
        wallpaper_mode="center",
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "LG3D"
