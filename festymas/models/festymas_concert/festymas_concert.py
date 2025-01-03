# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields, api
import requests
import base64


class FestymasConcert(models.Model):
    _name = "festymas.concert"
    _description = "Festymas Concert"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    location_id = fields.Many2one("festymas.location", string="Location")
    start_date = fields.Date(string="Start Date")
    price = fields.Float(string="Price")
    visit_count = fields.Integer(string="Visit Count", default=0)
    festymas_participant_ids = fields.Many2many(
        "festymas.participant", string="Participants"
    )
    festymas_genre_ids = fields.Many2many("festymas.genre", string="Genres")
    genres = fields.Char(string="Genres", compute="_compute_genres")
    image_url = fields.Char(string="Image URL")
    festymas_festival_ids = fields.Many2many("festymas.festival", string="Festivals")
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
    image = fields.Image(
        string="Imagen",
        compute="_compute_image",
        max_width=1920,
        max_height=1920,
        store=True,
    )

    @api.depends("image_url")
    def _compute_image(self):
        for record in self:
            if record.image_url:
                try:
                    response = requests.get(record.image_url)
                    if response.status_code == 200:
                        record.image = base64.b64encode(response.content)
                    else:
                        record.image = False
                except Exception as e:
                    record.image = False
            else:
                record.image = False

    @api.depends("festymas_genre_ids")
    def _compute_genres(self):
        for record in self:
            record.genres = ", ".join(record.festymas_genre_ids.mapped("name"))
