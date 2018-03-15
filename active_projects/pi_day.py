# -*- coding: utf-8 -*-

from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.compositions import *
from animation.playground import *
from animation.continual_animation import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.fractals import *
from topics.number_line import *
from topics.combinatorics import *
from topics.numerals import *
from topics.three_dimensions import *
from topics.objects import *
from topics.probability import *
from topics.complex_numbers import *
from scene import Scene
from scene.reconfigurable_scene import ReconfigurableScene
from scene.zoomed_scene import *
from scene.moving_camera_scene import *
from camera import *
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from topics.graph_scene import *
from topics.common_scenes import *

RESOURCE_DIR = os.path.join(MEDIA_DIR, "3b1b_videos", "π Day 2018", "images")
def get_image(name):
    return ImageMobject(os.path.join(RESOURCE_DIR, name))

def get_circle_drawing_terms(radius = 1, positioning_func = lambda m : m.center()):
    circle = Circle(color = YELLOW, radius = 1.25)
    positioning_func(circle)
    radius = Line(circle.get_center(), circle.points[0])
    radius.highlight(WHITE)
    one = TexMobject("1")
    one.scale(0.75)
    one_update = UpdateFromFunc(
        one, lambda m : m.move_to(
            radius.get_center() + \
            0.25*rotate_vector(radius.get_vector(), TAU/4)
        ),
    )
    decimal = DecimalNumber(0, num_decimal_points = 4, show_ellipsis = True)
    decimal.scale(0.75)
    def reposition_decimal(decimal):
        vect = radius.get_vector()
        unit_vect = vect/np.linalg.norm(vect)
        angle = radius.get_angle()
        alpha = (-np.cos(2*angle) + 1)/2
        interp_length = interpolate(decimal.get_width(), decimal.get_height(), alpha)
        buff = interp_length/2 + MED_SMALL_BUFF
        decimal.move_to(radius.get_end() + buff*unit_vect)
        decimal.shift(UP*decimal.get_height()/2)
        return decimal

    kwargs = {"run_time" : 3, "rate_func" : bezier([0, 0, 1, 1])} 
    changing_decimal = ChangingDecimal(
        decimal, lambda a : a*TAU,
        position_update_func = reposition_decimal,
        **kwargs
    )

    terms = VGroup(circle, radius, one, decimal)
    generate_anims1 = lambda : [ShowCreation(radius), Write(one)]
    generate_anims2 = lambda : [
        ShowCreation(circle, **kwargs),
        Rotating(radius, about_point = radius.get_start(), **kwargs),
        changing_decimal,
        one_update,
    ]

    return terms, generate_anims1, generate_anims2

##

