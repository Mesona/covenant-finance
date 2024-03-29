#!/usr/bin/python3

from src.covenant import Covenant


def semita():
    """A sample covenant laid out on page 68 of the covenants book."""
    cov = Covenant(
        name = 'Semita Errabunda',
        season = 'spring',
        income_sources = {'trading' : 100},
        treasury = 100.0,
    )

    matching_magic_items = [item for item in cov.armory.magic if item["saving_category"] == "servants"]

    cov.laboratories.add_lab("Carolus", "Carolus", 0)
    cov.laboratories.add_lab("Mari", "Mari", 0)
    cov.laboratories.add_lab("Mortamis", "Mortamis", 0)
    cov.laboratories.add_lab("Tillitus", "Tillitus", 0)
    cov.laboratories.add_lab("Darius", "Darius", 2)

    crafters = [
            ("bookbinder", "crafter", "bookbinder", "writing", 6, "rare"),
            ("illuminator", "crafter", "illuminator", "writing", 6, "rare"),
            ("brewer1", "crafter", "brewer", "provisions", 6, "common"),
            ("brewer2", "crafter", "brewer", "provisions", 6, "common"),
            ("bass", "crafter", "carpenter", "buildings", 6, "common"),
            ("carp", "crafter", "carpenter", "buildings", 6, "common"),
            ("thatch", "crafter", "thatcher", "buildings", 6, "common"),
            ("fern", "crafter", "furniture_maker", "buildings", 6, "common"),
            ("smith", "crafter", "blacksmith", "consumables", 6, "common"),
            ("candle", "crafter", "candlemaker", "consumables", 6, "common"),
            ("tinker", "crafter", "tinker", "consumables", 6, "common"),
            ("spy", "crafter", "cobbler", "consumables", 6, "common"),
    ]

    for i in range(12):
        cov.covenfolken.add_covenfolk(
                *crafters[i]
        )

    for i in range(4):
        cov.covenfolken.add_covenfolk(
            f"specialist{i}",
            "specialist",
        )

    for i in range(5):
        cov.covenfolken.add_covenfolk(
            f"dependant{i}",
            "dependant",
        )

    for i in range(20):
        cov.covenfolken.add_covenfolk(
            f"grog{i}",
            "grog",
        )

    for i in range(40):
        cov.covenfolken.add_covenfolk(
            f"laborer{i}",
            "laborer",
        )

    for i in range(16):
        cov.covenfolken.add_covenfolk(
            f"servant{i}",
            "servant",
        )

    for i in range(4):
        cov.covenfolken.add_covenfolk(
            f"teamster{i}",
            "teamster",
        )

    for i in range(4):
        cov.covenfolken.add_covenfolk(
            f"companion{i}",
            "companion",
        )

    for i in range(6):
        cov.covenfolken.add_covenfolk(
            f"horse{i}","horse",
        )

    cov.covenfolken.add_covenfolk(
            "Carolus", "magi",
    )
    cov.covenfolken.add_covenfolk(
            "Darius", "magi",
    )
    cov.covenfolken.add_covenfolk(
            "Mari", "magi",
    )
    cov.covenfolken.add_covenfolk(
            "Moratamis", "magi",
    )
    cov.covenfolken.add_covenfolk(
            "Tillitus", "magi",
    )

    for i in range(20):
        cov.armory.add_equipment("scalemail", "full", "standard")
        cov.armory.add_equipment("longsword", "weapon", "standard")
        cov.armory.add_equipment("shield", "weapon", "standard")
        cov.armory.add_equipment("axe", "weapon", "standard")
        cov.armory.add_equipment("longsword", "weapon", "standard")

    cov.armory.add_equipment(
            "Magic broom",
            "magic",
            "magic",
            "servants",
            2,
            "Does the work of 2 servants"
        )

    cov.armory.add_equipment(
            "Magic broom",
            "magic",
            "magic",
            "servants",
            2,
            "Does the work of 2 servants"
        )

    return cov
