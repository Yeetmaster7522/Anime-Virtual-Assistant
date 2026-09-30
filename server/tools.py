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
- create my own functions for web search and navigation
    - search
    - fetch
    - open
"""

# import os
import time
import subprocess
from pyautogui import screenshot
import tkinter as tk
from tkinter import messagebox
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import html2text

def get_datetime():
    """
    Returns local time
    """
    
    return time.strftime("%a %d %b %Y %H:%M:%S Local Time", time.localtime)

def take_screenshot(filepath: str|None=None):
    """
    Returns an Image object as well as save it to the specified file location
    """

    return screenshot(filepath)

def run_command(command: list[str]) -> tuple[str, str] | None:
    """
    Executes a system command asynchronously after explicit user confirmation via a GUI dialog.

    Args:
        command (list[str]): The system command split into a list of strings 
            (e.g., ["git", "status"]). Avoids raw shell parsing vulnerabilities.

    Returns:
        tuple[str, str] | None: A tuple containing (stdout, stderr) as strings if the 
            user approves execution. Returns None if the user rejects the action or 
            closes the confirmation window.
    """
    output = None

    root = tk.Tk()
    root.withdraw()

    response = messagebox.askyesno(title="Confirmation", message="Do you want to proceed?", detail=" ".join(command), icon="warning")

    if response:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )

        output = process.communicate()

    return output

def get_website_content(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        raw_html = page.content()

        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = True

        return converter.handle(raw_html)

def get_top_urls(query, limit=5):
    return []

async def browser_urls(urls: list[str]) -> None:
    """
    Use asyncio.run(browser_urls)
    """
    
    async with async_playwright as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        for url in urls:
            page = context.new_page()
            await page.goto(url)
        await page.pause()


if __name__ == "__main__":
    pass
    # get_website_content("https://www.abc.net.au/news/2026-09-30/federal-politics-greens-announce-new-leader-david-shoebridge/107211108")
    # browser_urls(["https://www.youtube.com/", "https://pypi.org/project/playwright-stealth/", "https://cstimer.net/"])