class PiTauDebate(PiCreatureScene):
    def construct(self):
        pi, tau = self.pi, self.tau
        self.add(pi, tau)

        pi_value = TextMobject("3.1415...!")
        pi_value.highlight(BLUE)
        tau_value = TextMobject("6.2831...!")
        tau_value.highlight(GREEN)

        self.play(PiCreatureSays(
            pi, pi_value,
            target_mode = "angry",
            look_at_arg = tau.eyes,
            # bubble_kwargs = {"width" : 3}
        ))
        self.play(PiCreatureSays(
            tau, tau_value,
            target_mode = "angry",
            look_at_arg = pi.eyes,
            bubble_kwargs = {"width" : 3, "height" : 2},
        ))
        self.wait()

        # Show tau
        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius = 1.25,
            positioning_func = lambda m : m.to_edge(RIGHT, buff = 2).to_edge(UP, buff = 1)
        )
        circle, radius, one, decimal = terms

        self.play(
            RemovePiCreatureBubble(pi),
            RemovePiCreatureBubble(tau),
            *generate_anims1()
        )
        self.play(
            tau.change, "hooray",
            pi.change, "sassy",
            *generate_anims2()
        )
        self.wait()


        # Show pi
        circle = Circle(color = RED, radius = 1.25/2)
        circle.rotate(TAU/4)
        circle.move_to(pi)
        circle.to_edge(UP, buff = MED_LARGE_BUFF)
        diameter = Line(circle.get_left(), circle.get_right())
        one = TexMobject("1")
        one.scale(0.75)
        one.next_to(diameter, UP, SMALL_BUFF)

        circum_line = diameter.copy().scale(np.pi)
        circum_line.match_style(circle)
        circum_line.next_to(circle, DOWN, buff = MED_LARGE_BUFF)
        # circum_line.to_edge(LEFT)
        brace = Brace(circum_line, DOWN, buff = SMALL_BUFF)
        decimal = DecimalNumber(np.pi, num_decimal_points = 4, show_ellipsis = True)
        decimal.scale(0.75)
        decimal.next_to(brace, DOWN, SMALL_BUFF)

        self.play(
            FadeIn(VGroup(circle, diameter, one)),
            tau.change, "confused",
            pi.change, "hooray"
        )
        self.add(circle.copy().fade(0.5))
        self.play(
            ReplacementTransform(circle, circum_line, run_time = 2)
        )
        self.play(GrowFromCenter(brace), Write(decimal))
        self.wait(3)
        # self.play()


    def create_pi_creatures(self):
        pi = self.pi = Randolph()
        pi.to_edge(DOWN).shift(4*LEFT)
        tau = self.tau = TauCreature(
            # mode = "angry",
            file_name_prefix = "TauCreatures",
            color = GREEN_E
        ).flip()
        tau.to_edge(DOWN).shift(4*RIGHT)
        return VGroup(pi, tau)

class HartlAndPalais(Scene):
    def construct(self):
        hartl_rect = ScreenRectangle(
            color = WHITE,
            stroke_width = 1,
        )
        hartl_rect.scale_to_fit_width(SPACE_WIDTH - 1)
        hartl_rect.to_edge(LEFT)
        palais_rect = hartl_rect.copy()
        palais_rect.to_edge(RIGHT)

        tau_words = TextMobject("$\\tau$ ``tau''")
        tau_words.next_to(hartl_rect, UP)

        hartl_words = TextMobject("Michael Hartl's \\\\ ``Tau manifesto''")
        hartl_words.next_to(hartl_rect, DOWN)

        palais_words = TextMobject("Robert Palais' \\\\ ``Pi is Wrong!''")
        palais_words.next_to(palais_rect, DOWN)

        for words in hartl_words, palais_words:
            words.scale(0.7, about_edge = UP)

        three_legged_creature = ThreeLeggedPiCreature(height = 1.5)
        three_legged_creature.next_to(palais_rect, UP)

        # self.add(hartl_rect, palais_rect)
        self.add(hartl_words)
        self.play(Write(tau_words))
        self.wait()
        self.play(FadeIn(palais_words))
        self.play(FadeIn(three_legged_creature))
        self.play(three_legged_creature.change_mode, "wave")
        self.play(Blink(three_legged_creature))
        self.play(Homotopy(
            lambda x, y, z, t : (x + 0.1*np.sin(2*TAU*t)*np.exp(-10*(t-0.5 - 0.5*(y-1.85))**2), y, z),
            three_legged_creature,
            run_time = 2,
        ))
        self.wait()

