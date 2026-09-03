import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
import numerology as num_engine
import predictions as pred_engine

# Set Streamlit Page Config
st.set_page_config(
    page_title="Vedic Numerology Dashboard",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main app background and global styles */
    .stApp {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    /* Tab formatting */
    button[data-baseweb="tab"] {
        color: #4b5563 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #7c3aed !important;
        border-color: #7c3aed !important;
    }
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f5f3ff !important;
        border: 1px solid #ddd6fe !important;
        border-radius: 8px !important;
        color: #1e293b !important;
    }
    .metric-card {
        background-color: #f5f3ff;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #ddd6fe;
        text-align: center;
        color: #1e293b;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #7c3aed;
    }
    .metric-label {
        font-size: 14px;
        color: #6d28d9;
    }
    /* Headers and texts */
    h1, h2, h3, h4, h5, h6, p, span, li, label, div {
        color: #1e293b !important;
    }
    .stMarkdown p, .stMarkdown li {
        color: #334155 !important;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f5f3ff !important;
        border-right: 1px solid #ddd6fe !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to render Vedic 3x3 Grid
def render_grid_html(counts, maha=None, antar=None, pratyantar=None, root=None, destiny=None):
    grid_layout = [
        [3, 1, 9],
        [6, 7, 5],
        [2, 8, 4]
    ]
    
    html = '<div style="display: flex; justify-content: center; margin: 10px 0;">'
    html += '<table style="border-collapse: collapse; border: 3px solid #7c3aed; text-align: center; font-family: monospace; width: 200px; height: 200px; background-color: #ffffff;">'
    
    for row in grid_layout:
        html += '<tr style="height: 66px;">'
        for cell in row:
            val_count = counts.get(cell, 0)
            text = f"{cell}" * val_count if val_count > 0 else ""
            
            is_maha = (cell == maha)
            is_antar = (cell == antar)
            is_praty = (cell == pratyantar)
            is_destiny = (cell == destiny)
            is_root = (cell == root)
            
            # Colored TEXT on white background (priority order)
            if is_praty:
                fg_color = "#ec4899"  # Pink
            elif is_antar:
                fg_color = "#d97706"  # Gold/Amber (readable yellow)
            elif is_maha:
                fg_color = "#7c3aed"  # Violet
            elif is_destiny:
                fg_color = "#16a34a"  # Green
            elif is_root:
                fg_color = "#2563eb"  # Blue
            elif text:
                fg_color = "#374151"  # Dark gray
            else:
                fg_color = "#d1d5db"  # Very light gray for empty
                
            border_style = "1px solid #ddd6fe"
            cell_title = f"Number {cell}: count {val_count}"
            status = []
            if is_root: status.append(f"Root: {root}")
            if is_destiny: status.append(f"Destiny: {destiny}")
            if is_maha: status.append("Mahadasha")
            if is_antar: status.append("Antardasha")
            if is_praty: status.append("Pratyantardasha")
            if status:
                cell_title += f" ({', '.join(status)})"
                
            font_size = "18px" if len(text) <= 3 else ("14px" if len(text) <= 5 else "11px")
            font_weight = "bold" if (is_maha or is_antar or is_praty or is_root or is_destiny) else "600"
            
            html += f'<td title="{cell_title}" style="border: {border_style}; background-color: #ffffff; color: {fg_color}; width: 66px; font-weight: {font_weight}; font-size: {font_size};">'
            html += f'{text if text else "&nbsp;"}'
            html += '</td>'
        html += '</tr>'
    html += '</table>'
    html += '</div>'
    return html

# App title and description
st.title("🔮 Local Vedic Numerology Web Application")
st.markdown("Replicating the complete Vedic Grid, Mahadasha schedule, Matchmaking scoring, and Muhurat timing calculations.")

# Sidebar - Main Profile Inputs
st.sidebar.header("User Profile")
name = st.sidebar.text_input("Full Name", "Rahul Sharma")
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

# DOB Input with separate Day / Month / Year dropdowns for easy year selection
st.sidebar.subheader("Date of Birth")
dob_col1, dob_col2, dob_col3 = st.sidebar.columns(3)
with dob_col1:
    dob_day = st.number_input("Day", min_value=1, max_value=31, value=14, step=1)
with dob_col2:
    dob_month = st.number_input("Month", min_value=1, max_value=12, value=10, step=1)
with dob_col3:
    dob_year = st.number_input("Year", min_value=1900, max_value=2100, value=1988, step=1)

try:
    dob = date(dob_year, dob_month, dob_day)
except ValueError:
    st.sidebar.error("Invalid date! Please correct Day/Month/Year.")
    st.stop()

# Compute core properties
root_num = num_engine.get_root_number(dob.day)
destiny_num = num_engine.get_destiny_number(dob.day, dob.month, dob.year)
natal_digits = num_engine.get_vedic_grid_digits(dob.day, dob.month, dob.year)
natal_counts = num_engine.construct_grid_array(natal_digits)

# Convert Name to Chaldean
first_name = name.split()[0] if name else ""
first_name_val = num_engine.calculate_compound_value(first_name)
full_name_val = num_engine.calculate_compound_value(name)

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "👤 Single Profile Analysis",
    "📅 Dasha Timeline & Custom Grids",
    "💑 Matchmaking (Kundali Matching)",
    "📳 Mobile, Vehicle & House Numerology"
])

