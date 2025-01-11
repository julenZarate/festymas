# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields, api
import requests
import base64


class FestymasFestival(models.Model):
    _name = "festymas.festival"
    _description = "Festymas Festival"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    location_id = fields.Many2one("festymas.location", string="Location")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    price = fields.Float(string="Price")
    image_url = fields.Char(string="Image URL")
    genres = fields.Char(string="Genres", compute="_compute_genres")
    visit_count = fields.Integer(string="Visit Count", default=0)
    festymas_concert_ids = fields.Many2many(
        string="Concerts", comodel_name="festymas.concert"
    )
    festymas_genre_ids = fields.Many2many("festymas.genre", string="Genres")
    image = fields.Image(
        string="Imagen",
        compute="_compute_image",
        max_width=1920,
        max_height=1920,
        store=True,
    )
    city_id = fields.Many2one(string="City", related="location_id.city_id")

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