class ManyFormulas(Scene):
    def construct(self):
        formulas = VGroup(
            TexMobject("\\sin(x + \\tau) = \\sin(x)"),
            TexMobject("e^{\\tau i} = 1"),
            TexMobject("n! \\approx \\sqrt{\\tau n} \\left(\\frac{n}{e} \\right)^n"),
            TexMobject("c_n = \\frac{1}{\\tau} \\int_0^\\tau f(x) e^{inx}dx"),
        )
        formulas.arrange_submobjects(DOWN, buff = MED_LARGE_BUFF)
        formulas.to_edge(LEFT)

        self.play(LaggedStart(FadeIn, formulas, run_time = 3))

        circle = Circle(color = YELLOW, radius = 2)
        circle.to_edge(RIGHT)
        radius = Line(circle.get_center(), circle.get_right())
        radius.highlight(WHITE)

        angle_groups = VGroup()
        for denom in 5, 4, 3, 2:
            radius_copy = radius.copy()
            radius_copy.rotate(TAU/denom, about_point = circle.get_center())
            arc = Arc(
                angle = TAU/denom,
                stroke_color = RED,
                stroke_width = 4,
                radius = circle.radius,
            )
            arc.shift(circle.get_center())
            mini_arc = arc.copy()
            mini_arc.set_stroke(WHITE, 2)
            mini_arc.scale(0.15, about_point = circle.get_center())
            tau_tex = TexMobject("\\tau/%d"%denom)
            point = mini_arc.point_from_proportion(0.5)
            tau_tex.next_to(point, direction = point - circle.get_center())
            angle_group = VGroup(radius_copy, mini_arc, tau_tex, arc)
            angle_groups.add(angle_group)


        angle_group = angle_groups[0]
        self.play(*map(FadeIn, [circle, radius]))
        self.play(
            circle.set_stroke, {"width" : 1,},
            FadeIn(angle_group),
        )
        self.wait()
        for group in angle_groups[1:]:
            self.play(Transform(angle_group, group, path_arc = TAU/8))
            self.wait()

class HistoryOfOurPeople(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Today: The history \\\\ of our people.",
            bubble_kwargs = {"width" : 4, "height" : 3}
        )
        self.change_all_student_modes("hooray")
        self.wait()
        self.play(*[
            ApplyMethod(pi.change, "happy", self.screen)
            for pi in self.pi_creatures
        ])
        self.wait(4)

class TauFalls(Scene):
    def construct(self):
        tau = TauCreature()
        bottom = np.min(tau.body.points[:,1])*UP
        angle = -0.15*TAU
        tau.generate_target()
        tau.target.change("angry")
        tau.target.rotate(angle, about_point = bottom)
        self.play(Rotate(tau, angle, rate_func = rush_into, path_arc = angle, about_point = bottom))
        # self.play(MoveToTarget(tau, rate_func = rush_into, path_arc = angle))
        self.play(MoveToTarget(tau))
        self.wait()

class EulerWrites628(Scene):
    CONFIG = {
        "camera_config" : {
            "background_alpha" : 255,
        }
    }
    def construct(self):
        image = ImageMobject(os.path.join(RESOURCE_DIR, "dalembert_zoom"))
        image.scale_to_fit_width(2*SPACE_WIDTH - 1)
        image.to_edge(UP, buff = MED_SMALL_BUFF)
        image.fade(0.15)
        rect = Rectangle(
            width = 12, 
            height = 0.5,
            stroke_width = 0,
            fill_opacity = 0.3,
            fill_color = GREEN,
        )
        rect.insert_n_anchor_points(20)
        rect.apply_function(lambda p : np.array([p[0], p[1] - 0.005*p[0]**2, p[2]]))
        rect.rotate(0.012*TAU)
        rect.move_to(image)
        rect.shift(0.15*DOWN)

        words = TextMobject(
            "``Let", "$\\pi$", "be the", "circumference", 
            "of a circle whose", "radius = 1''",
        )
        words.highlight_by_tex_to_color_map({
            "circumference" : YELLOW,
            "radius" : GREEN,
        })
        words.next_to(image, DOWN)
        pi = words.get_part_by_tex("\\pi").copy()

        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius = 1, 
            positioning_func = lambda circ : circ.next_to(words, DOWN, buff = 1.25)
        )
        circle, radius, one, decimal = terms

        unwrapped_perimeter = Line(ORIGIN, TAU*RIGHT)
        unwrapped_perimeter.match_style(circle)
        unwrapped_perimeter.next_to(circle, DOWN)
        brace = Brace(unwrapped_perimeter, UP, buff = SMALL_BUFF)

        perimeter = TexMobject(
            "\\pi\\epsilon\\rho\\iota\\mu\\epsilon\\tau\\rho\\text{o}\\varsigma",
            "\\text{ (perimeter)}",
            "="
        )
        perimeter.next_to(brace, UP, submobject_to_align = perimeter[1], buff = SMALL_BUFF)
        perimeter[0][0].highlight(GREEN)

        self.play(FadeInFromDown(image))
        self.play(
            Write(words), 
            GrowFromPoint(rect, rect.point_from_proportion(0.9))
        )
        self.wait()
        self.play(*generate_anims1())
        self.play(*generate_anims2())
        self.play(terms.shift, UP)
        self.play(
            pi.scale, 2,
            pi.shift, DOWN, 
            pi.highlight, GREEN
        )
        self.wait()
        self.play(
            GrowFromCenter(brace),
            circle.set_stroke, YELLOW, 1,
            ReplacementTransform(circle.copy(), unwrapped_perimeter),
            decimal.scale, 1.25,
            decimal.next_to, perimeter[-1].get_right(), RIGHT,
            ReplacementTransform(pi, perimeter[0][0]),
            Write(perimeter),
        )
        self.wait()

