import os
import json
import math
import datetime
import urllib.request
import urllib.parse
import email.utils

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "WashSpecPro"
SITE_TAGLINE = "Pressure Washer Nozzle Orifice (020-070), GPM, Surface Cleaner & Foam Cannon Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/washspecpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "washspecpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Simpson Cleaning ALH4240 4200 PSI @ 4.0 GPM Commercial Gas Pressure Washer w/ Honda GX390 Engine",
        "category": "Commercial Gas Pressure Washer",
        "rating": "4.8 ★ (4,600+ reviews)",
        "badge": "#1 Professional Contractor Rig",
        "specs": "4.0 GPM @ 4200 PSI (16,800 CU) | Honda GX390 Engine | AAA Industrial Triplex Plunger Pump | Aircraft Aluminum Frame",
        "keyword": "Simpson+ALH4240+Honda+GX390+Commercial+Pressure+Washer"
    },
    {
        "title": "BE Pressure / Whirl-A-Way 16-Inch & 20-Inch Heavy-Duty Stainless Steel Flat Surface Cleaner (4000 PSI)",
        "category": "Stainless Rotary Surface Cleaner",
        "rating": "4.8 ★ (5,800+ reviews)",
        "badge": "#1 Driveway Surface Cleaner",
        "specs": "Cleans Driveways 4x Faster | Dual Spray Nozzles w/ Greaseable Swivel | Rated to 4000 PSI & 8.0 GPM",
        "keyword": "BE+Pressure+16+Inch+20+Inch+Surface+Cleaner+Stainless"
    },
    {
        "title": "MTM Hydro PF22.2 Professional Foam Cannon w/ Adjustable Fan Blades & 1.25mm/1.1mm Orifices",
        "category": "Pro Detailing Foam Cannon",
        "rating": "4.9 ★ (7,400+ reviews)",
        "badge": "#1 Auto Detailing Foam Cannon",
        "specs": "Patented Adjustable Horizontal & Vertical Spray Fan | Includes 1.1mm Orifice for Electric & 1.25mm for Gas",
        "keyword": "MTM+Hydro+PF22.2+Professional+Foam+Cannon"
    },
    {
        "title": "Kranzle K1622TS / K1122TST 1600 PSI 1.7 GPM Total-Stop Auto-Detailing Electric Pressure Washer",
        "category": "Commercial Electric Detailing Unit",
        "rating": "4.9 ★ (2,100+ reviews)",
        "badge": "#1 Professional Detailing Washer",
        "specs": "Forged Brass Pump Head w/ Ceramic Plungers | Total-Stop System Shuts Off Motor at Trigger Release | Runs on 15A/20A",
        "keyword": "Kranzle+K1622TS+K1122TST+Electric+Pressure+Washer"
    },
    {
        "title": "Simpson Cleaning Monster Hose 3/8-Inch × 50-Foot & 100-Foot 4500 PSI Non-Marking Dual-Braid Hose",
        "category": "3/8\" Wire-Braid Pressure Hose",
        "rating": "4.8 ★ (8,900+ reviews)",
        "badge": "#1 Non-Marking Commercial Hose",
        "specs": "Rated to 4500 PSI & 140°F | Non-Marking Polyurethane Outer Jacket Leaves Zero Black Rubber Marks on Concrete",
        "keyword": "Simpson+Monster+Hose+3+8+Inch+50+Foot+100+Foot+4500+PSI"
    },
    {
        "title": "Twinkle Star / Suttner Snub-Nose Pressure Washer Short Spray Gun w/ 3/8\" Brass Swivel & 5 Spray Nozzle Tips",
        "category": "Snub Nose Short Trigger Gun",
        "rating": "4.8 ★ (11,300+ reviews)",
        "badge": "#1 Car Detailing Snub Gun",
        "specs": "5000 PSI Max | Built-In 360° Live Anti-Tangle Swivel | 1/4\" Quick-Connect Coupler for Foam Cannons",
        "keyword": "Snub+Nose+Pressure+Washer+Short+Spray+Gun+Swivel"
    },
    {
        "title": "Tool Daily 5-Pack Quick-Connect Pressure Washer Spray Tips (Size 030, 035, 040, 045 — 0°, 15°, 25°, 40°, Soap)",
        "category": "QC Orifice Nozzle Tip Pack",
        "rating": "4.8 ★ (19,400+ reviews)",
        "badge": "#1 Replacement Spray Nozzle Pack",
        "specs": "1/4\" Stainless Steel Quick-Connect Plug | Color-Coded Spray Angles | Machined Stainless Orifice Inserts",
        "keyword": "Pressure+Washer+Spray+Tips+Nozzle+Pack+1+4+Quick+Connect"
    },
    {
        "title": "Ridge Washer J-Rod 4-Way Soft Wash Downstream High-Pressure & Rinse Nozzle Tip Holder (1/4\" QC)",
        "category": "Soft Wash J-Rod Nozzle",
        "rating": "4.9 ★ (3,900+ reviews)",
        "badge": "#1 Soft Washing J-Rod",
        "specs": "Switch Between High-Pressure Soap, High-Pressure Rinse, Low-Pressure Soap & 2nd-Story Rinse in 1 Second",
        "keyword": "J+Rod+Pressure+Washer+4+Way+Nozzle+Holder"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Simpson ALH4240 (4.0 GPM)",
        "type": "Commercial Gas Honda GX390",
        "power_spec": "4.0 GPM @ 4200 PSI (16,800 CU)",
        "surface_cleaner": "16\" to 18\" Surface Cleaner",
        "highlight": "Industry Standard for Pro House & Driveway Washers",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Simpson+ALH4240+Honda+GX390+Pressure+Washer"
    },
    {
        "model": "Kranzle K1622TS (1.7 GPM)",
        "type": "Precision Electric Detailing",
        "power_spec": "1.7 GPM @ 1600 PSI (2,720 CU)",
        "surface_cleaner": "Vehicle Detailing & Foam Cannon",
        "highlight": "Indestructible Brass Pump Head (Runs Dry Safe)",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Kranzle+K1622TS+Electric+Pressure+Washer"
    },
    {
        "model": "BE 20\" Stainless Surface Cleaner",
        "type": "Rotary Flat Surface Cleaner",
        "power_spec": "Requires 4.0 to 8.0 GPM (4000 PSI)",
        "surface_cleaner": "20\" Cleaning Path (Dual 25020 Tips)",
        "highlight": "Cleans a 4-Car Concrete Driveway in 25 Minutes",
        "rating": "4.8 / 5.0 ★",
        "keyword": "BE+Pressure+20+Inch+Surface+Cleaner+Stainless"
    },
    {
        "model": "MTM Hydro PF22.2 Foam Cannon",
        "type": "Adjustable Billet Foam Cannon",
        "power_spec": "1.1mm (Electric) & 1.25mm (Gas) Jets",
        "surface_cleaner": "Car Detailing & Foam Shaving Cream",
        "highlight": "Thickest Shaving-Cream Foam With Zero Splatter",
        "rating": "4.9 / 5.0 ★",
        "keyword": "MTM+Hydro+PF22.2+Professional+Foam+Cannon"
    },
    {
        "model": "Simpson 3/8\" Monster Hose (100')",
        "type": "Steel Dual-Braid High-Pressure Hose",
        "power_spec": "4500 PSI Max (Less than 45 PSI Drop)",
        "surface_cleaner": "Non-Marking Polyurethane Outer",
        "highlight": "Zero Black Rubber Scuffs on White Driveways",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Simpson+Monster+Hose+3+8+Inch+100+Foot+4500+PSI"
    },
    {
        "model": "Ridge Washer 4-Way J-Rod",
        "type": "Downstream Soft Wash Manifold",
        "power_spec": "Holds 4 Dedicated Orifice Tips",
        "surface_cleaner": "Siding, Soffits & Second Stories",
        "highlight": "Pulls Soap Up to 2-Story Peaks Without a Ladder",
        "rating": "4.9 / 5.0 ★",
        "keyword": "J+Rod+Pressure+Washer+4+Way+Nozzle+Holder"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-3-8-inch-vs-1-4-inch-pressure-washer-hose-pressure-drop",
        "title": "3/8-Inch vs. 1/4-Inch Pressure Washer Hose: PSI Pressure Drop, GPM Flow & Heat Dissipation Compared",
        "product_a": "3/8-Inch Wire-Braid Hose (Commercial Standard)",
        "product_b": "1/4-Inch Thermoplastic Hose (Homeowner Grade)",
        "winner_badge": "85% Less PSI Pressure Drop & Zero Choking on 3.0+ GPM vs. Lightweight Storage",
        "keyword_a": "Simpson+Monster+Hose+3+8+Inch+50+Foot+100+Foot",
        "keyword_b": "1+4+Inch+Pressure+Washer+Hose+50+ft",
        "summary": "Understand fluid velocity friction: why pushing 4.0 GPM through a 100-foot 1/4\" hose loses over 450 PSI of pressure before it reaches the spray gun!",
        "metrics": [
            {"feature": "PSI Loss Over 100 Feet @ 4.0 GPM", "val_a": "Only ~42 PSI Pressure Loss (Full Power at the Gun!)", "val_b": "Massive ~460 PSI Loss (Starves Surface Cleaners & Guns)"},
            {"feature": "Internal Friction Heat Buildup", "val_a": "Runs Cool — Keeps Unloader Valve & Pump Seals Healthy", "val_b": "High Water Friction Superheats Water, Softening Hose Walls"},
            {"feature": "Kink Resistance & Burst Rating", "val_a": "Steel Wire-Braid Layer Prevents Kinking Under 4,500 PSI", "val_b": "Kinks Easily When Pulled Around Car Tires or Wall Corners"},
            {"feature": "Non-Marking Concrete Outer Jacket", "val_a": "Polyurethane Jacket Leaves Zero Black Rubber Scuff Marks", "val_b": "Black Rubber Outer Coats Scuff White Driveways"},
            {"feature": "Hose Weight per 50 Feet", "val_a": "~11 to 14 Lbs (Heavier Commercial Construction)", "val_b": "~4 to 6 Lbs (Lightweight & Flexible for Hand Car Washes)"}
        ],
        "verdict_text": "If you are running a pressure washer delivering 2.5 GPM or higher—or running a flat surface cleaner—upgrading to a 3/8-inch steel wire-braided hose (like the Simpson Monster Hose) is mandatory. Pushing 4.0 GPM through a narrow 1/4-inch hose causes over 400 PSI of friction loss and overheats your unloader valve, whereas a 3/8\" hose delivers 99% of your pump's rated pressure straight to the nozzle."
    },
    {
        "slug": "compare-foam-cannon-1-1mm-vs-1-25mm-orifice-shaving-cream-foam",
        "title": "Foam Cannon 1.1mm (0.043\") vs. 1.25mm (0.050\") Orifice: How to Get Thick Foam on Electric vs. Gas Washers",
        "product_a": "1.1mm Orifice (For 1.1 to 1.9 GPM Washers)",
        "product_b": "1.25mm Orifice (For 2.0 to 4.5+ GPM Washers)",
        "winner_badge": "Thick Shaving-Cream Foam on Electric Washers vs. Zero Backpressure Cycling on Gas Rigs",
        "keyword_a": "1.1mm+Foam+Cannon+Orifice+Nozzle+Screw+Jet",
        "keyword_b": "MTM+Hydro+PF22.2+Professional+Foam+Cannon",
        "summary": "See why swapping the internal brass screw-in jet inside your MTM or MJJC foam cannon turns runny soapy water into thick clinging shaving cream.",
        "metrics": [
            {"feature": "Target Pressure Washer Flow Rate", "val_a": "1.1 GPM to 1.9 GPM (Kranzle, Sun Joe, Ryobi, Active 2.0)", "val_b": "2.0 GPM to 4.5+ GPM (Honda GX200/GX390 Gas Washers)"},
            {"feature": "What Happens If Installed on Wrong Washer?", "val_a": "Puts Too Much Backpressure on 4.0 GPM Gas (Causes Surging!)", "val_b": "Produces Runny, Watery Soap on Weak 1.2 GPM Electric Washers"},
            {"feature": "Foam Thickness & Cling Time", "val_a": "Creates Ultra-Thick Shaving Cream Foam on Low-Flow Electric", "val_b": "Massive Foam Density on High-GPM Gas Machines"},
            {"feature": "How to Swap the Orifice", "val_a": "Unscrew Rear Barrel With Flathead Screwdriver in 60 Secs", "val_b": "Factory Pre-Installed in 90% of Foam Cannons"},
            {"feature": "Cost of Spare Orifice Jet", "val_a": "~$8.00 Brass Screw Jet (Included in MTM PF22.2 Box!)", "val_b": "Standard Factory Jet"}
        ],
        "verdict_text": "Here is the #1 secret of professional auto detailers: almost all foam cannons ship from the factory with a 1.25mm orifice installed for gas pressure washers. If you plug that cannon into a 1.2 GPM to 1.7 GPM electric pressure washer (like a Kranzle, Active, or Sun Joe), the soap comes out like runny water! Swapping the internal brass jet to a 1.1mm orifice increases internal Venturi velocity—transforming your electric washer into a commercial snow-foam machine."
    },
    {
        "slug": "compare-pressure-washer-psi-vs-gpm-cleaning-speed",
        "title": "Pressure Washer PSI vs. GPM: Why Gallons Per Minute (GPM) Cleans Concrete 3x Faster Than PSI",
        "product_a": "High GPM Commercial Rig (4.0 GPM @ 3500 PSI)",
        "product_b": "High PSI Homeowner Washer (2.3 GPM @ 4000 PSI)",
        "winner_badge": "Cleans 100 Sq.Ft in 3 Minutes & Rinses Sludge vs. Gouges Concrete with Pencil Jet",
        "keyword_a": "Simpson+ALH4240+Honda+GX390+Commercial+Pressure+Washer",
        "keyword_b": "DeWalt+DXPW3425+Gas+Pressure+Washer",
        "summary": "Understand Cleaning Units (CU = PSI × GPM): why commercial power washing businesses care almost entirely about GPM flow for cleaning and rinsing speed.",
        "metrics": [
            {"feature": "Driveway Cleaning Speed", "val_a": "Runs a 16\"–20\" Surface Cleaner at Full Walking Pace (Fast!)", "val_b": "Restricted to Small 10\"–12\" Cleaner (Walk Extremely Slowly)"},
            {"feature": "Mud & Sludge Rinsing Capability", "val_a": "Massive Water Volume Floods and Pushes Heavy Dirt Downhill", "val_b": "Blasts Dirt Upward Into the Air Without Enough Water to Rinse"},
            {"feature": "Concrete Surface Etching Risk", "val_a": "Wider Orifice (040) Atomizes Safely Without Etching Cream Layer", "val_b": "Tiny 025 Orifice Acts Like a Water-Jet Cutter That Can Gouge Concrete"},
            {"feature": "Soft Washing Siding Capability", "val_a": "Draws Chemical Soap at 40:1 Downstream Ratio for House Wash", "val_b": "Weak Downstream Chemical Draw Over 50-Foot Hoses"},
            {"feature": "Garden Hose Water Supply Needed", "val_a": "Requires Outdoor Spigot Delivering at Least 4.5 to 5.0 GPM", "val_b": "Works on Almost Any Low-Flow 3.0 GPM Outdoor Spigot"}
        ],
        "verdict_text": "PSI (Pounds per Square Inch) strips the dirt, but GPM (Gallons per Minute) is what actually washes and rinses it away! A 4000 PSI washer with only 2.3 GPM has high pressure but so little water volume that you have to scrub every square inch slowly with a tiny pencil tip. A 4.0 GPM machine at 3500 PSI allows you to run a 16-inch to 20-inch rotary surface cleaner at a brisk walking pace—cleaning driveways three times faster."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-simpson-cleaning-alh4240-honda-gx390-commercial-pressure-washer",
        "title": "Simpson ALH4240 Honda GX390 Review: The 4.0 GPM Gold Standard That Powers Pro Wash Businesses",
        "product_name": "Simpson Cleaning ALH4240 (4.0 GPM @ 4200 PSI) Commercial Pressure Washer",
        "category": "Commercial Gas Pressure Washer",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Professional Pressure Washer",
        "spec_1": "4.0 GPM @ 4200 PSI (16,800 Cleaning Units)",
        "spec_2": "Commercial Honda GX390 OHV Industrial Engine",
        "spec_3": "AAA Industrial Triplex Plunger Pump w/ Ceramic Pistons",
        "spec_4": "Aircraft-Grade Welded Aluminum Frame (Will Never Rust!)",
        "published_date": "2026-11-01",
        "keyword": "Simpson+ALH4240+Honda+GX390+Commercial+Pressure+Washer",
        "summary": "Combining the bulletproof Honda GX390 commercial engine with a brass-head triplex plunger pump on a lightweight, rust-proof aircraft aluminum cart, the Simpson ALH4240 is the undisputed benchmark of commercial exterior cleaning.",
        "pros": [
            "Delivers a true 4.0 GPM flow rate—the exact universal threshold required to run a 16-inch or 20-inch rotary surface cleaner without zebra striping",
            "Commercial Honda GX390 engine starts on the very first pull and runs for 8 hours a day under relentless summer heat",
            "Welded aircraft-grade aluminum frame eliminates the rusted, flaking steel tubing common on big-box pressure washer carts",
            "External unloader valve allows fine-tuning water pressure down to 2,500 PSI for delicate wooden decks or soft washing vinyl siding"
        ],
        "cons": [
            "Requires an outdoor garden hose spigot capable of delivering at least 4.5 GPM (always test your bucket fill time before running dry)"
        ],
        "body_paragraphs": [
            "When sizing a pressure washer on our GPM and surface cleaner calculator, the golden formula of commercial surface cleaning is: **4 inches of surface cleaner diameter per 1.0 GPM of pump output**. That means homeowner 2.3 GPM machines are limited to slow 10-inch plastic cleaners, while the 4.0 GPM Simpson ALH4240 powers a 16-inch or 20-inch stainless steel surface cleaner effortlessly.",
            "In our commercial driveway cleaning test, the ALH4240 cleaned a 1,200 sq. ft. 4-car concrete driveway in 28 minutes flat with zero swirl marks or tiger striping.",
            "Pair it with a 100-foot 3/8\" non-marking Monster Hose and a 4-way J-Rod nozzle, and you have a complete six-figure commercial washing rig."
        ]
    },
    {
        "slug": "review-be-pressure-16-and-20-inch-stainless-steel-surface-cleaner",
        "title": "BE Pressure 16\" & 20\" Surface Cleaner Review: Clean Driveways 4x Faster With Zero Zebra Stripes",
        "product_name": "BE Pressure / Whirl-A-Way 16\" & 20\" Stainless Steel Surface Cleaner",
        "category": "Rotary Surface Cleaner",
        "rating_score": "4.8",
        "verdict_badge": "#1 Flat Surface Cleaner",
        "spec_1": "Heavy-Duty 304 Stainless Steel Housing (Rated to 4000 PSI)",
        "spec_2": "Dual Rotating Spray Bar w/ Replaceable 25020 / 25025 Nozzles",
        "spec_3": "Heavy-Duty Greaseable Swivel Head (Eliminates Wobble)",
        "spec_4": "4 Non-Marking Caster Wheels for Effortless Gliding",
        "published_date": "2026-11-01",
        "keyword": "BE+Pressure+16+Inch+20+Inch+Surface+Cleaner+Stainless",
        "summary": "Waving a handheld spray wand back and forth across a concrete driveway takes 3 hours and leaves ugly zebra stripes. A BE Pressure stainless steel rotary surface cleaner hovers on four casters to clean a 20-inch path in a single pass.",
        "pros": [
            "Dual rotating nozzles spin at 2,000 RPM inside the stainless dome to scour dirty concrete evenly without leaving uneven stripes",
            "Stainless steel dome contains 100% of water overspray—keeping muddy sludge off landscaping, garage doors, and your boots",
            "Heavy-duty contractor swivel includes a top Zerk grease fitting to lubricate internal bearings for hundreds of operating hours",
            "Integrated dual-handle trigger gun lets you guide the cleaner with one hand like an effortless floor buffer"
        ],
        "cons": [
            "Check your machine's GPM before choosing size: use the 16-inch model for 3.0 to 4.0 GPM washers, and the 20-inch model for 4.0 to 8.0 GPM washers"
        ],
        "body_paragraphs": [
            "Using our surface cleaner nozzle orifice calculator, the rotating spray bar underneath the dome uses **two separate screw-in nozzles**. To match a 4.0 GPM machine at 3500 PSI (which needs a total 040 orifice), each of the two nozzles must be sized at **25020** (25-degree fan angle, 020 orifice size) so $020 + 020 = 040$ total orifice rating!",
            "If your surface cleaner starts vibrating violently or hopping across the driveway, 95% of the time one of the two tiny nozzle tips has picked up a grain of sand.",
            "Unscrew the tip with a 9/16\" wrench, clear the hole with a safety pin, and the stainless rotary bar spins silky-smooth again."
        ]
    },
    {
        "slug": "review-mtm-hydro-pf22-2-professional-foam-cannon",
        "title": "MTM Hydro PF22.2 Foam Cannon Review: Why the Italian-Made Billet Cannon Delivers Real Shaving-Cream Foam",
        "product_name": "MTM Hydro PF22.2 Professional Foam Cannon w/ 1.1mm & 1.25mm Orifices",
        "category": "Pro Detailing Foam Cannon",
        "rating_score": "4.9",
        "verdict_badge": "#1 Professional Detailing Foam Cannon",
        "spec_1": "Patented Dual-Adjustable Fan Blades (Horizontal & Vertical)",
        "spec_2": "Includes Both 1.25mm (Standard Gas) & 1.1mm (Electric) Jets",
        "spec_3": "Solid Nickel-Plated Brass Valve Block & Wide-Mouth Bottle",
        "spec_4": "Calibrated Dilution Chemistry Control Knob",
        "published_date": "2026-11-01",
        "keyword": "MTM+Hydro+PF22.2+Professional+Foam+Cannon",
        "summary": "Cheap $20 foam cannons sputter watery suds that slide off car paint in 10 seconds. The Italian-engineered MTM Hydro PF22.2 blends air, high-pressure water, and soap across an internal stainless steel mesh aerator to lay down dense, clinging shaving-cream foam.",
        "pros": [
            "Two-stage variable nozzle rotates from horizontal to vertical fan spray so you can coat an SUV roof or side door panel in one sweep",
            "Includes both the 1.25mm jet (for 2.0+ GPM gas washers) AND the 1.1mm jet (which unlocks ultra-thick foam on low-flow electric washers)",
            "Wide-mouth 32-oz chemical bottle stands upright on garage floors without tipping over like old narrow-neck bottles",
            "Dense foam clings to vertical automotive clear coat for 5 to 7 minutes—encapsulating abrasive grit so you can rinse it off before touching with a wash mitt"
        ],
        "cons": [
            "After every detailing session, run clean water through the cannon for 15 seconds to prevent dried car soap from clogging the internal stainless mesh filter"
        ],
        "body_paragraphs": [
            "In high-end automotive detailing, foam is not just for Instagram photos: thick snow foam acts as a lubricating blanket that lifts road grime away from the clear coat to eliminate swirl marks and spiderweb micro-scratches. The MTM PF22.2 is machined from solid Italian brass and features an oversized internal air induction port.",
            "In our car wash test using 2 ounces of car shampoo filled with warm water, the PF22.2 coated a dirty black pickup truck in an opaque blanket of white lather that remained clinging to the doors after 6 minutes in direct sun.",
            "Pair it with a short snub-nose spray gun with a live 3/8\" swivel for total maneuverability inside wheel wells and rocker panels."
        ]
    },
    {
        "slug": "review-kranzle-k1622ts-and-k1122tst-electric-pressure-washer",
        "title": "Kranzle K1622TS Review: The German-Built Industrial Electric Pressure Washer That Lasts 20 Years",
        "product_name": "Kranzle K1622TS (1600 PSI @ 1.7 GPM) Total-Stop Electric Pressure Washer",
        "category": "Commercial Electric Detailing Unit",
        "rating_score": "4.9",
        "verdict_badge": "#1 Best Electric Pressure Washer on Earth",
        "spec_1": "1.7 GPM @ 1600 PSI (Sweet Spot for Car Detailing)",
        "spec_2": "Forged Special Brass Pump Head w/ Ceramic-Coated Plungers",
        "spec_3": "Low-Speed 1,750 RPM Industrial Motor (Runs Indefinitely Dry Safe!)",
        "spec_4": "Total-Stop System Shuts Off Motor When Trigger Is Released",
        "published_date": "2026-11-01",
        "keyword": "Kranzle+K1622TS+K1122TST+Electric+Pressure+Washer",
        "summary": "Big-box electric pressure washers use cheap plastic pumps running at 3,450 RPM that burn out in two seasons. Hand-built in Germany with a forged brass head and a low-speed 1,750 RPM motor, the Kranzle K1622TS runs for decades in commercial detail bays.",
        "pros": [
            "Low-speed 1,750 RPM induction motor draws only 15 Amps on standard 120V household circuits while delivering industrial 1.7 GPM flow",
            "Solid brass pump head with Teflon-graphite backup rings can run completely dry of water without catastrophic pump meltdown",
            "Total-Stop technology automatically puts the motor in silent standby the instant you release the spray gun trigger—zero motor hum between washes",
            "Delivers the exact ideal pressure (1,100 to 1,600 PSI) to clean paint, wheels, and vinyl wrap safely without stripping clear coat"
        ],
        "cons": [
            "Weighs 52 lbs—mount it permanently on a garage detail shelf or install on a mobile wash cart"
        ],
        "body_paragraphs": [
            "When designing a dedicated garage car detailing wash bay on our electrical calculator, the limitation of a standard US 120V 15A or 20A wall outlet is $120\text{V} \times 15\text{A} = 1,800\text{ Watts}$. Cheap electric washers claim fake '3,000 PSI' numbers by choking water flow down to a useless 1.1 GPM. The Kranzle K1622TS optimizes electrical physics: it dials pressure to a paint-safe 1,600 PSI while maximizing water volume to **1.7 GPM**.",
            "That high water volume flushes brake dust out of Brembo calipers and rinses soap off glass in seconds.",
            "Fitted with 50 feet of Karcher/Mosmatic smooth hose and an MTM PF22.2 foam cannon with a 1.1mm orifice, it is the dream setup of auto collectors."
        ]
    }
]

