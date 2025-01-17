# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields, api
import requests
import base64


class FestymasParticipant(models.Model):
    _name = "festymas.participant"
    _description = "Festymas Participants, Bands and Artists"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    country_id = fields.Many2one("res.country", string="Country")
    city_id = fields.Many2one("res.city", string="City")
    festymas_concert_ids = fields.Many2many("festymas.concert", string="Concerts")
    festymas_artist_ids = fields.Many2many("festymas.artist", string="Artist")
    festymas_genre_ids = fields.Many2many("festymas.genre", string="Genre")
    is_solo_singer = fields.Boolean(string="Is solo singer?")
    image_url = fields.Char(string="Image URL")
    genres = fields.Char(string="Genres", compute="_compute_genres")
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