class HeroAndVillain(Scene):
    CONFIG = {
        "camera_config" : {
            "background_alpha" : 255,
        } 
    }
    def construct(self):
        good_euler = get_image("Leonhard_Euler_by_Handmann")
        bad_euler_pixelated = get_image("Leonard_Euler_pixelated")
        bad_euler = get_image("Leonard_Euler_revealed")
        pictures = good_euler, bad_euler_pixelated, bad_euler
        for mob in pictures:
            mob.scale_to_fit_height(5)

        good_euler.move_to(SPACE_WIDTH*LEFT/2)
        bad_euler.move_to(SPACE_WIDTH*RIGHT/2)
        bad_euler_pixelated.move_to(bad_euler)

        good_euler_label = TextMobject("Leonhard Euler")
        good_euler_label.next_to(good_euler, DOWN)
        tau_words = TextMobject("Used 6.2831...")
        tau_words.next_to(good_euler, UP)
        tau_words.highlight(GREEN)

        bad_euler_label = TextMobject("Also Euler...")
        bad_euler_label.next_to(bad_euler, DOWN)
        pi_words = TextMobject("Used 3.1415...")
        pi_words.highlight(RED)
        pi_words.next_to(bad_euler, UP)

        self.play(
            FadeInFromDown(good_euler),
            Write(good_euler_label)
        )
        self.play(LaggedStart(FadeIn, tau_words))
        self.wait()
        self.play(FadeInFromDown(bad_euler_pixelated))
        self.play(LaggedStart(FadeIn, pi_words))
        self.wait(2)
        self.play(
            FadeIn(bad_euler),
            Write(bad_euler_label),
        )
        self.remove(bad_euler_pixelated)
        self.wait(2)

class AnalysisQuote(Scene):
    def construct(self):
        analysis = get_image("Analysis_page_showing_pi")
        analysis.scale_to_fit_height(2*SPACE_HEIGHT)
        analysis.to_edge(LEFT, buff = 0)

        text = TextMobject(
            "``\\dots set the radius of",
            "the circle\\dots to be = 1, \\dots \\\\",
            "through approximations the",
            "semicircumference \\\\", "of said circle",
            "has been found to be", "$= 3.14159\\dots$,\\\\",
            "for which number, for the sake of",
            "brevity, \\\\ I will write", "$\pi$\\dots''",
            alignment = ''
        )
        pi_formula = TexMobject(
            "\\pi", "=", "{ \\text{semicircumference}", "\\over", "\\text{radius}}"
        )
        text.scale_to_fit_width(SPACE_WIDTH)
        text.next_to(analysis, RIGHT, LARGE_BUFF)
        text.to_edge(UP)

        HIGHLIGHT_COLOR= GREEN
        for mob in text, pi_formula:
            mob.highlight_by_tex_to_color_map({
                "semicircumference" : HIGHLIGHT_COLOR,
                "3.14" : HIGHLIGHT_COLOR,
                "\pi" : HIGHLIGHT_COLOR
            })

        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius = 1,
            positioning_func = lambda circ : circ.next_to(text, DOWN, LARGE_BUFF)
        )
        terms[0].highlight(HIGHLIGHT_COLOR)
        terms[-1].highlight(HIGHLIGHT_COLOR)

        pi_formula.next_to(terms, DOWN, buff = 0)
        pi_formula.align_to(text, alignment_vect = RIGHT)
        pi_formula[0].scale(2, about_edge = RIGHT)

        self.add(analysis)
        self.play(*generate_anims2(), rate_func = lambda t : 0.5*smooth(t))
        self.play(LaggedStart(FadeIn,text), run_time = 5)
        self.play(FadeIn(pi_formula))
        self.wait()

