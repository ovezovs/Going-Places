######################################################################
# Author: Shageldi Ovezov
# Username: ovezovs
#
# Assignment: P01: Oh, The Places You'll Go!
#
# Purpose:  To create a map of locations
#           where the user is originally from or has visited,
#           and to use tuples and lists correctly.
######################################################################
# Acknowledgements:
#
# Original Authors: Dr. Scott Heggen and Dr. Jan Pearce

# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

# importing all necessary libraries
import turtle
import reverse_geocoder as rg
import cv2
import time
import datetime
import imageio
import PIL
import PIL.Image

from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox


def parse_file(filename):
    """
    Iterates through the file, and creates the list of places

    :param filename: the name of the file to be opened
    :return: a list representing multiple places
    """

    file_content = open(filename, 'r')           # Opens file for reading

    str_num = file_content.readline()           # The first line of the file, which is the number of entries in the file
    str_num = int(str_num[:-1])                 # The '/n' character needs to be removed

    places_list = []
    for i in range(str_num):
        places_list.append(extract_place(file_content))         # Assembles the list of places

    file_content.close()
    return places_list


def extract_place(file_content):
    """
    This function extracts five lines out of file_content,
    which is a variable holding all of the file content from the calling function. Each extracted line represents,
    in order, the place's name, location, latitude, longitude, and user color. The function returns the five elements
    to the function call as a tuple.

    :param file_content: contents of the file which represents all places
    :return: a tuple representing a single place.
    """

    # creating a tuple of variables and assigning values from another tuple:
    (name, location, latitude, longitude, user_color) = (file_content.readline().strip("\n"), \
 file_content.readline().strip("\n"), file_content.readline().strip("\n"), file_content.readline().strip("\n"), \
 file_content.readline().strip("\n"))

    place_tuple = (name, location, float(latitude), float(longitude), user_color)
    return place_tuple


class Place:
    """Places pins on the world map that represent places"""
    def __init__(self, name="", y=0, x=0, color="", location=None):
        """setting attributes for an object of the class"""
        self.name = name
        self.location = location
        self.x = x
        self.y = y
        self.color = color
        self.long = self.x_to_longitude(self.x)
        self.lat = self.y_to_latitude(self.y)
        self.shape = "arrow"


    def x_to_longitude(self, x):
        """converts value of x coordinate to longitude
        :param x: x value of the clicked place
        :return: returns longitude value
        """
        longitude = (2*x*120)/wn.window_height()
        return longitude

    def y_to_latitude(self, y):
        """converts value of y coordinate to latitude
        :return: returns latitude value
        """
        latitude = (2 * y * 195) / wn.window_width()
        return latitude

    def create_pin(self):
        """creates pins on the specified/clicked locations on the world map"""

        # setting up a turtle and its attributes:
        self.sha = turtle.Turtle()
        self.sha.speed(0)
        self.sha.color("red")        # default color
        self.sha.shape(self.shape)
        if self.shape == "arrow":    # default turtle shape
            self.sha.right(90)
        self.sha.shapesize(1)

        # moving turtle to a specified location and placing a pin
        self.sha.penup()
        self.sha.goto(self.x, self.y)
        self.sha.stamp()

        # labeling and coloring the pin
        self.sha.color(self.color)
        self.sha.pencolor(self.color)
        label = self.name + "'s place:\n      " + self.location
        self.sha.write(label, font=("Arial", 8, "bold"))

    def __str__(self):
        """enables to print a Place object as a string
        :return: returns a string with placeholders for the object's attributes
        """

        return """\nInformation about you and your chosen place:\n
    Your name: {0}\n    Location: {1}\n    Latitude and Longitude: {2},   {3}
    Chosen color: {4}""".format(self.name, self.location, self.lat, self.long, self.color)

    def coords_to_address(self):
        """finds the address for the user-clicked x, y coordinate
        :return: address in a "city, state, country" format
        """

        coords = (self.lat, self.long)

        result = rg.search(coords)   # reverse_geocode library for finding a location based on latitude and longitude
        str_result = str(result[0])
        str_result1 = str_result[13:(len(str_result)) - 2]

        # a set of list and string operations for extracting only city, state, and country information from
        # the result of the reverse geocoding:
        string_result2 = ""
        punctuation = "(), "
        for i in str_result1:
            if i not in punctuation:
                string_result2 += i
        list_address = string_result2.split("'")
        for j in list_address:
            if j == "":
                list_address.remove(j)

        # Location in the following format: City, State, Country
        location = "{0}, {1}, {2}".format(list_address[5], list_address[7], list_address[-1])

        return location

    def MyTkinter(self):
        """creates tkinter window for the users to input their information"""

        # setting up a Tkinter window
        self.root = Tk()
        self.root.geometry("350x300")
        self.root.title("User Information")  # Sets root window title
        heading = Label(self.root, text="""Please fill out the following spaces!\nIf you would like your 
        picture to be in place of a default pin, click the "Take a selfie" button\nAfter, click save.""", bg="blue",
                        fg="white", width="350", height="2")   # creating a heading for the window
        heading.pack()

        name_label = Label(self.root, text="Enter your name *", fg="green")  # Asking users to input their name
        color_label = Label(self.root, text="Choose a color for your pin *", fg="green")   # Asking user's to
                                                                                           # choose a color

        name_label.place(x=20, y=60)
        color_label.place(x=20, y=115)

        self.name_entry = Entry(self.root)        # textbox for user name entry
        self.color_entry = Combobox(self.root)    # combobox for the user to choose a color
        self.color_entry['values'] = ("Red", "Green", "Blue", "Orange", "Purple", "Pink", "White", "Black", "Yellow")
        self.color_entry.current(1)

        self.name_entry.place(x=20, y=85)
        self.color_entry.place(x=20, y=140)

        selfie_button = Button(self.root, text="Take a selfie", command=lambda: self.capture_user_image(), fg="black")
        selfie_button.place(x=20, y=175)     # a button that calls a function to capture user's image

        submit_button = Button(self.root, text="Save", command=lambda: self.save_info(), bg="yellow", fg="black",
                               width="35", height="1")
        submit_button.place(x=20, y=220)     # a button to save the all user information

        self.root.mainloop()

    def save_info(self):
        """First, saves the information retrieved from the Tkinter window. After, quits the Tkinter
        application"""

        self.name = self.name_entry.get()    # get user's name from Tk textbox
        self.color = self.color_entry.get()  # get the chosen color from combobox

        self.root.quit()
        self.root.destroy()   # exiting Tkinter app

    def capture_user_image(self):
        """triggers a web camera, takes a picture, and saves it as a turtle's shape
        :return: None
        """
        # taking a picture with web camera and saving it
        camera_port = 0  # index of camera
        camera = cv2.VideoCapture(camera_port)
        time.sleep(0.1)
        return_value, image = camera.read()
        cv2.imwrite("captures/opencv.png", image)  # saving the capture

        # reducing the size of the taken picture
        im = PIL.Image.open("captures/opencv.png")
        im1 = im.resize((30, 30))
        im1.save("captures/small_pic.png")

        # Converting the PNG image into GIF file
        open_image = [imageio.imread("captures/small_pic.png")]
        output_file = 'captures/user_turtle_shapes/Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
        imageio.mimsave(output_file, open_image, duration=0.2)   # saving GIF

        wn.addshape(output_file)   # adding the GIF file to the turtle screen
        self.shape = output_file   # setting the GIF as turtle shape


