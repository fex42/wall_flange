from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

pipe_dia = 99.0
wall_thickness = 2.5
pipe_height = 67.0
flange_dia = 128.0
holes_dia = 119.0
hole_dia = 4.6
apothema = 5.0

with BuildPart() as wall_flange:
    with BuildSketch():
        Circle(pipe_dia/2)
        Circle(pipe_dia/2 - wall_thickness, mode=Mode.SUBTRACT)
    extrude(amount=pipe_height)
    with BuildSketch():
        Circle(flange_dia/2)
        Circle(pipe_dia/2, mode=Mode.SUBTRACT)
    extrude(amount=wall_thickness)

    # fillet on outer flange/pipe edge makes it hopefully more stable
    edge = wall_flange.edges().filter_by_position(axis=Axis.Z, minimum=wall_thickness, maximum=wall_thickness)[0]
    fillet(objects=edge, radius=1.0)
    # hexagon grid
    with BuildSketch() as grid_sk:
        Circle(radius=pipe_dia/2)
        with HexLocations(apothema, 11, 10):
            RegularPolygon(apothema, 6, mode=Mode.SUBTRACT)
    extrude(amount=wall_thickness)
    # screw holes
    with BuildSketch():
        with PolarLocations(holes_dia/2, 4):
            Circle(hole_dia/2)
    extrude(amount=2*wall_thickness, mode=Mode.SUBTRACT)

show_object(wall_flange)

wall_flange.part.export_step("wall_flange.step")