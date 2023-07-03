import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from PyPDF2 import PdfReader
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pdf2image import convert_from_path
import os
import random
import numpy as np

np.random.seed(42)

def snspd_image():
    folder_path = './data/snspd'
    image_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            image_files.append(os.path.join(folder_path, filename))

    if image_files:
        random_image_path = random.choice(image_files)
        return random_image_path
    else:
        return None

def snspd_output():
    folder_path = './data/output'
    image_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            image_files.append(os.path.join(folder_path, filename))

    if image_files:
        random_image_path = random.choice(image_files)
        return random_image_path
    else:
        return None

def snspd_data():
    # Generate random peaks
    num_peaks = np.random.randint(2, 5)  # Randomly select the number of peaks
    peak_centers = np.random.uniform(1200, 1800, size=num_peaks)  # Randomly select the peak centers
    peak_amplitudes = np.random.randint(100, 500, size=num_peaks)  # Randomly select the peak amplitudes

    # Generate the x values (wavelength)
    x = np.linspace(1000, 2000, 300)

    # Generate the y values (number of photons) with added noise
    y = np.zeros_like(x)
    for center, amplitude in zip(peak_centers, peak_amplitudes):
        y += amplitude * np.exp(-(x - center)**2 / 100**2)  # Gaussian distribution with a standard deviation of 100

    # Add random noise to the y-values
    noise = np.random.normal(0, 30, size=len(y))  # Adjust the standard deviation (50) to control the noise level
    y += noise

    return x, y


# Initialize tkinter
root = tk.Tk()

# Store references to the plot, image, and PDF windows
plot_window = None
image_window = None
output_window = None
pdf_window = None

# Store references to the image and PDF PhotoImage objects
image_photo = None
output_photo = None
pdf_photo = None

def display_plot(x, y):
    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('No of Photons')
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
    image_path = snspd_image()
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

def display_output():
    # Display an output image in the tkinter window
    output_path = snspd_output()
    output_image = Image.open(output_path)
    output_image = output_image.resize((850, 1100))  # Resize the image to fit the window

    global output_photo, output_window

    # Close the previous output window if it exists
    if output_window is not None:
        output_window.destroy()

    # Create a new output window
    output_window = tk.Toplevel(root)
    output_window.title('Output Display')

    # Create a PhotoImage object and keep a reference to it
    output_photo = ImageTk.PhotoImage(output_image)

    output_label = tk.Label(output_window, image=output_photo)
    output_label.pack()

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


# Call the functions to initialize the windows
x, y = snspd_data()
display_plot(x, y)
display_image()
display_output()

def key_pressed(event):
    if event.keysym == 'space':
        # Call the functions to regenerate the data
        x, y = snspd_data()

        # Update the plot
        if plot_window is not None:
            display_plot(x, y)

        # Update the image
        if image_window is not None:
            display_image()

        # Update the output
        if output_window is not None:
            display_output()

    elif event.keysym == 'Escape':
        root.quit()

# Bind the key press event to the root window
root.bind('<KeyPress>', key_pressed)

# Start the tkinter event loop
root.mainloop()