def handler(x, y):
    """handles the mouse click event and calls several functions to """

    user_obj = Place("", y, x, "")
    user_obj.MyTkinter()
    user_obj.location = user_obj.coords_to_address()  # return a string (text) with address

    print(str(user_obj))
    user_obj.create_pin()
    messagebox.showinfo("YOUR PIN IS READY!!!", str(user_obj))   # displays all information about user and location


def key_handle():
    """handles the 'q' key presses. When 'q' is pressed, terminates the turtle window"""
    wn.bye()

def main():
    """
    This program is designed to place pins on a world map.
    Each place is represented as a tuple.
    Each tuple is then added to a list.
    The list of tuples is used to populate the map.
    Uses mouse clicks to place a pin on a location desired by a user.

    :return: None
    """

    # A sample file was created for you to use here: places.txt
    in_file = input("Enter the name of your input file: ")
    global wn
    wn = turtle.Screen()
    wn.setup(width=1100, height=650, startx=0, starty=0)
    wn.bgpic("world-map.gif")
    wn.title("Oh, The Places You'll Go!")

    place_list = parse_file(in_file)        # Generates place_list from the file
    object_list = []    # empty list to save the Place objects

    # Creating a Place object for each place specified in places.txt file
    p1 = Place(place_list[0][0], (place_list[0][2] / 120) * wn.window_height() / 2,
               (place_list[0][3] / 195) * wn.window_width() / 2, place_list[0][4], place_list[0][1])
    object_list.append(p1)
    p2 = Place(place_list[1][0], (place_list[1][2] / 120) * wn.window_height() / 2,
               (place_list[1][3] / 195) * wn.window_width() / 2, place_list[1][4], place_list[1][1])
    object_list.append(p2)
    p3 = Place(place_list[2][0], (place_list[2][2] / 120) * wn.window_height() / 2,
               (place_list[2][3] / 195) * wn.window_width() / 2, place_list[2][4], place_list[2][1])
    object_list.append(p3)
    p4 = Place(place_list[3][0], (place_list[3][2] / 120) * wn.window_height() / 2,
               (place_list[3][3] / 195) * wn.window_width() / 2, place_list[3][4], place_list[3][1])
    object_list.append(p4)
    p5 = Place(place_list[4][0], (place_list[4][2] / 120) * wn.window_height() / 2,
               (place_list[4][3] / 195) * wn.window_width() / 2, place_list[4][4], place_list[4][1])
    object_list.append(p5)

    for objct in object_list:
        objct.create_pin()     # Placing pins for each Place object

    print("Map created with first 5 places!")

    wn.onclick(handler)         # passing x, y location to mouse click handler
    wn.onkey(key_handle, "q")   # terminates the program with a click on q key
    wn.listen()
    wn.mainloop()


if __name__ == "__main__":
    main()
