# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields


class FestymasParticipant(models.Model):
    _inherit = "res.users"

    favorite_concert_ids = fields.Many2many(
        "festymas.concert", string="Favorite Concerts"
    )
    favorite_festival_ids = fields.Many2many(
        "festymas.festival", string="Favorite Festivals"
    )
    favorite_participant_ids = fields.Many2many(
        "festymas.participant", string="Favorite Participants"
    )
    ubication_latitude = fields.Float(string="Ubication Latitude")
    ubication_longitude = fields.Float(string="Ubication Longitude")
    distance = fields.Float(string="Distance")
    favorite_genre_ids = fields.Many2many("festymas.genre", string="Genres")
    friend_users_ids = fields.Many2many(
        "res.users", "res_users_res_users_rel", "user_id", "friend_id", string="Friends"
    )
