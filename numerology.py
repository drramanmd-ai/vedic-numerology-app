from datetime import date, timedelta

def reduce_digit(val):
    """Reduces any number to a single digit (1-9)."""
    while val > 9:
        val = sum(int(d) for d in str(val))
    return val

def get_root_number(day):
    """Calculates the Root (Psychic) Number from birth day."""
    return reduce_digit(day)

def get_destiny_number(day, month, year):
    """Calculates the Destiny Number from DOB digits."""
    return reduce_digit(day + month + year)

def get_chaldean_char_value(char):
    """Returns the Chaldean value of an uppercase letter."""
    mapping = {
        'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
        'B': 2, 'K': 2, 'R': 2,
        'C': 3, 'G': 3, 'L': 3, 'S': 3,
        'D': 4, 'M': 4, 'T': 4,
        'E': 5, 'H': 5, 'N': 5, 'X': 5,
        'U': 6, 'V': 6, 'W': 6,
        'O': 7, 'Z': 7,
        'F': 8, 'P': 8
    }
    return mapping.get(char.upper(), 0)

def calculate_compound_value(text):
    """Calculates the sum of digits/letters of any text using Chaldean mappings."""
    total = 0
    for char in text:
        if char.isdigit():
            total += int(char)
        elif char.isalpha():
            total += get_chaldean_char_value(char)
    return total

def get_vedic_grid_digits(day, month, year, include_root=True):
    """
    Extracts grid digits from birth date.
    Rules:
      1. DOB Day digits, Month digits, and Year digits (excluding century).
      2. Destiny number.
      3. Root number (only if day is double-digit and not 10, 20, 30).
    """
    digits = []
    
    # 1. Day digits
    for d in str(day):
        if d != '0':
            digits.append(int(d))
            
    # 2. Month digits
    for d in str(month):
        if d != '0':
            digits.append(int(d))
            
    # 3. Year digits (excluding century)
    year_2digit = year % 100
    for d in f"{year_2digit:02d}":
        if d != '0':
            digits.append(int(d))
            
    # 4. Destiny number
    destiny = get_destiny_number(day, month, year)
    digits.append(destiny)
    
    # 5. Root number
    root = get_root_number(day)
    # Check exclusion rules
    is_double_digit = (day >= 10 and day <= 31)
    is_multiple_of_10 = (day in [10, 20, 30])
    should_add_root = is_double_digit and not is_multiple_of_10
    
    if should_add_root and include_root:
        digits.append(root)
        
    return digits

def construct_grid_array(digits):
    """Constructs the counts of digits 1-9 in the Vedic Grid layout."""
    counts = {i: 0 for i in range(1, 10)}
    for d in digits:
        if 1 <= d <= 9:
            counts[d] += 1
    return counts

# Standard Vedic Grid Layout:
# 3 1 9
# 6 7 5
# 2 8 4
GRID_LAYOUT = [
    [3, 1, 9],
    [6, 7, 5],
    [2, 8, 4]
]

def get_mahadashas(birth_date, root_num, max_age=90):
    """
    Generates Mahadasha periods sequentially.
    First Mahadasha is of Root planet, lasting R years.
    Subsequent Mahadashas follow 1->2->...->9 loops, lasting planet number years.
    """
    mahadashas = []
    current_start = birth_date
    current_planet = root_num
    
    # First Mahadasha lasts root years
    duration = current_planet
    current_end = date(current_start.year + duration, current_start.month, current_start.day) - timedelta(days=1)
    age = 0
    mahadashas.append({
        "planet": current_planet,
        "start_date": current_start,
        "end_date": current_end,
        "duration": duration,
        "age_start": age,
        "age_end": age + duration
    })
    
    age += duration
    current_start = current_end + timedelta(days=1)
    
    while age < max_age:
        # Sequentially loop planets 1-9
        current_planet = current_planet + 1
        if current_planet > 9:
            current_planet = 1
        duration = current_planet
        current_end = date(current_start.year + duration, current_start.month, current_start.day) - timedelta(days=1)
        mahadashas.append({
            "planet": current_planet,
            "start_date": current_start,
            "end_date": current_end,
            "duration": duration,
            "age_start": age,
            "age_end": age + duration
        })
        age += duration
        current_start = current_end + timedelta(days=1)
        
    return mahadashas

