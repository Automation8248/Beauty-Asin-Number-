import os
import time
import random
import requests
from playwright.sync_api import sync_playwright

# GitHub Secrets se token fetch karna
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Aapki di hui Beauty Products ki list (Strictly Beauty Only)
beauty_products = [
    "Vitamin C Brightening Serum","Hyaluronic Acid Serum","Retinol Cream","Niacinamide Serum","Collagen Serum",
    "Peptide Cream","Bakuchiol Serum","Snail Mucin Essence","Glass Skin Serum","SPF Moisturizer",
    "Sunscreen Stick","Tinted Sunscreen","Acne Spot Gel","Salicylic Face Wash","Tea Tree Serum",
    "Gel Moisturizer","Ceramide Cream","Overnight Mask","Clay Mask","Charcoal Mask",
    "AHA Toner","Glycolic Peel","Lactic Acid Exfoliant","Ice Roller","Gua Sha Tool",
    "Jade Roller","Under Eye Cream","Caffeine Eye Serum","Eye Patches","Lip Mask",
    "Lip Scrub","Lip Plumper","Lip Oil","Face Mist","Rose Toner",
    "Micellar Water","Makeup Balm","Cleansing Oil","Foam Cleanser","Cream Cleanser",
    "Double Cleanser Set","Brightening Cream","Dark Spot Serum","Freckle Cream","Anti-Redness Serum",
    "Sensitive Moisturizer","Aloe Vera Gel","Vitamin E Cream","Night Cream","Neck Cream",
    "Neck Serum","Face Oil","Facial Steamer","Blackhead Vacuum","Pore Serum",
    "Anti-Pollution Cream","Blue Light Serum","Retinol Mask","Sheet Mask","Toner Pads",
    "Exfoliating Pads","Glow Serum","Vitamin B5 Serum","Zinc Serum","Green Tea Serum",
    "Centella Cream","Face Oil Glow","Peptide Serum","Barrier Cream","Probiotic Cream",
    "Face Mist Cooling","Gel Mask","Lip Mask Night","Oil Cleanser","Facial Kit",
    "Anti-Aging Set","Collagen Mask","Vitamin Face Wash","Jelly Mask","Radiance Serum",
    "Tightening Cream","Wrinkle Cream","Lifting Serum","Glow Cream","Repair Balm",
    "Essence Water","Anti-Dull Serum","Renewal Cream","Face Scrub","Ampoule Serum",
    "Calming Gel","Ice Globes","Facial Kit Anti-Aging","Deep Clean Mask","Detox Serum",
    "Oil Control Serum","Matte Moisturizer","Face Oil Hydrating","Plumping Serum","Acne Kit",
    "Pore Cream","Face Pack","Radiance Booster","Glow Cream Daily","Dark Circle Kit",
    "Face Mask Brightening","Soft Lotion","Tone Serum","Blemish Cream","Face Brush",
    "Polish Kit","Massage Tool","Glow Kit","Detox Oil","Repair Serum",
    "Hydration Cream","Anti-Aging Oil","Bright Kit","Combo Set",

    "Skin Tint","Matte Foundation","BB Cream","CC Cream","Concealer Stick",
    "Liquid Concealer","Setting Powder","Compact Powder","Setting Spray","Primer",
    "Pore Primer","Glow Primer","Cream Blush","Liquid Blush","Powder Blush",
    "Highlighter Drops","Highlighter Powder","Cream Highlighter","Bronzer","Cream Bronzer",
    "Contour Stick","Contour Palette","Eyeshadow Palette","Nude Palette","Glitter Shadow",
    "Eyeliner Pen","Gel Eyeliner","Mascara","Lash Mascara","False Lashes",
    "Lash Glue","Brow Pencil","Brow Gel","Brow Pomade","Matte Lipstick",
    "Glossy Lipstick","Lip Gloss","Lip Tint","Lip Stain","Lip Liner",
    "Lip Plumper","Lip Oil","Makeup Fixer","Makeup Wipes","Beauty Blender",
    "Brush Set","Foundation Brush","Powder Brush","Blush Brush","Eye Brush Set",
    "Eyelash Curler","LED Mirror","Travel Kit","Mini Kit","Full Kit",
    "HD Foundation","Airbrush Kit","Corrector Palette","Brightener","Matte Powder",
    "Glow Powder","Shadow Stick","Liquid Eyeliner","Brow Tint","Brow Soap",
    "Face Palette","Contour Cream","Glow Drops","Skin Perfector","Primer Serum",
    "Multi Stick","Eye Glitter","Eye Primer","Lash Serum","Waterproof Liner",
    "Lip Kit","Nude Kit","Red Kit","Gloss Set","Gift Set",

    "Hair Growth Oil","Onion Oil","Castor Oil","Coconut Oil","Hair Serum",
    "Keratin Mask","Protein Mask","Deep Conditioner","Hair Repair","Split Serum",
    "Heat Spray","Hair Gel","Hair Wax","Hair Spray","Volume Spray",
    "Sea Salt Spray","Dry Shampoo","Anti-Dandruff Shampoo","Sulfate Shampoo","Organic Shampoo",
    "Hydration Shampoo","Hair Fall Shampoo","Dry Conditioner","Leave Conditioner","Detangler",
    "Curl Cream","Curl Gel","Straight Cream","Smooth Serum","Thick Spray",
    "Hair Fiber","Growth Serum","Scalp Serum","Scalp Scrub","Hair Spa",
    "Hair Color","Color Spray","Root Powder","Bleach Kit","Toner",
    "Purple Shampoo","Hair Gloss","Shine Spray","Repair Oil","Anti-Frizz Cream",
    "Styling Cream","Curl Cream","Hair Gel Strong","Texture Spray","Smooth Cream",
    "Volume Powder","Thick Serum","Nourish Oil","Herbal Oil","Ayurvedic Oil",
    "Hair Fall Kit","Growth Kit","Repair Kit","Straight Kit","Smooth Kit",
    "Combo Hair","Scalp Massager","Steam Cap","Hair Straightener","Hair Curler",
    "Blow Dryer","Hot Brush","Tool Set","Curl Band","Silk Wrap",
    "Satin Pillow","Hair Bonnet","Hair Clips","Hair Bands","Hair Brush",
    "Detangle Brush","Paddle Brush","Round Brush","Roller Set","Tool Organizer",

    "Body Lotion","Body Butter","Body Oil","Body Serum","Firming Cream",
    "Stretch Cream","Cellulite Cream","Coffee Scrub","Sugar Scrub","Salt Scrub",
    "Gloves","Body Wash","Shower Oil","Body Mist","Perfume",
    "Long Perfume","Natural Perfume","Deodorant","Roll-On","Whitening Lotion",
    "Bright Cream","Tanning Oil","Self Tanner","Body Sunscreen","After Sun",
    "Polish Kit","Bath Bomb","Bubble Bath","Foot Cream","Foot Scrub",
    "Foot Mask","Heel Cream","Hand Cream","Nail Strengthener","Cuticle Oil",
    "Nail Polish","Gel Kit","Nail Art","Nail Dryer","Gift Set Body",
    "Intimate Wash","Hygiene Spray","Body Acne Spray","Glow Oil","Shimmer Lotion",
    "Massage Oil","Spa Kit","Detox Kit","Combo Body","Glow Kit Body",

    "LED Mask","Microcurrent Device","Toning Device","Skin Analyzer","Blackhead Tool",
    "Facial Steamer","Face Massager","Skin Scrubber","RF Device","Ice Roller Tool",
    "Heated Curler","Brush Cleaner","Facial Brush","Laser Removal","Epilator",
    "Electric Razor","Straight Brush","Auto Curler","Ionic Dryer","Scalp Device",
    "Laser Cap","Heated Brush","Nail Drill","UV Lamp","Makeup Fridge",
    "Smart Mirror","LED Organizer","Facial Sauna","Rejuvenation Device","Acne Device",
    "Wrinkle Device","Eye Massager","Neck Massager","Spa Machine","Beauty Kit"
]

