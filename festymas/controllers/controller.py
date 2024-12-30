# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)

import json
import logging
import math

from odoo import http
from odoo.exceptions import AccessDenied
from odoo.http import request

_logger = logging.getLogger(__name__)


class FestymasController(http.Controller):
    _items_per_page = 10
    _items_per_home = 10

    @http.route(
        [
            "/festymas/concerts",
            "/festymas/concerts/<string:id>",
            "/festymas/concerts/page/<int:page>",
            "/festymas/concerts/home",
            "/festymas/concerts/search/<string:search>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_concerts(self, id=None, page=None, search=None, **kw):
        model = "festymas.concert"
        fields = [
            "name",
            "description",
            "location_id",
            "start_date",
            "price",
            "festymas_participant_ids",
            "festymas_festival_ids",
            "festymas_genre_ids",
            "cartel_1920",
            "visit_count",
        ]
        login_error = False
        if login_error:
            return login_error
        if request.httprequest.path == "/festymas/concerts/home":
            data = self._get_festymas_home(fields, model)
            return data
        domain = self._get_domain(model, id, search)
        data, max_pages = self._get_filtered_data(model, fields, domain, page)
        return data, max_pages

    @http.route(
        [
            "/festymas/festivals",
            "/festymas/festivals/<string:id>",
            "/festymas/festivals/page/<int:page>",
            "/festymas/festivals/home",
            "/festymas/festivals/search/<string:search>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_festivals(self, id=None, page=None, search=None, **kw):
        model = "festymas.festival"
        fields = [
            "name",
            "description",
            "location_id",
            "start_date",
            "end_date",
            "price",
            "festymas_concert_ids",
            "festymas_genre_ids",
            "cartel_1920",
            "visit_count",
        ]
        login_error = False
        if login_error:
            return login_error
        if request.httprequest.path == "/festymas/festivals/home":
            data = self._get_festymas_home(fields, model)
            return data
        data, max_pages = self._get_filtered_data(model, fields, domain, page)
        return data, max_pages

    @http.route(
        [
            "/festymas/participants",
            "/festymas/participants/<string:id>",
            "/festymas/participants/page/<int:page>",
            "/festymas/participants/home",
            "/festymas/participants/search/<string:search>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_participants(self, id=None, page=None, search=None, **kw):
        model = "festymas.participant"
        fields = [
            "name",
            "description",
            "country_id",
            "festymas_concert_ids",
            "festymas_artist_ids",
            "festymas_concert_ids",
            "festymas_genre_ids",
            "cartel_1920",
        ]
        login_error = False
        if login_error:
            return login_error
        if request.httprequest.path == "/festymas/participants/home":
            data = self._get_festymas_home(fields, model)
            return data
        domain = self._get_domain(model, id, search)
        data, max_pages = self._get_filtered_data(model, fields, domain, page)
        return data, max_pages

    @http.route(
        [
            "/festymas/locations",
            "/festymas/locations/<string:id>",
            "/festymas/locations/page/<int:page>",
            "/festymas/locations/search/<string:search>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_locations(self, id=None, page=None, search=None, **kw):
        model = "festymas.location"
        fields = [
            "name",
            "description",
            "city_id",
            "state_id",
            "country_id",
            "festymas_concert_ids",
            "festymas_festival_ids",
        ]
        login_error = False
        if login_error:
            return login_error
        domain = self._get_domain(model, id, search)
        data, max_pages = self._get_filtered_data(model, fields, domain, page)
        return data, max_pages

    @http.route(
        [
            "/festymas/artists",
            "/festymas/artists/<string:id>",
            "/festymas/artists/page/<int:page>",
            "/festymas/artists/search/<string:search>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_artist(self, id=None, page=None, search=None, **kw):
        model = "festymas.artist"
        fields = ["name", "description", "festymas_participant_ids"]
        login_error = False
        if login_error:
            return login_error
        domain = self._get_domain(model, id, search)
        data, max_pages = self._get_filtered_data(model, fields, domain, page)
        return data, max_pages

    @http.route(
        [
            "/festymas/genres",
            "/festymas/genres/<string:id>",
            "/festymas/genres/page/<int:page>",
            "/festymas/genres/search/<string:search>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_genres(self, id=None, page=None, search=None, **kw):
        model = "festymas.genre"
        fields = [
            "name",
            "description",
            "festymas_participant_ids",
            "festymas_festival_ids",
            "festymas_concert_ids",
        ]
        login_error = False
        if login_error:
            return login_error
        domain = self._get_domain(model, id, search)
        data, max_pages = self._get_filtered_data(model, fields, domain, page)
        return data, max_pages

    @http.route(
        [
            "/festymas/cities",
            "/festymas/cities/<string:id>",
            "/festymas/cities/page/<int:page>",
            "/festymas/cities/search/<string:search>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_cities(self, id=None, page=None, search=None, **kw):
        model = "res.city"
        fields = [
            "name",
        ]
        login_error = False
        if login_error:
            return login_error
        domain = self._get_domain(model, id, search)
        data, max_pages = self._get_filtered_data(model, fields, domain, page)
        return data, max_pages

    @http.route(
        [
            "/festymas/states",
            "/festymas/states/<string:id>",
            "/festymas/states/page/<int:page>",
            "/festymas/states/search/<string:search>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_states(self, id=None, page=None, search=None, **kw):
        model = "res.country"
        domain = [("country_id", "=", 68)]
        login_error = False
        if login_error:
            return login_error
        domain = self._get_domain(model, id, search)
        data, max_pages = self._get_filtered_data(model, fields, domain, page)
        return data, max_pages

    def _get_domain(self, model, id, search):
        domain = []
        if request.dispatcher:
            body = request.dispatcher.jsonrequest
            if body.get("ubication"):
                domain += self._generate_ubication_domain(body.get("ubication"))
                if not domain:
                    return []
            body = request.dispatcher.jsonrequest
            if body.get("adjustment"):
                domain += self._generate_adjustment_domain(body.get("adjustment"))
        if id:
            ids = id.split(",")
            domain.append(("id", "in", ids))
        if search:
            domain.append(("name", "ilike", search))
        return domain

    def _get_filtered_data(self, model, fields, domain, page):
        offset = False
        limit = False
        sort = False
        model_env = request.env[model]
        search_fields = fields
        _logger.info("Checking festymas {}...".format(model))

        if request.httprequest.args.get("sort_by"):
            sort = (
                request.httprequest.args.get("sort_by")
                + " "
                + request.httprequest.args.get("sort_in")
            )
        if page:
            offset = ((page - 1) * self._items_per_page,)
            limit = self._items_per_page
        filtered_data = model_env.sudo().search_read(
            domain=domain,
            fields=search_fields,
            limit=limit,
            offset=offset,
            order=sort,
        )
        max_pages = {
            "pagination": {
                "max_pages": math.ceil(
                    self._get_model_count(model, domain) / self._items_per_page
                )
            }
        }
        return filtered_data, max_pages

    def _get_festymas_home(self, fields, model):
        data = (
            request.env[model]
            .sudo()
            .search_read(
                [], fields=fields, order="visit_count desc", limit=self._items_per_home
            )
        )
        return data

    def _get_model_count(self, model, domain=[]):
        count = request.env[model].sudo().search_count(domain)
        return count

    def _generate_adjustment_domain(self, adjustments):
        domain = []
        for adjustment in adjustments:
            domain.append((adjustment, "in", adjustments[adjustment]))
        return domain

    def _generate_ubication_domain(self, ubication):
        domain = []
        location_ids = []
        location_ids = self.ubicaciones_en_radio(ubication)
        if not location_ids:
            return domain
        domain.append(("location_id.id", "in", location_ids))
        return domain

    def ubicaciones_en_radio(self, ubication):
        """
        Encuentra todas las ubicaciones dentro de una distancia máxima
        alrededor de una ubicación dada.
        """
        location_ids = []
        lat_dispositivo = ubication["latitude"]
        lon_dispositivo = ubication["longitude"]
        distancia_maxima = ubication["distance"]
        ubicaciones_backend = (
            request.env["festymas.location"]
            .sudo()
            .search_read([], fields=["ubication_x", "ubication_y"])
        )
        for ubicacion in ubicaciones_backend:
            lat = ubicacion["ubication_x"]
            lon = ubicacion["ubication_y"]
            distancia = self.calcular_distancia(
                lat_dispositivo, lon_dispositivo, lat, lon
            )
            if distancia <= distancia_maxima:
                location_ids.append(ubicacion["id"])

        return location_ids

    def calcular_distancia(self, lat1, lon1, lat2, lon2):
        """
        Calcula la distancia entre dos puntos en la superficie de la Tierra
        utilizando la fórmula de Haversine.
        """
        # Radio de la Tierra en kilómetros
        radio_tierra = 6371.0

        # Convertir grados a radianes
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Diferencia de latitud y longitud
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad

        # Aplicar la fórmula de Haversine
        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia = radio_tierra * c

        return distancia

    @staticmethod
    def _check_login(headers):
        db = "festymas_test"
        if not db:
            return http.Response("Not found Database in request", status=404)
        try:
            db_list = http.db_list(force=True)
        except AccessDenied:
            return http.Response("Access Denied", status=403)
        if db not in db_list:
            return http.Response(
                "Not found {} Database in " "environment".format(db), status=400
            )
        request.session.db = db
        festymas_token = (
            request.env["ir.config_parameter"].sudo().get_param("festymas.token")
        )
        if not festymas_token:
            return http.Response("Not found Festymas Token In Environment", status=500)
        token = headers.get("Authorization")
        if not token:
            return http.Response("Not found Authorization", status=404)
        if token != festymas_token:
            return http.Response("Invalid Authorization", status=401)
