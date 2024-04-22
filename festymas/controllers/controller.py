# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)

import json
import logging

from odoo import http
from odoo.exceptions import AccessDenied, MissingError
from odoo.http import request

_logger = logging.getLogger(__name__)


class FestymasController(http.Controller):
    @http.route(
        ["/festymas/concerts", "/festymas/concerts/<int:id>"],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_concerts(self, id=None, **kw):
        domain = []
        fields = [
            "name",
            "description",
            "location_id",
            "date",
            "festymas_participant_ids",
            "cartel_1920",
        ]
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if id:
            domain = [("id", "=", id)]
        data = self.get_festymas_concerts(fields, domain)

        return data

    @http.route(
        ["/festymas/festivals", "/festymas/festivals/<int:id>"],
        type="json",
        auth="none",
        no_jsonrpc=True,
    )
    def festymas_festivals(self, id=None, **kw):
        domain = []
        fields = [
            "name",
            "description",
            "location_id",
            "start_date",
            "end_date",
            "festymas_concert_ids",
            "cartel_1920",
        ]
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if id:
            domain = [("id", "=", id)]
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_festivals(fields, domain)

        return data

    @http.route(
        ["/festymas/locations", "/festymas/locations/<int:id>"],
        type="json",
        auth="none",
        no_jsonrpc=True,
    )
    def festymas_locations(self, id=None, **kw):
        domain = []
        fields = [
            "name",
            "description",
            "festymas_concert_ids",
            "festymas_festival_ids",
        ]
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if id:
            domain = [("id", "=", id)]
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_locations(fields, domain)

        return data

    @http.route(
        ["/festymas/participants", "/festymas/participants/<int:id>"],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_participants(self, id=None, **kw):
        domain = []
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
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if id:
            domain = [("id", "=", id)]
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_participants(fields, domain)

        return data

    @http.route(
        [
            "/festymas/artists",
            "/festymas/artists/<int:id>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_artist(self, id=None, **kw):
        domain = []
        fields = ["name", "description", "festymas_participant_ids"]
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if id:
            domain = [("id", "=", id)]
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_artists(fields, domain)

        return data

    @http.route(
        [
            "/festymas/genres",
            "/festymas/genres/<int:id>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_genres(self, id=None, **kw):
        domain = []
        fields = ["name", "description", "festymas_participant_ids"]
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if id:
            domain = [("id", "=", id)]
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_genres(fields, domain)

        return data

    @staticmethod
    def _check_login(headers):
        db = "festymas"
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
        endpoint = headers.environ.get("PATH_INFO")
        method = headers.environ.get("REQUEST_METHOD")
        if endpoint == "/festymas/concerts/" and method != "GET":
            return http.Response("Only GET method is allowed", status=500)

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

    @staticmethod
    def get_festymas_concerts(fields, domain):
        festymas_concerts_env = request.env["festymas.concert"]
        search_fields = fields
        _logger.info("Checking festymas concerts...")
        festymas_concerts = festymas_concerts_env.sudo().search_read(
            domain=domain, fields=search_fields
        )
        return festymas_concerts

    @staticmethod
    def get_festymas_festivals(fields, domain):
        festymas_festival_env = request.env["festymas.festival"]
        search_fields = fields
        _logger.info("Checking festymas festivals...")
        festymas_festivals = festymas_festival_env.sudo().search_read(
            domain=domain, fields=search_fields
        )
        return festymas_festivals

    @staticmethod
    def get_festymas_locations(fields, domain):
        festymas_location_env = request.env["festymas.location"]
        search_fields = fields
        _logger.info("Checking festymas locations...")
        festymas_locations = festymas_location_env.sudo().search_read(
            domain=domain, fields=search_fields
        )
        return festymas_locations

    @staticmethod
    def get_festymas_participants(fields, domain):
        festymas_participant_env = request.env["festymas.participant"]
        search_fields = fields
        _logger.info("Checking festymas participants...")
        festymas_participants = festymas_participant_env.sudo().search_read(
            domain=domain, fields=search_fields
        )
        return festymas_participants

    @staticmethod
    def get_festymas_artists(fields, domain):
        festymas_artist_env = request.env["festymas.artist"]
        search_fields = fields
        _logger.info("Checking festymas artists...")
        festymas_artists = festymas_artist_env.sudo().search_read(
            domain=domain, fields=search_fields
        )
        return festymas_artists

    @staticmethod
    def get_festymas_genres(fields, domain):
        festymas_genre_env = request.env["festymas.genre"]
        search_fields = fields
        _logger.info("Checking festymas artists...")
        festymas_genres = festymas_genre_env.sudo().search_read(
            domain=domain, fields=search_fields
        )
        return festymas_genres
