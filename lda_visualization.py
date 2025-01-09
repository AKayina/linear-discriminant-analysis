# import numpy as np
# from manim import *
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# import random
# import os

# class LDAPlot(Scene):
#     def construct(self):
#         # Create directory for saved frames if it doesn't exist
#         if not os.path.exists('saved_frames'):
#             os.makedirs('saved_frames')
        
#         # Initialize frame counter
#         self.frame_counter = 0

#         def save_frame(name):
#             """Helper function to save frames"""
#             self.camera.get_image().save(
#                 f'saved_frames/frame_{self.frame_counter:03d}_{name}.png'
#             )
#             self.frame_counter += 1

#         # Create axes with specified ranges
#         axes = Axes(
#             x_range=[70, 110],  # X-pitch range
#             y_range=[35, 100],   # Y-amplitude range
#             axis_config={"color": BLUE},
#             x_length=7,  # Set the x-length to fit the 4:3 ratio
#             y_length=5.25  # Set the y-length to maintain the 4:3 aspect ratio
#         )

#         # Label the axes
#         x_label = Text("Pitch (Hz)", font_size=24).next_to(axes.x_axis, DOWN)
#         y_label = Text("Amplitude (dB)", font_size=24).next_to(axes.y_axis, LEFT).rotate(90 * DEGREES)

#         # Randomize healthy data points within the range (75-85, 85-95)
#         healthy_points = [
#             (random.uniform(75, 85), random.uniform(85, 95)) for _ in range(10)
#         ]
        
#         # Randomize unhealthy data points within the range (55-70, 45-65)
#         unhealthy_points = [
#             (random.uniform(55, 70), random.uniform(45, 65)) for _ in range(10)
#         ]

#         # Shift the data points slightly to the right (increase X values)
#         shift_value = 20  # Shift to the right by 20 units
#         healthy_points = [(x + shift_value, y) for x, y in healthy_points]
#         unhealthy_points = [(x + shift_value, y) for x, y in unhealthy_points]

#         # Convert to numpy arrays for LDA
#         healthy_points_np = np.array(healthy_points)
#         unhealthy_points_np = np.array(unhealthy_points)

#         # Combine the healthy and unhealthy data
#         X = np.vstack((healthy_points_np, unhealthy_points_np))
#         y = np.array([1] * len(healthy_points) + [0] * len(unhealthy_points))

#         # Perform LDA (Linear Discriminant Analysis)
#         lda = LinearDiscriminantAnalysis()
#         lda.fit(X, y)

#         # Get the decision boundary (line equation)
#         def decision_boundary(x):
#             return (-lda.coef_[0][0] * x - lda.intercept_[0]) / lda.coef_[0][1]

#         # Create data points (dots for healthy and unhealthy)
#         healthy_dot_mobjects = [Dot(axes.c2p(x, y), color=BLUE) for x, y in healthy_points]
#         unhealthy_dot_mobjects = [Dot(axes.c2p(x, y), color=RED) for x, y in unhealthy_points]

#         # Create line for the decision boundary (animated)
#         x_vals = np.linspace(axes.x_range[0], axes.x_range[1], 100)
#         y_vals = decision_boundary(x_vals)

#         # Create a line using the decision boundary points
#         decision_line = Line(axes.c2p(x_vals[0], y_vals[0]), axes.c2p(x_vals[-1], y_vals[-1]), color=GREEN)

#         # Title for the plot
#         title = Text("LDA", font_size=36).to_edge(UP)

#         # Create legend
#         legend_title = Text("Class", font_size=20).shift(UP * 3.5 + RIGHT * 4)
#         healthy_legend_dot = Dot(color=BLUE).shift(UP * 3 + RIGHT * 4)
#         unhealthy_legend_dot = Dot(color=RED).shift(UP * 2.5 + RIGHT * 4)
#         healthy_legend_label = Text("Healthy", font_size=16).next_to(healthy_legend_dot, RIGHT)
#         unhealthy_legend_label = Text("Unhealthy", font_size=16).next_to(unhealthy_legend_dot, RIGHT)

#         # Animation sequence with frame saving
#         self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
#         save_frame("initial_setup")

#         self.play(FadeIn(legend_title), FadeIn(healthy_legend_dot), FadeIn(unhealthy_legend_dot), 
#                   FadeIn(healthy_legend_label), FadeIn(unhealthy_legend_label))
#         save_frame("with_legend")

#         self.play(LaggedStartMap(FadeIn, healthy_dot_mobjects, shift=UP))
#         save_frame("healthy_points")