TARGET_COUNT = 10

def run_scraper():
    # Randomly ek beauty product select karna
    selected_product = random.choice(beauty_products)
    search_query = selected_product.replace(" ", "+")
    print(f"Today's Selected Product: {selected_product}")
    
    asins = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={
                "server": "http://31.59.20.176:6754",
                "username": "oxulhyvs",
                "password": "ukzzq3m862fa"
            }
        )
        
        context = browser.new_context(
            locale="en-US",
            timezone_id="America/New_York",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()

        # Added &i=beauty to strictly filter out other categories at the Amazon search level
        url = f"https://www.amazon.com/s?k={search_query}&i=beauty&page=1"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(3) # Human-like delay
            
            elements = page.locator("div[data-asin]").all()
            
            for el in elements:
                asin = el.get_attribute("data-asin")
                
                # NAYA LOGIC: Check karega ki product ka naam page ke text mein hai ya nahi
                try:
                    card_text = el.inner_text().lower()
                    is_beauty_related = selected_product.lower() in card_text
                except:
                    is_beauty_related = False

                # Check valid 10-character ASIN aur strictly beauty match
                if asin and len(asin) == 10 and asin.isupper() and is_beauty_related:
                    asins.add(asin)
                    if len(asins) >= TARGET_COUNT:
                        break
                        
        except Exception as e:
            print(f"Error while scraping: {e}")

        browser.close()
        
    return list(asins)[:TARGET_COUNT]

# Script run karna
final_asins = run_scraper()

# Telegram Messaging
if final_asins:
    # ⚠️ SIRF ASIN numbers, koi extra text nahi jaisa aapne manga tha
    message = "\n".join(final_asins)

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
    print(f"✅ Sent {len(final_asins)} pure beauty ASINs to Telegram!")
else:
    print("⚠️ 0 ASINs found. Proxy ya block ka issue ho sakta hai.")
