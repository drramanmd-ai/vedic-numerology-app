from fpdf import FPDF
import datetime
import predictions as pred_engine
import numerology as num_engine

PLANET_NAMES = {
    1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu",
    5: "Mercury", 6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"
}

class VedicPDF(FPDF):
    def clean_text(self, txt):
        if isinstance(txt, str):
            return txt.replace('”', '"').replace('“', '"').replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
        return txt

    def cell(self, w=None, h=None, txt='', *args, **kwargs):
        txt = self.clean_text(txt)
        super().cell(w, h, txt, *args, **kwargs)

    def multi_cell(self, w, h=None, txt='', *args, **kwargs):
        txt = self.clean_text(txt)
        super().multi_cell(w, h, txt, *args, **kwargs)
    def header(self):
        # Violet accent bar at top
        self.set_fill_color(124, 58, 237)
        self.rect(0, 0, 210, 4, 'F')
        # Title
        self.set_y(8)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(124, 58, 237)
        self.cell(0, 10, 'Vedic Numerology Report', 0, 1, 'C')
        # Thin line under title
        self.set_draw_color(124, 58, 237)
        self.set_line_width(0.5)
        self.line(15, 19, 195, 19)
        self.ln(6)

    def footer(self):
        self.set_y(-12)
        self.set_font('Arial', 'I', 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}  |  Generated: {datetime.datetime.now().strftime("%d-%b-%Y %H:%M")}', 0, 0, 'C')
    
    def section_title(self, title, emoji=""):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(124, 58, 237)
        self.set_fill_color(245, 243, 255)
        full = f"  {emoji}  {title}" if emoji else f"  {title}"
        self.cell(0, 8, full, 0, 1, 'L', fill=True)
        self.ln(3)
    
    def label_value(self, label, value, label_w=45):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(55, 65, 81)
        self.cell(label_w, 6, label, 0, 0)
        self.set_font('Arial', '', 10)
        self.set_text_color(31, 41, 55)
        self.cell(0, 6, str(value), 0, 1)
    
    def body_text(self, text, indent=12):
        self.set_font('Arial', '', 9)
        self.set_text_color(55, 65, 81)
        self.set_x(indent)
        self.multi_cell(190 - (indent - 10), 4.5, text, 0, 'L')
    
    def bullet(self, text, indent=14):
        self.set_font('Arial', '', 9)
        self.set_text_color(55, 65, 81)
        self.set_x(indent)
        self.multi_cell(190 - (indent - 10), 4.5, f"  {text}", 0, 'L')


def draw_grid_at_xy(pdf, x, y, counts, maha=None, antar=None, pratyantar=None, root=None, destiny=None):
    """Draw Vedic 3x3 grid with colored TEXT on white background."""
    grid_layout = [
        [3, 1, 9],
        [6, 7, 5],
        [2, 8, 4]
    ]
    col_width = 15
    row_height = 8
    
    # Draw outer border
    pdf.set_draw_color(124, 58, 237)
    pdf.set_line_width(0.6)
    pdf.rect(x, y, col_width * 3, row_height * 3)
    pdf.set_line_width(0.2)
    
    current_y = y
    for row in grid_layout:
        pdf.set_xy(x, current_y)
        for cell in row:
            val_count = counts.get(cell, 0)
            text = f"{cell}" * val_count if val_count > 0 else "-"
            
            is_maha = (cell == maha)
            is_antar = (cell == antar)
            is_praty = (cell == pratyantar)
            is_destiny = (cell == destiny)
            is_root = (cell == root)
            
            # White background always
            pdf.set_fill_color(255, 255, 255)
            
            # Colored text based on role
            if is_praty:
                pdf.set_text_color(236, 72, 153)  # Pink
                pdf.set_font('Arial', 'B', 10)
            elif is_antar:
                pdf.set_text_color(217, 119, 6)  # Gold/Amber
                pdf.set_font('Arial', 'B', 10)
            elif is_maha:
                pdf.set_text_color(124, 58, 237)  # Violet
                pdf.set_font('Arial', 'B', 10)
            elif is_destiny:
                pdf.set_text_color(22, 163, 74)  # Green
                pdf.set_font('Arial', 'B', 10)
            elif is_root:
                pdf.set_text_color(37, 99, 235)  # Blue
                pdf.set_font('Arial', 'B', 10)
            elif val_count > 0:
                pdf.set_text_color(55, 65, 81)  # Dark gray
                pdf.set_font('Arial', '', 9)
            else:
                pdf.set_text_color(200, 200, 200)  # Light gray for empty
                pdf.set_font('Arial', '', 9)
                
            pdf.set_draw_color(221, 214, 254)
            pdf.cell(col_width, row_height, text, border=1, align='C', fill=True)
        current_y += row_height


