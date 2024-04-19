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
