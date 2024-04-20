# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields


class FestymasGenre(models.Model):
    _name = "festymas.genre"
    _description = "Festymas Genre"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    festymas_concert_ids = fields.Many2many("festymas.concert", string="Concerts")
    festymas_artist_ids = fields.Many2many("festymas.artist", string="Artists")
    festymas_participant_ids = fields.Many2many("festymas.participant", string="Participants")
    festymas_festival_ids = fields.Many2many("festymas.festival", string="Festivals")