class QuarterTurn(Scene):
    def construct(self):
        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius = 2,
            positioning_func = lambda circ : circ.move_to(4*RIGHT)
        )
        circle, radius, one, decimal = terms
        circle_ghost = circle.copy().set_stroke(YELLOW_E, 1)
        radius_ghost = radius.copy().set_stroke(WHITE, 1)

        self.add(circle_ghost, radius_ghost)
        self.play(
            *generate_anims2(),
            rate_func = lambda t : 0.25*smooth(t)
        )
        self.wait()

        pi_halves = TexMobject("\\pi", "/2")
        pi_halves[0].highlight(RED)
        tau_fourths = TexMobject("\\tau", "/4")
        tau_fourths[0].highlight(GREEN)
        for mob in pi_halves, tau_fourths:
            mob.next_to(decimal, UP)

        self.play(FadeInFromDown(pi_halves))
        self.wait()
        self.play(
            pi_halves.shift, 0.75*UP,
            FadeInFromDown(tau_fourths)
        )
        self.wait()

class UsingTheta(Scene):
    def construct(self):
        plane = NumberPlane(x_unit_size = 3, y_unit_size = 3)
        # plane.main_lines.fade(0.5)
        # plane.secondary_lines.fade(0.5)
        plane.fade(0.5)
        self.add(plane)

        circle = Circle(radius = 3)
        circle.set_stroke(YELLOW, 2)
        self.add(circle)

        radius = Line(ORIGIN, circle.get_right())
        arc = Arc(radius = 0.5, angle = TAU, num_anchors = 200)
        arc.highlight(GREEN)
        start_arc = arc.copy()

        theta = TexMobject("\\theta", "=")
        theta[0].match_color(arc)
        theta.add_background_rectangle()
        update_theta = ContinualUpdateFromFunc(
            theta, lambda m : m.shift(
                rotate_vector(0.9*RIGHT, radius.get_angle()/2) \
                - m[1][0].get_center()
            )
        )

        angle = Integer(0, unit = "^\\circ")
        update_angle = ContinualChangingDecimal(
            angle, lambda a : radius.get_angle()*(360/TAU),
            position_update_func = lambda a : a.next_to(theta, RIGHT, SMALL_BUFF)
        )

        self.add(update_theta, update_angle)
        last_frac = 0
        for frac in 1./4, 1./12, 3./8, 1./6, 5./6:
            self.play(
                Rotate(radius, angle = (frac-last_frac)*TAU, about_point = ORIGIN),
                UpdateFromAlphaFunc(
                    arc,
                    lambda m, a : m.pointwise_become_partial(
                        start_arc, 0, interpolate(last_frac, frac, a)
                    )
                ),
                run_time = 3
            )
            last_frac = frac
            self.wait()