#         self.play(LaggedStartMap(FadeIn, unhealthy_dot_mobjects, shift=DOWN))
#         save_frame("all_points")

#         self.play(Create(decision_line))
#         save_frame("decision_line")

#         # Store projected points and their lines
#         projected_points = []
#         projection_lines = []

#         # Animate mapping data points to the decision line with color changes
#         for i, point in enumerate(healthy_dot_mobjects + unhealthy_dot_mobjects):
#             point_coords = point.get_center()
#             x_value = axes.p2c(point_coords)[0]
#             y_value = decision_boundary(x_value)
#             decision_point = axes.c2p(x_value, y_value)

#             line_to_boundary = Line(point_coords, decision_point, color=YELLOW)
#             projection_lines.append(line_to_boundary)

#             if point in healthy_dot_mobjects:
#                 point_on_line = Dot(decision_point, color=BLUE)
#             else:
#                 point_on_line = Dot(decision_point, color=RED)
            
#             projected_points.append(point_on_line)
#             self.play(Create(line_to_boundary), FadeIn(point_on_line))
#             save_frame(f"projection_{i}")

#         # Group decision line and projected points
#         decision_group = VGroup(decision_line, *projected_points)
        
#         # Fade out everything except decision line, projected points, and title
#         fade_group = VGroup(
#             axes, x_label, y_label,
#             *healthy_dot_mobjects, *unhealthy_dot_mobjects,
#             *projection_lines,
#             legend_title, healthy_legend_dot, unhealthy_legend_dot,
#             healthy_legend_label, unhealthy_legend_label
#         )
        
#         self.play(FadeOut(fade_group))
#         save_frame("faded_elements")
        
#         # Calculate the angle to rotate the decision line horizontal
#         start_point = decision_line.get_start()
#         end_point = decision_line.get_end()
#         angle = np.arctan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
        
#         # Animate the decision line and projected points to horizontal position
#         self.play(
#             decision_group.animate
#                 .rotate(-angle)
#                 .scale(1.5)
#                 .move_to(ORIGIN)
#         )
#         save_frame("final_position")

#         self.wait(2)
#         save_frame("final_frame")

# # To run and save frames, use:
# # manim -pqh --save_sections lda_plot.py LDAPlot



import numpy as np
from manim import *
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import random
import os

# Configure Manim to use a white background
config.background_color = WHITE

