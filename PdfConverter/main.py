from tkinter import *
from tkinter import filedialog
from PIL import Image
from pdf2image import convert_from_path
import os

background = "#F3F0EC"
text_font = "#383E45"

def ob_enter(e):
    open_button['background'] = 'black'

def ob_leave(e):
    open_button['background'] = 'red'

def tpop_enter(e):
    to_png_or_pdf_button['background'] = 'black'

def tpop_leave(e):
    to_png_or_pdf_button['background'] = 'red'

def cb_enter(e):
    convert_button['background'] = 'black'

def cb_leave(e):
    convert_button['background'] = 'red'

# Switch function convert to png or pdf
def to_png_or_pdf():
    global test
    global selected_image_path

    # If switch button clicked, forget file selection
    message_label.place_forget()
    selected_image_path = None

    if test == 0:
        to_png_or_pdf_button.config(text="Pdf to Png")
        open_button["command"] = open_pdf
        convert_button["command"] = convert_to_png
        convert_button.config(text="Convert to Png")
        test = 1
    elif test == 1:
        to_png_or_pdf_button.config(text="Png to Pdf")
        open_button["command"] = open_image
        convert_button["command"] = convert_to_pdf
        convert_button.config(text="Convert to PDF")
        test = 0

    return test

# Function to open an Image in pdf/jpg/jpeg
def open_image():
    global convert_button_placed
    global filename

    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    if image_path:
        global selected_image_path
        selected_image_path = image_path

        filename = os.path.basename(image_path)

        to_png_or_pdf_button.config(font=("Arial", 23))
        to_png_or_pdf_button.place(relx=0.88, rely=0.9, anchor=CENTER, width=180, height=50)
        message_label.config(text="Selected image : /{}".format(filename), fg=text_font, font=("Arial", 20))
        open_button.place(relx=0.5, rely=0.4, anchor=CENTER, width=300, height=60)
        message_label.place(relx=0.5, rely=0.5, anchor=CENTER, width=1080, height=40)
        convert_button.config(text="Convert to Pdf")
        convert_button.place(relx=0.5, rely=0.63, anchor=CENTER, width=700, height=100)
        convert_button_placed = True

# Function to open a PDF
def open_pdf():
    global convert_button_placed
    global filename

    pdf_path = filedialog.askopenfilename(filetypes=[("Pdf Files", "*.pdf")])

    if pdf_path:
        global selected_image_path
        selected_image_path = pdf_path

        filename = os.path.basename(pdf_path)

        to_png_or_pdf_button.config(font=("Arial", 23))
        to_png_or_pdf_button.place(relx=0.88, rely=0.9, anchor=CENTER, width=180, height=50)
        message_label.config(text="Selected pdf : /{}".format(filename), fg=text_font, font=("Arial", 20))
        open_button.place(relx=0.5, rely=0.4, anchor=CENTER, width=300, height=60)
        message_label.place(relx=0.5, rely=0.5, anchor=CENTER, width=1080, height=40)
        convert_button.config(text="Convert to Png")
        convert_button.place(relx=0.5, rely=0.63, anchor=CENTER, width=700, height=100)
        convert_button_placed = True

# Function to convert an image to a PDF
def convert_to_pdf(*args):
    global pdf_title

    if not convert_button_placed:
        return
    
    if not selected_image_path:
        message_label.config(text="Select an image !", fg="red")
        message_label.place(relx=0.5, rely=0.5, anchor=CENTER, width=1080, height=40)
        return

    image = Image.open(selected_image_path)
    rgb_image = image.convert('RGB')

    pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], initialfile=os.path.splitext(os.path.basename(filename))[0])
    if not pdf_path:
        return
    rgb_image.save(pdf_path)

    message_label.config(text="Conversion success !", fg="green", font=("Arial", 40))
    message_label.place(relx=0.5, rely=0.6, anchor=CENTER, width=1080, height=40)
    convert_button.place_forget()

# Function to convert a PDF to an image
def convert_to_png(*args):
    global pdf_title

    if not convert_button_placed:
        return

    if not selected_image_path:
        message_label.config(text="Select a PDF !", fg="red")
        message_label.place(relx=0.5, rely=0.5, anchor=CENTER, width=1080, height=40)
        return

    images = convert_from_path(selected_image_path, dpi=200, poppler_path=r'poppler-0.68.0\bin')

    for i, image in enumerate(images):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg")], initialfile=os.path.splitext(os.path.basename(filename))[0])
        if not file_path:
            return

        file_name = os.path.basename(file_path)
        file_name_without_ext, file_ext = os.path.splitext(file_name)

        if len(images) > 1:
            file_name_without_ext = f"{file_name_without_ext}_{i}"

        if not file_ext:
            file_ext = ".png"

        output_path = os.path.join(os.path.dirname(file_path), file_name_without_ext + file_ext)
        image.save(output_path, "PNG")

    message_label.config(text="Conversion success!", fg="green", font=("Arial", 30))
    convert_button.place_forget()

# Initialisation of Tkinter
root = Tk()
root.title("PDF Converter")
root.geometry("1080x720")
root.resizable(False, False)
root.config(bg=background)

# Creation title in root
title = Label(root, text="PDF CONVERTER", bg=background, fg=text_font, font=("Arial", 50, "bold"))
title.place(relx=0.5, y=100, anchor=CENTER, width=570, height=60)

test = 0

# Creation switch button
to_png_or_pdf_button = Button(root, text="Png to Pdf", command=to_png_or_pdf, bg="red", fg="white", font=("Arial", 30))
to_png_or_pdf_button.place(relx=0.5, rely=0.4, anchor=CENTER, width=250, height=60)
to_png_or_pdf_button.bind("<Enter>", tpop_enter)
to_png_or_pdf_button.bind("<Leave>", tpop_leave)

# Creation open file button
open_button = Button(root, text="Open image", command=open_image, bg="red", fg="white", font=("Arial", 30))
open_button.place(relx=0.5, rely=0.55, anchor=CENTER, width=500, height=80)
open_button.bind("<Enter>", ob_enter)
open_button.bind("<Leave>", ob_leave)

# Creation label for informations texts
message_label = Label(root, text="", bg=background, fg=text_font, font=("Arial", 20))

# Creation convert button
convert_button_placed = False
convert_button = Button(root, text="", command=convert_to_pdf, bg="red", fg="white", font=("Arial", 40))
convert_button.bind("<Enter>", cb_enter)
convert_button.bind("<Leave>", cb_leave)

selected_image_path = None

# Function to leave when escape key pressed
def on_escape(event):
    root.destroy()

root.bind('<Escape>', on_escape)
root.bind('<Return>', convert_to_pdf)

root.mainloop()
