# import the modules
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import threading
import asyncio
import os
from bleak import BleakClient, BleakScanner

#initialize global data
data = ""
prev_data=""


ADDRESS = "84:FC:E6:00:B7:66"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def main():
    global data
    client = None  # Initialize the client variable outside the try block
    device = await BleakScanner.find_device_by_address(ADDRESS)
    if device is None:
        print("could not find device with address ", ADDRESS)
        return
    else:
        print("Device Foundwith address ",ADDRESS)
    try:
        client = BleakClient(ADDRESS)
        # paired = await client.pair()
        # print(f"Paired: {paired}")
        await client.connect()
        print(f"Connected: {client.is_connected}")
        while True:
            data_bytes = await client.read_gatt_char(CHARACTERISTIC_UUID)
            data = bytearray.decode(data_bytes)
            # print(data, "BLE")
            # await asyncio.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        await client.disconnect()
        unpaired = await client.unpair()
        print(f"UnPaired: {unpaired}")
    finally:
        if client and client.is_connected:
            disconnect = await client.disconnect()
            print(f"disconnected: {disconnect}")
            unpaired = await client.unpair()
            print(f"UnPaired: {unpaired}")

class ImageProcessorApp:
    def __init__(self , master):
        self.master = master
        self.master.title("Image Processor")

        # Initialize variables
        self.image_list = []
        self.current_image_index = 0

        # Create GUI components
        self.label = tk.Label(self.master)
        self.label.pack(expand=True, fill="both")

        self.zoom_in_button = tk.Button(self.master, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side="left")

        self.zoom_out_button = tk.Button(self.master, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side="left")

        self.next_button = tk.Button(self.master, text="Next", command=self.next_image)
        self.next_button.pack(side="left")

        self.prev_button = tk.Button(self.master, text="Previous", command=self.prev_image)
        self.prev_button.pack(side="left")

        self.rotate_left_button = tk.Button(self.master, text="Rotate Left", command=self.rotate_left)
        self.rotate_left_button.pack(side="left")

        self.rotate_right_button = tk.Button(self.master, text="Rotate Right", command=self.rotate_right)
        self.rotate_right_button.pack(side="left")

        self.load_image_button = tk.Button(self.master, text="Load Image", command=self.load_image)
        self.load_image_button.pack(side="left")
        
        self.monitor_condition()

    def monitor_condition(self):
        # Check the condition here
        global data,prev_data
        if data != prev_data:
            print(data)
            if data == "Rotate_Left":
                self.rotate_left()
            elif data == "Rotate_Right":
                self.rotate_right()
            elif data == "Swipe_Right":
                self.next_image()
            elif data == "Swipe_Left":
                self.prev_image()
            elif data == "Grab":
                self.zoom_in()
            elif data == "Pinch":
                self.zoom_out()
            prev_data=data
        
        # Schedule the method to run again after a certain time (in milliseconds)
        self.master.after(1, self.monitor_condition)

    def load_image(self):
        # get the path/directory
        dir_path = filedialog.askdirectory()
        # file_path = filedialog.askopenfilename(filetypes=[("Image files", "*")])
        for images in os.listdir(dir_path):
 
            # check if the image ends with png
            if (images.endswith(".jpg")):
                # print(os.path.join(dir_path,images))
                image_path = os.path.join(dir_path,images)
                
                print("Selected file:", image_path)  # Print the selected file path for debugging
                try:
                    image = cv2.imread(image_path)
                    if image is not None:
                        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        self.image_list.append(image_rgb)
                        self.current_image_index = len(self.image_list) - 1
                        self.update_display()
                    else:
                        print("Error: Unable to read the image.")
                except Exception as e:
                    print("Error loading image:", str(e))

    def update_display(self):
        if self.image_list and 0 <= self.current_image_index < len(self.image_list):
            current_image = self.image_list[self.current_image_index]
            image = Image.fromarray(current_image)
            photo = ImageTk.PhotoImage(image)
            self.label.config(image=photo)
            self.label.image = photo

    def zoom_in(self):
        if self.image_list:
            current_image = self.image_list[self.current_image_index]
            zoomed_image = cv2.resize(current_image, (int(current_image.shape[1] * 1.2), int(current_image.shape[0] * 1.2)))
            self.image_list[self.current_image_index] = zoomed_image
            self.update_display()

    def zoom_out(self):
        if self.image_list:
            current_image = self.image_list[self.current_image_index]
            zoomed_image = cv2.resize(current_image, (int(current_image.shape[1] / 1.2), int(current_image.shape[0] / 1.2)))
            self.image_list[self.current_image_index] = zoomed_image
            self.update_display()

    def next_image(self):
        if self.image_list:
            if self.current_image_index < len(self.image_list) - 1:
                self.current_image_index += 1
                self.update_display()

    def prev_image(self):
        if self.image_list:
            if self.current_image_index > 0:
                self.current_image_index -= 1
                self.update_display()

    def rotate_left(self):
        if self.image_list:
            current_image = self.image_list[self.current_image_index]
            rotated_image = cv2.rotate(current_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.image_list[self.current_image_index] = rotated_image
            self.update_display()

    def rotate_right(self):
        if self.image_list:
            current_image = self.image_list[self.current_image_index]
            rotated_image = cv2.rotate(current_image, cv2.ROTATE_90_CLOCKWISE)
            self.image_list[self.current_image_index] = rotated_image
            self.update_display()


def Application():
    global data
    data = ""
    root = tk.Tk()
    app = ImageProcessorApp(root)


    root.mainloop()

def ble_Device():
    asyncio.run(main())

#multi Threading
Ble_device = threading.Thread(target=ble_Device)
application = threading.Thread(target=Application)

Ble_device.start()
application.start()