class ThingsNamedAfterEuler(Scene):
    def construct(self):
        group = VGroup(*map(TextMobject, [
            "Euler's formula (Complex analysis)",
            "Euler's formula (Graph theory)",
            "Euler's formula (Mechanical engineering)",
            "Euler's formula (Analytical number theory)",
            "Euler's formula (Continued fractions)",
            "Euler-Lagrance equations (mechanics)",
            "Euler number (topology)",
            "Euler equations (fluid dynamics)",
            "Euler angles (rigid-body mechanics)",
            "Euler totient function (number theory)",
        ]))
        group.arrange_submobjects(DOWN, aligned_edge = LEFT)
        group.scale_to_fit_height(2*SPACE_HEIGHT - 1)

        self.play(LaggedStart(FadeIn, group, lag_ratio = 0.2, run_time = 12))
        self.wait()

class EulerThinking(Scene):
    def construct(self):
        image = get_image("Leonhard_Euler_by_Handmann")
        image.scale_to_fit_height(4)
        image.to_edge(DOWN)
        image.shift(4*LEFT)
        bubble = ThoughtBubble(height = 4.5)
        bubble.next_to(image, RIGHT)
        bubble.to_edge(UP, buff = SMALL_BUFF)
        bubble.shift(0.8*LEFT)
        bubble.set_fill(BLACK, 0.3)

        pi_vs_tau = TextMobject(
            "Should $\\pi$ represent \\\\", "3.1415...", 
            "or", "6.2831...", "?"
        )
        pi_vs_tau.highlight_by_tex_to_color_map({
            "3.14" : GREEN,    
            "6.28" : RED,
        })
        pi_vs_tau.move_to(bubble.get_bubble_center())

        question = TexMobject(
            "\\frac{1}{1} + \\frac{1}{4} + \\frac{1}{9} + \\frac{1}{16} + \\cdots = ",
            "\\;???"
        )
        question[0].gradient_highlight(BLUE_C, BLUE_B)
        question.move_to(bubble.get_bubble_center())
        question.shift(2*SMALL_BUFF*UP)

        cross = Cross(pi_vs_tau)
        cross.set_stroke(RED, 8)

        self.add(image)
        self.play(
            ShowCreation(bubble),
            Write(pi_vs_tau)
        )
        self.play(ShowCreation(cross))
        self.wait()
        self.play(
            FadeOut(VGroup(pi_vs_tau, cross)),
            FadeIn(question),
        )
        self.wait()


class WhatIsRight(PiCreatureScene):
    CONFIG = {
        "default_pi_creature_kwargs" : {
            "color" : BLUE_D,
            "filp_at_start" : False,
        },
        "default_pi_creature_start_corner" : DOWN,
    }
    def construct(self):
        randy = self.pi_creature
        randy.scale(0.75, about_edge = DOWN)
        title = TextMobject("Which is ``right''?")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)

        sum_over_N_converges = TexMobject("1+2+3+\\cdots = -\\frac{1}{12}")
        sum_over_N_diverges = TexMobject("1+2+3+\\cdots \\text{ Diverges}")

        literal_derivative = TexMobject(
            "f'(x) = \\frac{f(x+dx) - f(x)}{dx}"
        )
        limit_derivative = TexMobject(
            "f'(x) = \\lim_{h \\to 0}\\frac{f(x+h) - f(x)}{h}"
        )

        divide_by_zero_definable = TexMobject(
            "\\frac{1}{0}", "\\text{ has meaning}"
        )
        divide_by_zero_undefinable = TexMobject(
            "\\frac{1}{0}", "\\text{ is undefined}"
        )

        left_mobs = VGroup(
            sum_over_N_converges, literal_derivative,
            divide_by_zero_definable
        )
        right_mobs = VGroup(
            sum_over_N_diverges, limit_derivative,
            divide_by_zero_undefinable
        )

        for mob in left_mobs:
            mob.next_to(randy, UP)
            mob.shift(3.5*LEFT)
        for mob in right_mobs:
            mob.next_to(randy, UP)
            mob.shift(3.5*RIGHT)

        left_mobs.gradient_highlight(YELLOW_C, YELLOW_D)
        right_mobs.gradient_highlight(GREEN_C, GREEN_D)

        self.play(randy.change, "pondering", title)
        self.wait()
        self.play(randy.change, "sassy", title)
        self.wait()

        last_terms = VGroup()
        for left, right in zip(left_mobs, right_mobs)[:-1]:
            right.align_to(left)
            self.play(
                randy.change, "raise_right_hand",
                FadeInFromDown(left),
                last_terms.shift, 1.75*UP
            )
            self.wait()
            self.play(
                randy.change, "raise_left_hand",
                FadeInFromDown(right)
            )
            self.play(randy.change, "plain", right)
            last_terms.add(left, right, title)
        self.play(
            randy.change, "shruggie",
            FadeInFromDown(left_mobs[-1]),
            FadeInFromDown(right_mobs[-1]),
            last_terms.shift, 1.75*UP,
        )
        self.wait(4)

