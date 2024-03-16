import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# Глобальный список для хранения путей обработанных изображений
processed_images = []

def remove_metadata():
    global processed_images
    processed_images.clear()  # Очистка списка при каждом новом нажатии
    for image_path in selected_images:
        img = Image.open(image_path)
        data = img.getdata()
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(data)

        # Генерируем временное имя файла, не сохраняя его на диск
        processed_images.append((new_img, os.path.basename(image_path)))
    
    if processed_images:
        status_label.config(text=f"Metadata removed from {len(processed_images)} images. Ready to save.")
    else:
        status_label.config(text="No images selected or processed.")

def save_images():
    if not processed_images:
        messagebox.showinfo("No images to save", "Please, remove metadata from images first.")
        return

    # Папка для сохранения результатов
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        for img, name in processed_images:
            new_filename = os.path.join(folder_selected, f"cleaned_{name}")
            img.save(new_filename)
        messagebox.showinfo("Success", f"All images have been saved to {folder_selected}")
        status_label.config(text="Images saved successfully.")

def select_images():
    global selected_images
    file_types = [('Images', '*.jpeg *.jpg *.png')]
    selected_images = filedialog.askopenfilenames(title="Select Images", filetypes=file_types)
    if selected_images:
        status_label.config(text=f"{len(selected_images)} images selected. Ready to remove metadata.")

app = tk.Tk()
app.title("Metadata Remover")

selected_images = []

select_button = tk.Button(app, text="Select Images", command=select_images)
select_button.pack()

remove_button = tk.Button(app, text="Remove Metadata", command=remove_metadata)
remove_button.pack()

save_button = tk.Button(app, text="Save Images", command=save_images)
save_button.pack()

status_label = tk.Label(app, text="No images selected.")
status_label.pack()

app.mainloop()
