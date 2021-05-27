import bpy
import bmesh
import numpy as np
import sys, os 
import re
import time
dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirname)

from src.Utils import *
from src.Camera import *
from src.RaiLoader import *
from src.RaiAnim import *
from src.RenderEngine import *

time_start_script = time.process_time()

########################################################
# CUSTOM SETTINGS
########################################################
Nsegments = 1 #display N segments. -1: display all segments
NkeyframeSteps = 1  # use every n-th keyframe, interpolate inbetween

renderAnimation = True
renderImage = ~renderAnimation
doZoom = False
doZoomOut = False
doRotate = True
doMoveUp = False

tPaddingEnd = 25  # number of frames to append after algorithms converged
tZoomStart = 20
tZoomOutDuration = 25
tRotationStart = 20
tMoveUpStart = 20
cameraLocation = Vector((-2.5, -6.25, +5.32))
cameraFocusPoint = Vector((0,0,0))

print(sys.argv)
_, _, _, _, _, _, folder, collada_filename, anim_filename, video_filename = sys.argv
# folder = "data/animations/all_robots/"
# collada_filename = "z.dae"  # oz: always use this (since the task is the same)
# anim_filename = "133_pcl-1000-100_ex_0_animation_NO_PLAN_converted.txt"  # 116_pcl-noise_2_anim
# video_filename = "test_vid"
print(f"folder: {folder}")
print(f"collada_filename: {collada_filename}")
print(f"anim_filename: {anim_filename}")
print(f"video_filename: {video_filename}")
# filename = os.path.basename(os.path.dirname(folder))
########################################################
# Load collada file and preprocess the objects
########################################################
gripper_name = "finger"
floor_name = "floor"
rai = RaiLoader(folder, anim_filename, collada_filename,
                gripper_name, floor_name)
rai.draw_plan()
rai.generateKeyframesFromAnim(Nsegments, NkeyframeSteps)

setBackgroundColor((.2,.2,.2))

###############################################################################
## LIGHTNING
###############################################################################
lightLocation = 0.3*(cameraLocation-cameraFocusPoint)+Vector((0,0,+5))
# addLightSourceSun(lightLocation)
addLightSourcePoint(lightLocation)

###############################################################################
## CAMERA
###############################################################################
bpy.context.scene.frame_end += tPaddingEnd
tend = bpy.context.scene.frame_end 
camera = Camera(cameraLocation, cameraFocusPoint)

if doZoom:
    camera.zoomIn(tZoomStart, tZoomStart+50)
if doZoomOut:
    camera.zoomOut(tZoomStart+50+50, tZoomStart+50+50+tZoomOutDuration)
if doRotate:
    camera.rotate(tRotationStart, tend, hor_speed=0., ver_speed=-0.001)
if doMoveUp:
    camera.move_camera(tMoveUpStart, tMoveUpStart+20, axis=2, dist=0.2)

## set view to camera
for area in bpy.context.screen.areas:
  if area.type == 'VIEW_3D':
    area.spaces[0].region_3d.view_perspective = 'CAMERA'
    break

###############################################################################
## RENDERING
###############################################################################

render = RenderEngine(folder)

if renderImage:
  render.LastFrameToPNG(os.path.join(folder, video_filename + ".png"))

if renderAnimation:
  render.ToMP4(os.path.join(folder, video_filename + ".mp4"))

elapsed_time = time.process_time() - time_start_script
print("TIME for RENDERING: %f (in s), %f (in m), %f (in h)"%\
    (elapsed_time,elapsed_time/60,elapsed_time/60/60))
