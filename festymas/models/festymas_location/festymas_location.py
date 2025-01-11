# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from geopy.geocoders import Nominatim


class FestymasLocation(models.Model):
    _name = "festymas.location"
    _description = "Festymas Location"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    festymas_concert_ids = fields.One2many(
        "festymas.concert", "location_id", string="Concerts"
    )
    festymas_festival_ids = fields.One2many(
        "festymas.festival", "location_id", string="Festivals"
    )
    is_concert_hall = fields.Boolean(
        string="Is concert hall?",
    )
    city_id = fields.Many2one(
        "res.city",
        "City",
        auto_join=True,
        ondelete="cascade",
        index=True,
    )
    image_url = fields.Char(string="Image URL")
    state_id = fields.Many2one(related="city_id.state_id")
    country_id = fields.Many2one(related="city_id.country_id")
    ubication_x = fields.Float(string="Ubication X")
    ubication_y = fields.Float(string="Ubication Y")
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

    def write(self, vals):
        if "city_id" in vals:
            geolocator = Nominatim(user_agent="pepito")
            city_record = self.env["res.city"].browse(vals["city_id"])
            location = geolocator.geocode(
                city_record.name + " " + city_record.state_id.name
            )
            self.ubication_x = location.latitude
            self.ubication_y = location.longitude
        return super(FestymasLocation, self).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        geolocator = Nominatim(user_agent="pepito")
        city_record = self.env["res.city"].browse(vals_list[0]["city_id"])
        location = geolocator.geocode(
            city_record.name + " " + city_record.state_id.name
        )
        vals_list[0]["ubication_x"] = location.latitude
        vals_list[0]["ubication_y"] = location.longitude
        return super(FestymasLocation, self).create(vals_list)