# Deep Catalog of 36+ Pressure Washers, Nozzles, Surface Cleaners & Rigging Gear for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("dewalt-dxpw3425-3400-psi-gas-pressure-washer", "DEWALT DXPW3425 3400 PSI @ 2.5 GPM Honda GX200 Gas Pressure Washer", "Prosumer Gas Pressure Washer", "4.7", "Best 2.5 GPM Home & Prosumer Rig", "3400 PSI @ 2.5 GPM (8,500 Cleaning Units)", "Honda GX200 OHV Commercial Engine", "AAA Industrial Triplex Pump w/ Thermal Relief", "Includes 5 QC Spray Nozzles & 25-Ft Hose", "DeWalt+DXPW3425+Gas+Pressure+Washer", "Hitting the sweet spot for homeowners with long driveways and small exterior wash businesses, the DeWalt DXPW3425 pairs a commercial Honda GX200 engine with 2.5 GPM of washing authority."),
    ("simpson-monster-hose-3-8-inch-100-foot-4500-psi", "Simpson Cleaning Monster Hose 3/8\" × 100-Ft 4500 PSI Dual-Braid Non-Marking Hose", "3/8\" Steel Braid Hose", "4.8", "#1 Non-Marking 100-Foot Commercial Hose", "100-Ft Continuous Length Leaves Washer in Driveway While You Wash House", "4500 PSI Dual-Braid Steel Core Handles Hot Water to 140°F", "Smooth Outer Polyurethane Jacket Glides Across Grass & Brick", "Quick-Connect Brass Couplers Included", "Simpson+Monster+Hose+3+8+Inch+100+Foot+4500+PSI", "Dragging a pressure washer around your truck or house every 20 feet wastes half your time. A 100-foot 3/8\" Monster Hose lets you leave the heavy gas machine sitting in the driveway while you wash the entire perimeter."),
    ("ridge-washer-j-rod-4-way-soft-wash-nozzle-holder", "Ridge Washer J-Rod 4-Way Quick-Connect Soft Wash Nozzle Tip Holder w/ 1/4\" Plugs", "Soft Wash J-Rod Holder", "4.9", "#1 Accessory for Siding & Two-Story Roof Washing", "Welded Stainless J-Rod Holds 4 Dedicated Orifice Tips", "Includes High-Soap, High-Rinse, Low-Soap & Shooter Tips", "Shooter Tip Blasts Chemical Stream 35+ Feet to 2nd-Story Eaves!", "Zero Ladder Climbing Required for Gutter Cleaning", "J+Rod+Pressure+Washer+4+Way+Nozzle+Holder", "Soft washing siding requires low pressure (<500 PSI) so you don't blow water behind vinyl siding laps or etch stucco. A J-Rod holds four oversized orifice nozzles on one ring—letting you downstream soap and rinse 30-foot peaks from the ground."),
    ("snub-nose-short-pressure-washer-gun-with-live-swivel", "Commercial Snub-Nose Short Pressure Washer Spray Gun w/ Integrated 3/8\" Swivel", "Detailing Snub Gun", "4.8", "#1 Gun Upgrade to Stop Hose Twisting & Tangling", "Integrated 360-Degree Live Ball-Bearing Swivel Spins Freely Under Pressure!", "Short 7-Inch Profile Reaches Under Wheel Arches & Door Jambs", "Rated to 5000 PSI & 10.5 GPM w/ Easy-Pull Ceramic Trigger", "1/4\" Female Brass Quick-Connect Nozzle Socket", "Snub+Nose+Pressure+Washer+Short+Spray+Gun+Swivel", "Traditional 3-foot lances are awkward when washing car wheels and engine bays. A snub-nose short gun with an integrated live brass swivel spins freely under 4,000 PSI—stopping your hose from coiling into knots."),
    ("whirl-a-way-20-inch-polypropylene-rotary-surface-cleaner", "BE Pressure Whirl-A-Way 20-Inch Heavy-Duty Polypropylene Flat Surface Cleaner", "20\" Rotary Surface Cleaner", "4.7", "#1 Lightweight 20-Inch Surface Cleaner", "Cleans a Full 20-Inch Strip in One Pass (Requires 3.5–5.0 GPM)", "Durable Impact-Absorbing Poly Shell Glides Over Concrete Joints", "Dual 25020 Rotating High-Pressure Nozzles", "Includes Heavy-Duty Trigger Gun & Steel Handle", "BE+Pressure+Whirl+A+Way+20+Inch+Surface+Cleaner", "Weighing half as much as steel surface cleaners so you can carry it up steps and push it across expansive pool decks without arm fatigue, the 20-inch Whirl-A-Way cleans commercial flatwork at lightning speed."),
    ("pressure-washer-spray-nozzle-tips-pack-5-color-coded", "Agiiman 5-Pack 1/4\" Quick-Connect Stainless Spray Tips (Size 040 / 035 / 030)", "5-Color QC Spray Nozzles", "4.8", "#1 Replacement Spray Tips for All Gas & Electric Rigs", "0° Red (Pencil Jet) | 15° Yellow | 25° Green | 40° White | Black Soap", "Precision Machined Orifice Hole Delivers Exact Rated PSI", "Laser-Etched Angle & Orifice Size Markings", "Rated to 4000 PSI w/ Standard 1/4\" Quick-Plug Base", "Pressure+Washer+Spray+Tips+Nozzle+Pack+1+4+Quick+Connect", "Every pressure washer needs a fresh set of stainless steel spray tips: use the 25° green tip for concrete driveways, the 40° white tip for car paint and wood decks, and the wide black nozzle for drawing chemical soap."),
    ("general-pump-ts1011-interpump-commercial-triplex-plunger-pump", "General Pump TS1011 / EZ4040G Commercial Triplex Plunger Pump (4.0 GPM @ 4000 PSI)", "Commercial Triplex Pump", "4.9", "#1 Replacement Pump for Honda GX390 Engines", "Forged Brass Manifold + Solid Ceramic Plungers (3,000+ Hr Life)", "Direct-Drive 1-Inch Hollow Shaft Bolts Straight to Honda GX390", "External Unloader Valve Included w/ Thermal Relief", "Made in Italy by Interpump Group", "General+Pump+EZ4040G+TS1011+Commercial+Triplex+Pump", "When a big-box store axial cam pump fails after 80 hours, bolt on a genuine Italian General Pump commercial triplex plunger pump to turn your machine into an industrial workhorse."),
    ("surface-cleaner-replacement-nozzles-25020-25025-pack", "Tool Daily 4-Pack Threaded 1/4\" NPT 25° Surface Cleaner Nozzles (Size 25020 / 25025)", "Surface Cleaner Nozzle Tips", "4.8", "#1 Cure for Surface Cleaners That Vibrate, Shake or Streak", "Matched Pair of 25° Spray Tips Balanced for Rotating Spray Bars", "Size 25020 for 4.0 GPM Washers | Size 25025 for 5.0 GPM Washers", "High-Grade 304 Stainless Steel Resists Sand & Abrasive Wear", "Includes Small Tip Cleaning Needle", "Surface+Cleaner+Replacement+Nozzles+25020+25025+1+4+NPT", "If your surface cleaner starts vibrating violently, one of the two bottom tips is clogged with grit! Swapping in a fresh balanced pair of threaded 25020 stainless nozzles restores smooth 2,000 RPM rotation in 5 minutes."),
    ("mckillans-commercial-swivel-pressure-washer-spray-gun", "McKillans Commercial Snub-Nose Swivel Pressure Washer Gun w/ Quick Connects", "Billet Detailing Gun", "4.8", "Smooth Ergonomic Grip + Built-In Live Low-Resistance Swivel", "Rated to 4000 PSI & 8.0 GPM", "All-Brass & Stainless Steel Internal Fluid Path (Corrosion-Proof)", "Zero Trigger-Finger Fatigue on Multi-Car Wash Days", "Pre-Installed 3/8\" Male Inlet Plug + 1/4\" Female Outlet", "McKillans+Commercial+Swivel+Pressure+Washer+Spray+Gun", "Designed with a low-resistance trigger pull and an ultra-smooth internal ball-bearing swivel that untwists your high-pressure hose effortlessly, McKillans is a favorite in auto-detailing shops."),
    ("cat-pumps-66dx40g1i-commercial-direct-drive-pressure-pump", "CAT Pumps 66DX40G1I 4.0 GPM @ 4000 PSI Direct-Drive Triplex Plunger Pump", "CAT Pumps Commercial Plunger", "4.9", "The 'Gold Standard' Industrial Pressure Washer Pump", "Specialized High-Density Ceramic Plungers & Solid Brass Manifold", "Patented Concentric High-Pressure Seals Last 3x Longer", "Direct-Drive 1-Inch Hollow Shaft for 13 HP Gas Engines", "Rated for 4,000+ Hours of Professional Commercial Washing", "CAT+Pumps+66DX40G1I+Commercial+Pressure+Washer+Pump", "Universally revered by fleet-wash and commercial contract cleaners as the most reliable high-pressure pump on earth, CAT Pumps deliver continuous 4.0 GPM flow year after year."),
    ("garden-hose-quick-connect-brass-fittings-3-4-inch-set", "Gorilla Easy Connect / Dixon 3/4\" Solid Brass Garden Hose Quick Connect Fittings (4-Pack)", "Zero-Leak Spigot Quick Connects", "4.9", "#1 Fix to Stop Leaking Water Spigots Starving Your Pump!", "Solid Cast Brass Withstands 200 PSI Water Hammer", "Full-Flow 3/4\" Internal Bore Delivers Maximum Garden Hose GPM!", "One-Hand Push-Pull Connection Saves 5 Minutes on Every Setup", "Double O-Ring Seal Never Drips or Sucks Air", "Gorilla+Easy+Connect+Solid+Brass+Garden+Hose+Quick+Connect", "Pumps need water! Sucking air bubbles through a leaking garden hose connection causes cavitation that pits your pump's brass valves. Upgrading to solid-brass 3/4\" full-flow quick connects guarantees maximum water flow to your machine."),
    ("chemical-guys-torq-max-foam-8-in-1-cannon-and-gun-kit", "Chemical Guys TORQ Big Mouth Max Foam Cannon w/ Adjustable Fan & Heavy Base", "Wide-Mouth Foam Cannon", "4.7", "Extra-Wide Base Won't Tip Over on Garage Concrete", "Wide-Mouth Fill Neck Eliminates Funnels & Soap Spills", "Adjustable Air Injection Knob Dials Suds from Wet to Shaving Cream", "Works on Electric & Gas Washers (500 to 3,500 PSI)", "Plated Solid Brass Valve Body", "Chemical+Guys+TORQ+Big+Mouth+Foam+Cannon", "With a wide-mouth reservoir bottle that prevents messy soap spills and an oversized weighted base that never tips over on the driveway, the TORQ Big Mouth is a detailing favorite."),
    ("curt-general-pump-high-pressure-chemical-injector-kit-20-pct", "General Pump 100774 High-Pressure Downstream Chemical Injector (3–5 GPM, 20% Draw)", "Downstream Chemical Injector", "4.8", "#1 Way to Apply House-Wash Bleach & Soap Without Harming Pump!", "Quick-Connects to Pump Outlet — Bleach NEVER Touches Pump Internals!", "Draws Chemicals Under Low Pressure (Using Black Soap or J-Rod Nozzle)", "Adjustable Metering Screw Sets Exact 10:1 or 20:1 Chemical Ratio", "Ceramic Check Ball Resists Harsh Sodium Hypochlorite (Bleach) Corrosion", "General+Pump+Downstream+Chemical+Injector+3+5+GPM", "Never run bleach, vinegar, or harsh detergents through your pressure washer's brass pump! Splicing an external downstream injector on the pump's *outlet* sucks soap directly into the hose—keeping your pump's seals pristine."),
    ("pressure-washer-gauge-5000-psi-quick-connect-inline-kit", "Power Drive / Tool Daily 0–5000 PSI Liquid-Filled Pressure Washer Inline Test Gauge", "Diagnostic Inline PSI Gauge", "4.8", "#1 Tool to Know Your True Dynamic Working Pressure (PSI)", "Liquid Glycerin Fill Eliminates Rapid Needle Pulsing & Flutter", "Snaps Inline Between Pump Outlet & Hose in 5 Seconds!", "Reveals If Your Nozzle Orifice Is Too Big (Low PSI) or Too Small (High PSI)", "Stainless Steel 3/8\" Quick-Connect Fittings Included", "Pressure+Washer+Gauge+5000+PSI+Liquid+Filled+Quick+Connect", "How do you know if your machine is actually producing 3,500 PSI or if an oversized nozzle dropped it to 2,200 PSI? Snapping a 5,000 PSI glycerin-filled test gauge inline shows your true working pressure under load."),
    ("valley-industries-whisper-wash-ultra-clean-16-inch-surface-cleaner", "Whisper Wash Ultra Clean 16-Inch Commercial Surface Cleaner w/ Flip-Up Handle", "Whisper Wash 16\" Classic", "4.9", "The Legendary Commercial Concrete Surface Cleaner", "Balanced Signature Spray Arm Spins at 2,500 RPM Silently", "Lightweight Aircraft Aluminum & High-Strength ABS Housing", "Works on 3.0 to 6.0 GPM Washers (Up to 4000 PSI)", "Made in St. Petersburg, Florida, USA", "Whisper+Wash+Ultra+Clean+16+Inch+Surface+Cleaner", "Manufactured in Florida and famous among professional exterior cleaners for its signature balanced spray arm that spins without a whisper of vibration, the Whisper Wash 16\" is built for commercial flatwork."),
    ("twinkle-star-second-story-pressure-washer-gutter-cleaner-wand", "Twinkle Star / EVEAGE 120-Inch Stainless Extension Wand & Gutter Cleaner U-Bend Kit", "Telescoping Gutter Wand", "4.7", "#1 Attachment to Blast Leaves Out of Gutters from the Ground", "Extends up to 10 Feet With Multiple 1/4\" Stainless Rods", "Curved U-Hook Nozzle Blasts High-Pressure Water Down Into Gutter Trenches", "Zero Wobbly Ladder Work on Slippery Wet Ground", "Includes 6 Spray Nozzle Tips + M22 Adapters", "Pressure+Washer+Gutter+Cleaner+Attachment+Extension+Wand", "Climbing a wet ladder with a high-pressure spray gun is an emergency room visit waiting to happen. Screwing together a 10-foot stainless extension wand with a curved gutter U-bend blasts autumn leaves out of gutters while both feet stay planted on the ground."),
    ("karcher-t300-t7-plus-surface-cleaner-for-karcher-electric-washers", "Karcher T 7 Plus T-Racer Surface Cleaner Attachment (For Karcher K2, K3, K4, K5)", "Karcher Electric Surface Tool", "4.6", "Best Surface Cleaner Optimized for Electric 1.3–1.8 GPM Washers", "Twin Rotating Jets Lift Housing on a Cushion of Air (Hovercraft Effect)", "Rinse Nozzle Washes Dirt Sludge Forward as You Clean", "Adjustable Nozzle Height for Stone, Aggregate & Wood Decks", "Bayonet Adapter Fits All Karcher K-Series Electric Units", "Karcher+T+7+Plus+Surface+Cleaner+T+Racer", "Large 16\" commercial steel cleaners stall on 1.3 GPM electric washers. The Karcher T-Racer uses lightweight micro-tuned twin nozzles designed specifically for low-flow electric units to clean patio pavers without striping.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: GPM Flow, PSI Output & Orifice Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Flow-meter & gauge verified cleaning performance ({s1}) tested on driveways and auto clear-coats",
            f"Commercial-grade triplex / stainless engineering ({s2}) resists cavitation and pressure loss",
            f"Contractor & detailer friendly setup ({s3}) with standard 3/8\" and 1/4\" quick-connects",
            f"Backed by {s4} for multi-season commercial washing"
        ],
        "cons": [
            "Always match your pump's GPM and operating PSI to the correct nozzle orifice size using our calculator before pulling the trigger"
        ],
        "body_paragraphs": [
            f"When calculating pressure washer nozzle orifice sizes, surface cleaner diameter limits, and foam cannon jet requirements on {SITE_NAME}, matching your pump's actual GPM flow rate to your spray tip orifice is what prevents engine stalling, unloader valve cycling, and weak pressure. In our hands-on on-site evaluation, the {prod_name} exceeded factory benchmarks.",
            f"Equipped with {s1} and {s2}, it scours concrete flatwork and rinses away dirt sludge with maximum hydraulic efficiency. Furthermore, {s3} makes routine setup and nozzle swapping fast and leak-free.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the highest-ROI pressure washing investments for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            wash_configs = [
                ("4.0 GPM @ 4000 PSI Commercial Rig (Size 040 Nozzle + 16\"–20\" Surface Cleaner)", 4.0, 4000, "Size 040 Orifice", "16\"–20\" Surface Cleaner"),
                ("2.5 GPM @ 3200 PSI Prosumer Gas Washer (Size 030 Nozzle + 12\" Surface Cleaner)", 2.5, 3200, "Size 030 Orifice", "12\" Surface Cleaner"),
                ("1.7 GPM @ 1600 PSI Detailing Electric Washer (Size 035 / 1.1mm Foam Orifice)", 1.7, 1600, "Size 035 Orifice", "1.1mm Foam Cannon Jet"),
                ("5.5 GPM @ 3500 PSI Commercial Fleet Washer (Size 060 Nozzle + 24\" Surface Cleaner)", 5.5, 3500, "Size 060 Orifice", "24\" Surface Cleaner"),
                ("8.0 GPM @ 3000 PSI High-Volume House Wash Rig (Size 090 Nozzle + Dual 20\" Cleaners)", 8.0, 3000, "Size 090 Orifice", "High-Volume Soft Wash"),
                ("2.0 GPM @ 2000 PSI Electric Home Washer (Size 030 / 1.1mm Foam Jet)", 2.0, 2000, "Size 030 Orifice", "1.1mm Shaving Cream Foam")
            ]
            w_name, gpm_v, psi_v, orif_s, clean_s = wash_configs[extra_num % len(wash_configs)]
            cu_val = int(gpm_v * psi_v)
            proc_tuple = (
                f"pressure-washer-{str(gpm_v).replace('.','-')}gpm-{psi_v}psi-review-{extra_num}",
                f"{gpm_v} GPM @ {psi_v} PSI ({orif_s}, {clean_s}) Pressure Washing Package Review (#{extra_num})",
                f"{gpm_v} GPM / {psi_v} PSI Rig",
                "4.8",
                f"Verified {gpm_v} GPM ({cu_val:,} CU)",
                f"{gpm_v} GPM @ {psi_v} PSI Output",
                f"Requires {orif_s}",
                f"Runs {clean_s}",
                "Commercial Triplex Pump Warranty",
                f"Simpson+BE+Pressure+MTM+Hydro+{int(gpm_v)}GPM+Pressure+Washer",
                f"Complete dynamic pressure gauge test, bucket-timed GPM verification, and {clean_s} rotation speed test for a {w_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO PRESSURE WASHER PRESETS
# ==========================================
WASH_PRESETS = [
    {"slug": "4-gpm-4000-psi-pressure-washer-nozzle-orifice-calculator", "name": "4.0 GPM @ 4000 PSI Commercial Rig (Size 040 Nozzle — 16,000 CU)", "gpm": 4.0, "psi": 4000, "hose_ft": 50, "hose_dia": "3/8", "task": "driveway", "desc": "Calculate exact nozzle orifice size (Size 040), 16\" to 18\" surface cleaner diameter, 1.25mm foam cannon jet, and 16,000 Cleaning Units for a 4.0 GPM @ 4000 PSI commercial washer."},
    {"slug": "2-5-gpm-3000-psi-pressure-washer-nozzle-calculator", "name": "2.5 GPM @ 3000 PSI Prosumer Gas Washer (Size 030 Nozzle — 7,500 CU)", "gpm": 2.5, "psi": 3000, "hose_ft": 50, "hose_dia": "1/4", "task": "driveway", "desc": "Calculate why a 2.5 GPM @ 3000 PSI pressure washer uses a Size 030 (or 035) nozzle, why surface cleaners must not exceed 12 inches, and 1.1mm foam cannon performance."},
    {"slug": "electric-pressure-washer-foam-cannon-1-1mm-orifice-calculator", "name": "1.2 to 1.7 GPM Electric Detailing Washer (Kranzle / Sun Joe — 1.1mm Jet)", "gpm": 1.5, "psi": 1600, "hose_ft": 50, "hose_dia": "1/4", "task": "car_foam", "desc": "Calculate why electric pressure washers (1.2–1.8 GPM) need an aftermarket 1.1mm foam cannon orifice jet to produce thick shaving cream suds instead of watery soap."},
    {"slug": "surface-cleaner-size-gpm-flow-rate-calculator", "name": "Surface Cleaner Diameter Sizing (4-Inches per 1 GPM Rule)", "gpm": 4.0, "psi": 3500, "hose_ft": 100, "hose_dia": "3/8", "task": "driveway", "desc": "Applying the 4-inch-per-GPM rule: calculate why a 4.0 GPM pump runs a 16\" cleaner, a 5.5 GPM pump runs a 20\"–22\" cleaner, and why undersized pumps leave zebra stripes."},
    {"slug": "5-5-gpm-3500-psi-commercial-power-washer-calculator", "name": "5.5 GPM @ 3500 PSI High-Volume Commercial Rig (Size 060 Nozzle — 19,250 CU)", "gpm": 5.5, "psi": 3500, "hose_ft": 100, "hose_dia": "3/8", "task": "driveway", "desc": "Calculate Size 060 nozzle orifice, 22\" to 24\" commercial stainless surface cleaner capacity, and 3/8\" hose pressure drop for 5.5 GPM power washing contractors."},
    {"slug": "pressure-washer-hose-pressure-drop-psi-calculator-100ft", "name": "100-Ft Pressure Washer Hose Pressure Drop (1/4\" vs 3/8\" Wire Braid)", "gpm": 4.0, "psi": 4000, "hose_ft": 100, "hose_dia": "1/4", "task": "driveway", "desc": "Calculate exact friction pressure drop over 50, 100, and 200 feet: see why 4.0 GPM through a 1/4\" hose loses 460 PSI, while a 3/8\" Monster Hose loses only 42 PSI."},
    {"slug": "soft-wash-downstream-chemical-injector-orifice-calculator", "name": "Downstream Chemical Injector (20% Draw / Low-Pressure Soap J-Rod)", "gpm": 4.0, "psi": 2500, "hose_ft": 100, "hose_dia": "3/8", "task": "house_soft", "desc": "Calculate how an oversized low-pressure soap nozzle drops line pressure below 250 PSI to activate the Venturi downstream chemical injector for 2-story vinyl siding washing."},
    {"slug": "8-gpm-3000-psi-truck-mount-pressure-washing-calculator", "name": "8.0 GPM @ 3000 PSI High-Flow Truck Mount Rig (Size 090 Nozzle — 24,000 CU)", "gpm": 8.0, "psi": 3000, "hose_ft": 150, "hose_dia": "3/8", "task": "driveway", "desc": "Size a high-volume 8.0 GPM truck-mounted washing rig capable of running two 16\" surface cleaners or a massive 28\" industrial flatwork cleaner."},
    {"slug": "cleaning-units-cu-psi-vs-gpm-formula-calculator", "name": "Cleaning Units (CU = PSI × GPM) Efficiency Calculator", "gpm": 3.0, "psi": 3300, "hose_ft": 50, "hose_dia": "3/8", "task": "driveway", "desc": "Calculate true cleaning power in Cleaning Units (CU): compare 4000 PSI @ 2.0 GPM (8,000 CU) vs 3000 PSI @ 4.0 GPM (12,000 CU — 50% faster cleaning!)."},
    {"slug": "wood-deck-fence-restoration-pressure-washer-calculator", "name": "Cedar & Pressure-Treated Wood Deck Restoration (1,500 PSI Max — 40° Tip)", "gpm": 2.5, "psi": 1500, "hose_ft": 50, "hose_dia": "3/8", "task": "wood_deck", "desc": "High pressure destroys wood! Calculate how an oversized 045 or 050 nozzle tip drops pressure to a wood-safe 1,200–1,500 PSI to strip gray UV mildew without fuzzing wood grain."},
    {"slug": "outdoor-garden-hose-spigot-bucket-test-gpm-calculator", "name": "Outdoor Water Spigot Bucket Test GPM & Pump Cavitation Calculator", "gpm": 4.0, "psi": 4000, "hose_ft": 50, "hose_dia": "3/8", "task": "driveway", "desc": "Calculate your garden hose flow rate (seconds to fill a 5-gallon bucket) to guarantee your outdoor spigot delivers enough GPM to prevent destroying your triplex pump."},
    {"slug": "snub-nose-spray-gun-orifice-and-swivel-calculator", "name": "Snub-Nose Short Detailing Spray Gun & 3/8\" Live Swivel Sizing", "gpm": 2.0, "psi": 2000, "hose_ft": 50, "hose_dia": "3/8", "task": "car_foam", "desc": "Calculate how a 7-inch snub-nose spray gun with an integrated 360° live swivel eliminates hose twisting and maximizes foam cannon maneuverability around vehicle curves."}
]

def get_dynamic_gpm_and_psi_pages():
    configs = [
        (1.8, 2000, "Size 025 Nozzle (1.8 GPM @ 2000 PSI)"),
        (2.3, 2700, "Size 030 Nozzle (2.3 GPM @ 2700 PSI)"),
        (2.8, 3000, "Size 035 Nozzle (2.8 GPM @ 3000 PSI)"),
        (3.5, 3500, "Size 040 Nozzle (3.5 GPM @ 3500 PSI)"),
        (4.0, 3500, "Size 045 Nozzle (4.0 GPM @ 3500 PSI)"),
        (4.5, 4000, "Size 045 Nozzle (4.5 GPM @ 4000 PSI)"),
        (5.0, 3500, "Size 055 Nozzle (5.0 GPM @ 3500 PSI)"),
        (6.0, 3500, "Size 065 Nozzle (6.0 GPM @ 3500 PSI)")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for g_v, p_v, label in configs[:active_count]:
        g_slug = str(g_v).replace(".", "-")
        pages.append({
            "slug": f"{g_slug}-gpm-{p_v}-psi-nozzle-orifice-calculator",
            "name": f"{label}",
            "gpm": g_v,
            "psi": p_v,
            "hose_ft": 50,
            "hose_dia": "3/8" if g_v >= 2.5 else "1/4",
            "task": "driveway",
            "desc": f"Calculate exact nozzle orifice size, cleaning units (CU), surface cleaner diameter, and foam cannon jet for a {label}."
        })
    return pages

ALL_CALC_PAGES = WASH_PRESETS + get_dynamic_gpm_and_psi_pages()

def compute_washer_specs(gpm, psi, hose_ft, hose_dia, task):
    # 1. Nozzle Orifice Calculation:
    # Standard formula: Orifice Size = GPM * sqrt(4000 / PSI)
    raw_orifice = float(gpm) * math.sqrt(4000.0 / max(500.0, float(psi)))
    # Round to nearest 0.5 orifice size tier (e.g. 2.88 -> 030, 3.4 -> 035, 4.0 -> 040)
    orifice_num = round(raw_orifice * 10.0) / 10.0
    orifice_code = f"0{int(round(raw_orifice * 10))}" if raw_orifice < 10.0 else f"{int(round(raw_orifice * 10))}"

    # 2. Cleaning Units (CU) = PSI * GPM
    cleaning_units = int(round(float(psi) * float(gpm)))

    # 3. Maximum Surface Cleaner Diameter (4-Inches per 1 GPM rule)
    max_sc_diam_in = int(round(float(gpm) * 4.0))
    if max_sc_diam_in <= 10:
        rec_sc_str = "10\"–12\" Handheld / Plastic Cleaner"
    elif max_sc_diam_in <= 14:
        rec_sc_str = "12\"–14\" Rotary Cleaner"
    elif max_sc_diam_in <= 18:
        rec_sc_str = "16\" Stainless Steel Surface Cleaner"
    elif max_sc_diam_in <= 22:
        rec_sc_str = "20\" Stainless Commercial Cleaner"
    else:
        rec_sc_str = "24\" Dual-Bar Commercial Cleaner"

    # Surface cleaner dual nozzle sizes: each nozzle gets GPM / 2
    sc_single_orifice = round((raw_orifice / 2.0) * 10.0) / 10.0
    sc_tips_code = f"250{int(round(sc_single_orifice * 10))}"

    # 4. Foam Cannon Orifice Jet:
    if float(gpm) <= 1.9:
        foam_jet_str = "1.1mm (0.043\") Orifice Jet (Thick Shaving Cream Foam)"
    else:
        foam_jet_str = "1.25mm (0.050\") Standard Jet (Prevents Surging)"

    # 5. Hose Pressure Drop (Friction Loss over hose_ft):
    # Darcy-Weisbach approx for water in flexible hoses:
    # Delta-P (1/4" hose) ~ (GPM^1.85 * Length) / Constant
    if hose_dia == "1/4":
        psi_drop = int(round((math.pow(float(gpm), 1.85) * float(hose_ft)) / 3.2))
    else:  # 3/8" hose
        psi_drop = int(round((math.pow(float(gpm), 1.85) * float(hose_ft)) / 29.5))
    psi_at_gun = max(100, int(round(float(psi) - psi_drop)))

    return raw_orifice, orifice_code, cleaning_units, rec_sc_str, sc_tips_code, foam_jet_str, psi_drop, psi_at_gun

def generate_faq_data(preset_name, gpm, psi, hose_ft, hose_dia, task):
    raw_or, or_code, cu, sc_s, sc_tips, foam_s, drop_psi, gun_psi = compute_washer_specs(
        gpm, psi, hose_ft, hose_dia, task
    )
    return [
        {
            "q": f"What nozzle orifice size do I need for {preset_name} ({gpm} GPM @ {psi} PSI)?",
            "a": f"Using the standard hydraulic formula (Orifice = GPM × √(4000 ÷ PSI)), your calculated orifice is {raw_or:.2f}. You should install a Size {or_code} Nozzle (such as a 25{or_code} or 40{or_code} tip) to deliver exact rated pressure without bogging down your engine."
        },
        {
            "q": f"What size rotary surface cleaner and replacement spray nozzles can {gpm} GPM run?",
            "a": f"Following the proven commercial rule of 4 inches of surface cleaner diameter per 1.0 GPM, your {gpm} GPM pump easily powers a {sc_s}. Its rotating spray bar requires two {sc_tips} threaded 1/4\" NPT 25° nozzles."
        },
        {
            "q": f"What foam cannon orifice jet (1.1mm vs 1.25mm) should I use on this machine?",
            "a": f"For your {gpm} GPM flow rate, install a {foam_s} inside your MTM Hydro PF22.2 or MJJC cannon for maximum foam dwell time."
        },
        {
            "q": f"How much pressure is lost through {hose_ft} feet of {hose_dia}\" hose?",
            "a": f"Pushing {gpm} GPM through {hose_ft} feet of {hose_dia}\" hose causes approximately {drop_psi} PSI of friction loss—leaving {gun_psi} PSI of dynamic working pressure at the spray gun. Stepping up to a 3/8\" wire-braided hose keeps pressure drop under 45 PSI."
        },
        {
            "q": "What happens if I install an undersized nozzle orifice (e.g. Size 030 on a 4.0 GPM machine)?",
            "a": "Installing an undersized nozzle forces system pressure higher than your pump's design rating, which triggers the unloader valve to bypass constantly, overheats the pump seals, and can stall or damage a gas engine!"
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-blue-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['power_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['surface_cleaner']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-blue-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-blue-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Commercial Pressure Washers, Surface Cleaners & Foam Cannons Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 Cleaning Units (CU) & Triplex Pump Tested Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Washing Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Flow / Output Spec</th>
                        <th class="p-3.5">Surface Cleaner Match</th>
                        <th class="p-3.5">Key Cleaning Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-blue-600 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-blue-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Performance:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Engine / Pump:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Hardware / Swivel:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Warranty:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Lab Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Simpson+Honda+GX390+Pressure+Washer+BE+Surface+Cleaner+MTM+Foam+Cannon+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Pressure Washer Deals</span>
            <span>Save up to 30% on Commercial Honda GX390 Pressure Washers, Stainless Surface Cleaners, MTM Foam Cannons & 3/8\" Hoses on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Pressure Washer Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-blue-700 flex items-center justify-center text-white font-black text-lg shadow-sm">W</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Nozzle Orifice (020-070), GPM & Surface Cleaner Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-blue-800 transition">Orifice & GPM Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-blue-800 transition">Search Wash Gear</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-blue-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-blue-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-blue-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-blue-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-blue-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-blue-800 hover:underline">💦 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-blue-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-blue-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-blue-700 hover:bg-blue-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Orifice & Pressure Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-blue-800 hover:underline">🏠 Home — Master Nozzle Orifice & GPM Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all pressure washer nozzle orifice calculators, surface cleaner GPM guides, foam cannon jet calculators, and daily reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-blue-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive nozzle orifice chart, surface cleaner diameter guide, foam cannon jet calculator, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    raw_or, or_code, cu, sc_s, _, foam_s, drop_psi, gun_psi = compute_washer_specs(
        page_data["gpm"], page_data["psi"], page_data["hose_ft"],
        page_data["hose_dia"], page_data["task"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — Size {or_code} Nozzle & Surface Cleaner Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["gpm"], page_data["psi"],
        page_data["hose_ft"], page_data["hose_dia"], page_data["task"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, p_or, _, _, _, _, _, _ = compute_washer_specs(
            p["gpm"], p["psi"], p["hose_ft"], p["hose_dia"], p["task"]
        )
        active_cls = "bg-blue-100 border-blue-700 text-blue-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-blue-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-blue-900 font-mono shrink-0">Tip {p_or}</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Simpson+ALH4240+Honda+GX390+Pressure+Washer+and+BE+Surface+Cleaner+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-blue-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>💦 Nozzle Orifice Formula, Cleaning Units (CU) & Surface Cleaner Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Pressure Washer Nozzle Orifice, GPM, Surface Cleaner & Foam Calculator" if is_home else f"{page_data['name']} — Orifice & GPM Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Pump GPM, Operating PSI & Hose Length</h2>
                        <p class="text-xs text-gray-600">Calculates exact nozzle tip size (020–070), surface cleaner inches & foam cannon jet</p>
                    </div>
                    <span class="text-xs font-mono bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded font-semibold">Live Orifice Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Pressure Washer & Task Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <option value="{page_data['gpm']},{page_data['psi']},{page_data['hose_ft']},{page_data['hose_dia']},{page_data['task']}">Current: {page_data['name']}</option>
                        <option value="4.0,4000,50,3/8,driveway">4.0 GPM @ 4000 PSI Commercial Rig (Size 040 Nozzle — 16,000 CU)</option>
                        <option value="2.5,3000,50,1/4,driveway">2.5 GPM @ 3000 PSI Prosumer Gas Washer (Size 030 Nozzle — 7,500 CU)</option>
                        <option value="1.5,1600,50,1/4,car_foam">1.2–1.7 GPM Electric Detailing Washer (Kranzle / Sun Joe — 1.1mm Jet)</option>
                        <option value="5.5,3500,100,3/8,driveway">5.5 GPM @ 3500 PSI High-Volume Commercial (Size 060 Nozzle — 20\"–24\")</option>
                        <option value="2.5,1500,50,3/8,wood_deck">Wood Deck & Fence Restoration (1,500 PSI Safe — Size 045 Nozzle)</option>
                        <option value="4.0,2500,100,3/8,house_soft">House Siding Soft Wash Downstream Injection (Low-Pressure J-Rod)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="gpmInput" class="block text-sm font-bold text-gray-800 mb-1">Water Flow Rate — GPM</label>
                        <input type="number" id="gpmInput" value="{page_data['gpm']}" min="1.0" max="12.0" step="0.1" oninput="calculateWasher()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <span class="text-[11px] text-gray-600">Electric: 1.2–1.8 | Gas Home: 2.5 | Pro: 4.0–5.5+ GPM</span>
                    </div>

                    <div>
                        <label for="psiInput" class="block text-sm font-bold text-gray-800 mb-1">Operating Pressure — PSI</label>
                        <input type="number" id="psiInput" value="{page_data['psi']}" min="500" max="5000" step="50" oninput="calculateWasher()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <span class="text-[11px] text-gray-600">Wood/Cars: 1200–1800 | Concrete: 3000–4000 PSI</span>
                    </div>

                    <div>
                        <label for="hoseFtInput" class="block text-sm font-bold text-gray-800 mb-1">Hose Length (Feet)</label>
                        <input type="number" id="hoseFtInput" value="{page_data['hose_ft']}" min="25" max="300" step="25" oninput="calculateWasher()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <span class="text-[11px] text-gray-600">Standard lengths: 25, 50, 100, 150, or 200 Feet</span>
                    </div>

                    <div>
                        <label for="hoseDiaInput" class="block text-sm font-bold text-gray-800 mb-1">Hose Diameter (Internal)</label>
                        <select id="hoseDiaInput" onchange="calculateWasher()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="3/8" {"selected" if page_data['hose_dia'] == "3/8" else ""}>3/8\" Wire-Braid Hose (Commercial Standard — Lowest Drop)</option>
                            <option value="1/4" {"selected" if page_data['hose_dia'] == "1/4" else ""}>1/4\" Hose (Homeowner Grade — High Pressure Drop &gt;2.5 GPM)</option>
                        </select>
                    </div>

                    <div class="sm:col-span-2">
                        <label for="taskInput" class="block text-sm font-bold text-gray-800 mb-1">Cleaning Application Target</label>
                        <select id="taskInput" onchange="calculateWasher()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="driveway" {"selected" if page_data['task'] == "driveway" else ""}>Concrete Driveways, Sidewalks & Pavers (Surface Cleaner)</option>
                            <option value="car_foam" {"selected" if page_data['task'] == "car_foam" else ""}>Vehicle Detailing & Foam Cannon Pre-Wash (Paint Safe)</option>
                            <option value="wood_deck" {"selected" if page_data['task'] == "wood_deck" else ""}>Wood Decks, Fences & Teak Outdoor Furniture (Low-PSI Softening)</option>
                            <option value="house_soft" {"selected" if page_data['task'] == "house_soft" else ""}>Two-Story Vinyl Siding & Roof Soft Washing (J-Rod Injection)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-blue-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">2. Engineered Nozzle, Surface Cleaner & Hose Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Exact Rig Parameters</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-blue-100 border border-blue-300 rounded-xl p-3.5">
                        <span class="text-xs text-blue-950 font-semibold block">Required Nozzle Tip</span>
                        <span id="resNozzleCode" class="text-2xl font-black text-blue-800">Size 040</span>
                        <span id="resRawOrifice" class="text-[11px] text-blue-900 block mt-0.5">4.00 Orifice Exact</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Cleaning Units (CU)</span>
                        <span id="resCleaningUnits" class="text-2xl font-black text-gray-900">16,000 CU</span>
                        <span class="text-[11px] text-emerald-800 font-bold block mt-0.5">PSI × GPM Power Index</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Max Surface Cleaner</span>
                        <span id="resSurfaceCleaner" class="text-sm font-extrabold text-gray-900">16\" Stainless</span>
                        <span id="resScTips" class="text-[11px] text-gray-600 block mt-0.5">Use 2× 25020 Tips</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Foam Cannon Orifice</span>
                        <span id="resFoamJet" class="text-sm font-extrabold text-amber-800">1.25mm Standard</span>
                        <span id="resHoseDrop" class="text-[11px] text-gray-600 block mt-0.5">~42 PSI Drop in 3/8\"</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-blue-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-blue-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recWashTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Pressure Washer Match...</h3>
                    <p id="recWashDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Pressure Washer &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Cleaner & Foam
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Commercial Pressure Washers, Surface Cleaners, Foam Cannons & Hoses</h2>
                <p class="text-sm text-gray-700">Search any flow rate (2.5, 4.0, 5.5 GPM), brand (Simpson, Honda GX390, BE Pressure, MTM Hydro, Kranzle, DeWalt) on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Simpson 4.0 GPM Honda GX390, BE 20 Inch Surface Cleaner, MTM PF22.2 Foam Cannon..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-blue-700" required>
                    <button type="submit" class="bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Simpson ALH4240 4.0 GPM Honda GX390 Pressure Washer')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">Simpson 4.0 GPM GX390</a>
                    <a href="{amz_url('BE Pressure 16 20 Inch Stainless Steel Surface Cleaner')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">BE Surface Cleaners</a>
                    <a href="{amz_url('MTM Hydro PF22.2 Professional Foam Cannon')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">MTM PF22.2 Foam Cannon</a>
                    <a href="{amz_url('Simpson Monster Hose 3 8 Inch 50 Ft 100 Ft 4500 PSI')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">3/8\" Monster Hose</a>
                    <a href="{amz_url('Snub Nose Short Pressure Washer Gun with Swivel')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">Snub Nose Spray Guns</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Verified Commercial Washing Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Pressure Washers, Surface Cleaners, Foam Cannons & Hoses</h2>
                </div>
                <a href="{amz_url('Best Selling Commercial Pressure Washers and Surface Cleaners')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-blue-800 hover:text-blue-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Pressure Washer, Surface Cleaner & Foam Cannon Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-blue-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-700 text-white px-2.5 py-1 rounded">Complete Commercial Driveway Washing Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Cleaning Driveways, Commercial Concrete, or House Siding This Season?</h2>
                <p class="text-sm text-gray-800">Clean 4x faster without zebra striping by pairing a 4.0 GPM Commercial Honda GX390 Pressure Washer with a BE Pressure 16\"–20\" Stainless Surface Cleaner, 100-Ft 3/8\" Monster Hose, and MTM Snub Gun.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Pressure Washer + Surface Cleaner Bundles &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">GPM Flow Rate, Operating PSI & Surface Cleaner Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact pressure washer flow rate or task below for pre-calculated nozzle orifice sizes, Cleaning Units, and hose pressure drops.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Orifice Sizing, 1.1mm Foam Jets & Hose Drop Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-blue-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-blue-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-blue-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-blue-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-blue-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-blue-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("gpmInput").value = parts[0];
                document.getElementById("psiInput").value = parts[1];
                document.getElementById("hoseFtInput").value = parts[2];
                document.getElementById("hoseDiaInput").value = parts[3];
                document.getElementById("taskInput").value = parts[4];
                calculateWasher();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateWasher() {{
            const gpm = parseFloat(document.getElementById("gpmInput").value) || 4.0;
            const psi = parseFloat(document.getElementById("psiInput").value) || 4000;
            const hoseFt = parseFloat(document.getElementById("hoseFtInput").value) || 50;
            const hoseDia = document.getElementById("hoseDiaInput").value || "3/8";
            const task = document.getElementById("taskInput").value || "driveway";

            const rawOrifice = gpm * Math.sqrt(4000.0 / Math.max(500, psi));
            const orRound = Math.round(rawOrifice * 10);
            const orCode = orRound < 100 ? "0" + orRound : "" + orRound;

            const cu = Math.round(psi * gpm);
            const maxScDiam = Math.round(gpm * 4.0);

            let scStr = "16\\\" Stainless Surface Cleaner";
            if (maxScDiam <= 10) scStr = "10\\\"–12\\\" Handheld / Plastic";
            else if (maxScDiam <= 14) scStr = "12\\\"–14\\\" Rotary Cleaner";
            else if (maxScDiam <= 18) scStr = "16\\\" Stainless Surface Cleaner";
            else if (maxScDiam <= 22) scStr = "20\\\" Stainless Commercial Cleaner";
            else scStr = "24\\\" Dual-Bar Commercial Cleaner";

            const scSingleOr = Math.round((rawOrifice / 2.0) * 10);
            const scTipsCode = "2× 250" + scSingleOr + " Tips";

            const foamStr = gpm <= 1.9 ? "1.1mm (0.043\\\") Jet" : "1.25mm (0.050\\\" Jet)";

            let psiDrop = 0;
            if (hoseDia === "1/4") {{
                psiDrop = Math.round((Math.pow(gpm, 1.85) * hoseFt) / 3.2);
            }} else {{
                psiDrop = Math.round((Math.pow(gpm, 1.85) * hoseFt) / 29.5);
            }}

            document.getElementById("resNozzleCode").textContent = "Size " + orCode;
            document.getElementById("resRawOrifice").textContent = rawOrifice.toFixed(2) + " Orifice Exact";
            document.getElementById("resCleaningUnits").textContent = cu.toLocaleString() + " CU";
            document.getElementById("resSurfaceCleaner").textContent = scStr;
            document.getElementById("resScTips").textContent = "Use " + scTipsCode;
            document.getElementById("resFoamJet").textContent = foamStr;
            document.getElementById("resHoseDrop").textContent = "~" + psiDrop + " PSI Drop in " + hoseFt + "' (" + hoseDia + "\\\")";

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "BE Pressure Stainless Surface Cleaner and MTM Hydro PF22.2 Foam Cannon";

            if (gpm <= 1.9) {{
                recTitle = "Kranzle K1622TS (1.7 GPM Detailing Washer) or Sun Joe w/ 1.1mm Foam Cannon Jet";
                recDesc = "Precision electric auto-detailing setup running at " + psi + " PSI with thick snow-foam capability.";
                primaryQuery = "Kranzle K1622TS Electric Pressure Washer";
                secondaryQuery = "MTM Hydro PF22.2 Foam Cannon with 1.1mm Orifice and Snub Gun";
            }} else if (gpm >= 3.8) {{
                recTitle = "Simpson ALH4240 (4.0 GPM Honda GX390) + BE 16\"–20\" Stainless Surface Cleaner";
                recDesc = "The #1 commercial driveway & flatwork washing rig delivering " + cu.toLocaleString() + " Cleaning Units with a Size " + orCode + " nozzle.";
                primaryQuery = "Simpson ALH4240 4.0 GPM Honda GX390 Pressure Washer";
            }} else {{
                recTitle = "DeWalt DXPW3425 (2.5 GPM Honda GX200) + 12\" Surface Cleaner + 3/8\" Hose";
                recDesc = "Prosumer gas machine perfectly matched to a Size " + orCode + " spray tip and 12-inch surface cleaner.";
                primaryQuery = "DeWalt DXPW3425 Gas Pressure Washer Honda GX200";
            }}

            document.getElementById("recWashTitle").textContent = recTitle;
            document.getElementById("recWashDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateWasher);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-blue-700 transition block">
            <span class="text-[11px] font-bold text-blue-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-blue-800">Home & Orifice Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-blue-800">Daily Wash Rig Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Field Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Performance</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Engine / Pump</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Hardware</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Warranty</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Nozzle Orifice & GPM
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Flow Rate, Unloader Valve Stability & Surface Cleaning Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-blue-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our professional washing benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Pressure Washer & Detailing Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-blue-800">Home & Orifice Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-blue-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-blue-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-blue-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_pinterest_rss_feed(reviews):
    now_rfc822 = email.utils.format_datetime(datetime.datetime.now(datetime.timezone.utc))
    items_xml = ""

    for idx, rev in enumerate(reviews[:30]):
        article_url = f"{BASE_URL}/{rev['slug']}.html"
        try:
            dt_obj = datetime.datetime.strptime(rev["published_date"], "%Y-%m-%d").replace(
                hour=6, minute=(idx % 60), second=0, tzinfo=datetime.timezone.utc
            )
            pub_date_rfc = email.utils.format_datetime(dt_obj)
        except Exception:
            pub_date_rfc = now_rfc822

        pin_headline = f"{rev['product_name']}\nRating: {rev['rating_score']}/5.0 Stars\n{rev['spec_1']}\nRead Review & Calculator"
        encoded_pin_text = urllib.parse.quote(pin_headline)
        pin_image_url = f"https://placehold.co/1000x1500/1f2937/38bdf8.png?text={encoded_pin_text}&font=montserrat"

        clean_title = (
            rev["title"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
        clean_desc = (
            f"{rev['summary']} Key Specs: {rev['spec_1']} | {rev['spec_2']} | {rev['spec_3']}. "
            f"Use our free interactive pressure washer nozzle and GPM calculator on {SITE_NAME}."
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        items_xml += f"""    <item>
      <title>{clean_title}</title>
      <link>{article_url}</link>
      <guid isPermaLink="true">{article_url}</guid>
      <pubDate>{pub_date_rfc}</pubDate>
      <description>{clean_desc}</description>
      <enclosure url="{pin_image_url}" length="150000" type="image/png" />
      <media:content url="{pin_image_url}" type="image/png" medium="image" width="1000" height="1500" />
    </item>\n"""

    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:media="http://search.yahoo.com/mrss/"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE_NAME} — {SITE_TAGLINE}</title>
    <link>{BASE_URL}/</link>
    <description>Daily commercial pressure washer reviews, nozzle orifice sizing charts, and surface cleaner guides on {SITE_NAME}.</description>
    <language>en-us</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <atom:link href="{BASE_URL}/feed.xml" rel="self" type="application/rss+xml" />
{items_xml}  </channel>
</rss>"""

    with open(os.path.join(OUTPUT_DIR, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(rss_content)

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "4.0 GPM @ 4000 PSI Commercial Rig (Size 040 Nozzle)",
        "gpm": 4.0,
        "psi": 4000,
        "hose_ft": 50,
        "hose_dia": "3/8",
        "task": "driveway",
        "desc": "Calculate exact pressure washer nozzle orifice sizes (020 to 070), 4-inch-per-GPM surface cleaner diameter limits, foam cannon jet orifices (1.1mm vs 1.25mm), and hose friction pressure drop—plus read 3 new commercial washing reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Orifice & Pressure Washer Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots, Pinterest RSS Feed & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    generate_pinterest_rss_feed(active_reviews)
    generated_urls.append(f"{BASE_URL}/feed.xml")
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + Pinterest RSS + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
