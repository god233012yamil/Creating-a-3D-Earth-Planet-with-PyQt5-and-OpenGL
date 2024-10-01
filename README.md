# Creating a 3D Earth Planet with PyQt5 and OpenGL
This Python script utilizes PyQt5 and OpenGL to render a textured rotating sphere within a GUI window. The core functionality is managed by the OpenGLWindow class, which handles OpenGL initialization, rendering, and updating of the scene. The class accepts two key parameters: texture_image for the texture applied to the sphere, and an optional bg_image for the background. Textures are loaded using the PIL library, ensuring proper formatting for OpenGL. The paintGL method is responsible for drawing the textured sphere and background on each frame, rotating the sphere continuously. The MainWindow class integrates the OpenGL widget into the PyQt5 GUI, while the main function sets up and runs the application. This modular design allows for flexible customization of the textures, enabling the use of different images dynamically.

## Step-by-step Guide on How this Code Works:

### Step 1: Import Necessary Libraries

The script begins by importing several essential libraries:

- PyQt5 (QApplication, QMainWindow, QOpenGLWidget) for creating the GUI.
- OpenGL (GL and GLU) for handling 3D rendering operations.
- PIL (Image) for loading and manipulating texture images.

### Step 2: Define the OpenGLWindow Class

The OpenGLWindow class is a custom QOpenGLWidget that contains the main logic for rendering a textured 3D sphere.

- __init__ method: Initializes the OpenGL widget, accepting a texture_image parameter for the sphere’s texture and an optional bg_image parameter for the background texture. It also sets up a timer to update the scene every 16 milliseconds (approximately 60 FPS).

### Step 3: OpenGL Initialization in initializeGL

The initializeGL method is called once when the OpenGL context is created. This method:

- Clears the background color to black.
- Enables depth testing to ensure 3D objects are rendered correctly.
- Enables texture mapping and loads both the sphere and background textures using the load_texture method, which reads the image file and converts it into an OpenGL-compatible texture.

### Step 4: Handling Resizing with resizeGL

The resizeGL method adjusts the OpenGL viewport size whenever the window is resized. This ensures the scene scales correctly based on the new window dimensions.

### Step 5: Rendering the Scene in paintGL

The paintGL method is responsible for rendering the actual scene:

1. Clears the color and depth buffers.
2. Resets the model-view matrix to prepare for new object transformations.
3. Draws the background by binding the background texture and rendering a textured quad.
4. Rotates the sphere around the Y-axis, applying the texture_image to it using gluSphere.
5. Increments the rotation angle for continuous movement.

### Step 6: Updating the Scene

The update_frame method triggers a repaint of the scene by calling update(), which will invoke paintGL. This method is tied to a timer to ensure the scene refreshes at a steady rate, producing smooth animation.

### Step 7: Loading Textures with load_texture

The load_texture method reads an image file using PIL, flips the image vertically (to match OpenGL’s coordinate system), and converts it into RGBA format. The resulting data is then sent to OpenGL to create and bind the texture.

### Step 8: Drawing the Textured Sphere

The draw_textured_sphere method creates a textured sphere using GLU’s gluSphere function. It binds the sphere’s texture before rendering, ensuring the correct image is applied.

### Step 9: Define the MainWindow Class

The MainWindow class extends QMainWindow and acts as a container for the OpenGL widget. It accepts the texture_image and optional bg_image parameters and initializes the OpenGLWindow widget inside the main window.

### Step 10: Running the Application

The main function initializes the PyQt5 application, creates an instance of MainWindow, and passes the paths to the sphere and background images. It then starts the application event loop using app.exec_(), which keeps the window open and interactive.

### Step 11: Customization and Execution

The if __name__ == "__main__": block defines the texture and background image paths and starts the application by calling main(). Users can modify these paths to apply different textures to the sphere or background.

### Code Output Image 

![image](https://github.com/user-attachments/assets/2e670f41-2409-4a5a-af4a-e901b04a6c68)

### License
This project is licensed under the GNU General Public License. See the LICENSE file for more information.
