# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields


class FestymasParticipant(models.Model):
    _name = "festymas.participant"
    _description = "Festymas Participants, Bands and Artists"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    location_id = fields.Many2one("festymas.location", string="Location")
    festymas_concert_ids = fields.Many2many("festymas.concert", string="Concerts")
