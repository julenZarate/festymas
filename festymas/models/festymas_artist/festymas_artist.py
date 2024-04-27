# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields


class FestymasArtist(models.Model):
    _name = "festymas.artist"
    _description = "Festymas Artists"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    festymas_participant_ids = fields.Many2many(
        "festymas.participant", string="Participants"
    )
    festymas_genre_ids = fields.Many2many("festymas.genre", string="Genres")
