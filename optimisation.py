#from typing_extensions import runtime
from manim import *
from pathlib import *
import os
# Commands
FLAGS = f"-pql" # quality: l(low), m(medium), h(high)
SCENE = "Optimisation"

# Parameters for axes
x_max = 9
y_max = 9
# max (40x+50y)   ->  max (0.8x+y) (profit)
# 10x + 10y = 50  ->     x + y = 5 (lys)
# 10x + 20y = 80  ->  0.5x + y = 4 (roses)
# 20x + 10y = 80  ->    2x + y = 8 (jonquilles)

p0 = -0.8
b0 = 3.
p = [-1., -0.5, -2.]
b = [5., 4., 8.]
colors = [GREEN_A, GREEN_B, GREEN_C]
nc = len(p)
assert(nc == len(b))

def f_factory(i):
    def f(x):
        return p[i]*x+b[i]
    return f

def fi_factory(i):
    def fi(y):
        return (y-b[i])/p[i] 
    return fi
 
fs = [f_factory(i) for i in range(nc)]
fis = [fi_factory(i) for i in range(nc)]

def line_intersection(i, j): # index in fs fis
    x = -(b[i]-b[j]+0.)/(p[i]-p[j])
    y = (p[i]*b[j]-p[j]*b[i]+0.)/(p[i]-p[j])
    return x, y

class Optimisation(Scene):
    def construct(self):
        b = ValueTracker(b0)

        axes = Axes(
            x_range = [0,x_max,1],
            y_range = [0,y_max,1], 
            x_length = 6, 
            y_length = 5,
            x_axis_config={"numbers_to_include": [1,4,5,8]},
            y_axis_config={"numbers_to_include": [1,4,5,8]}
        )
        labels = axes.get_axis_labels(
            x_label=Tex("$x_1$"), y_label=Tex("$x_2$")
        )
        
        cs = []
        for i in range (nc):
            cs.append(
                axes.plot(
                lambda x : fs[i](x),
                x_range = [0,fis[i](0)],
                color = colors[i] #random_color()#interpolate_color(GREEN, YELLOW, (i+0.)/nc)
                )
            )
        
        areas = []
        for i in range (nc):
            areas.append(
                axes.get_area(
                cs[i], 
                [0, fis[i](0)], 
                #bounded_graph=curve_1, 
                color=cs[i].get_color(), 
                opacity=0.2
                )
            )

        moving_line = always_redraw(
            lambda : axes.plot(
                lambda x : p0*x+b.get_value(),
                x_range = [0, -(b.get_value()+0.)/p0],
                color = YELLOW
                )
        )

        # Texts
        text_profit = (
            Tex("Profit : ")
            .next_to(axes,DOWN, buff = 0.3)
            .set_color(YELLOW)
            #.add_background_rectangle()
        )
        val_profit =  always_redraw(
            lambda : DecimalNumber(num_decimal_places=2)
                .set_value(b.get_value()*50)
                .next_to(text_profit,RIGHT, buff = 0.1)
                .set_color(YELLOW)
        )#.add_background_rectangle()

        texts_flowers = [
            Tex("Lys").next_to(cs[0],UL, buff = 0.3).shift( DOWN*0.5 ).shift( LEFT*0.5 ),
            Tex("Roses").next_to(cs[1],UL, buff = 0.3).shift( DOWN*0.5 ).shift( LEFT*0.5 ),
            Tex("Jonquilles").next_to(cs[2],UL, buff = 0.3).shift( DOWN*0.5 ).shift( LEFT*0.5 )
        ]

        # Animation
        self.play(Create(axes))
        self.play(Create(labels))
        for i in range (nc):
            self.play(Write(texts_flowers[i]))
            self.play(Create(cs[i]))
            self.add(areas[i])
        self.wait()
        self.play(Create(moving_line))
        self.play(Write(text_profit))
        self.add(val_profit)
        self.wait()
        
        x0, y0 = line_intersection(0,1)
        y1 = y0 - p0*x0
        self.play(b.animate.set_value(y1), runtime=15, rate_functions=linear)
        self.wait(5)


if __name__ == '__main__':
    script_name = f"{Path(__file__).resolve()}"
    os.system(f"manim {script_name} {SCENE} {FLAGS}")