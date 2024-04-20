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
    is_concert_hall = fields.Boolean(
        string="Is concert hall?",
    )
    # images
    cartel_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    # resized fields stored (as attachment) for performance
    cartel_1024 = fields.Image(
        "Image 1024", related="cartel_1920", max_width=1024, max_height=1024, store=True
    )
    cartel_512 = fields.Image(
        "Image 512", related="cartel_1920", max_width=512, max_height=512, store=True
    )
    cartel_256 = fields.Image(
        "Image 256", related="cartel_1920", max_width=256, max_height=256, store=True
    )
    cartel_128 = fields.Image(
        "Image 128", related="cartel_1920", max_width=128, max_height=128, store=True
    )
