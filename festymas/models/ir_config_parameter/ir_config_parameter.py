# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)
import secrets

from odoo import models
from odoo.tools import mute_logger


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    @mute_logger("odoo.addons.base.models.ir_config_parameter")
    def init(self, force=False):
        res = super().init(force=force)
        key = "festymas.token"
        param = self.search([("key", "=", key)])
        if not param:
            self.create({"key": key, "value": secrets.token_hex(16)})
        return res
