from typing import Dict
import re


# ============================================================
# Normalize Restaurant Name
# ============================================================

def normalize_name(name: str) -> str:
    """
    Normalize restaurant names for comparison.

    Examples:
    Paradise Food Court -> paradise
    Paradise Restaurant -> paradise
    Paradise Biryani -> paradise
    """

    if not name:
        return ""

    name = name.lower()

    words_to_remove = [
        "restaurant",
        "restaurants",
        "food",
        "food court",
        "biryani",
        "hotel",
        "cafe",
        "kitchen",
    ]

    for word in words_to_remove:
        name = name.replace(word, "")

    name = re.sub(r"[^a-z0-9 ]", "", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


# ============================================================
# Compare Restaurant Profiles
# ============================================================

def validate_restaurant_data(
    pdf_profile: Dict,
    website_profile: Dict,
):
    """
    Validate that Website and PDF belong to the same restaurant.
    """

    conflicts = []

    pdf_name = normalize_name(
        pdf_profile.get("restaurant_name", "")
    )

    website_name = normalize_name(
        website_profile.get("restaurant_name", "")
    )

    # --------------------------------------------------------
    # Restaurant Name Missing
    # --------------------------------------------------------

    if not pdf_name:
        return {
            "valid": False,
            "message": "Restaurant name could not be extracted from the PDF.",
            "conflicts": ["Missing restaurant name in PDF"],
        }

    if not website_name:
        return {
            "valid": False,
            "message": "Restaurant name could not be extracted from the Website.",
            "conflicts": ["Missing restaurant name in Website"],
        }

    # --------------------------------------------------------
    # Restaurant Name Validation
    # --------------------------------------------------------

    if (
        pdf_name != website_name
        and pdf_name not in website_name
        and website_name not in pdf_name
    ):
        conflicts.append(
            f"Restaurant name mismatch ({pdf_name} vs {website_name})"
        )

    # --------------------------------------------------------
    # Phone
    # --------------------------------------------------------

    if (
        pdf_profile.get("phone")
        and website_profile.get("phone")
        and pdf_profile["phone"] != website_profile["phone"]
    ):
        conflicts.append("Phone number mismatch")

    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------

    if (
        pdf_profile.get("email")
        and website_profile.get("email")
        and pdf_profile["email"] != website_profile["email"]
    ):
        conflicts.append("Email mismatch")

    # --------------------------------------------------------
    # Address
    # --------------------------------------------------------

    if (
        pdf_profile.get("address")
        and website_profile.get("address")
        and pdf_profile["address"].strip().lower()
        != website_profile["address"].strip().lower()
    ):
        conflicts.append("Restaurant address mismatch")

    # --------------------------------------------------------
    # Timings
    # --------------------------------------------------------

    if (
        pdf_profile.get("timings")
        and website_profile.get("timings")
        and pdf_profile["timings"].strip().lower()
        != website_profile["timings"].strip().lower()
    ):
        conflicts.append("Restaurant timings mismatch")

    # --------------------------------------------------------
    # Final Result
    # --------------------------------------------------------

    if conflicts:
        return {
            "valid": False,
            "message": "Restaurant website and uploaded menu PDF do not belong to the same restaurant.",
            "conflicts": conflicts,
        }

    return {
        "valid": True,
        "message": "Restaurant verified successfully.",
        "conflicts": [],
    }