class LDAPlot(Scene):
    def construct(self):
        # Create directory for saved frames if it doesn't exist
        if not os.path.exists('saved_frames'):
            os.makedirs('saved_frames')
        
        # Initialize frame counter
        self.frame_counter = 0

        def save_frame(name):
            """Helper function to save frames"""
            self.camera.get_image().save(
                f'saved_frames/frame_{self.frame_counter:03d}_{name}.png'
            )
            self.frame_counter += 1

        # Create axes with specified ranges - now with black color
        axes = Axes(
            x_range=[70, 110],
            y_range=[35, 100],
            axis_config={
                "color": BLACK,
                "stroke_width": 1.2,
                "tip_length": 0.1
            },
            x_length=7,
            y_length=5.25
        )

        # Label the axes with black text
        x_label = Text("Pitch (Hz)", font_size=24, color=BLACK).next_to(axes.x_axis, DOWN)
        y_label = Text("Amplitude (dB)", font_size=24, color=BLACK).next_to(axes.y_axis, LEFT).rotate(90 * DEGREES)

        # Randomize healthy data points within the range (75-85, 85-95)
        healthy_points = [
            (random.uniform(75, 85), random.uniform(85, 95)) for _ in range(10)
        ]
        
        # Randomize unhealthy data points within the range (55-70, 45-65)
        unhealthy_points = [
            (random.uniform(55, 70), random.uniform(45, 65)) for _ in range(10)
        ]

        # Shift the data points slightly to the right (increase X values)
        shift_value = 20
        healthy_points = [(x + shift_value, y) for x, y in healthy_points]
        unhealthy_points = [(x + shift_value, y) for x, y in unhealthy_points]

        # Convert to numpy arrays for LDA
        healthy_points_np = np.array(healthy_points)
        unhealthy_points_np = np.array(unhealthy_points)

        # Combine the healthy and unhealthy data
        X = np.vstack((healthy_points_np, unhealthy_points_np))
        y = np.array([1] * len(healthy_points) + [0] * len(unhealthy_points))

        # Perform LDA
        lda = LinearDiscriminantAnalysis()
        lda.fit(X, y)

        # Get the decision boundary (line equation)
        def decision_boundary(x):
            return (-lda.coef_[0][0] * x - lda.intercept_[0]) / lda.coef_[0][1]

        # Create data points (dots for healthy and unhealthy)
        # Using darker colors for better visibility on white background
        healthy_dot_mobjects = [Dot(axes.c2p(x, y), color="BLUE", radius=0.08) for x, y in healthy_points]  # Darker blue
        unhealthy_dot_mobjects = [Dot(axes.c2p(x, y), color="RED", radius=0.08) for x, y in unhealthy_points]  # Darker red

        # Create line for the decision boundary
        x_vals = np.linspace(axes.x_range[0], axes.x_range[1], 100)
        y_vals = decision_boundary(x_vals)
        decision_line = Line(
            axes.c2p(x_vals[0], y_vals[0]),
            axes.c2p(x_vals[-1], y_vals[-1]),
            color=GREEN,
            stroke_width=4
        )

        # Title for the plot - black text
        title = Text("Linear Discriminant Analysis", font_size=28, color=BLACK).to_edge(UP)

        # Create legend with black text and darker colors
        legend_title = Text("Class", font_size=18, color=BLACK).shift(UP * 3 + RIGHT * 4)
        healthy_legend_dot = Dot(color="BLUE",).shift(UP * 2.5 + RIGHT * 4)
        unhealthy_legend_dot = Dot(color="RED",).shift(UP * 2 + RIGHT * 4)
        healthy_legend_label = Text("Healthy", font_size=16, color=BLACK).next_to(healthy_legend_dot, RIGHT)
        unhealthy_legend_label = Text("Unhealthy", font_size=16, color=BLACK).next_to(unhealthy_legend_dot, RIGHT)

        # Animation sequence with frame saving
        self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
        save_frame("initial_setup")

        self.play(FadeIn(legend_title), FadeIn(healthy_legend_dot), FadeIn(unhealthy_legend_dot), 
                  FadeIn(healthy_legend_label), FadeIn(unhealthy_legend_label))
        save_frame("with_legend")

        self.play(LaggedStartMap(FadeIn, healthy_dot_mobjects, shift=UP))
        save_frame("healthy_points")

        self.play(LaggedStartMap(FadeIn, unhealthy_dot_mobjects, shift=DOWN))
        save_frame("all_points")

        self.play(Create(decision_line))
        save_frame("decision_line")

        # Store projected points and their lines
        projected_points = []
        projection_lines = []

        # Animate mapping data points to the decision line
        for i, point in enumerate(healthy_dot_mobjects + unhealthy_dot_mobjects):
            point_coords = point.get_center()
            x_value = axes.p2c(point_coords)[0]
            y_value = decision_boundary(x_value)
            decision_point = axes.c2p(x_value, y_value)

            # # Using a darker yellow for projection lines
            # line_to_boundary = Line(point_coords, decision_point, color="#DAA520", stroke_width=2)  # Darker yellow
            # projection_lines.append(line_to_boundary)

            # Using dashed lines for projections
            line_to_boundary = DashedLine(
                point_coords, 
                decision_point, 
                color=GREY,
                stroke_width=1,
                dash_length=0.1,  # Length of each dash
                dashed_ratio=0.5  # Ratio of dash to space (0.5 means equal dash and space)
            )
            projection_lines.append(line_to_boundary)

            if point in healthy_dot_mobjects:
                point_on_line = Dot(decision_point, color="BLUE")
            else:
                point_on_line = Dot(decision_point, color="RED")
            
            projected_points.append(point_on_line)
            self.play(Create(line_to_boundary), FadeIn(point_on_line))
            save_frame(f"projection_{i}")

        decision_group = VGroup(decision_line, *projected_points)
        
        fade_group = VGroup(
            axes, x_label, y_label,
            *healthy_dot_mobjects, *unhealthy_dot_mobjects,
            *projection_lines
        )
        
        self.play(FadeOut(fade_group))
        save_frame("faded_elements")
        
        start_point = decision_line.get_start()
        end_point = decision_line.get_end()
        angle = np.arctan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
        
        self.play(
            decision_group.animate
                .rotate(-angle)
                .scale(1.5)
                .move_to(ORIGIN)
        )
        save_frame("final_position")

        self.wait(2)
        save_frame("final_frame")

# To run and save frames:
# manim -pqh --save_sections lda_visualization.py LDAPlot