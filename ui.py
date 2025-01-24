import bpy
import os
import time
import datetime

from .time_tracker import tt
from .functions import get_data_dir, get_properties

class UI_TimeTracker(bpy.types.Panel):
    """Creates a Panel in the scene context of sidebar"""
    bl_label = "Time Tracker"
    bl_idname = "SCENE_PT_timetracker_panel"
    bl_space_type = 'VIEW_3D'  # Correct space type for the 3D View
    bl_region_type = 'UI'  # 'UI' is the region type for the Sidebar
    bl_context = "objectmode"  # You can change this depending on the context where you want the panel to appear
    bl_category = "Time Tracker"

    def draw(self, context):
        props = get_properties(context)
        layout = self.layout

        scene = context.scene

        box = layout.box()
        row = box.row()
        row.label(text="Time:")
        row.label(text=tt.get_work_time(props))
        box.prop(props, "interaction_threshhold", text='Inactivity Threshhold (s)')
        
        last_stop = tt.get_last_stop()
        if last_stop:
            box_ls = box.box()
            box_ls.label(text="Last Stop:")
            row_ls = box_ls.row()
            row_ls.label(text="From:")
            row_ls.label(text=str(last_stop["start"]))
            
            row_ls = box_ls.row()
            row_ls.label(text="To:")
            row_ls.label(text=str(last_stop["stop"]))

        #tt.update_time(props) # has to run but only updates diff when active
        if props.tracking:
            box.operator("time_tracker.pause", icon='PAUSE')
        else:
            box.operator("time_tracker.continue", icon='PLAY')

        box = layout.box()
        box.operator("time_tracker.show_time_table", text="Show Time Table")
        # TODO button to open time track file
            
def track_timer_redraw():
    context = bpy.context
    if context.area:
        context.area.tag_redraw()
        print("redraw")
    else:
        
        print("no redraw")
    return 1


#bpy.app.timers.register(track_timer_redraw, first_interval=3.0)