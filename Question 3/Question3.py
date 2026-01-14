import turtle
import math

# -----------------------------
# Recursive function to draw the pattern on a line
# -----------------------------
def draw_pattern(t, length, depth):
    """
    Draws a single edge with recursive indentations.
    
    Args:
        t (turtle.Turtle): The turtle object
        length (float): Length of the current segment
        depth (int): Recursion depth
    """
    if depth == 0:
        t.forward(length)  # Base case: draw straight line
    else:
        # Divide the line into 3 segments
        segment = length / 3

        # Draw first segment
        draw_pattern(t, segment, depth - 1)

        # Turn to create inward equilateral triangle
        t.left(60)            # Turn left 60° for inward triangle
        draw_pattern(t, segment, depth - 1)

        t.right(120)          # Turn right 120° to complete the triangle
        draw_pattern(t, segment, depth - 1)

        t.left(60)            # Turn back to original direction
        draw_pattern(t, segment, depth - 1)

# -----------------------------
# Function to draw a full polygon
# -----------------------------
def draw_polygon(t, sides, length, depth):
    """
    Draws a polygon with recursive patterns on each edge.
    
    Args:
        t (turtle.Turtle): Turtle object
        sides (int): Number of sides of the polygon
        length (float): Length of each side
        depth (int): Recursion depth
    """
    angle = 360 / sides  # Exterior angle of polygon
    for _ in range(sides):
        draw_pattern(t, length, depth)
        t.right(angle)

# -----------------------------
# Main program
# -----------------------------
def main():
    # Get user input
    sides = int(input("Enter the number of sides: "))
    length = float(input("Enter the side length: "))
    depth = int(input("Enter the recursion depth: "))

    # Setup turtle
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)  # Fastest speed
    t.penup()
    t.goto(-length/2, length/2)  # Start at top-left for better centering
    t.pendown()

    # Draw the polygon with recursive patterns
    draw_polygon(t, sides, length, depth)

    # Finish
    t.hideturtle()
    screen.mainloop()

# Run the program
if __name__ == "__main__":
    main()