# ================= TAB 1: SINGLE PROFILE ANALYSIS =================
with tab1:
    st.header(f"Vedic Numerology Analysis for {name}")
    
    # PDF Download Button
    import pdf_generator
    active_combos = pred_engine.get_active_combinations(natal_counts)
    preds = pred_engine.get_life_predictions(natal_counts, root_num, destiny_num)
    rem = pred_engine.REMEDIES.get(root_num, "")
    prec = pred_engine.PRECAUTIONS.get(root_num, "")
    dob_str = dob.strftime("%Y-%m-%d")
    
    try:
        pdf_data = pdf_generator.generate_general_pdf(
            name, dob_str, root_num, destiny_num, natal_counts, 
            active_combos, rem, prec, full_name_val
        )
        st.download_button(
            label="📥 Download General Profile PDF",
            data=pdf_data,
            file_name=f"{name.replace(' ', '_')}_General_Profile.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error preparing PDF report: {e}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{root_num}</div>
            <div class="metric-label">Root Number (Psychic)</div>
        </div>
        <br>
        <div class="metric-card">
            <div class="metric-value">{destiny_num}</div>
            <div class="metric-label">Destiny Number (Life Path)</div>
        </div>
        <br>
        <div class="metric-card">
            <div class="metric-value">{full_name_val} ({num_engine.reduce_digit(full_name_val)})</div>
            <div class="metric-label">Full Name Compound Number</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        comp_info = pred_engine.COMPOUND_NUMBERS.get(full_name_val, {"aura": "-", "summary": "Unknown", "description": "", "notes": ""})
        aura_lbl = "Positive (+)" if comp_info["aura"] == "+" else "Negative (-)"
        aura_color = "#16a34a" if comp_info["aura"] == "+" else "#dc2626"
        
        st.markdown(f"""
        <div style='background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; font-size: 13px; color: #1e293b;'>
            <b style='color: #7c3aed;'>Compound Number {full_name_val} Info:</b><br>
            <b>Aura Status:</b> <span style='color: {aura_color}; font-weight: bold;'>{aura_lbl}</span><br>
            <b>Summary:</b> {comp_info['summary']}<br>
            <b>Description:</b> {comp_info['description']}<br>
            <b>Action/Remedies:</b> {comp_info['notes']}
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.subheader("Natal Vedic Grid")
        st.markdown(render_grid_html(natal_counts, root=root_num, destiny=destiny_num), unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 12px;'>Standard 3x3 layout (3-1-9, 6-7-5, 2-8-4)</p>", unsafe_allow_html=True)
        
    with col3:
        st.subheader("Core Personality Traits")
        # Planets mapped to numbers
        planet_names = {
            1: "Sun (Surya) - Raja/King",
            2: "Moon (Chandrama) - Rani/Queen",
            3: "Jupiter (Guru) - Advisor",
            4: "Rahu - Shadow Planet",
            5: "Mercury (Budh) - Prince",
            6: "Venus (Shukra) - Luxuries/Guru",
            7: "Ketu - Shadow Planet",
            8: "Saturn (Shani) - Judge/Struggler",
            9: "Mars (Mangal) - Commander"
        }
        st.markdown(f"**Root Number Planet:** {planet_names.get(root_num, 'Unknown')}")
        st.markdown(f"**Destiny Number Planet:** {planet_names.get(destiny_num, 'Unknown')}")
        
        # Specific digit count traits
        st.markdown("### Grid Placements")
        for num in range(1, 10):
            cnt = natal_counts[num]
            if cnt > 0:
                if num == 1:
                    if destiny_num == 1:
                        trait_key = "multiple_with_d1" if cnt > 1 else "d1_single"
                    else:
                        trait_key = "multiple_no_d1" if cnt > 1 else "single"
                    st.markdown(f"- **Number {num} (count {cnt}):** {pred_engine.NUMBER_TRAITS[num][trait_key]}")
                elif num == 2:
                    trait_key = "double" if cnt == 2 else ("multiple" if cnt > 2 else "single")
                    st.markdown(f"- **Number {num} (count {cnt}):** {pred_engine.NUMBER_TRAITS[num][trait_key]}")
                elif num in [4, 8]:
                    trait_key = "even" if cnt % 2 == 0 else "odd"
                    st.markdown(f"- **Number {num} (count {cnt}):** {pred_engine.NUMBER_TRAITS[num][trait_key]}")
                elif num == 6:
                    trait_key = "multiple_with_d6" if (cnt > 1 and destiny_num == 6) else ("multiple_no_d6" if cnt > 1 else "single")
                    st.markdown(f"- **Number {num} (count {cnt}):** {pred_engine.NUMBER_TRAITS[num][trait_key]}")
                else:
                    trait_key = "multiple" if cnt > 1 else "single"
                    st.markdown(f"- **Number {num} (count {cnt}):** {pred_engine.NUMBER_TRAITS[num][trait_key]}")
                    
    st.markdown("---")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Active Yogas & Grid Combinations")
        active_combos = pred_engine.get_active_combinations(natal_counts)
        if active_combos:
            for combo in active_combos:
                with st.expander(combo["name"]):
                    st.write(combo["desc"])
        else:
            st.info("No major specific yogas active in the natal chart.")
            
    with col_b:
        st.subheader("Remedies & Precautions")
        # Root number remedies
        st.markdown(f"**Remedy for Root Number {root_num}:**")
        st.info(pred_engine.REMEDIES.get(root_num, ""))
        st.markdown(f"**Precautions for Root Number {root_num}:**")
        st.warning(pred_engine.PRECAUTIONS.get(root_num, ""))
        
    st.markdown("---")
    st.subheader("🔮 Life Predictions")
    preds = pred_engine.get_life_predictions(natal_counts, root_num, destiny_num)
    for category, text in preds.items():
        with st.expander(f"{category} Forecast"):
            st.write(text)

    st.markdown("---")
    st.subheader("🔤 Name Analysis & Spelling Correction Plan")
    name_analysis = pred_engine.analyze_name_compatibility(first_name, name, root_num, destiny_num)
    
    n_col1, n_col2 = st.columns(2)
    with n_col1:
        st.markdown(f"""
        <div style='background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; color: #1e293b;'>
            <b style='color: #7c3aed; font-size: 15px;'>First Name Compound: {name_analysis['first_val']}</b> ({first_name})<br>
            <b>Vibration:</b> <span style='color: {"#16a34a" if name_analysis["first_aura"] == "+" else "#dc2626"}; font-weight: bold;'>{"Positive (+)" if name_analysis["first_aura"] == "+" else "Negative (-)"}</span><br>
            <b>Summary:</b> {name_analysis['first_summary']}<br>
            <b>Meaning:</b> {name_analysis['first_desc']}<br>
        </div>
        """, unsafe_allow_html=True)
        
    with n_col2:
        st.markdown(f"""
        <div style='background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; color: #1e293b;'>
            <b style='color: #7c3aed; font-size: 15px;'>Full Name Compound: {name_analysis['full_val']}</b> ({name})<br>
            <b>Vibration:</b> <span style='color: {"#16a34a" if name_analysis["full_aura"] == "+" else "#dc2626"}; font-weight: bold;'>{"Positive (+)" if name_analysis["full_aura"] == "+" else "Negative (-)"}</span><br>
            <b>Summary:</b> {name_analysis['full_summary']}<br>
            <b>Meaning:</b> {name_analysis['full_desc']}<br>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if name_analysis["action"] != "No Change":
        action_color = "#d97706" if name_analysis["action"] == "Drop Last Name" else "#dc2626"
        action_html = f"<div style='background-color:#f5f3ff;border:2px solid #ddd6fe;border-radius:8px;padding:15px;color:#1e293b;'>"
        action_html += f"<b style='font-size:16px;'>Suggested Action: </b>"
        action_html += f"<span style='color:{action_color};font-weight:bold;font-size:16px;'>{name_analysis['action']}</span>"
        action_html += f"<p style='margin-top:8px;font-size:13px;color:#4b5563;'>"
        action_html += f"<b>Name compatibility check:</b> Full name reduces to single digit <b>{name_analysis['single_digit']}</b>. "
        action_html += f"Relationship with Root ({root_num}): <b>{name_analysis['rel_root']}</b>. "
        action_html += f"Relationship with Destiny ({destiny_num}): <b>{name_analysis['rel_dest']}</b>. "
        if name_analysis['comp_reason']:
            action_html += f"<br><span style='color:#dc2626;font-weight:bold;'>Reason: {name_analysis['comp_reason']}</span>"
        action_html += f"</p></div>"
        
        st.markdown(action_html, unsafe_allow_html=True)
        
        target_html = f"<div style='background-color:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:15px;margin-top:10px;color:#1e293b;font-size:13px;'>"
        target_html += f"<b style='color:#d97706;'>💡 Target Compounds for Spelling Adjustments:</b><br>"
        target_html += f"To align your name with your core numbers, adjust spelling so that your name compound matches one of these positive values: "
        target_html += f"<b>{', '.join(str(x) for x in name_analysis['target_compounds'])}</b> (which all reduce to friendly numbers <b>{', '.join(str(y) for y in name_analysis['common_friends'])}</b>)."
        target_html += f"</div>"
        
        st.markdown(target_html, unsafe_allow_html=True)
    else:
        st.success("🎉 Your name compound is already fully compatible and vibrationally positive! No spelling corrections are required.")

    # Add the Friendship Table (Only for client's core numbers)
    st.markdown("---")
    st.subheader("🤝 Vedic Numerology Friendship Table")
    
    core_nums = [root_num]
    if destiny_num != root_num:
        core_nums.append(destiny_num)
        
    friend_rows = ""
    for r_num in core_nums:
        friends = num_engine.FRIENDSHIP_TABLE[r_num][0]
        neutrals = num_engine.FRIENDSHIP_TABLE[r_num][1]
        enemies = num_engine.FRIENDSHIP_TABLE[r_num][2]
        
        friends_str = ", ".join(str(x) for x in sorted(friends))
        neutrals_str = ", ".join(str(x) for x in sorted(neutrals)) if neutrals else "None"
        enemies_str = ", ".join(str(x) for x in sorted(enemies)) if enemies else "None"
        
        role = "Root Number" if r_num == root_num else "Destiny Number"
        if root_num == destiny_num:
            role = "Root & Destiny Number"
            
        friend_rows += f"<tr style='background-color: #f5f3ff; font-weight: bold;'>"
        friend_rows += f"<td style='border: 1px solid #ddd6fe; padding: 8px; text-align: center; color: #1e293b;'><b>{r_num} ({role})</b></td>"
        friend_rows += f"<td style='border: 1px solid #ddd6fe; padding: 8px; text-align: center; color: #16a34a;'>{friends_str}</td>"
        friend_rows += f"<td style='border: 1px solid #ddd6fe; padding: 8px; text-align: center; color: #4b5563;'>{neutrals_str}</td>"
        friend_rows += f"<td style='border: 1px solid #ddd6fe; padding: 8px; text-align: center; color: #dc2626;'>{enemies_str}</td>"
        friend_rows += "</tr>"
        
    table_html = f"<table style='border-collapse: collapse; width: 100%; border: 1px solid #ddd6fe; font-family: monospace; font-size: 13px;'>"
    table_html += f"<tr style='background-color: #7c3aed; color: #ffffff;'>"
    table_html += f"<th style='border: 1px solid #ddd6fe; padding: 10px; text-align: center;'>Number</th>"
    table_html += f"<th style='border: 1px solid #ddd6fe; padding: 10px; text-align: center;'>Friend</th>"
    table_html += f"<th style='border: 1px solid #ddd6fe; padding: 10px; text-align: center;'>Neutral</th>"
    table_html += f"<th style='border: 1px solid #ddd6fe; padding: 10px; text-align: center;'>Enemy</th>"
    table_html += f"</tr>"
    table_html += friend_rows
    table_html += f"</table>"
    
    st.markdown(table_html, unsafe_allow_html=True)

# ================= TAB 2: DASHA TIMELINE & CUSTOM GRIDS =================
with tab2:
    st.header("Dasha Schedules & Time-Travel Grids")
    
    col_timeline, col_detail = st.columns([1, 2])
    
    with col_timeline:
        st.subheader("Mahadasha Timeline")
        mahadashas = num_engine.get_mahadashas(dob, root_num)
        
        m_df = pd.DataFrame(mahadashas)
        m_df["Planet Name"] = m_df["planet"].map({
            1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 
            5: "Mercury", 6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"
        })
        m_df["Start Date"] = m_df["start_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        m_df["End Date"] = m_df["end_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        
        st.dataframe(m_df[["Planet Name", "start_date", "end_date", "duration", "age_start"]], 
                     column_config={
                         "Planet Name": "Planet",
                         "start_date": "Start Date",
                         "end_date": "End Date",
                         "duration": "Duration (Yrs)",
                         "age_start": "Age Start"
                     }, use_container_width=True)
                     
    with col_detail:
        st.subheader("Custom Time-Travel Grid Range")
        
        col_yr1, col_yr2 = st.columns(2)
        with col_yr1:
            from_yr = st.number_input("From Year", min_value=1900, max_value=2150, value=max(dob.year, 1900))
        with col_yr2:
            to_yr = st.number_input("To Year", min_value=1900, max_value=2150, value=min(max(dob.year + 10, date.today().year + 8), 2150))
            
        if from_yr > to_yr:
            st.error("From Year must be less than or equal to To Year.")
        else:
            st.markdown("### Color Legend for Grids:")
            st.markdown(
                '<span style="background-color: #2563eb; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-right: 5px;">Root (Blue)</span>'
                '<span style="background-color: #16a34a; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-right: 5px;">Destiny (Green)</span>'
                '<span style="background-color: #7c3aed; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-right: 5px;">Maha (Violet)</span>'
                '<span style="background-color: #eab308; color: #000; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-right: 5px;">Antar (Yellow)</span>'
                '<span style="background-color: #ec4899; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 12px;">Pratyantar (Pink)</span>',
                unsafe_allow_html=True
            )
            
            # Retrieve dasha grids for range
            for yr in range(from_yr, to_yr + 1):
                # active Mahadasha
                active_maha = None
                for dasha in mahadashas:
                    if dasha["start_date"].year <= yr <= dasha["end_date"].year:
                        active_maha = dasha["planet"]
                        break
                        
                active_antar = num_engine.get_antardasha(dob, yr, root_num)
                
                # Construct Year grid (Natal digits + Mahadasha planet + Antardasha planet)
                year_digits = natal_digits + ([active_maha] if active_maha else []) + [active_antar]
                year_counts = num_engine.construct_grid_array(year_digits)
                pratyantars = num_engine.get_pratyantardashas(dob, yr, active_antar)
                
                # Check for litigation in this specific year grid
                lit_flag = (year_counts[9] > 0 and year_counts[4] > 0 and year_counts[5] == 0 and year_counts[4] % 2 != 0) or \
                           (year_counts[5] > 0 and year_counts[4] > 0 and year_counts[9] == 0 and year_counts[4] % 2 != 0) or \
                           (year_counts[6] == 0)
                
                exp_title = f"📅 Year {yr} | Mahadasha: {active_maha or 'None'}, Antardasha: {active_antar}"
                if lit_flag:
                    exp_title += " ⚠️ litigation active"
                    
                with st.expander(exp_title):
                    # Calculate new yogas for the year
                    natal_yogas = pred_engine.get_active_combinations(natal_counts)
                    natal_yoga_names = {y['name'] for y in natal_yogas}
                    yearly_yogas = pred_engine.get_active_combinations(year_counts)
                    new_yearly_yogas = [y for y in yearly_yogas if y['name'] not in natal_yoga_names]

                    if new_yearly_yogas:
                        st.markdown("**🔔 New Yogas Activated During this Dasha:**")
                        for ny in new_yearly_yogas:
                            st.warning(f"**{ny['name']}**: {ny['desc']}")
                    
                    # Yearly PDF Download
                    try:
                        yearly_pdf_data = pdf_generator.generate_yearly_pdf(
                            name, dob_str, yr, active_maha, active_antar, 
                            year_counts, pratyantars, root_num, destiny_num, year_digits,
                            new_yearly_yogas=new_yearly_yogas
                        )
                        st.download_button(
                            label=f"📥 Download {yr} Yearly Analysis PDF",
                            data=yearly_pdf_data,
                            file_name=f"{name.replace(' ', '_')}_{yr}_Yearly_Analysis.pdf",
                            mime="application/pdf",
                            key=f"dl_pdf_yr_{yr}"
                        )
                    except Exception as e:
                        st.error(f"Error preparing Yearly PDF: {e}")
                        
                    # Side-by-side grids layout (Natal & Yearly)
                    col_natal, col_yearly = st.columns(2)
                    
                    with col_natal:
                        st.markdown("**Natal Grid:**")
                        st.markdown(render_grid_html(natal_counts, root=root_num, destiny=destiny_num), unsafe_allow_html=True)
                        
                    with col_yearly:
                        st.markdown("**Yearly Grid:**")
                        st.markdown(render_grid_html(year_counts, maha=active_maha, antar=active_antar, root=root_num, destiny=destiny_num), unsafe_allow_html=True)
                        if lit_flag:
                            st.warning("Litigation combinations active in the grid this year!")
                            
                    # Yearly Dasha Activation Analysis
                    dasha_analysis = pred_engine.analyze_yearly_dasha(root_num, destiny_num, natal_counts, active_maha, active_antar, year_counts)
                    
                    st.markdown("##### 🔮 Yearly Dasha Activation Analysis")
                    st.markdown(f"**Overall Trend:** {dasha_analysis['overall']}")
                    
                    synergy_color = "#16a34a" if dasha_analysis["synergy_label"] == "Double Positive (Golden Synergy)" else ("#dc2626" if dasha_analysis["synergy_label"] == "Double Negative (Conflict Synergy)" else "#d97706")
                    st.markdown(f"<div style='background-color:#f8fafc;border-left:5px solid {synergy_color};border-radius:4px;padding:12px;margin-bottom:15px;color:#1e293b;'><b style='font-size:14px;color:{synergy_color};'>{dasha_analysis['synergy_label']}</b><br><span style='font-size:12.5px;'>{dasha_analysis['synergy_desc']}</span></div>", unsafe_allow_html=True)
                    
                    da_col1, da_col2 = st.columns(2)
                    with da_col1:
                        st.info(f"💰 **Finance & Career:**\n\n{dasha_analysis['finance']}")
                        st.success(f"🏠 **Assets & Properties:**\n\n{dasha_analysis['assets']}")
                    with da_col2:
                        st.warning(f"✈️ **Travel & Settling:**\n\n{dasha_analysis['travel']}")
                        st.error(f"⚖️ **Litigation & Conflicts:**\n\n{dasha_analysis['litigation']}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                            
                    st.markdown("#### Monthly / Pratyantardasha Grids (8 × Planet Number Days)")
                    
                    # Color legend bar
                    st.markdown("""<div style='display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 12px; font-size: 12px;'>
                        <span><b style='color: #2563eb;'>■</b> Root</span>
                        <span><b style='color: #16a34a;'>■</b> Destiny</span>
                        <span><b style='color: #7c3aed;'>■</b> Mahadasha</span>
                        <span><b style='color: #d97706;'>■</b> Antardasha</span>
                        <span><b style='color: #ec4899;'>■</b> Pratyantardasha</span>
                    </div>""", unsafe_allow_html=True)
                    
                    # Display all 9 monthly grids side-by-side in rows of 3
                    for row_idx in range(0, 9, 3):
                        p_cols = st.columns(3)
                        for col_idx in range(3):
                            p_idx = row_idx + col_idx
                            if p_idx < len(pratyantars):
                                p_block = pratyantars[p_idx]
                                p_planet = p_block["planet"]
                                p_name = {
                                    1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu",
                                    5: "Mercury", 6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"
                                }[p_planet]
                                p_start = p_block["start_date"].strftime("%d-%b-%Y")
                                p_end = p_block["end_date"].strftime("%d-%b-%Y")
                                
                                with p_cols[col_idx]:
                                    st.markdown(f"<div style='text-align: center; font-weight: bold; color: #7c3aed !important;'>Period {p_idx+1}: {p_name} ({p_planet})<br><span style='font-size: 11px; color: #64748b !important;'>{p_start} to {p_end}</span></div>", unsafe_allow_html=True)
                                    # construct pratyantar grid
                                    praty_digits = year_digits + [p_planet]
                                    praty_counts = num_engine.construct_grid_array(praty_digits)
                                    st.markdown(render_grid_html(praty_counts, maha=active_maha, antar=active_antar, pratyantar=p_planet, root=root_num, destiny=destiny_num), unsafe_allow_html=True)
                                    
                                    # Generate observation card
                                    obs = pred_engine.generate_monthly_observation(active_maha, active_antar, p_planet, praty_counts, root_num, destiny_num)
                                    m_status = pred_engine.get_planet_status(active_maha, destiny_num, praty_counts)
                                    a_status = pred_engine.get_planet_status(active_antar, destiny_num, praty_counts)
                                    p_status = pred_engine.get_planet_status(p_planet, destiny_num, praty_counts)
                                    
                                    syn_label = "Mixed Phase"
                                    syn_color = "#d97706" # Orange
                                    if m_status == "Positive" and a_status == "Positive" and p_status == "Positive":
                                        syn_label = "Golden Month (Triple Positive Synergy)"
                                        syn_color = "#16a34a" # Green
                                    elif m_status == "Negative" and a_status == "Negative" and p_status == "Negative":
                                        syn_label = "Caution Month (Triple Negative Synergy)"
                                        syn_color = "#dc2626" # Red
                                        
                                    obs_html = f"<div style='background:#f5f3ff;border:1px solid #ddd6fe;border-radius:8px;padding:10px;margin-top:6px;font-size:12px;color:#334155;'>"
                                    obs_html += f"<div style='margin-bottom:6px;'><b style='color:{syn_color};'>Synergy: {syn_label}</b></div>"
                                    obs_html += f"<div style='margin-bottom:6px;'><b style='color:#7c3aed;'>🔍 Observation:</b> {obs.get('observation', '')}</div>"
                                    obs_html += f"<div style='margin-bottom:6px;'><b style='color:#16a34a;'>💎 Remedies:</b><br>{'<br>'.join('• ' + r for r in obs.get('remedies', []))}</div>"
                                    obs_html += f"<div><b style='color:#d97706;'>💡 Suggestions:</b><br>{'<br>'.join('• ' + s for s in obs.get('suggestions', []))}</div>"
                                    obs_html += f"</div>"
                                    
                                    st.markdown(obs_html, unsafe_allow_html=True)
                    
                    # Year-level remedy summary
                    maha_rem = pred_engine.DETAILED_REMEDIES.get(active_maha, {})
                    antar_rem = pred_engine.DETAILED_REMEDIES.get(active_antar, {})
                    st.markdown("---")
                    st.markdown(f"#### 🔮 Yearly Remedies & Suggestions for {yr}")
                    rem_c1, rem_c2, rem_c3 = st.columns(3)
                    with rem_c1:
                        st.markdown(f"""<div style='background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 10px; padding: 14px; text-align: center;'>
                        <div style='font-size: 24px;'>💎</div>
                        <div style='font-weight: bold; color: #7c3aed !important;'>Crystal & Gemstone</div>
                        <div style='font-size: 12px; color: #334155 !important;'>Mahadasha: {maha_rem.get('crystal', 'N/A')}<br>Gemstone: {maha_rem.get('gemstone', 'N/A')}</div>
                        </div>""", unsafe_allow_html=True)
                    with rem_c2:
                        st.markdown(f"""<div style='background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 10px; padding: 14px; text-align: center;'>
                        <div style='font-size: 24px;'>🙏</div>
                        <div style='font-weight: bold; color: #7c3aed !important;'>Mantras & Prayers</div>
                        <div style='font-size: 12px; color: #334155 !important;'>Mahadasha: {maha_rem.get('mantra', 'N/A')}<br>Deity: {maha_rem.get('deity', 'N/A')}</div>
                        </div>""", unsafe_allow_html=True)
                    with rem_c3:
                        st.markdown(f"""<div style='background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 10px; padding: 14px; text-align: center;'>
                        <div style='font-size: 24px;'>🎨</div>
                        <div style='font-weight: bold; color: #7c3aed !important;'>Color Therapy & Attire</div>
                        <div style='font-size: 12px; color: #334155 !important;'>Lucky: {maha_rem.get('colors', 'N/A')}<br>Avoid: {maha_rem.get('colors_avoid', 'N/A')}</div>
                        </div>""", unsafe_allow_html=True)

# ================= TAB 3: MATCHMAKING =================
with tab3:
    st.header("Vedic Matchmaking (Quotient Matching)")
    
    col_boy, col_girl = st.columns(2)
    
    with col_boy:
        st.subheader("Boy Details")
        boy_name = st.text_input("Boy Name", "Amit")
        boy_dob_val = st.date_input("Boy Date of Birth", date(1984, 8, 18), min_value=date(1920, 1, 1), max_value=date(2090, 12, 31))
        
    with col_girl:
        st.subheader("Girl Details")
        girl_name = st.text_input("Girl Name", "Kiran")
        girl_dob_val = st.date_input("Girl Date of Birth", date(1986, 6, 3), min_value=date(1920, 1, 1), max_value=date(2090, 12, 31))
        
    if st.button("Evaluate Match Compatibility"):
        match_res = num_engine.evaluate_matchmaking(boy_dob_val, girl_dob_val)
        
        st.markdown("---")
        st.subheader("Compatibility Scorecard")
        
        try:
            import pdf_generator
            boy_dob_str = boy_dob_val.strftime("%Y-%m-%d")
            girl_dob_str = girl_dob_val.strftime("%Y-%m-%d")
            pdf_data = pdf_generator.generate_matchmaking_pdf(boy_name, boy_dob_str, girl_name, girl_dob_str, match_res)
            st.download_button(
                label="📥 Download Matchmaking PDF",
                data=pdf_data,
                file_name=f"Matchmaking_{boy_name}_and_{girl_name}.pdf".replace(' ', '_'),
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error preparing Matchmaking PDF: {e}")
            
        # Display main metrics
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if match_res["is_approved"]:
                st.success(f"💖 MATCH APPROVED! Total Score: {match_res['total_score']} / 100")
            else:
                st.error(f"❌ MATCH NOT RECOMMENDED. Total Score: {match_res['total_score']} / 100")
                
        with col_m2:
            st.markdown(f"**Boy's Root/Destiny:** {match_res['boy_root']} / {match_res['boy_destiny']}")
            st.markdown(f"**Girl's Root/Destiny:** {match_res['girl_root']} / {match_res['girl_destiny']}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("**Boy's Natal Grid:**")
            boy_digits = num_engine.get_vedic_grid_digits(boy_dob_val.day, boy_dob_val.month, boy_dob_val.year)
            boy_counts = num_engine.construct_grid_array(boy_digits)
            st.markdown(render_grid_html(boy_counts, root=match_res['boy_root'], destiny=match_res['boy_destiny']), unsafe_allow_html=True)
            
        with col_g2:
            st.markdown("**Girl's Natal Grid:**")
            girl_digits = num_engine.get_vedic_grid_digits(girl_dob_val.day, girl_dob_val.month, girl_dob_val.year)
            girl_counts = num_engine.construct_grid_array(girl_digits)
            st.markdown(render_grid_html(girl_counts, root=match_res['girl_root'], destiny=match_res['girl_destiny']), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
            
        # Display breakdown
        st.subheader("Points Breakdown")
        breakdown_df = pd.DataFrame([
            {"Quotient": "Root & Destiny compatibility", "Score": f"{match_res['rd_score']} / 20"},
            {"Quotient": "Emotional Quotient (Moon 2, Venus 6)", "Score": f"{match_res['eq_score']} / 20"},
            {"Quotient": "Practical Quotient (Saturn 8, Rahu 4, Sun 1)", "Score": f"{match_res['pq_score']} / 20"},
            {"Quotient": "Money Quotient (1, 5, 8, Destiny 6)", "Score": f"{match_res['mon_score']} / 20"},
            {"Quotient": "Extra Marriage Savers (+3, +7, +8)", "Score": f"{match_res['savers_score']} / 20"},
        ])
        st.table(breakdown_df)
        
        # Rejections
        if match_res["rejections"]:
            st.subheader("🔴 Hard Rejections (Fails)")
            for rej in match_res["rejections"]:
                st.error(rej)
        else:
            st.success("No hard rejections active.")
            
        # Warnings & Litigation Checks
        if match_res["warnings"]:
            st.subheader("⚠️ Warnings & Cautions")
            for warn in match_res["warnings"]:
                st.warning(warn)
        else:
            st.success("No warnings active.")

        if match_res.get("litigation_years"):
            st.markdown("### 🏛️ Litigation Check: Active Yearly Grids")
            for lit_info in match_res["litigation_years"]:
                st.markdown(f"**Year: {lit_info['year']}**")
                col_lit_b, col_lit_g = st.columns(2)
                
                with col_lit_b:
                    label = "Boy's Yearly Grid"
                    if lit_info["boy_litigation"]:
                        if lit_info.get("boy_savior"):
                            label += " 🔴 (Litigation Active, but Savior 7/8 Present 🛡️)"
                        else:
                            label += " 🔴 (Litigation Active)"
                    st.markdown(f"*{label}*")
                    st.markdown(render_grid_html(lit_info['boy_counts'], maha=lit_info['boy_maha'], antar=lit_info['boy_antar'], root=match_res['boy_root'], destiny=match_res['boy_destiny']), unsafe_allow_html=True)
                
                with col_lit_g:
                    label = "Girl's Yearly Grid"
                    if lit_info["girl_litigation"]:
                        if lit_info.get("girl_savior"):
                            label += " 🔴 (Litigation Active, but Savior 7/8 Present 🛡️)"
                        else:
                            label += " 🔴 (Litigation Active)"
                    st.markdown(f"*{label}*")
                    st.markdown(render_grid_html(lit_info['girl_counts'], maha=lit_info['girl_maha'], antar=lit_info['girl_antar'], root=match_res['girl_root'], destiny=match_res['girl_destiny']), unsafe_allow_html=True)
                
                st.markdown("<hr>", unsafe_allow_html=True)

# ================= TAB 4: MOBILE & VEHICLE NUMEROLOGY =================
with tab4:
    st.header("Name, Mobile & Vehicle Analysis")
    
    col_n1, col_n2 = st.columns([1, 2])
    
    with col_n1:
        st.subheader("Name Evaluation Utility")
        test_name = st.text_input("Enter Name to Analyze", "Ravi Soni")
        
        t_first = test_name.split()[0] if test_name else ""
        t_first_comp = num_engine.calculate_compound_value(t_first)
        t_full_comp = num_engine.calculate_compound_value(test_name)
        
        t_first_single = num_engine.reduce_digit(t_first_comp)
        t_full_single = num_engine.reduce_digit(t_full_comp)
        
        st.markdown(f"**First Name Compound:** {t_first_comp} ({t_first_single})")
        st.markdown(f"**Full Name Compound:** {t_full_comp} ({t_full_single})")
        
        # Check compatibility with current profile
        root_rel = num_engine.get_relationship(root_num, t_full_single)
        dest_rel = num_engine.get_relationship(destiny_num, t_full_single)
        
        st.write(f"Name vs Root ({root_num}): **{root_rel}**")
        st.write(f"Name vs Destiny ({destiny_num}): **{dest_rel}**")
        
        if root_rel == 'Enemy':
            st.error("Warning: Name number is inimical to your Root number. Can trigger health problems.")
        if dest_rel == 'Enemy':
            st.error("Warning: Name number is inimical to your Destiny number. Can trigger professional issues.")
            
        st.subheader("Aura Lookups")
        with st.expander(f"Compound Number {t_full_comp} Info"):
            info = pred_engine.COMPOUND_NUMBERS.get(t_full_comp, {})
            if info:
                st.markdown(f"**Aura Status:** `{info['aura']}` ({'Positive' if info['aura']=='+' else 'Negative'})")
                st.markdown(f"**Summary:** {info['summary']}")
                st.markdown(f"**Description:** {info['description']}")
                st.markdown(f"**Action/Remedies:** {info['notes']}")
            else:
                st.write("Number beyond standard range. Check single-digit reduction.")
                
    with col_n2:
        st.subheader("Chaldean Alphabets Key Table")
        chaldean_data = []
        for val in range(1, 9):
            chars = [k for k, v in {
                'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
                'B': 2, 'K': 2, 'R': 2,
                'C': 3, 'G': 3, 'L': 3, 'S': 3,
                'D': 4, 'M': 4, 'T': 4,
                'E': 5, 'H': 5, 'N': 5, 'X': 5,
                'U': 6, 'V': 6, 'W': 6,
                'O': 7, 'Z': 7,
                'F': 8, 'P': 8
            }.items() if v == val]
            chaldean_data.append({"Value": val, "Alphabets": ", ".join(chars)})
        st.table(pd.DataFrame(chaldean_data))
        
        st.subheader("Mobile & House/Vehicle Suitability Engine")
        item_type = st.selectbox("Select Asset Type", ["Mobile Number", "House Number", "Vehicle Plate"])
        num_str = st.text_input("Enter Number (letters are resolved)", "DL4C1242" if item_type=="Vehicle Plate" else "9953705568")
        
        if num_str:
            comp_val = num_engine.calculate_compound_value(num_str)
            single_val = num_engine.reduce_digit(comp_val)
            
            st.info(f"Calculated Compound Sum: **{comp_val}** (Reduces to single digit **{single_val}**)")
            
            # Check friendship against driver/owner
            root_fit = num_engine.get_relationship(root_num, single_val)
            dest_fit = num_engine.get_relationship(destiny_num, single_val)
            
            st.write(f"Asset compatibility with your Root ({root_num}): **{root_fit}**")
            st.write(f"Asset compatibility with your Destiny ({destiny_num}): **{dest_fit}**")
            
            info = pred_engine.COMPOUND_NUMBERS.get(comp_val, {})
            if info:
                st.write(f"**Aura Diagnostic:** {'Positive' if info['aura']=='+' else 'Negative'} ({info['aura']})")
                st.write(f"**Implications:** {info['description']}")
                
        # Muhurat Calculator
        st.subheader("📅 Auspicious Muhurat Range Planner")
        m_start = st.date_input("Start Evaluation Date", date.today())
        m_end = st.date_input("End Evaluation Date", date.today() + timedelta(days=7))
        m_purpose = st.selectbox("Purpose of Muhurat", ["Business", "Marriage"])
        
        if m_start > m_end:
            st.error("Start date must be before end date.")
        else:
            muhurat_list = num_engine.evaluate_muhurat_dates(m_start, m_end, purpose=m_purpose)
            m_df = pd.DataFrame(muhurat_list)
            m_df["Date"] = m_df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
            m_df["Reasons / Checkers"] = m_df["reasons"].apply(lambda x: " | ".join(x))
            
            st.dataframe(m_df[["Date", "root", "destiny", "status", "Reasons / Checkers"]],
                         column_config={
                             "Date": "Date",
                             "root": "Root",
                             "destiny": "Destiny",
                             "status": "Muhurat Aura",
                             "Reasons / Checkers": "Details"
                         }, use_container_width=True)
            
            st.info("Note: Default auspicious time for Abhijeet Muhurat is recommended between 11:45 AM and 12:15 PM.")
