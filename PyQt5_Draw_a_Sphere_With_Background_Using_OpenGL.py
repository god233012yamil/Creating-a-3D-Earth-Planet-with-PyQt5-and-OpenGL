import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


class OpenGLWindow(QOpenGLWidget):
    """
    A custom QOpenGLWidget class for rendering a rotating textured sphere using OpenGL.
    """

    def __init__(self, texture_image: str, background_image: str, parent: QMainWindow = None) -> None:
        """
        Initialize the OpenGLWindow with the parent widget.

        :param texture_image: Path to the texture image.
        :param parent: The parent widget, typically a QMainWindow.
        """
        super(OpenGLWindow, self).__init__(parent)
        self.angle = 0.0  # Angle for sphere rotation
        self.texture = None  # Texture ID for the sphere
        self.texture_image: str = texture_image  # texture image
        self.bg_texture: int = None  # Texture ID for the background
        self.background_image: str = background_image  # background image

        # Timer to update the frame every 16ms (~60 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(16)

    def initializeGL(self) -> None:
        """
        Set up the OpenGL environment. Called once before rendering starts.
        Initializes the background color, depth testing, and texture loading.
        """
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering
        glEnable(GL_TEXTURE_2D)  # Enable texture mapping
        self.texture = self.load_texture(self.texture_image)  # Load the texture image

        # Load the background image as a texture
        if len(self.background_image) > 0:
            self.bg_texture = self.load_texture(self.background_image)

    def resizeGL(self, w: int, h: int) -> None:
        """
        Handle resizing of the OpenGL viewport.

        :param w: The new width of the widget.
        :param h: The new height of the widget.
        """
        glViewport(0, 0, w, h)  # Set the viewport to cover the whole widget
        glMatrixMode(GL_PROJECTION)  # Set up the projection matrix
        glLoadIdentity()
        gluPerspective(45.0, w / h if h != 0 else 1.0, 0.1, 100.0)  # Set perspective projection
        glMatrixMode(GL_MODELVIEW)  # Switch back to the model view matrix

    def paintGL(self) -> None:
        """
        Render the scene. Called every time the widget needs to be repainted.
        Clears the screen and draws a rotating textured sphere.
        """
        # Clear screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  

        # Reset transformations
        glLoadIdentity()

        # Render the background
        if self.bg_texture is not None:
            self.render_background()

        # Move camera back to see the sphere
        # If you want to see the cube closer, then change camera position.
        # This line controls the camera's position.
        glTranslatef(0.0, 0.0, -4.5)

        # Rotate the sphere
        glRotatef(self.angle, 2.0, -1.0, -1.0)
        # glRotatef(self.angle, 1.0, 0.0, 0.0)  # Rotate the sphere around the X-axis
        # glRotatef(self.angle, 0.0, 1.0, 0.0)  # Rotate the sphere around the Y-axis
        # glRotatef(self.angle, 0.0, 0.0, 1.0)  # Rotate the sphere around the Z-axis

        # Apply scaling to increase the cube size
        glScalef(1.0, 1.0, 1.0)  # glScalef(2.0, 2.0, 2.0)

        # Draw the textured sphere
        # self.draw_textured_sphere(1.0, 32, 32)  # radius, slices, stacks
        self.draw_textured_sphere(1.5, 32, 32)  # radius, slices, stacks

    def render_background(self) -> None:
        """
        Draws a textured quad as the background using the background image.
        """
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.width(), 0, self.height())
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Bind the background texture
        glBindTexture(GL_TEXTURE_2D, self.bg_texture)

        # Draw a quad that covers the entire window
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.width(), 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.width(), self.height())
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0.0, self.height())
        glEnd()

        # Restore the previous projection and modelview matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glEnable(GL_DEPTH_TEST)

    def update_frame(self) -> None:
        """
        Update the rotation angle and repaint the widget.
        This is called periodically by the QTimer to animate the sphere.
        """
        self.angle += 0.5  # 1.0  # Increment rotation angle speed
        self.update()  # Request an update (repaint)

    def load_texture(self, image_file: str) -> int:
        """
        Load a texture from an image file using the Pillow library.

        :param image_file: The file path of the image to load as a texture.
        :return: The OpenGL texture ID.
        """
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Load the image using Pillow
        image = Image.open(image_file)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image vertically for OpenGL
        img_data = image.convert("RGBA").tobytes()

        # Create the texture
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        # Set texture parameters
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id

    def draw_textured_sphere(self, radius: float, slices: int, stacks: int) -> None:
        """
        Draw a textured sphere using gluSphere and apply a texture to it.

        :param radius: The radius of the sphere.
        :param slices: The number of vertical segments (longitude).
        :param stacks: The number of horizontal segments (latitude).
        """
        glBindTexture(GL_TEXTURE_2D, self.texture)  # Bind the texture

        # Create a new quadric object for the sphere
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)  # Enable texturing for the sphere
        gluSphere(quadric, radius, slices, stacks)  # Draw the sphere

        gluDeleteQuadric(quadric)  # Clean up the quadric object


class MainWindow(QMainWindow):
    """
    Main application window that contains the OpenGL widget.
    """

    def __init__(self) -> None:
        """
        Initialize the main window and set up the OpenGL widget.
        """
        super().__init__()
        self.setWindowTitle('OpenGL with PyQt5: Textured Sphere')
        self.setGeometry(100, 100, 800, 600)

        # Add the OpenGL widget to the window
        # Planet Earth Day Map without background
        self.opengl_widget = OpenGLWindow("8k_earth_daymap.jpg", "", self)
        # Planet Earth Day Map with a background
        # self.opengl_widget = OpenGLWindow("8k_earth_daymap.jpg", "night-sky-star-background.png", self)
        self.setCentralWidget(self.opengl_widget)


def main() -> None:
    """
    The main function to initialize and run the PyQt5 application.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
