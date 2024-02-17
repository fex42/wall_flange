from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

pipe_dia = 99.0
wt = 2.5 # wall thickness
pipe_height = 67.0
flange_dia = 128.0
holes_dia = 119.0
hole_dia = 4.6

with BuildPart() as wall_flange:
    with BuildSketch():
        Circle(pipe_dia/2)
        Circle(pipe_dia/2 - wt, mode=Mode.SUBTRACT)
    extrude(amount=pipe_height)
    with BuildSketch():
        Circle(flange_dia/2)
        Circle(pipe_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=wt)

    # fillet on outer flange/pipe edge
    edge = wall_flange.edges().filter_by_position(axis=Axis.Z, minimum=wt-1, maximum=wt+1)[0]
    fillet(objects=edge, radius=1.0)

    # screw holes
    with BuildSketch():
        with PolarLocations(holes_dia/2, 4):
            Circle(hole_dia/2)
    extrude(amount=2*wt, mode=Mode.SUBTRACT)

show_object(wall_flange)

wall_flange.part.export_step("wall_flange.step")