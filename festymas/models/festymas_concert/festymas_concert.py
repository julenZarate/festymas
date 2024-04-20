# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields


class FestymasConcert(models.Model):
    _name = "festymas.concert"
    _description = "Festymas Concert"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    location_id = fields.Many2one("festymas.location", string="Location")
    date = fields.Date(string="Date")
    festymas_participant_ids = fields.Many2many(
        "festymas.participant", string="Participants"
    )
    festymas_genre_ids = fields.Many2many(
        "festymas.genre", string="Genres"
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