class AskPuzzle(TeacherStudentsScene):
    def construct(self):
        series = TexMobject(
            "\\frac{1}{1} + \\frac{1}{4} + \\frac{1}{9} + \\cdots + " +\
            "\\frac{1}{n^2} + \\cdots = ", "\\,???"
        )
        series[0].gradient_highlight(BLUE_C, BLUE_B)
        series[1].highlight(YELLOW)

        question = TextMobject(
            "How should we think about\\\\",
            "$\\displaystyle \\sum_{n=1}^\\infty \\frac{1}{n^s}$",
            "for arbitrary $s$?"
        )
        question[1].highlight(BLUE)
        question[0].shift(SMALL_BUFF*UP)

        response = TextMobject(
            "What do you mean by ", 
            "$\\displaystyle \\sum_{n = 1}^{\\infty}$", 
            "?"
        )
        response[1].highlight(BLUE)

        self.teacher_says(series)
        self.change_all_student_modes("pondering", look_at_arg = series)
        self.wait(3)
        self.play(
            FadeOut(self.teacher.bubble),
            self.teacher.change, "happy",
            series.scale, 0.5,
            series.to_corner, UP+LEFT,
            PiCreatureSays(
                self.students[0], question,
                target_mode = "raise_left_hand"
            )
        )
        self.change_student_modes(
            None, "confused", "confused",
            added_anims = [self.students[0].look_at, question]
        )
        self.wait(2)

        self.students[0].bubble.content = VGroup()
        self.play(
            RemovePiCreatureBubble(self.students[0]),
            question.scale, 0.5,
            question.next_to, series, DOWN, MED_LARGE_BUFF, LEFT,
            PiCreatureSays(self.teacher, response)
        )
        self.change_all_student_modes("erm")
        self.wait(3)

class ChangeTopic(PiCreatureScene):
    def construct(self):
        pi, tau = self.pi_creatures
        title = TextMobject("Happy $\\pi$ day!")
        title.scale(1.5)
        title.to_edge(UP, buff = MED_SMALL_BUFF)
        self.add(title)

        question = TextMobject(
            "Have you ever seen why \\\\",
            "$\\displaystyle \\frac{2}{1} \\cdot \\frac{2}{3} \\cdots"+ \
            "\\frac{4}{3} \\cdot \\frac{4}{5} \\cdot" + \
            "\\frac{6}{5} \\cdot \\frac{6}{7} \\cdots = \\frac{\\pi}{2}$", "?"
        )
        question[0].shift(MED_SMALL_BUFF*UP)
        question[1].gradient_highlight(YELLOW, GREEN)

        self.play(
            PiCreatureSays(
                tau, "We should \\emph{really} celebrate \\\\ on 6/28!",
                target_mode = "angry",
            ),
            pi.change, "guilty",
        )
        self.wait(2)
        self.play(
            PiCreatureSays(pi, question),
            RemovePiCreatureBubble(
                tau, target_mode = "pondering", look_at_arg = question,
            )
        )
        self.play(pi.change, "pondering", question)
        self.wait(4)


    def create_pi_creatures(self):
        tau = TauCreature(color = GREEN_E)
        pi = Randolph().flip()
        VGroup(pi, tau).scale(0.75)
        tau.to_edge(DOWN).shift(3*LEFT)
        pi.to_edge(DOWN).shift(3*RIGHT)
        return pi, tau

