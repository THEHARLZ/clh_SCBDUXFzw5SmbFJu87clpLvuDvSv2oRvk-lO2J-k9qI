#!/usr/bin/env python3
"""
Flux Capacitor Calculator
Inspired by Back to the Future

"Roads? Where we're going, we don't need roads." - Doc Brown
"""

import random

# The magic number - 1.21 gigawatts!
GIGAWATTS_REQUIRED = 1.21

# Key dates from the Back to the Future trilogy
ICONIC_DATES = {
    "original_departure": "October 26, 1985",
    "destination_1955": "November 5, 1955",
    "destination_2015": "October 21, 2015",
    "destination_1885": "September 2, 1885",
}


def calculate_power_status(available_gigawatts: float) -> dict:
    """
    Check if you have enough power for the flux capacitor.

    Args:
        available_gigawatts: The amount of power available in gigawatts

    Returns:
        A dict containing the power status and message
    """
    if available_gigawatts >= GIGAWATTS_REQUIRED:
        surplus = available_gigawatts - GIGAWATTS_REQUIRED
        return {
            "ready": True,
            "message": "Great Scott! The flux capacitor is ready!",
            "surplus_gigawatts": round(surplus, 2),
        }
    else:
        deficit = GIGAWATTS_REQUIRED - available_gigawatts
        return {
            "ready": False,
            "message": "Heavy! You need more power!",
            "deficit_gigawatts": round(deficit, 2),
        }


def get_time_travel_quote() -> str:
    """Return an iconic Back to the Future quote."""
    quotes = [
        '"Roads? Where we\'re going, we don\'t need roads." - Doc Brown',
        '"Great Scott!" - Doc Brown',
        '"This is heavy." - Marty McFly',
        '"If my calculations are correct, when this baby hits 88 miles per hour, '
        'you\'re gonna see some serious stuff." - Doc Brown',
        '"Nobody calls me chicken." - Marty McFly',
    ]

    return random.choice(quotes)


def display_flux_capacitor_ascii():
    """Display ASCII art of the flux capacitor."""
    flux_art = r"""
    ╔═══════════════════════════╗
    ║      FLUX CAPACITOR       ║
    ║         ⚡ ⚡ ⚡           ║
    ║        \  |  /            ║
    ║         \ | /             ║
    ║          \|/              ║
    ║           █               ║
    ║          /|\              ║
    ║         / | \             ║
    ║        /  |  \            ║
    ║         ⚡ ⚡ ⚡           ║
    ║   1.21 GIGAWATTS NEEDED   ║
    ╚═══════════════════════════╝
    """
    print(flux_art)


def main():
    """Main function - run the flux capacitor calculator."""
    print("\n" + "=" * 50)
    print("🚗 DELOREAN TIME MACHINE - FLUX CAPACITOR SYSTEM 🚗")
    print("=" * 50)

    display_flux_capacitor_ascii()

    print("\n📅 Iconic Time Travel Dates:")
    for event, date in ICONIC_DATES.items():
        print(f"   • {event.replace('_', ' ').title()}: {date}")

    print(f"\n⚡ Power Required: {GIGAWATTS_REQUIRED} Gigawatts")

    # Example power check
    test_power = 1.5
    status = calculate_power_status(test_power)
    print(f"\n🔋 Current Power: {test_power} Gigawatts")
    print(f"   Status: {'✅ READY' if status['ready'] else '❌ NOT READY'}")
    print(f"   Message: {status['message']}")

    if status["ready"]:
        print(f"   Surplus: {status['surplus_gigawatts']} Gigawatts")
    else:
        print(f"   Deficit: {status['deficit_gigawatts']} Gigawatts")

    print(f"\n💬 Quote of the day: {get_time_travel_quote()}")
    print("\n" + "=" * 50)
    print("Remember: When this baby hits 88 mph, you're gonna see some serious stuff!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
