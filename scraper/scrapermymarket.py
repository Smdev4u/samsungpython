import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog
from urllib.parse import urlparse, unquote
import time
import threading

# Set the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to create the image directory if it doesn't exist
def create_image_dir(brand_name):
    image_dir = os.path.join(script_dir, f"product_images_{brand_name}")
    os.makedirs(image_dir, exist_ok=True)
    return image_dir

# Function to get a valid filename from a URL and ensure it is unique
def get_valid_filename(url, counter, image_dir):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filename, ext = os.path.splitext(filename)
    filename = unquote(filename)
    final_filename = f"{filename}_{counter}{ext}"
    path = os.path.join(image_dir, final_filename)
    count = 1
    while os.path.exists(path):
        final_filename = f"{filename}_{counter}_{count}{ext}"
        path = os.path.join(image_dir, final_filename)
        count += 1
    return final_filename

# Function to download image with retries
def download_image(url, path, retries=3, delay=5):
    if os.path.exists(path):
        return True  # Skip download if the file already exists
    for attempt in range(retries):
        try:
            with open(path, 'wb') as f:
                img_response = requests.get(url)
                img_response.raise_for_status()
                f.write(img_response.content)
            return True
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                messagebox.showerror("Error", f"Failed to download image after {retries} attempts: {e}")
                return False

# Function to extract float value from price string
def extract_float_from_price(price_str):
    match = re.search(r'\d+(\.\d+)?', price_str)
    return float(match.group()) if match else None

# Function to generate a unique product code
def generate_product_code(counter):
    return f"PRD-{counter:05d}"

# Function to scrape a single page
def scrape_page(url, listbox, counter, unit, category, stock_alert, brand_name):
    products = []
    image_dir = create_image_dir(brand_name)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding  # Ensure the correct encoding
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch page: {e}")
        return products, counter
    
    soup = BeautifulSoup(response.content, 'html.parser')
    product_containers = soup.find_all('div', class_='product-item')

    for product in product_containers:
        # Extracting Product Name
        name_tag = product.find('a', class_='product-item__title text--strong link')
        if not name_tag:
            continue
        name = name_tag.text.strip()

        # Extracting Product Price
        price_tag = product.find('span', class_='price')
        if not price_tag:
            continue
        price_str = price_tag.text.strip()
        price = extract_float_from_price(price_str)
        cost = round(price * 0.7, 2) if price else None

        # Extracting Product Vendor
        vendor_tag = product.find('a', class_='product-item__vendor link')
        brand = vendor_tag.text.strip() if vendor_tag else "Unknown Brand"

        # Extracting Primary Product Image
        primary_image_tag = product.find('img', class_='product-item__primary-image')
        if primary_image_tag and primary_image_tag.get('src'):
            image_url = "https:" + primary_image_tag.get('src')
        else:
            continue  # Skip if no image is found

        # Generate unique product code
        counter += 1
        product_code = generate_product_code(counter)

        # Generate unique image name and path
        image_name = get_valid_filename(image_url, counter, image_dir)
        image_path = os.path.join(image_dir, image_name)
        
        # Check if image exists before downloading
        if not os.path.exists(image_path):
            if not download_image(image_url, image_path):
                continue

        # Add product information to listbox and products list
        product_info = f"Code: {product_code}, Brand: {brand}, Name: {name}, Price: {price}, Cost: {cost}, Unit: {unit}, Category: {category}, Stock Alert: {stock_alert}"
        listbox.insert(tk.END, product_info)

        products.append({
            'name': name,
            'code': product_code,
            'category': category,
            'brand': brand,
            'cost': cost,
            'price': price,
            'unit': unit,
            'stock_alert': stock_alert,
            'image': os.path.join(image_dir, image_name),
            'note': 'note'  # You can modify this to add any notes if needed
        })
    
    return products, counter

# Function to scrape all pages
def scrape_all_pages(base_url, listbox, progress_label, unit, category, stock_alert, brand_name):
    all_products = []
    page_number = 1
    counter = 0
    
    while True:
        url = f"{base_url}?page={page_number}#catalog-listing"
        progress_label.config(text=f"Scraping page {page_number}...")
        products, counter = scrape_page(url, listbox, counter, unit, category, stock_alert, brand_name)
        
        if not products:
            break
        
        all_products.extend(products)
        page_number += 1
    
    progress_label.config(text="Scraping completed.")
    return all_products

# Function to save data to an Excel file
def save_to_excel(products, filename="scraped_products.xlsx"):
    if not products:
        messagebox.showinfo("No Data", "No products to save.")
        return

    df = pd.DataFrame(products)
    excel_path = os.path.join(script_dir, filename)
    df.to_excel(excel_path, index=False, engine='xlsxwriter')
    messagebox.showinfo("Success", f"Data saved to {excel_path}")

# Function to start scraping (threaded)
def start_scraping():
    def scraping_thread():
        base_url = url_entry.get()
        unit = unit_entry.get()
        category = category_entry.get()
        stock_alert = stock_alert_entry.get()
        brand_name = brand_entry.get()
        
        if not base_url:
            messagebox.showerror("Error", "Please enter a valid URL")
            return
        if not unit:
            messagebox.showerror("Error", "Please enter a unit")
            return
        if not category:
            messagebox.showerror("Error", "Please enter a category")
            return
        if not stock_alert:
            messagebox.showerror("Error", "Please enter a stock alert value")
            return
        if not brand_name:
            messagebox.showerror("Error", "Please enter a brand name")
            return
        
        try:
            stock_alert_value = int(stock_alert)
        except ValueError:
            messagebox.showerror("Error", "Stock alert value must be an integer")
            return
        
        try:
            listbox.delete(0, tk.END)
            global all_products
            all_products = scrape_all_pages(base_url, listbox, progress_label, unit, category, stock_alert_value, brand_name)
            if not all_products:
                messagebox.showinfo("No Data", "No products found or failed to scrape any data.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during scraping: {e}")
            return
        
        save_to_excel(all_products)

    threading.Thread(target=scraping_thread).start()

# Create the main application window
app = tk.Tk()
app.title("Product Scraper")
app.geometry("800x600")

# Create and place the URL entry field and label
url_label = tk.Label(app, text="Enter URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)

# Create and place the unit entry field and label
unit_label = tk.Label(app, text="Enter Unit (default value):")
unit_label.pack(pady=5)

unit_entry = tk.Entry(app, width=50)
unit_entry.pack(pady=5)
unit_entry.insert(0, "default unit")  # Insert a default value

# Create and place the category entry field and label
category_label = tk.Label(app, text="Enter Category (or choose from list):")
category_label.pack(pady=5)

category_entry = tk.Entry(app, width=50)
category_entry.pack(pady=5)

# Create and place the stock alert entry field and label
stock_alert_label = tk.Label(app, text="Enter Stock Alert value:")
stock_alert_label.pack(pady=5)

stock_alert_entry = tk.Entry(app, width=50)
stock_alert_entry.pack(pady=5)

# Create and place the brand entry field and label
brand_label = tk.Label(app, text="Enter Brand:")
brand_label.pack(pady=5)

brand_entry = tk.Entry(app, width=50)
brand_entry.pack(pady=5)

# Create and place the scrape button
scrape_button = tk.Button(app, text="Start Scraping", command=start_scraping)
scrape_button.pack(pady=10)

# Create and place the listbox to display scraped products
listbox = tk.Listbox(app, width=100, height=15)
listbox.pack(pady=10)

# Create and place the progress label
progress_label = tk.Label(app, text="")
progress_label.pack(pady=5)

# Start the Tkinter event loop
app.mainloop()
