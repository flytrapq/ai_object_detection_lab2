import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import requests
import io
import shutil

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.upload = tk.Button(self)
        self.upload["text"] = "Upload Image"
        self.upload["command"] = self.upload_image
        self.upload.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def upload_image(self):
        filepath = filedialog.askopenfilename()
        self.send_request(filepath)

    def send_request(self, filepath):
        token = "rest_api_token"
        project_id = "project_id"
        model = "model_name"
        headers = {"X-Auth-token": token, "Content-Type": "application/octet-stream"}

        with open(filepath, 'rb') as handle:
            r = requests.post('https://platform.sentisight.ai/api/predict/{}/{}/'.format(project_id,model), headers=headers, data=handle)
    
        if r.status_code == 200:
            print('Response from REST API:')
            response = r.json()
            print(response)  # Print the JSON response
            self.display_image(filepath, response)
        else:
            print('Error occurred with REST API.')
            print('Status code: {}'.format(r.status_code))
            print('Error message: ' + r.text)

    def display_image(self, filepath, response):
        image = Image.open(filepath)
        draw = ImageDraw.Draw(image)
        for obj in response:
            x0, y0, x1, y1 = obj['x0'], obj['y0'], obj['x1'], obj['y1']
            label = obj['label']
            draw.rectangle(((x0, y0), (x1, y1)), outline="red", width=5)
            draw.text((x0, y0 - 10), label, fill="black")
        image.save("output.png")
        photo = ImageTk.PhotoImage(image)
        new_window = tk.Toplevel(self)
        label = tk.Label(new_window, image=photo)
        label.image = photo
        label.pack()


root = tk.Tk()
app = Application(master=root)
app.mainloop()
