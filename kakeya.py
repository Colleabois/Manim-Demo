from manim import *

class PointWithTrace(Scene):
    def construct(self):
        path = VMobject()
        dot = Dot()
        path.set_points_as_corners([dot.get_center(), dot.get_center()])
        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        self.add(path, dot)
        self.play(Rotating(dot, radians=PI, about_point=RIGHT, run_time=2))
        self.wait()
        self.play(dot.animate.shift(UP))
        self.play(dot.animate.shift(LEFT))
        self.wait()

class RotationUpdater(Scene):
    def construct(self):
        def updater_forth(mobj, dt):
            mobj.rotate_about_origin(dt)
        def updater_back(mobj, dt):
            mobj.rotate_about_origin(-dt)
        line_reference = Line(ORIGIN, LEFT).set_color(WHITE)
        line_moving = Line(ORIGIN, LEFT).set_color(YELLOW)
        line_moving.add_updater(updater_forth)
        self.add(line_reference, line_moving)
        self.wait(2)
        line_moving.remove_updater(updater_forth)
        line_moving.add_updater(updater_back)
        self.wait(2)
        line_moving.remove_updater(updater_back)
        self.wait(0.5)

class Kakeya(Scene):
    def construct(self):
        def updater_forth(mobj, dt):
            mobj.rotate_about_origin(dt)

        path = VMobject()
        path2 = VMobject()
        needle_reference = Line(ORIGIN, LEFT).set_color(WHITE)
        needle_moving = Line(ORIGIN, LEFT).set_color(YELLOW)
        dot = Dot(LEFT)
        dot2 = Dot(0.5*LEFT)
        path.set_points_as_corners([dot.get_center(), dot.get_center()])
        path2.set_points_as_corners([dot2.get_center(), dot2.get_center()])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)
        def update_path2(path2):
            previous_path = path2.copy()
            previous_path.add_points_as_corners([dot2.get_center()])
            path2.become(previous_path)

        path.add_updater(update_path)
        path2.add_updater(update_path2)
        needle_moving.add_updater(updater_forth)
        dot.add_updater(updater_forth)
        dot2.add_updater(updater_forth)
        self.add(path, path2, dot, dot2, needle_reference,needle_moving)
        self.wait(5)
        