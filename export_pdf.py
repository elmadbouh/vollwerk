import asyncio
import os
from playwright.async_api import async_playwright

async def export_pdf():
    input_file = 'file://' + os.path.abspath('export_card.html')
    output_combined = 'vollwerk_business_card_combined.pdf'
    output_front = 'vollwerk_business_card_front.pdf'
    output_back = 'vollwerk_business_card_back.pdf'

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        print(f"Loading {input_file}...")
        await page.goto(input_file, wait_until="networkidle")
        
        # Ensure fonts are loaded
        await page.evaluate("document.fonts.ready")

        # PDF options for 91mm x 60mm (85x54 + 3mm bleed)
        pdf_options = {
            "width": "91mm",
            "height": "60mm",
            "print_background": True,
            "margin": {"top": "0", "right": "0", "bottom": "0", "left": "0"}
        }

        print("Generating Combined PDF...")
        await page.pdf(path=output_combined, **pdf_options)
        
        print("Generating Front PDF...")
        await page.pdf(path=output_front, page_ranges="1", **pdf_options)
        
        print("Generating Back PDF...")
        await page.pdf(path=output_back, page_ranges="2", **pdf_options)
        
        await browser.close()
        print("Success! PDFs generated using Playwright.")

if __name__ == "__main__":
    asyncio.run(export_pdf())
