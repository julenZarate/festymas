# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields


class FestymasFestival(models.Model):
    _name = "festymas.festival"
    _description = "Festymas Festival"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    location_id = fields.Many2one("festymas.location", string="Location")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    festymas_concert_ids = fields.Many2many("festymas.concert", string="Concerts")