def get_weekday_planet(dt):
    """Maps date's weekday to Vedic planet number."""
    # Excel WEEKDAY(date, 1): Sunday = 1, Monday = 2, ..., Saturday = 7
    excel_weekday = dt.isoweekday() % 7 + 1
    mapping = {
        1: 1,  # Sunday -> Sun (1)
        2: 2,  # Monday -> Moon (2)
        3: 9,  # Tuesday -> Mars (9)
        4: 5,  # Wednesday -> Mercury (5)
        5: 3,  # Thursday -> Jupiter (3)
        6: 6,  # Friday -> Venus (6)
        7: 8,  # Saturday -> Saturn (8)
    }
    return mapping[excel_weekday]

def get_antardasha(birth_date, target_year, root_num):
    """
    Calculates Antardasha for target year.
    Formula: SingleDigit(Year_2Digit + Root + Month + Day_Planet_Number)
    """
    target_dt = date(target_year, birth_date.month, birth_date.day)
    day_planet = get_weekday_planet(target_dt)
    year_2digit = target_year % 100
    total_sum = year_2digit + root_num + birth_date.month + day_planet
    return reduce_digit(total_sum)

def get_pratyantardashas(birth_date, target_year, antar_planet):
    """
    Calculates Pratyantardasha micro-periods (each of duration 8 * Planet days).
    Starts from active Antardasha planet, sequencing sequentially.
    """
    pratyantars = []
    current_start = date(target_year, birth_date.month, birth_date.day)
    current_planet = antar_planet
    
    for i in range(9):
        duration_days = 8 * current_planet
        current_end = current_start + timedelta(days=duration_days)
        pratyantars.append({
            "planet": current_planet,
            "start_date": current_start,
            "end_date": current_end,
            "duration": duration_days
        })
        current_start = current_end + timedelta(days=1)
        current_planet += 1
        if current_planet > 9:
            current_planet = 1
            
    return pratyantars

# Friendship Table
# Root Number: (Friends, Neutrals, Enemies)
FRIENDSHIP_TABLE = {
    1: ({1, 2, 4, 7}, {5, 6, 8}, {3, 9}),
    2: ({1, 2, 7, 9}, {3, 4, 5, 6}, {8}),
    3: ({3, 6, 9}, {2, 4, 5, 7, 8}, {1}),
    4: ({1, 2, 4, 7, 8}, {5, 6}, {3, 9}),
    5: ({3, 5, 6, 9}, {1, 2, 4, 7, 8}, set()),
    6: ({3, 6, 9}, {1, 2, 4, 5, 7, 8}, set()),
    7: ({2, 3, 6}, {1, 4, 5, 7, 8}, {9}),
    8: ({3, 4, 6, 8}, {2, 5, 7}, {1, 9}),
    9: ({3, 6, 9}, {1, 2, 5, 8}, {4, 7})
}

def get_relationship(n1, n2):
    """Returns 'Friend', 'Neutral', or 'Enemy' for two numbers."""
    if n1 not in FRIENDSHIP_TABLE:
        return 'Neutral'
    friends, neutrals, enemies = FRIENDSHIP_TABLE[n1]
    if n2 in friends:
        return 'Friend'
    if n2 in enemies:
        return 'Enemy'
    return 'Neutral'

