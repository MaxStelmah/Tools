import sys
import os
import pyautogui
from PIL import Image, ImageDraw, ImageFilter, ImageTk, ImageFont
import cv2
import numpy as np
import tkinter as tk
from tkinter import colorchooser, simpledialog
from datetime import datetime
import math

def take_screenshot():
    return pyautogui.screenshot()

def draw_arrow(image, start, end, color=(255, 0, 0), width=5):
    draw = ImageDraw.Draw(image)
    arrow_length, arrow_width = 20, 10
    total_length = math.hypot(end[0] - start[0], end[1] - start[1])
    
    if total_length:
        line_end_length = total_length - arrow_length + (width / 2)
        new_end = (
            start[0] + line_end_length * (end[0] - start[0]) / total_length,
            start[1] + line_end_length * (end[1] - start[1]) / total_length
        )
        
        draw.line([start, new_end], fill=color, width=width)
        
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        arrow_tip = end
        arrow_left = (end[0] - arrow_length * math.cos(angle - math.pi / 6),
                      end[1] - arrow_length * math.sin(angle - math.pi / 6))
        arrow_right = (end[0] - arrow_length * math.cos(angle + math.pi / 6),
                       end[1] - arrow_length * math.sin(angle + math.pi / 6))
        draw.polygon([arrow_tip, arrow_left, arrow_right], fill=color)
    
    return image

def draw_rectangle(image, top_left, bottom_right, color=(255, 0, 0), width=5):
    draw = ImageDraw.Draw(image)
    draw.rectangle([top_left, bottom_right], outline=color, width=width)
    return image

def draw_bar(image, top_left, bottom_right, color=(255, 0, 0)):
    draw = ImageDraw.Draw(image)
    draw.rectangle([top_left, bottom_right], fill=color)
    return image

def draw_text(image, position, text, color=(255, 0, 0), font_size=20):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", font_size)
    draw.text(position, text, fill=color, font=font)
    return image

def draw_dashed_rectangle(draw, top_left, bottom_right, color=(255, 0, 0), width=2, dash=(5, 5)):
    x1, y1 = top_left
    x2, y2 = bottom_right
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    for i in range(x1, x2, dash[0] + dash[1]):
        draw.line([(i, y1), (i + dash[0], y1)], fill=color, width=width)
        draw.line([(i, y2), (i + dash[0], y2)], fill=color, width=width)
    for i in range(y1, y2, dash[0] + dash[1]):
        draw.line([(x1, i), (x1, i + dash[0])], fill=color, width=width)
        draw.line([(x2, i), (x2, i + dash[0])], fill=color, width=width)

def blur_area(image, top_left, bottom_right):
    x1, y1 = min(top_left[0], bottom_right[0]), min(top_left[1], bottom_right[1])
    x2, y2 = max(top_left[0], bottom_right[0]), max(top_left[1], bottom_right[1])
    image_np = np.array(image)
    roi = image_np[y1:y2, x1:x2]
    roi = cv2.GaussianBlur(roi, (21, 21), 0)
    image_np[y1:y2, x1:x2] = roi
    return Image.fromarray(image_np)