class SpecialThanks(Scene):
    def construct(self):
        title = TextMobject("Special thanks to:")
        title.to_edge(UP, LARGE_BUFF)
        title.scale(1.5)
        title.highlight(BLUE)
        h_line = Line(LEFT, RIGHT).scale(4)
        h_line.next_to(title, DOWN)
        h_line.set_stroke(WHITE, 1)

        people = VGroup(*map(TextMobject, [
            "Ben Hambrecht",
            "University Library Basel",
            "Martin Mattmüller",
            "Library of the Institut de France",
        ]))
        people.arrange_submobjects(DOWN, aligned_edge = LEFT, buff = MED_LARGE_BUFF)
        people.next_to(h_line, DOWN)

        self.add(title, h_line, people)

class EndScene(PatreonEndScreen):
    CONFIG = {
        "camera_config" : {
            "background_alpha" : 255,
        }
    }
    def construct(self):
        self.add_title()
        title = self.title
        basel_screen = ScreenRectangle(height = 2.35)
        basel_screen.next_to(title, DOWN)
        watch_basel = TextMobject(
            "One such actual piece of math", "(quite pretty!)",
        )
        watch_basel[0].highlight(YELLOW)
        watch_basel.next_to(basel_screen, DOWN, submobject_to_align = watch_basel[0])

        self.add(watch_basel)
        # self.add(basel_screen)

        line = DashedLine(SPACE_WIDTH*LEFT, SPACE_WIDTH*RIGHT)
        line.next_to(watch_basel, DOWN)
        self.add(line)

        plushie_square = Square(side_length = 2)
        plushie_square.to_corner(DOWN+LEFT, buff = MED_LARGE_BUFF)
        plushie_square.shift(UP)

        plushie_words = TextMobject(
            "Plushie pi \\\\ creatures \\\\ now available.",
            alignment = ""
        )
        plushie_words.next_to(plushie_square, RIGHT)

        self.add(plushie_words)
        # self.add(plushie_square)

        instagram_line = TextMobject(
            "randy\\_the\\_pi"
        )
        instagram_logo = ImageMobject("instagram_logo")
        instagram_logo.match_height(instagram_line)
        instagram_logo.next_to(instagram_line, LEFT, SMALL_BUFF)
        instagram = Group(instagram_logo, instagram_line)
        instagram.next_to(line, DOWN)
        instagram.shift(SPACE_WIDTH*RIGHT/2)
        self.add(instagram)


        pictures = Group(*[
            ImageMobject("randy/randy_%s"%name)
            for name in [
                "science",
                "cooking",
                "in_a_can",
                "sandwhich",
                "lab",
                "fractal",
                "flowers",
                "group",
                "labcoat",
                "tennis",
            ]
        ])
        for i, picture in enumerate(pictures):
            picture.scale_to_fit_height(2)
            picture.next_to(instagram, DOWN, aligned_edge = RIGHT)
            if i%3 != 0:
                picture.next_to(last_picture, LEFT, buff = 0)
            self.play(FadeIn(picture, run_time = 2))
            last_picture = picture

class Thumbnail(Scene):
    def construct(self):
        pi, eq, num = formula = TexMobject(
            "\\pi", "=", "6.283185\\dots"
        )
        formula.scale(2)
        pi.scale(1.5, about_edge = RIGHT)
        formula.set_stroke(BLUE, 1)
        formula.scale_to_fit_width(2*SPACE_WIDTH - 2)
        # formula.shift(0.5*RIGHT)
        self.add(formula)

        words = TextMobject("...according to Euler.")
        words.scale(1.5)
        words.next_to(formula, DOWN, MED_LARGE_BUFF)
        self.add(words)






