def evaluate_matchmaking(boy_dob, girl_dob):
    """
    Evaluates marriage compatibility on a 100-point scale.
    Returns score breakdown, rejections list, warnings, and result.
    """
    # 1. Calculate Roots & Destinies
    b_root = get_root_number(boy_dob.day)
    b_dest = get_destiny_number(boy_dob.day, boy_dob.month, boy_dob.year)
    
    g_root = get_root_number(girl_dob.day)
    g_dest = get_destiny_number(girl_dob.day, girl_dob.month, girl_dob.year)
    
    # 2. Construct grids
    b_digits = get_vedic_grid_digits(boy_dob.day, boy_dob.month, boy_dob.year)
    g_digits = get_vedic_grid_digits(girl_dob.day, girl_dob.month, girl_dob.year)
    
    b_counts = construct_grid_array(b_digits)
    g_counts = construct_grid_array(g_digits)
    
    rejections = []
    
    # Hard Fail: Basic Compatibility Groups
    # Group A: 1, 2, 4, 7
    # Group B: 3, 6, 9
    # Group C: 5
    # Group D: 8 (never 8 or 4)
    def get_group(r):
        if r in [1, 2, 4, 7]: return 'A'
        if r in [3, 6, 9]: return 'B'
        if r == 5: return 'C'
        if r == 8: return 'D'
        return 'Unknown'
        
    b_grp = get_group(b_root)
    g_grp = get_group(g_root)
    
    if b_grp == 'A' and g_grp != 'A':
        rejections.append("Root Group Mismatch: Boy is Group A (1,2,4,7) and Girl is not.")
    elif b_grp == 'B' and g_grp != 'B':
        rejections.append("Root Group Mismatch: Boy is Group B (3,6,9) and Girl is not.")
    elif b_grp == 'C' and g_grp != 'C':
        rejections.append("Root Group Mismatch: Boy is Group C (5) and Girl is not.")
    elif b_grp == 'D':
        if g_root in [8, 4]:
            rejections.append("Forbidden Match: Root 8 must never marry Root 8 or 4.")
    if g_grp == 'D' and b_root in [8, 4]:
        rejections.append("Forbidden Match: Root 8 must never marry Root 8 or 4.")
        
    # Hard Fail: Triple Numbers in either grid
    for num in [2, 3, 4, 7]:
        if b_counts[num] >= 3:
            rejections.append(f"Grid Rejection: Boy's grid contains triple {num}s ({' '.join([str(num)]*3)}).")
        if g_counts[num] >= 3:
            rejections.append(f"Grid Rejection: Girl's grid contains triple {num}s ({' '.join([str(num)]*3)}).")
            
    # Hard Fail: Destiny 1 or 5 with missing 2, 6, 8
    def is_cold_or_selfish(dest, counts):
        if dest in [1, 5]:
            if counts[2] == 0 and counts[6] == 0 and counts[8] == 0:
                return True
        return False
        
    if is_cold_or_selfish(b_dest, b_counts):
        rejections.append(f"Grid Rejection: Boy has Destiny {b_dest} and is missing 2, 6, and 8 (Cold Stone / Selfish).")
    if is_cold_or_selfish(g_dest, g_counts):
        rejections.append(f"Grid Rejection: Girl has Destiny {g_dest} and is missing 2, 6, and 8 (Cold Stone / Selfish).")
        
    # Age check warning: D4 and D8 marry after 30
    warnings = []
    # Note: Age must be checked in the app, but we can flag it here.
    if b_dest in [4, 8]:
        warnings.append("Destiny Check: Boy has Destiny 4/8 and should marry after age 30.")
    if g_dest in [4, 8]:
        warnings.append("Destiny Check: Girl has Destiny 4/8 and should marry after age 30.")
        
    # 3. 100-Point Scoring
    # Root & Destiny Matching: 20 pts
    # Friend = 10 pts, Neutral = 5 pts, Enemy = 0 pts for both Root and Destiny
    r_rel = get_relationship(b_root, g_root)
    d_rel = get_relationship(b_dest, g_dest)
    
    r_pts = 10 if r_rel == 'Friend' else (5 if r_rel == 'Neutral' else 0)
    d_pts = 10 if d_rel == 'Friend' else (5 if d_rel == 'Neutral' else 0)
    rd_score = r_pts + d_pts
    
    # quotients scoring helper
    def get_quotient_score(b_rels, g_rels, category_name):
        if not b_rels or not g_rels:
            # Fallback to Root/Destiny matching score
            return rd_score
        
        # Check enemy relationships between Boy and Girl elements
        enemy_count = 0
        for b in b_rels:
            for g in g_rels:
                if get_relationship(b, g) == 'Enemy':
                    enemy_count += 1
        score = 20 - (10 * enemy_count)
        return max(0, score)
        
    # Emotional Quotient (EQ): 20 pts (Moon=2, Venus=6)
    b_eq = [x for x in [2, 6] if b_counts[x] > 0]
    g_eq = [x for x in [2, 6] if g_counts[x] > 0]
    eq_score = get_quotient_score(b_eq, g_eq, "EQ")
    
    # Practical Quotient (PQ): 20 pts (Saturn=8, Rahu=4, Sun=1)
    b_pq = [x for x in [1, 4, 8] if b_counts[x] > 0]
    g_pq = [x for x in [1, 4, 8] if g_counts[x] > 0]
    pq_score = get_quotient_score(b_pq, g_pq, "PQ")
    
    # Money Quotient: 20 pts (1, 5, 8, Destiny 6)
    b_mon = [x for x in [1, 5, 8] if b_counts[x] > 0]
    if b_dest == 6:
        b_mon.append(6)
    g_mon = [x for x in [1, 5, 8] if g_counts[x] > 0]
    if g_dest == 6:
        g_mon.append(6)
    mon_score = get_quotient_score(b_mon, g_mon, "Money")
    
    # Extra Points (Marriage Savers): 20 pts
    b_savers = b_counts[3] + b_counts[7] + b_counts[8]
    g_savers = g_counts[3] + g_counts[7] + g_counts[8]
    savers_score = min(20, b_savers + g_savers)
    
    total_score = rd_score + eq_score + pq_score + mon_score + savers_score
    
    # 4. 5-Year Litigation Check
    current_year = date.today().year
    litigation_flagged = False
    litigation_years = []
    
    for yr in range(current_year, current_year + 5):
        # Boy's yearly dasha grid
        b_maha_planet = None
        b_dashas = get_mahadashas(boy_dob, b_root)
        for dasha in b_dashas:
            if dasha["start_date"].year <= yr <= dasha["end_date"].year:
                b_maha_planet = dasha["planet"]
                break
        b_antar_planet = get_antardasha(boy_dob, yr, b_root)
        
        b_yr_digits = b_digits + ([b_maha_planet] if b_maha_planet else []) + [b_antar_planet]
        b_yr_counts = construct_grid_array(b_yr_digits)
        
        # Girl's yearly dasha grid
        g_maha_planet = None
        g_dashas = get_mahadashas(girl_dob, g_root)
        for dasha in g_dashas:
            if dasha["start_date"].year <= yr <= dasha["end_date"].year:
                g_maha_planet = dasha["planet"]
                break
        g_antar_planet = get_antardasha(girl_dob, yr, g_root)
        
        g_yr_digits = g_digits + ([g_maha_planet] if g_maha_planet else []) + [g_antar_planet]
        g_yr_counts = construct_grid_array(g_yr_digits)
        
        def has_litigation(counts):
            if counts[6] == 0:
                return True
            if counts[9] > 0 and counts[4] > 0 and counts[5] == 0:
                if counts[4] % 2 != 0:
                    return True
            if counts[5] > 0 and counts[4] > 0 and counts[9] == 0:
                if counts[4] % 2 != 0:
                    return True
            return False
            
        b_lit = has_litigation(b_yr_counts)
        g_lit = has_litigation(g_yr_counts)
        
        b_savior = b_maha_planet in [7, 8] or b_antar_planet in [7, 8]
        g_savior = g_maha_planet in [7, 8] or g_antar_planet in [7, 8]
        
        if b_lit or g_lit:
            litigation_flagged = True
            litigation_years.append({
                "year": yr,
                "boy_litigation": b_lit,
                "girl_litigation": g_lit,
                "boy_savior": b_savior,
                "girl_savior": g_savior,
                "boy_counts": b_yr_counts,
                "girl_counts": g_yr_counts,
                "boy_maha": b_maha_planet,
                "boy_antar": b_antar_planet,
                "girl_maha": g_maha_planet,
                "girl_antar": g_antar_planet
            })
            
    if litigation_flagged:
        warnings.append("Litigation Warning: Litigation or disputes will be active for at least one partner in the next 5 years.")
        
    is_approved = (total_score >= 50) and (not rejections)
    
    return {
        "boy_root": b_root,
        "boy_destiny": b_dest,
        "girl_root": g_root,
        "girl_destiny": g_dest,
        "rd_score": rd_score,
        "eq_score": eq_score,
        "pq_score": pq_score,
        "mon_score": mon_score,
        "savers_score": savers_score,
        "total_score": total_score,
        "rejections": rejections,
        "warnings": warnings,
        "is_approved": is_approved,
        "litigation_years": litigation_years
    }

