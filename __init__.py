# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# FIXME replace/remove depsgraph handler (last interaction)

import bpy

from .functions import get_properties, get_time_track_file, persist_time_info
from .time_tracker import tt
from . import auto_load
from bpy.app.handlers import persistent

@persistent
def load_handler(dummy):
    # TIME TRACK UPDATER
    if not bpy.app.timers.is_registered(track_timer):
        bpy.app.timers.register(track_timer, first_interval=0.1)
        
    """
    # LAST INTERACT. HANDLER
    if track_last_interaction in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(track_last_interaction)
    print("Adding handler 'track_last_interaction'.")
    
    bpy.app.handlers.depsgraph_update_post.append(track_last_interaction)
    """
"""
import time
def track_last_interaction(scene):
    try:
        tt._last_interaction_time = int(time.time())  # Setze den Zeitstempel auf den aktuellen Zeitpunkt
        print(f"Letzte Interaktion: {tt._last_interaction_time}")
    except Exception as e:
        print(f"Last interaction not documented. Error {e}.")
"""


@persistent
def on_save_file(dummy):
    try:
        if not persist_time_info(get_time_track_file(), tt.get_work_time(get_properties(bpy.context), pretty=False)):
            print(f"Error. Cannot persist data of blend file {bpy.data.filepath}.")
    except Exception as e:
        print(f"Cannot save time tracking data: {e}")



# TIMER
def track_timer():
    try:
        context = bpy.context
        if context.scene:
            # ONLY HERE DO STH.
            props = get_properties(context)
            time = tt.update_time(props)
            #print(f"Track timer is running...{time}")
    except Exception as e:
        print(f"Error in Time Tracker: {e}")

    return 1.0


# AUTO LOAD
auto_load.init()

def register():
    auto_load.register()

    # HANDLERS
    bpy.app.handlers.load_post.append(load_handler)
    bpy.app.handlers.save_pre.append(on_save_file)

    if not bpy.app.timers.is_registered(track_timer):
        bpy.app.timers.register(track_timer, first_interval=0.1)


def unregister():
    # TIMER
    if bpy.app.timers.is_registered(track_timer):
        bpy.app.timers.unregister(track_timer)

    # HANDLERS
    if load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)

    if on_save_file in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(on_save_file)

    """
    if track_last_interaction in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(track_last_interaction)
    """
    
    auto_load.unregister()

