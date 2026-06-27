import re
from typing import Dict


# ============================================================
# Restaurant Profile Extraction
# ============================================================

def extract_restaurant_profile(text: str) -> Dict:
    """
    Extract important restaurant information
    from PDF or Website text.
    """

    profile = {
        "restaurant_name": "",
        "phone": "",
        "email": "",
        "address": "",
        "timings": "",
        "menu": {}
    }

    if not text:
        return profile

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # --------------------------------------------------------
    # Restaurant Name
    # --------------------------------------------------------

    if lines:
        profile["restaurant_name"] = lines[0]

    # --------------------------------------------------------
    # Phone Number
    # --------------------------------------------------------

    phone = re.search(
        r'(\+?\d[\d\s-]{8,15})',
        text
    )

    if phone:
        profile["phone"] = phone.group(1).strip()

    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------

    email = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    if email:
        profile["email"] = email.group(0)

    # --------------------------------------------------------
    # Timings
    # --------------------------------------------------------

    timing = re.search(
        r'(\d{1,2}\s?(AM|PM)\s?[-–]\s?\d{1,2}\s?(AM|PM))',
        text,
        re.IGNORECASE
    )

    if timing:
        profile["timings"] = timing.group(1)

    # --------------------------------------------------------
    # Address
    # --------------------------------------------------------

    for line in lines:

        if any(
            word in line.lower()
            for word in [
                "road",
                "street",
                "lane",
                "colony",
                "city",
                "hyderabad",
                "bangalore",
                "mumbai",
                "address"
            ]
        ):
            profile["address"] = line
            break

    # --------------------------------------------------------
    # Menu Items
    # --------------------------------------------------------

    menu_pattern = re.compile(
        r'(.+?)\s+(₹|Rs\.?)?\s*(\d+)',
        re.IGNORECASE
    )

    for line in lines:

        match = menu_pattern.search(line)

        if match:

            item = match.group(1).strip()

            price = int(match.group(3))

            profile["menu"][item] = price

    return profile


# ============================================================
# Compare Restaurant Profiles
# ============================================================

def validate_restaurant_data(
    pdf_profile: Dict,
    website_profile: Dict,
):
    """
    PDF is treated as the latest source of truth.

    Every important field must match.
    """

    conflicts = []

    # --------------------------------------------------------
    # Restaurant Name
    # --------------------------------------------------------

    if (
        pdf_profile["restaurant_name"].lower()
        != website_profile["restaurant_name"].lower()
    ):
        conflicts.append("Restaurant name mismatch")

    # --------------------------------------------------------
    # Phone
    # --------------------------------------------------------

    if (
        pdf_profile["phone"]
        and website_profile["phone"]
        and pdf_profile["phone"] != website_profile["phone"]
    ):
        conflicts.append("Phone number mismatch")

    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------

    if (
        pdf_profile["email"]
        and website_profile["email"]
        and pdf_profile["email"] != website_profile["email"]
    ):
        conflicts.append("Email mismatch")

    # --------------------------------------------------------
    # Address
    # --------------------------------------------------------

    if (
        pdf_profile["address"]
        and website_profile["address"]
        and pdf_profile["address"].lower()
        != website_profile["address"].lower()
    ):
        conflicts.append("Restaurant address mismatch")

    # --------------------------------------------------------
    # Timings
    # --------------------------------------------------------

    if (
        pdf_profile["timings"]
        and website_profile["timings"]
        and pdf_profile["timings"].lower()
        != website_profile["timings"].lower()
    ):
        conflicts.append("Restaurant timings mismatch")

    # --------------------------------------------------------
    # Menu Items & Prices
    # --------------------------------------------------------

    pdf_menu = pdf_profile["menu"]
    website_menu = website_profile["menu"]

    for item, pdf_price in pdf_menu.items():

        if item not in website_menu:

            conflicts.append(
                f"Menu item missing on website: {item}"
            )

            continue

        if website_menu[item] != pdf_price:

            conflicts.append(
                f"Price mismatch for '{item}' "
                f"(PDF: ₹{pdf_price}, Website: ₹{website_menu[item]})"
            )

    # --------------------------------------------------------
    # Final Result
    # --------------------------------------------------------

    if conflicts:

        return {
            "valid": False,
            "message":
                "Restaurant website and latest uploaded menu PDF are not synchronized.",
            "conflicts": conflicts,
        }

    return {
        "valid": True,
        "message": "Restaurant verified successfully.",
        "conflicts": [],
    }