def save_image(image, save_folder):
    os.makedirs(save_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    save_path = os.path.join(save_folder, filename)
    image.save(save_path)
    print(f"Screenshot saved to {save_path}")

class ScreenshotEditor:
    def __init__(self, root, save_folder, window_title):
        self.root = root
        self.save_folder = save_folder
        self.gui_folder = os.path.join(os.path.dirname(__file__), "gui")
        self.root.title(window_title)
        self.current_tool = 'arrow'
        self.current_color = (255, 0, 0)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_toolbar()
        self.image = take_screenshot()
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.main_frame, width=self.photo.width(), height=self.photo.height())
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_image = self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.start_x = self.start_y = None
        self.history = [self.image.copy()]
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind('<Control-z>', lambda event: self.undo())
        self.root.bind('<Return>', lambda event: self.save_and_exit())

    def load_icon(self, icon_name, size=(24, 24)):
        icon_path = os.path.join(self.gui_folder, f"{icon_name}.png")
        if os.path.exists(icon_path):
            icon = Image.open(icon_path)
            icon = icon.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(icon)
        return None

    def create_toolbar(self):
        toolbar = tk.Frame(self.main_frame, bg='lightgrey')
        toolbar.pack(side=tk.TOP, fill=tk.X)
        icon_size = (32, 32)
        icons = {
            "arrow": (self.set_arrow_tool, "Draw Arrow"),
            "rectangle": (self.set_rectangle_tool, "Draw Rectangle"),
            "blur": (self.set_blur_tool, "Blur Area"),
            "color": (self.change_color, "Change Color"),
            "bar": (self.set_bar_tool, "Draw Bar"),
            "text": (self.set_text_tool, "Draw Text"),
            "cut": (self.set_cut_tool, "Cut Image"),
            "save": (self.save_image, "Save"),
            "undo": (self.undo, "Undo"),
            "exit": (self.root.quit, "Exit")
        }
        self.buttons = {}
        for icon_name, (command, tooltip) in icons.items():
            icon = self.load_icon(icon_name, icon_size)
            button = tk.Button(toolbar, image=icon, command=command, relief=tk.RAISED) if icon else tk.Button(toolbar, text=icon_name, command=command, relief=tk.RAISED)
            button.image = icon
            button.pack(side=tk.LEFT, padx=2, pady=2)
            button.bind("<Enter>", lambda event, tooltip=tooltip: self.show_tooltip(event, tooltip))
            button.bind("<Leave>", self.hide_tooltip)
            self.buttons[icon_name] = button
        self.tooltip = tk.Label(self.root, text="", relief=tk.SOLID, borderwidth=1)
        self.tooltip.pack_forget()

    def show_tooltip(self, event, text):
        x = event.widget.winfo_rootx() + event.widget.winfo_width() // 2
        y = event.widget.winfo_rooty() + event.widget.winfo_height()
        self.tooltip.configure(text=text)
        self.tooltip.place(x=x, y=y, anchor="n")

    def hide_tooltip(self, event):
        self.tooltip.place_forget()

    def set_tool(self, tool):
        self.current_tool = tool
        self.update_button_states()

    def set_arrow_tool(self): self.set_tool('arrow')
    def set_rectangle_tool(self): self.set_tool('rectangle')
    def set_blur_tool(self): self.set_tool('blur')
    def set_bar_tool(self): self.set_tool('bar')
    def set_text_tool(self): self.set_tool('text')
    def set_cut_tool(self): self.set_tool('cut')

    def change_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code[0]:
            self.current_color = tuple(int(c) for c in color_code[0])

    def update_button_states(self):
        for tool, button in self.buttons.items():
            button.config(relief=tk.SUNKEN if self.current_tool == tool else tk.RAISED)

    def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.preview_image = self.image.copy()

    def on_move_press(self, event):
        if self.start_x is not None and self.start_y is not None:
            preview = self.preview_image.copy()
            end_x, end_y = event.x, event.y
            if self.current_tool == 'arrow':
                preview = draw_arrow(preview, (self.start_x, self.start_y), (end_x, end_y), self.current_color)
            elif self.current_tool == 'rectangle':
                preview = draw_rectangle(preview, (self.start_x, self.start_y), (end_x, end_y), self.current_color)
            elif self.current_tool == 'bar':
                preview = draw_bar(preview, (self.start_x, self.start_y), (end_x, end_y), self.current_color)
            elif self.current_tool in ['blur', 'cut']:
                draw = ImageDraw.Draw(preview)
                draw_dashed_rectangle(draw, (self.start_x, self.start_y), (end_x, end_y), self.current_color)
            self.update_canvas(preview)

    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        if self.current_tool == 'arrow':
            self.image = draw_arrow(self.image, (self.start_x, self.start_y), (end_x, end_y), self.current_color)
        elif self.current_tool == 'rectangle':
            self.image = draw_rectangle(self.image, (self.start_x, self.start_y), (end_x, end_y), self.current_color)
        elif self.current_tool == 'bar':
            self.image = draw_bar(self.image, (self.start_x, self.start_y), (end_x, end_y), self.current_color)
        elif self.current_tool == 'blur':
            self.image = blur_area(self.image, (self.start_x, self.start_y), (end_x, end_y))
        elif self.current_tool == 'text':
            text = simpledialog.askstring("Input", "Enter text:")
            if text:
                self.image = draw_text(self.image, (self.start_x, self.start_y), text, self.current_color)
        elif self.current_tool == 'cut':
            self.image = self.image.crop((self.start_x, self.start_y, end_x, end_y))
        self.history.append(self.image.copy())
        self.update_canvas(self.image)
        self.start_x = self.start_y = None

    def update_canvas(self, image):
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(self.canvas_image, image=self.photo)

    def save_image(self):
        save_image(self.image, self.save_folder)

    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
            self.image = self.history[-1].copy()
            self.update_canvas(self.image)

    def save_and_exit(self):
        self.save_image()
        self.root.quit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Screenshot Editor")
    parser.add_argument("save_folder", help="Folder to save screenshots")
    parser.add_argument("--title", help="Title of the application window", default="Screenshot Editor")
    args = parser.parse_args()
    root = tk.Tk()
    app = ScreenshotEditor(root, args.save_folder, args.title)
    root.mainloop()