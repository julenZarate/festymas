# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
{
    "name": "Festymas",
    "version": "16.0.1.0.0",
    "category": "Festymas S.L",
    "author": "Julen Zarate",
    "license": "LGPL-3",
    "depends": ["base", "auth_signup", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/festymas_artist_views.xml",
        "views/festymas_genre_views.xml",
        "views/festymas_participant_views.xml",
        "views/festymas_concert_views.xml",
        "views/festymas_festival_views.xml",
        "views/festymas_location_views.xml",
        "views/menuitem_data.xml",
    ],
    "installable": True,
    "application": False,
}
