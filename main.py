import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from PyPDF2 import PdfReader
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pdf2image import convert_from_path
import RPi.GPIO as GPIO

# GPIO pin number for the push button
BUTTON_PIN = 17

# Initialize tkinter
root = tk.Tk()

# Store references to the plot, image, and PDF windows
plot_window = None
image_window = None
pdf_window = None

# Store references to the image and PDF PhotoImage objects
image_photo = None
pdf_photo = None

def display_plot():
    # Generate some data for the plot
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Plot')

    global plot_window

    # Close the previous plot window if it exists
    if plot_window is not None:
        plot_window.destroy()

    # Create a new plot window
    plot_window = tk.Toplevel(root)
    plot_window.title('Plot Display')

    # Create a tkinter frame for the plot
    plot_frame = ttk.Frame(plot_window, width=400, height=300)
    plot_frame.pack()

    # Convert the plot to a tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def display_image():
    # Display an image in the tkinter window
    image_path = 'data/test.png'
    image = Image.open(image_path)
    image = image.resize((800, 600))  # Resize the image to fit the window

    global image_photo, image_window

    # Close the previous image window if it exists
    if image_window is not None:
        image_window.destroy()

    # Create a new image window
    image_window = tk.Toplevel(root)
    image_window.title('Image Display')

    # Create a PhotoImage object and keep a reference to it
    image_photo = ImageTk.PhotoImage(image)

    image_label = tk.Label(image_window, image=image_photo)
    image_label.pack()


def display_pdf():
    # Display a rendered PDF in the tkinter window
    pdf_path = 'data/test.pdf'
    start_page = 0  # Specify the starting page
    end_page = 1  # Specify the ending page (exclusive)

    pages = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)
    if pages:
        page_image = pages[0]
        page_image = page_image.resize((800, 600))  # Resize the rendered PDF to fit the window

        global pdf_photo, pdf_window

        # Close the previous PDF window if it exists
        if pdf_window is not None:
            pdf_window.destroy()

        # Create a new PDF window
        pdf_window = tk.Toplevel(root)
        pdf_window.title('PDF Display')

        # Create a PhotoImage object and keep a reference to it
        pdf_photo = ImageTk.PhotoImage(page_image)

        pdf_label = tk.Label(pdf_window, image=pdf_photo)
        pdf_label.pack()


# Callback function for button press event
def button_pressed(channel):
    # Call the functions to display the plot, image, and PDF
    display_plot()
    display_image()
    display_pdf()


# Configure GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Add event detection for button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=200)

# Start the tkinter event loop
root.mainloop()

# Clean up GPIO on program exit
GPIO.cleanup()