def evaluate_muhurat_dates(start_date, end_date, purpose="Business"):
    """Evaluates suitability for business or marriage Muhurat in a date range."""
    evaluated_list = []
    curr = start_date
    
    while curr <= end_date:
        r = get_root_number(curr.day)
        d = get_destiny_number(curr.day, curr.month, curr.year)
        digits = get_vedic_grid_digits(curr.day, curr.month, curr.year)
        counts = construct_grid_array(digits)
        
        status = "Good"
        reasons = []
        
        if purpose == "Business":
            money_savers = counts[1] + counts[5] + counts[8] + (1 if d == 6 else 0)
            if counts[2] > 0 and counts[8] > 0 and counts[4] > 0:
                status = "Rejected"
                reasons.append("Rejected due to 2-8-4 layout presence (causes extreme life instability).")
            for num in [2, 3, 4, 7]:
                if counts[num] >= 3:
                    status = "Rejected"
                    reasons.append(f"Rejected due to triple {num}s ({' '.join([str(num)]*3)}).")
                    
            if status != "Rejected":
                if money_savers >= 2:
                    status = "Excellent"
                elif money_savers == 1:
                    status = "Good"
                else:
                    status = "Average"
            reasons.append(f"Money numbers count: {money_savers} ({'+1,' if counts[1]>0 else ''}{'+5,' if counts[5]>0 else ''}{'+8,' if counts[8]>0 else ''}{'D6' if d==6 else ''})")
            
        else: # Marriage
            settle_savers = counts[3] + counts[7] + counts[8]
            if counts[6] >= 2:
                status = "Rejected"
                reasons.append("Rejected due to 66 (causes family disturbances).")
            if counts[2] >= 2:
                status = "Rejected"
                reasons.append("Rejected due to 22 (causes emotional instability).")
            for num in [2, 3, 4, 7]:
                if counts[num] >= 3:
                    status = "Rejected"
                    reasons.append(f"Rejected due to triple {num}s ({' '.join([str(num)]*3)}).")
                    
            if status != "Rejected":
                if settle_savers >= 2:
                    status = "Excellent"
                elif settle_savers == 1:
                    status = "Good"
                else:
                    status = "Average"
            reasons.append(f"Marriage savers count: {settle_savers} ({'+3,' if counts[3]>0 else ''}{'+7,' if counts[7]>0 else ''}{'+8' if counts[8]>0 else ''})")
            
        evaluated_list.append({
            "date": curr,
            "root": r,
            "destiny": d,
            "status": status,
            "reasons": reasons
        })
        curr += timedelta(days=1)
        
    return evaluated_list
