import bpy

from .functions import get_properties

# BLENDER PROPERTIES

TIME_TRACK_FILE = 'time_tracks.json'


def toggle_stop_and_go(self, context):
    try:
        props = get_properties(context)
        if props.stopp_and_go:
            bpy.ops.wm.modal_event_logger()
        # else: logger will shutdown itself
    except Exception as e:
        print(e)

class TimeTrackerProperties(bpy.types.PropertyGroup):

    time: bpy.props.IntProperty(
        name="time",
        description="Time spent working on this file",
        default=0
    ) # type: ignore

    session_time: bpy.props.IntProperty(
        name="session time",
        description="Time spent on this file in one session",
        default=0
    ) # type: ignore

    tracking: bpy.props.BoolProperty(
        name="is_tracking",
        description="Returns if time tracking is running",
        default=True
    ) # type: ignore
    
    stopp_and_go: bpy.props.BoolProperty(
        name="stopp and go",
        description="Detects inactivity based on threshhold and stopps/starts tracking",
        default=True,
        update=toggle_stop_and_go
    ) # type: ignore

    interaction_threshhold: bpy.props.IntProperty(
        name="interaction_threshhold",
        description="Thresshold of inactivity (when to stop timing) in seconds",
        default=120
    ) # type: ignore

    # TODO UI sessions group per day

    session_sort: bpy.props.EnumProperty(
        name="Sort",
        description="sort sessions",
        items=[
            ('0', "Latest first", ""), 
            ('1', "Oldest first", "")
            ],
        default='0'
    ) # type: ignore

    session_filter: bpy.props.StringProperty(
        name="Filter",
        description="Filter sessions (id, date)",
        default=""
    ) # type: ignore


# Registration-Funktionen, falls nicht automatisch registriert:
def register():
    bpy.types.Scene.time_tracker_props = bpy.props.PointerProperty(type=TimeTrackerProperties)

def unregister():
    del bpy.types.Scene.time_tracker_props