def generate_general_pdf(name, dob_str, root, destiny, counts, active_combos, remedies, precautions, full_name_val):
    pdf = VedicPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Profile Summary Card
    pdf.section_title("Profile Summary", "")
    pdf.label_value("Full Name:", name)
    pdf.label_value("Date of Birth:", dob_str)
    pdf.label_value("Root Number:", f"{root}  ({PLANET_NAMES.get(root, '')})")
    pdf.label_value("Destiny Number:", f"{destiny}  ({PLANET_NAMES.get(destiny, '')})")
    pdf.label_value("Name Compound:", f"{full_name_val}")
    comp_info = pred_engine.COMPOUND_NUMBERS.get(full_name_val, {"aura": "-", "summary": "Unknown", "description": "", "notes": ""})
    pdf.label_value("Compound Aura:", "Positive (+)" if comp_info["aura"] == "+" else "Negative (-)")
    pdf.label_value("Compound Summary:", comp_info["summary"])
    
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(45, 5, "Compound Description:", 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(145, 4.5, comp_info["description"], 0, 'L')
    
    pdf.set_x(10)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(45, 5, "Actions/Remedies:", 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(145, 4.5, comp_info["notes"], 0, 'L')
    pdf.ln(4)
    
    # Natal Grid
    pdf.section_title("Natal Vedic Grid", "")
    grid_y = pdf.get_y()
    # Center the grid
    draw_grid_at_xy(pdf, 82, grid_y, counts, root=root, destiny=destiny)
    pdf.set_y(grid_y + 28)
    
    # Color legend
    pdf.set_font('Arial', 'I', 7)
    legend_items = [
        (37, 99, 235, "Blue = Root"),
        (22, 163, 74, "Green = Destiny"),
        (55, 65, 81, "Gray = Other")
    ]
    pdf.set_x(65)
    for r, g, b, label in legend_items:
        pdf.set_text_color(r, g, b)
        pdf.cell(25, 4, label, 0, 0, 'C')
    pdf.ln(6)
    
    # Traits Analysis
    pdf.section_title("Number Traits Analysis", "")
    for num in range(1, 10):
        cnt = counts.get(num, 0)
        if cnt > 0:
            if num == 1:
                if destiny == 1:
                    trait_key = "multiple_with_d1" if cnt > 1 else "d1_single"
                else:
                    trait_key = "multiple_no_d1" if cnt > 1 else "single"
                text = pred_engine.NUMBER_TRAITS[num][trait_key]
            elif num == 2:
                trait_key = "double" if cnt == 2 else ("multiple" if cnt > 2 else "single")
                text = pred_engine.NUMBER_TRAITS[num][trait_key]
            elif num in [4, 8]:
                trait_key = "even" if cnt % 2 == 0 else "odd"
                text = pred_engine.NUMBER_TRAITS[num][trait_key]
            elif num == 6:
                trait_key = "multiple_with_d6" if (cnt > 1 and destiny == 6) else ("multiple_no_d6" if cnt > 1 else "single")
                text = pred_engine.NUMBER_TRAITS[num][trait_key]
            else:
                trait_key = "multiple" if cnt > 1 else "single"
                text = pred_engine.NUMBER_TRAITS[num][trait_key]
            pdf.set_font('Arial', 'B', 9)
            pdf.set_text_color(124, 58, 237)
            pdf.set_x(12)
            pdf.cell(30, 5, f"Number {num} ({cnt}x):", 0, 0)
            pdf.set_font('Arial', '', 9)
            pdf.set_text_color(55, 65, 81)
            pdf.multi_cell(148, 5, text, 0, 'L')
            pdf.ln(1)
            
    pdf.ln(3)
    
    # Active Yogas
    pdf.section_title("Active Yogas & Grid Combinations", "")
    if active_combos:
        for combo in active_combos:
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(124, 58, 237)
            pdf.set_x(12)
            pdf.cell(0, 5, combo['name'], 0, 1)
            pdf.body_text(combo['desc'])
            pdf.ln(2)
    else:
        pdf.body_text('No major yogas active in the natal chart.')
        
    # Remedies & Precautions (new comprehensive section)
    pdf.add_page()
    pdf.section_title("Remedies & Crystal Therapy", "")
    
    root_rem = pred_engine.DETAILED_REMEDIES.get(root, {})
    dest_rem = pred_engine.DETAILED_REMEDIES.get(destiny, {})
    
    # Root Number Remedies
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 6, f"Root Number {root} - {root_rem.get('planet', '')}", 0, 1)
    pdf.ln(1)
    
    remedy_fields = [
        ("Mantra", "mantra"), ("Gemstone", "gemstone"), ("Crystal", "crystal"),
        ("Lucky Colors", "colors"), ("Fasting Day", "fasting_day"),
        ("Deity", "deity"), ("Donations", "donations"), ("Rituals", "rituals")
    ]
    for label, key in remedy_fields:
        val = root_rem.get(key, "")
        if val:
            pdf.set_font('Arial', 'B', 9)
            pdf.set_text_color(55, 65, 81)
            pdf.set_x(14)
            pdf.cell(28, 5, f"{label}:", 0, 0)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(148, 5, val, 0, 'L')
    
    pdf.ln(4)
    
    # Destiny Number Remedies
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(22, 163, 74)
    pdf.cell(0, 6, f"Destiny Number {destiny} - {dest_rem.get('planet', '')}", 0, 1)
    pdf.ln(1)
    
    for label, key in remedy_fields:
        val = dest_rem.get(key, "")
        if val:
            pdf.set_font('Arial', 'B', 9)
            pdf.set_text_color(55, 65, 81)
            pdf.set_x(14)
            pdf.cell(28, 5, f"{label}:", 0, 0)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(148, 5, val, 0, 'L')
    
    pdf.ln(4)
    
    # Precautions
    pdf.section_title("Precautions & Warnings", "")
    pdf.bullet(f"Root {root}: {precautions}")
    pdf.ln(2)
    pdf.bullet(f"Destiny {destiny}: {pred_engine.PRECAUTIONS.get(destiny, '')}")
    pdf.ln(4)
    
    # General Life Remedies
    pdf.section_title("General Life Remedies", "")
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 5, "Health & Wellness:", 0, 1)
    for tip in pred_engine.GENERAL_HEALTH_REMEDIES:
        pdf.bullet(tip)
    pdf.ln(3)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 5, "Business & Wealth:", 0, 1)
    for tip in pred_engine.GENERAL_BUSINESS_REMEDIES:
        pdf.bullet(tip)
    pdf.ln(3)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 5, "Relationships & Marriage:", 0, 1)
    for tip in pred_engine.GENERAL_RELATIONSHIP_REMEDIES:
        pdf.bullet(tip)
    
    # 1. Name Analysis Section
    pdf.add_page()
    pdf.section_title("Name Analysis & Spelling Correction Plan", "")
    
    first_name = name.split()[0] if name else ""
    name_analysis = pred_engine.analyze_name_compatibility(first_name, name, root, destiny)
    
    # First Name Compound info
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 6, f"First Name Compound: {name_analysis['first_val']} ({first_name})", 0, 1)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.set_x(14)
    pdf.cell(28, 5, "Vibration:", 0, 0)
    pdf.set_font('Arial', 'B', 9)
    if name_analysis["first_aura"] == "+":
        pdf.set_text_color(22, 163, 74) # Green
        pdf.cell(0, 5, "Positive (+)", 0, 1)
    else:
        pdf.set_text_color(220, 38, 38) # Red
        pdf.cell(0, 5, "Negative (-)", 0, 1)
        
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.set_x(14)
    pdf.cell(28, 5, "Summary:", 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 5, name_analysis["first_summary"], 0, 1)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_x(14)
    pdf.cell(28, 5, "Meaning:", 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.multi_cell(148, 4.5, name_analysis["first_desc"], 0, 'L')
    pdf.ln(3)
    
    # Full Name Compound info
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 6, f"Full Name Compound: {name_analysis['full_val']} ({name})", 0, 1)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.set_x(14)
    pdf.cell(28, 5, "Vibration:", 0, 0)
    pdf.set_font('Arial', 'B', 9)
    if name_analysis["full_aura"] == "+":
        pdf.set_text_color(22, 163, 74)
        pdf.cell(0, 5, "Positive (+)", 0, 1)
    else:
        pdf.set_text_color(220, 38, 38)
        pdf.cell(0, 5, "Negative (-)", 0, 1)
        
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.set_x(14)
    pdf.cell(28, 5, "Summary:", 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 5, name_analysis["full_summary"], 0, 1)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_x(14)
    pdf.cell(28, 5, "Meaning:", 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.multi_cell(148, 4.5, name_analysis["full_desc"], 0, 'L')
    pdf.ln(4)
    
    # Suggested Action
    if name_analysis["action"] != "No Change":
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(124, 58, 237)
        pdf.cell(32, 6, "Suggested Action:", 0, 0)
        
        if name_analysis["action"] == "Drop Last Name":
            pdf.set_text_color(217, 119, 6)
        else:
            pdf.set_text_color(220, 38, 38)
        pdf.cell(0, 6, name_analysis["action"], 0, 1)
        
        pdf.set_font('Arial', '', 9)
        pdf.set_text_color(55, 65, 81)
        comp_details = f"Compatibility check: Full name reduces to single digit {name_analysis['single_digit']}. "
        comp_details += f"Relationship with Root ({root}): {name_analysis['rel_root']}. "
        comp_details += f"Relationship with Destiny ({destiny}): {name_analysis['rel_dest']}."
        if name_analysis['comp_reason']:
            comp_details += f"\nReason: {name_analysis['comp_reason']}"
        pdf.set_x(10)
        pdf.multi_cell(190, 4.5, comp_details, 0, 'L')
        pdf.ln(3)
        
        pdf.set_font('Arial', 'B', 9.5)
        pdf.set_text_color(217, 119, 6)
        pdf.cell(0, 5, "Target Compounds for Spelling Correction:", 0, 1)
        pdf.set_font('Arial', '', 9)
        pdf.set_text_color(55, 65, 81)
        pdf.set_x(10)
        target_str = ", ".join(str(x) for x in name_analysis["target_compounds"])
        friend_str = ", ".join(str(y) for y in name_analysis["common_friends"])
        pdf.multi_cell(190, 4.5, f"Adjust spelling to target a positive compound number from: {target_str} (all reducing to friendly single digits: {friend_str}).", 0, 'L')
    else:
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(22, 163, 74) # Green
        pdf.cell(0, 6, "Suggested Action: No change required.", 0, 1)
        pdf.set_font('Arial', '', 9)
        pdf.set_text_color(55, 65, 81)
        pdf.cell(0, 5, "Your name compound is already fully compatible and vibrationally positive! No spelling corrections are required.", 0, 1)

    # 2. Add Friendship Table Matrix Section in PDF
    # 2. Add Friendship Table Matrix Section in PDF (Only for client's core numbers)
    pdf.add_page()
    pdf.section_title("Vedic Numerology Friendship Table", "")
    
    # Table headers
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(124, 58, 237)
    pdf.set_text_color(255, 255, 255)
    pdf.set_draw_color(221, 214, 254)
    
    col_w = [45, 50, 50, 45]
    pdf.cell(col_w[0], 8, "Number", border=1, align='C', fill=True)
    pdf.cell(col_w[1], 8, "Friend", border=1, align='C', fill=True)
    pdf.cell(col_w[2], 8, "Neutral", border=1, align='C', fill=True)
    pdf.cell(col_w[3], 8, "Enemy", border=1, align='C', fill=True)
    pdf.ln(8)
    
    # Rows
    core_nums = [root]
    if destiny != root:
        core_nums.append(destiny)
        
    pdf.set_font('Arial', 'B', 9)
    for r_num in core_nums:
        friends = num_engine.FRIENDSHIP_TABLE[r_num][0]
        neutrals = num_engine.FRIENDSHIP_TABLE[r_num][1]
        enemies = num_engine.FRIENDSHIP_TABLE[r_num][2]
        
        friends_str = ", ".join(str(x) for x in sorted(friends))
        neutrals_str = ", ".join(str(x) for x in sorted(neutrals)) if neutrals else "None"
        enemies_str = ", ".join(str(x) for x in sorted(enemies)) if enemies else "None"
        
        role = "Root" if r_num == root else "Destiny"
        if root == destiny:
            role = "Root & Destiny"
            
        pdf.set_fill_color(245, 243, 255)
        pdf.set_text_color(124, 58, 237)
        label = f"{r_num} ({role})"
            
        pdf.cell(col_w[0], 8, label, border=1, align='C', fill=True)
        pdf.set_text_color(22, 163, 74) # Green
        pdf.cell(col_w[1], 8, friends_str, border=1, align='C', fill=True)
        pdf.set_text_color(55, 65, 81) # Gray
        pdf.cell(col_w[2], 8, neutrals_str, border=1, align='C', fill=True)
        pdf.set_text_color(220, 38, 38) # Red
        pdf.cell(col_w[3], 8, enemies_str, border=1, align='C', fill=True)
        pdf.ln(8)
        
    # NEW SECTION: Career, Health & Relationships
    pdf.add_page()
    pdf.section_title("Numerology Health & Career Profiling", "")
    
    # Root Number Insights
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 6, f"Root Number {root} Insights", 0, 1)
    
    pdf.set_x(15)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(45, 5, "Lucky Dates & Days:", 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(145, 5, pred_engine.LUCKY_DATES_AND_DAYS.get(root, ""), 0, 'L')
    
    pdf.set_x(15)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(45, 5, "Favorable Professions:", 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(145, 5, pred_engine.FAVORABLE_PROFESSIONS.get(root, ""), 0, 'L')
    
    pdf.set_x(15)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(45, 5, "Probable Diseases:", 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(145, 5, pred_engine.PROBABLE_DISEASES.get(root, ""), 0, 'L')
    
    pdf.set_x(15)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(45, 5, "How to Win Over You:", 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(145, 5, pred_engine.HOW_TO_WIN_OVER_THEM.get(root, ""), 0, 'L')
    
    pdf.ln(4)
    
    # Destiny Number Insights
    if destiny != root:
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(22, 163, 74)
        pdf.cell(0, 6, f"Destiny Number {destiny} Insights", 0, 1)
        
        pdf.set_x(15)
        pdf.set_font('Arial', 'B', 9)
        pdf.set_text_color(55, 65, 81)
        pdf.cell(45, 5, "Lucky Dates & Days:", 0, 0)
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(145, 5, pred_engine.LUCKY_DATES_AND_DAYS.get(destiny, ""), 0, 'L')
        
        pdf.set_x(15)
        pdf.set_font('Arial', 'B', 9)
        pdf.set_text_color(55, 65, 81)
        pdf.cell(45, 5, "Favorable Professions:", 0, 0)
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(145, 5, pred_engine.FAVORABLE_PROFESSIONS.get(destiny, ""), 0, 'L')
        
        pdf.set_x(15)
        pdf.set_font('Arial', 'B', 9)
        pdf.set_text_color(55, 65, 81)
        pdf.cell(45, 5, "Probable Diseases:", 0, 0)
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(145, 5, pred_engine.PROBABLE_DISEASES.get(destiny, ""), 0, 'L')
        
        pdf.set_x(15)
        pdf.set_font('Arial', 'B', 9)
        pdf.set_text_color(55, 65, 81)
        pdf.cell(45, 5, "How to Win Over You:", 0, 0)
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(145, 5, pred_engine.HOW_TO_WIN_OVER_THEM.get(destiny, ""), 0, 'L')
        
        pdf.ln(4)

    return bytes(pdf.output(dest='S'))


def generate_yearly_pdf(name, dob_str, year, maha, antar, year_counts, pratyantars, root, destiny, year_digits, new_yearly_yogas=None):
    pdf = VedicPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    maha_name = PLANET_NAMES.get(maha, str(maha)) if maha else "N/A"
    antar_name = PLANET_NAMES.get(antar, str(antar))
    
    # Recalculate natal counts
    parts = dob_str.split('-')
    d_yr = int(parts[0])
    d_mo = int(parts[1])
    d_dy = int(parts[2])
    natal_digits = num_engine.get_vedic_grid_digits(d_dy, d_mo, d_yr)
    natal_counts = num_engine.construct_grid_array(natal_digits)
    
    # Year Summary Card
    pdf.section_title(f"Yearly Analysis for {year}", "")
    pdf.label_value("Name:", name)
    pdf.label_value("Date of Birth:", dob_str)
    pdf.label_value("Mahadasha:", f"{maha or 'N/A'}  ({maha_name})")
    pdf.label_value("Antardasha:", f"{antar}  ({antar_name})")
    pdf.label_value("Root / Destiny:", f"{root} ({PLANET_NAMES.get(root, '')}) / {destiny} ({PLANET_NAMES.get(destiny, '')})")
    pdf.ln(4)
    
    # Grid Comparison - Natal vs Yearly Side-by-Side
    pdf.section_title(f"Grid Comparison - Natal vs. {year} Yearly", "")
    grid_y = pdf.get_y()
    
    # Draw Natal Grid at X=45
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(124, 58, 237)
    pdf.set_xy(45, grid_y)
    pdf.cell(45, 5, "Natal Grid", 0, 1, 'C')
    draw_grid_at_xy(pdf, 45, grid_y + 6, natal_counts, root=root, destiny=destiny)
    
    # Draw Yearly Grid at X=120
    pdf.set_xy(120, grid_y)
    pdf.cell(45, 5, f"Yearly Grid ({year})", 0, 1, 'C')
    draw_grid_at_xy(pdf, 120, grid_y + 6, year_counts, maha=maha, antar=antar, root=root, destiny=destiny)
    
    pdf.set_y(grid_y + 6 + 28)
    
    # Color legend
    pdf.set_font('Arial', 'I', 7)
    legend = [
        (37, 99, 235, "Blue=Root"), (22, 163, 74, "Green=Destiny"),
        (124, 58, 237, "Violet=Maha"), (217, 119, 6, "Gold=Antar"),
        (236, 72, 153, "Pink=Pratyantar")
    ]
    pdf.set_x(42)
    for r, g, b, label in legend:
        pdf.set_text_color(r, g, b)
        pdf.cell(25, 4, label, 0, 0, 'C')
    pdf.ln(6)
    
    # Yearly Dasha Activation Analysis
    dasha_analysis = pred_engine.analyze_yearly_dasha(root, destiny, natal_counts, maha, antar, year_counts)
    
    pdf.section_title(f"Yearly Dasha Activation Analysis - {year}", "")
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 5, f"Overall Trend: {dasha_analysis['overall']}", 0, 1)
    pdf.ln(1)
    
    # Synergy Block in PDF
    pdf.set_font('Arial', 'B', 9)
    if dasha_analysis["synergy_label"] == "Double Positive (Golden Synergy)":
        pdf.set_text_color(22, 163, 74) # Green
    elif dasha_analysis["synergy_label"] == "Double Negative (Conflict Synergy)":
        pdf.set_text_color(220, 38, 38) # Red
    else:
        pdf.set_text_color(217, 119, 6) # Orange
    pdf.cell(0, 5, f"Dasha Synergy: {dasha_analysis['synergy_label']}", 0, 1)
    
    pdf.set_font('Arial', '', 8.5)
    pdf.set_text_color(55, 65, 81)
    pdf.multi_cell(0, 4.5, dasha_analysis["synergy_desc"], 0, 'L')
    pdf.ln(2)
    
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(55, 65, 81)
    
    pdf.set_x(12)
    pdf.cell(40, 5, "Finance & Career:", 0, 0)
    pdf.set_font('Arial', '', 8.5)
    pdf.multi_cell(140, 4.5, dasha_analysis["finance"], 0, 'L')
    
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_x(12)
    pdf.cell(40, 5, "Assets & Properties:", 0, 0)
    pdf.set_font('Arial', '', 8.5)
    pdf.multi_cell(140, 4.5, dasha_analysis["assets"], 0, 'L')
    
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_x(12)
    pdf.cell(40, 5, "Travel & Settling:", 0, 0)
    pdf.set_font('Arial', '', 8.5)
    pdf.multi_cell(140, 4.5, dasha_analysis["travel"], 0, 'L')
    
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_x(12)
    pdf.cell(40, 5, "Litigation & Conflicts:", 0, 0)
    pdf.set_font('Arial', '', 8.5)
    pdf.multi_cell(140, 4.5, dasha_analysis["litigation"], 0, 'L')
    pdf.ln(4)
    
    # New Yogas Activated by Dasha
    if new_yearly_yogas:
        pdf.section_title(f"New Yogas Activated in {year} Dasha", "")
        for combo in new_yearly_yogas:
            pdf.set_font('Arial', 'B', 9)
            pdf.set_text_color(220, 38, 38) # Red color for emphasis
            pdf.cell(0, 5, combo['name'], 0, 1)
            pdf.set_font('Arial', '', 8.5)
            pdf.set_text_color(51, 51, 51)
            pdf.multi_cell(0, 4.5, combo['desc'], 0, 'L')
            pdf.ln(2)
        pdf.ln(2)

    # Yearly Remedy Summary
    maha_rem = pred_engine.DETAILED_REMEDIES.get(maha, {})
    antar_rem = pred_engine.DETAILED_REMEDIES.get(antar, {})
    
    pdf.section_title(f"Yearly Remedies & Suggestions for {year}", "")
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 5, f"Mahadasha {maha_name} Remedies:", 0, 1)
    if maha_rem:
        pdf.bullet(f"Mantra: {maha_rem.get('mantra', 'N/A')}")
        pdf.bullet(f"Crystal: {maha_rem.get('crystal', 'N/A')}  |  Gemstone: {maha_rem.get('gemstone', 'N/A')}")
        pdf.bullet(f"Lucky Colors: {maha_rem.get('colors', 'N/A')}  |  Avoid: {maha_rem.get('colors_avoid', 'N/A')}")
        pdf.bullet(f"Deity: {maha_rem.get('deity', 'N/A')}  |  Fast: {maha_rem.get('fasting_day', 'N/A')}")
    pdf.ln(3)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(217, 119, 6)
    pdf.cell(0, 5, f"Antardasha {antar_name} Remedies:", 0, 1)
    if antar_rem:
        pdf.bullet(f"Mantra: {antar_rem.get('mantra', 'N/A')}")
        pdf.bullet(f"Crystal: {antar_rem.get('crystal', 'N/A')}  |  Gemstone: {antar_rem.get('gemstone', 'N/A')}")
        pdf.bullet(f"Lucky Colors: {antar_rem.get('colors', 'N/A')}")
    pdf.ln(4)
    
    # Monthly Grids with Observations
    pdf.add_page()
    pdf.section_title("Monthly Pratyantardasha Analysis", "")
    
    for p_idx, p_block in enumerate(pratyantars):
        p_planet = p_block["planet"]
        p_name = PLANET_NAMES[p_planet]
        p_start = p_block["start_date"].strftime("%d-%b-%Y")
        p_end = p_block["end_date"].strftime("%d-%b-%Y")
        
        # Check if we need a new page
        if pdf.get_y() > 215:
            pdf.add_page()
        
        # Period header with colored accent
        pdf.set_fill_color(245, 243, 255)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(124, 58, 237)
        pdf.cell(0, 6, f"  Period {p_idx+1}: {p_name} ({p_planet})  |  {p_start} to {p_end}", 0, 1, 'L', fill=True)
        pdf.ln(2)
        
        # Draw grid
        praty_digits = year_digits + [p_planet]
        praty_counts = num_engine.construct_grid_array(praty_digits)
        
        grid_y = pdf.get_y()
        draw_grid_at_xy(pdf, 15, grid_y, praty_counts, maha=maha, antar=antar, pratyantar=p_planet, root=root, destiny=destiny)
        
        # Observation text beside the grid
        obs = pred_engine.generate_monthly_observation(maha, antar, p_planet, praty_counts, root, destiny)
        
        text_x = 65
        pdf.set_xy(text_x, grid_y)
        
        m_status = pred_engine.get_planet_status(maha, destiny, praty_counts)
        a_status = pred_engine.get_planet_status(antar, destiny, praty_counts)
        p_status = pred_engine.get_planet_status(p_planet, destiny, praty_counts)
        
        syn_label = "Mixed Phase"
        syn_color = (217, 119, 6) # Orange
        if m_status == "Positive" and a_status == "Positive" and p_status == "Positive":
            syn_label = "Golden Month (Triple Positive Synergy)"
            syn_color = (22, 163, 74) # Green
        elif m_status == "Negative" and a_status == "Negative" and p_status == "Negative":
            syn_label = "Caution Month (Triple Negative Synergy)"
            syn_color = (220, 38, 38) # Red
            
        pdf.set_font('Arial', 'B', 8)
        pdf.set_text_color(*syn_color)
        pdf.cell(0, 4, f"Synergy: {syn_label}", 0, 1)
        
        pdf.set_x(text_x)
        pdf.set_font('Arial', 'B', 8)
        pdf.set_text_color(124, 58, 237)
        pdf.cell(0, 4, "Observation:", 0, 1)
        pdf.set_x(text_x)
        pdf.set_font('Arial', '', 8)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(130, 3.5, obs.get("observation", ""), 0, 'L')
        
        pdf.set_x(text_x)
        pdf.set_font('Arial', 'B', 8)
        pdf.set_text_color(22, 163, 74)
        pdf.cell(0, 4, "Remedies:", 0, 1)
        pdf.set_font('Arial', '', 8)
        pdf.set_text_color(55, 65, 81)
        for rem in obs.get("remedies", []):
            pdf.set_x(text_x)
            pdf.multi_cell(130, 3.5, f"- {rem}", 0, 'L')
        
        pdf.set_x(text_x)
        pdf.set_font('Arial', 'B', 8)
        pdf.set_text_color(217, 119, 6)
        pdf.cell(0, 4, "Suggestions:", 0, 1)
        pdf.set_font('Arial', '', 8)
        pdf.set_text_color(55, 65, 81)
        for sug in obs.get("suggestions", []):
            pdf.set_x(text_x)
            pdf.multi_cell(130, 3.5, f"- {sug}", 0, 'L')
        
        # Make sure we're below the grid
        min_y = grid_y + 26
        if pdf.get_y() < min_y:
            pdf.set_y(min_y)
        
        # Separator line
        pdf.set_draw_color(221, 214, 254)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(3)
    
    return bytes(pdf.output(dest='S'))
def generate_matchmaking_pdf(boy_name, boy_dob_str, girl_name, girl_dob_str, match_res):
    pdf = VedicPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.section_title("Vedic Matchmaking Report", "")
    
    # Profiles
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(95, 6, "Boy Details", 0, 0)
    pdf.cell(95, 6, "Girl Details", 0, 1)
    
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(95, 5, f"Name: {boy_name}", 0, 0)
    pdf.cell(95, 5, f"Name: {girl_name}", 0, 1)
    
    pdf.cell(95, 5, f"DOB: {boy_dob_str}", 0, 0)
    pdf.cell(95, 5, f"DOB: {girl_dob_str}", 0, 1)
    
    pdf.cell(95, 5, f"Root / Destiny: {match_res['boy_root']} / {match_res['boy_destiny']}", 0, 0)
    pdf.cell(95, 5, f"Root / Destiny: {match_res['girl_root']} / {match_res['girl_destiny']}", 0, 1)
    
    pdf.ln(5)
    
    # Scorecard
    pdf.section_title("Compatibility Scorecard", "")
    
    pdf.set_font('Arial', 'B', 12)
    if match_res['is_approved']:
        pdf.set_text_color(22, 163, 74)
        pdf.cell(0, 8, f"MATCH APPROVED! Total Score: {match_res['total_score']} / 100", 0, 1)
    else:
        pdf.set_text_color(220, 38, 38)
        pdf.cell(0, 8, f"MATCH NOT RECOMMENDED. Total Score: {match_res['total_score']} / 100", 0, 1)
        
    pdf.ln(3)
    
    # Breakdown
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 6, "Points Breakdown", 0, 1)
    
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(55, 65, 81)
    breakdown = [
        ("Root & Destiny compatibility", match_res['rd_score']),
        ("Emotional Quotient (Moon 2, Venus 6)", match_res['eq_score']),
        ("Practical Quotient (Saturn 8, Rahu 4, Sun 1)", match_res['pq_score']),
        ("Money Quotient (1, 5, 8, Destiny 6)", match_res['mon_score']),
        ("Extra Marriage Savers (+3, +7, +8)", match_res['savers_score']),
    ]
    
    for label, score in breakdown:
        pdf.cell(120, 5, label, 0, 0)
        pdf.cell(30, 5, f"{score} / 20", 0, 1)
        
    pdf.ln(5)
    
    # Rejections
    if match_res['rejections']:
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(220, 38, 38)
        pdf.cell(0, 6, "Hard Rejections (Fails)", 0, 1)
        for rej in match_res['rejections']:
            pdf.bullet(rej)
        pdf.ln(3)
        
    # Warnings
    if match_res['warnings']:
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(217, 119, 6)
        pdf.cell(0, 6, "Warnings & Cautions", 0, 1)
        for warn in match_res['warnings']:
            pdf.bullet(warn)
        pdf.ln(3)
        
    return bytes(pdf.output(dest='S'))
