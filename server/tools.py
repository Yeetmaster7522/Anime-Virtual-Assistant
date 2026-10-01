"""
BRAINSTORM
- time management
    - planning schedules, deadlines, and meetings
- information management
    - organising files, managing contacts, and handling documents
- task coordination
    - scheduling tasks
    - following up on work
    - helping with assignments across different departments
- communication support
    - handling emails
    - scheduling calls
    - managing digital correspondence
- strategic planning
    - creating action plans and setting goals
- workflow automation
- play games
- look busy

NEED TO
- open programs
"""

# import os
import time
import subprocess
from pyautogui import screenshot
import tkinter as tk
from tkinter import messagebox
from playwright.sync_api import sync_playwright
import html2text
from PIL import Image

def get_datetime() -> str:
    """
    Returns local time as str
    """
    
    return time.strftime("%a %d %b %Y %H:%M:%S Local Time", time.localtime)

def take_screenshot(filepath: str|None=None) -> Image:
    """
    Returns an Image object as well as save it to the specified file location

    Args
        filepath (str): where the image gets saved

    Returns Image object
    """

    return screenshot(filepath)

def run_command(command: str) -> tuple[str, str] | None:
    """
    Executes a system command asynchronously after explicit user confirmation via a GUI dialog.

    Args:
        command (str): The system command

    Returns:
        tuple[str, str] | None: A tuple containing (stdout, stderr) as strings if the 
            user approves execution. Returns None if the user rejects the action or 
            closes the confirmation window.
    """
    output = None

    root = tk.Tk()
    root.withdraw()

    response = messagebox.askyesno(title="Confirmation", message="Do you want to proceed?", detail=command, icon="warning")

    if response:
        process = subprocess.Popen(
            command.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )

        output = process.communicate()

    return output

def get_website_content(url: str) -> str:
    """
    Fetches a webpage and converts its HTML content into plain text

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The plain-text representation of the webpage content.
    """
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        raw_html = page.content()

        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = True

        return converter.handle(raw_html)

if __name__ == "__main__":
    print(get_website_content("https://www.abc.net.au/"))