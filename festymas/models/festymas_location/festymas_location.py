# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields


class FestymasLocation(models.Model):
    _name = "festymas.location"
    _description = "Festymas Location"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    festymas_concert_ids = fields.One2many(
        "festymas.concert", "location_id", string="Concerts"
    )
    festymas_festival_ids = fields.One2many(
        "festymas.festival", "location_id", string="Festivals"
    )
