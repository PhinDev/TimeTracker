import time
import bpy
from datetime import datetime

from .functions import TimingModel, get_properties, get_time_pretty, get_time_track_file, persist_time_info, read_json

# TODO groups for blend files (time table etc.)
# TODO tracking hours per day with dates etc.
 
class TIME_TRACKER_OT_pause(bpy.types.Operator):
    bl_idname = "time_tracker.pause"
    bl_label = "Pause"
    bl_description = "Pause Time Tracking"

    def execute(self, context):
        props = get_properties(context)

        props.tracking = False

        self.report({'INFO'}, f"Time Tracking paused")
        return {'FINISHED'}
    

class TIME_TRACKER_OT_continue(bpy.types.Operator):
    bl_idname = "time_tracker.continue"
    bl_label = "Continue"
    bl_description = "Continue Time Tracking"

    def execute(self, context):
        props = get_properties(context)

        props.tracking = True
        
        self.report({'INFO'}, f"Time Tracking continued")
        return {'FINISHED'}
    

class TIME_TRACKER_OT_time_table(bpy.types.Operator):
    bl_idname = "time_tracker.show_time_table"
    bl_label = "Time Table"
    bl_description = "Time table data of all tracked projects"

    _width = 600

    def execute(self, context):
        return {'FINISHED'}
    
    # Dialog-Inhalt
    def draw(self, context):
        layout = self.layout

        # save current time before reading
        tt.save()

        data = read_json(get_time_track_file())

        for file, attributes in data.items():
            box = layout.box()
            box.label(text=file)
            box.label(text=f"{get_time_pretty(attributes['seconds'])}")
            

    def invoke(self, context, event):
        # Öffnet eine Popup-Form

        # Holen der aktuellen Bildschirmgröße
        screen_width = context.window.width
        screen_height = context.window.height

        # Fenstergröße des Dialogs
        dialog_width = self._width
        dialog_height = 0

        # Berechnen der zentrierten Position
        center_x = (screen_width - dialog_width) // 2
        center_y = (screen_height - dialog_height) // 2

        # Position des Dialogs setzen
        context.window.cursor_warp(center_x, center_y)
        return context.window_manager.invoke_props_dialog(self, width=600)
    

   
# TODO if file changes might interfere w/ last inter time - reset on load_file?
class TimeTracker():
    _timing_obj: TimingModel = None
    _last_timing = 0
    _last_interaction_time = 0
    _is_active = True
    
    _last_tracking_stop = {
        "start": None,
        "stop": None
    }

    def __init__(self):
        self._last_timing = time.time()
        #TODO get props.time from file and (if existing and greater) ask user to overwrite/use existing time track from file


    def load_session(self):
        self._timing_obj = TimingModel.load_single_from_json(file_path=get_time_track_file(), blend_file=bpy.data.filepath)
        if not self._timing_obj:
            self._timing_obj = TimingModel(blend_file=bpy.data.filepath, seconds=0, sessions=[])
            
        self._timing_obj.add_session(0)
        print("Session loaded")


    def get_work_time(self, props, pretty: bool = True) -> str:
        if not pretty:
            return props.time
        return get_time_pretty(seconds=props.time)


    def get_session_time(self, props, pretty: bool = True) -> str:
        if not pretty:
            return props.session_time
        return get_time_pretty(seconds=props.session_time)

    """
    updates overall time and session through blend properties & Timing Data Interface "TimingModel"
    """
    def update_time(self, props):
        now = int(time.time()) # only seconds needed 
        if now == self._last_timing:
            return 0 # prevent 'washing' the last timestamp
        
        diff = int(now - self._last_timing)
        self._last_timing = now

        """
        # set tracking stop
        if self._last_interaction_time > 0 and (now - self._last_interaction_time) > props.interaction_threshhold:
            if self._is_active:
                props.time = props.time - props.interaction_threshhold
                local_time = datetime.datetime.now() - datetime.timedelta(seconds=props.interaction_threshhold)
                self._last_tracking_stop["start"] = local_time.strftime('%H:%M:%S')
                #print(f"Not tracking due to inactivity. Stopped at {str(local_time.strftime("%H:%M:%S"))}")
                print(f"Not tracking due to inactivity. Stopped tracking at {local_time.strftime('%H:%M:%S')} - time record: {tt.get_work_time(props)}")
            self._is_active = False
            return 0

        if not self._is_active: # set last stop
            local_time = datetime.datetime.now()
            self._last_tracking_stop["stop"] = local_time.strftime('%H:%M:%S')
            self._is_active = True
        """

        if props.tracking:
            # Blender Properties
            props.time = props.time + diff
            props.session_time = props.session_time + diff
            # I/O
            try:
                if not self._timing_obj:
                    self.load_session()

                self._timing_obj.update_session(props.time, props.session_time)

            except Exception as e:
                print(e)
        
        return props.time
    

    def get_all_sessions(self):
        return self._timing_obj.sessions if self._timing_obj else None


    def get_last_stop(self):
        stp = self._last_tracking_stop
        if stp["start"] is None or stp["stop"] is None or stp["start"] >= stp["stop"]:
            return None
        return self._last_tracking_stop


    def save(self):
        return persist_time_info(get_time_track_file(), self._timing_obj)

tt = TimeTracker()



# Registrierung des Handlers
def register():
    pass

def unregister():
    pass