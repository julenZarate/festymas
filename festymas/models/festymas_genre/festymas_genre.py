# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models, fields


class FestymasGenre(models.Model):
    _name = "festymas.genre"
    _description = "Festymas Genre"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
