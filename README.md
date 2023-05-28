# 2D-Pygame-Renderer-for-Moderngl
Renders 2D elements using the Pygame library

This is a simple script that converts a pygame surface to a moderngl texture and renders it to the screen. 
This script works with a 3D context with little to no issues. Just make sure you disable depth testing before rendering.
I would recommend creating a new method (something like "pg_render") where you do all of your drawing onto the surface and convert at the end.
Make sure to call the destroy method upon closing the application as moderngl doesn't have garbage collection!

Thank you!
