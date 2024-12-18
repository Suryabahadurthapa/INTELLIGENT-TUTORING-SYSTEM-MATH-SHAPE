#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install rdflib ipywidgets')


# In[5]:


import tkinter as tk
from tkinter import messagebox
import rdflib


# In[6]:


def load_ontology():
    g = rdflib.Graph()
    g.parse("math_shapes_ontology.owl", format="xml")
    return g


# In[7]:


def calculate_area(shape, base, height, side):
    try:
        base = float(base) if base else 0
        height = float(height) if height else 0
        side = float(side) if side else 0

        if shape == "Rectangle":
            if base > 0 and height > 0:
                return base * height
            else:
                raise ValueError("Rectangle requires both base and height.")
        elif shape == "Square":
            if side > 0:
                return side ** 2
            else:
                raise ValueError("Square requires a valid side length.")
        elif shape == "Triangle":
            if base > 0 and height > 0:
                return 0.5 * base * height
            else:
                raise ValueError("Triangle requires both base and height.")
        else:
            raise ValueError("Unknown shape")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")
        return None

def query_ontology(g, property_name, class_name):
    query = f"""
    SELECT ?value WHERE {{
        ?shape rdf:type <{class_name}> .
        ?shape <{property_name}> ?value .
    }}
    """
    result = g.query(query)
    values = [str(row[0]) for row in result]
    return values

def setup_gui():

    window = tk.Tk()
    window.title("Area Calculator")

    g = load_ontology()

    shape_label = tk.Label(window, text="Select Shape:")
    shape_label.grid(row=0, column=0)

    shape_options = ["Triangle", "Rectangle", "Square"]
    shape_var = tk.StringVar(window)
    shape_var.set(shape_options[0])

    shape_menu = tk.OptionMenu(window, shape_var, *shape_options)
    shape_menu.grid(row=0, column=1)

    base_label = tk.Label(window, text="Base Length:")
    base_label.grid(row=1, column=0)
    base_entry = tk.Entry(window)
    base_entry.grid(row=1, column=1)

    height_label = tk.Label(window, text="Height Length:")
    height_label.grid(row=2, column=0)
    height_entry = tk.Entry(window)
    height_entry.grid(row=2, column=1)

    side_label = tk.Label(window, text="Side Length:")
    side_label.grid(row=3, column=0)
    side_entry = tk.Entry(window)
    side_entry.grid(row=3, column=1)

    def update_fields(*args):
        shape = shape_var.get()
        if shape == "Rectangle":
            base_label.grid()
            base_entry.grid()
            height_label.grid()
            height_entry.grid()
            side_label.grid_remove()
            side_entry.grid_remove()
        elif shape == "Square":
            side_label.grid()
            side_entry.grid()
            base_label.grid_remove()
            base_entry.grid_remove()
            height_label.grid_remove()
            height_entry.grid_remove()
        elif shape == "Triangle":
            base_label.grid()
            base_entry.grid()
            height_label.grid()
            height_entry.grid()
            side_label.grid_remove()
            side_entry.grid_remove()

    shape_var.trace("w", update_fields)

    def on_calculate():
        shape = shape_var.get()
        base = base_entry.get()
        height = height_entry.get()
        side = side_entry.get()

        area = calculate_area(shape, base, height, side)
        if area is not None:
            result_label.config(text=f"Area: {area:.2f}")

    calculate_button = tk.Button(window, text="Calculate Area", command=on_calculate)
    calculate_button.grid(row=4, column=0, columnspan=2)

    result_label = tk.Label(window, text="Area: ")
    result_label.grid(row=5, column=0, columnspan=2)

    update_fields()

    window.mainloop()

if __name__ == "__main__":
    setup_gui()


# In[ ]:




