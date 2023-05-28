import pygame
import moderngl as gl
import numpy as np

class PG2D:
    def __init__(self, ctx, WINSIZE) -> None:
        self.ctx = ctx
        self.surface = pygame.Surface(WINSIZE, flags=pygame.SRCALPHA)

        self.pg_texture = self.ctx.texture(WINSIZE, 4)
        self.pg_texture.filter = gl.NEAREST, gl.NEAREST
        self.pg_texture.swizzle = 'BGRA'

        self.texture_program = self.ctx.program(
            vertex_shader="""
                #version 330

                in vec2 in_vert;
                in vec2 in_texcoord;
                out vec2 uv;

                void main() {

                    uv = in_texcoord;

                    gl_Position = vec4(in_vert, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330

                uniform sampler2D surface;

                out vec4 f_color;

                in vec2 uv;

                void main() {
                    f_color = texture(surface, uv);
                }
            """,
        )
        self.texture_program['surface'] = 0

        # vbo
        self.buffer = self.ctx.buffer(
            data=np.array([
                -1.0, 1.0, 0.0, 1.0,  # upper left
                -1.0, -1.0, 0.0, 0.0,  # lower left
                1.0, 1.0, 1.0, 1.0,  # upper right
                1.0, -1.0, 1.0, 0.0,  # lower right
            ], dtype='f4')
        )
        # vao
        self.quad = self.ctx.vertex_array(
            self.texture_program,
            [
                (
                    self.buffer,
                    "2f 2f",
                    "in_vert", "in_texcoord",
                )
            ],
        )
    def clear(self, color: tuple =(0,0,0,0)):
        self.surface.fill(color)
    def to_gl_texture(self):
        self.surface = pygame.transform.flip(self.surface, flip_x=False, flip_y=True)
        texture_data = self.surface.get_view('1')
        self.pg_texture.write(texture_data)
    def render(self):
        self.ctx.enable(gl.BLEND)
        self.pg_texture.use(location=0)
        self.quad.render(mode=gl.TRIANGLE_STRIP)
        self.ctx.disable(gl.BLEND)
    def destroy(self):
        self.quad.release()
        self.buffer.release()
        self.texture_program.release()
        self.pg_texture.release()
