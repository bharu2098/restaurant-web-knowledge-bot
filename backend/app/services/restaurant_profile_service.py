# ============================================================
# Restaurant Profiles
# ============================================================

website_profile = None
pdf_profile = None
merged_profile = None


# ============================================================
# Website Profile
# ============================================================

def set_website_profile(profile):
    global website_profile
    website_profile = profile


def get_website_profile():
    return website_profile


# ============================================================
# PDF Profile
# ============================================================

def set_pdf_profile(profile):
    global pdf_profile
    pdf_profile = profile


def get_pdf_profile():
    return pdf_profile


# ============================================================
# Merged Profile
# ============================================================

def set_merged_profile(profile):
    global merged_profile
    merged_profile = profile


def get_merged_profile():
    return merged_profile


# ============================================================
# Clear Profiles
# ============================================================

def clear_profiles():
    global website_profile
    global pdf_profile
    global merged_profile

    website_profile = None
    pdf_profile = None
    merged_profile = None