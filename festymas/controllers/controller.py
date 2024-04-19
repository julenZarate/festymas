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
        "/festymas/concerts", type="json", auth="none", no_jsonrpc=True
    )
    def festymas_concerts(self):
        fields = []
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_concerts(fields)

        return data

    @http.route(
        "/festymas/festivals", type="json", auth="none", no_jsonrpc=True
    )
    def festymas_festivals(self):
        fields = []
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_festivals(fields)

        return data

    @http.route(
        "/festymas/locations", type="json", auth="none", no_jsonrpc=True
    )
    def festymas_locations(self):
        fields = []
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_locations(fields)

        return data

    @http.route(
        "/festymas/participants", type="json", auth="none", no_jsonrpc=True
    )
    def festymas_participants(self):
        fields = []
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_participants(fields)

        return data

    @http.route(
        "/festymas/artist", type="json", auth="none", no_jsonrpc=True
    )
    def festymas_artist(self):
        fields = []
        login_error = self._check_login(request.httprequest.headers)
        if login_error:
            return login_error
        if request.httprequest.data != b"{}":
            fields = json.loads(request.httprequest.data)["fields"]
        data = self.get_festymas_artists(fields)

        return data

    @staticmethod
    def _check_login(headers):
        # Check Database in headers
        db = headers.get("db")
        if not db:
            return http.Response("Not found Database in request", status=404)

        # Check Database in environment
        try:
            db_list = http.db_list(force=True)
        except AccessDenied:
            return http.Response("Access Denied", status=403)
        if db not in db_list:
            return http.Response(
                "Not found {} Database in " "environment".format(db), status=400
            )

        request.session.db = db

        # Check Request Method
        endpoint = headers.environ.get("PATH_INFO")
        method = headers.environ.get("REQUEST_METHOD")
        if endpoint == "/festymas/concerts/" and method != "GET":
            return http.Response("Only GET method is allowed", status=500)

        festymas_token = (
            request.env["ir.config_parameter"].sudo().get_param("festymas.token")
        )

        # Check Created festymas_token
        if not festymas_token:
            return http.Response("Not found Festymas Token In Environment", status=500)

        # Check Authorization
        token = headers.get("Authorization")
        if not token:
            return http.Response("Not found Authorization", status=404)

        # Check valid Token
        if token != festymas_token:
            return http.Response("Invalid Authorization", status=401)

    @staticmethod
    def get_festymas_concerts(fields=[]):
        festymas_concerts_env = request.env["festymas.concert"]
        search_fields = fields
        _logger.info("Checking festymas concerts...")
        festymas_concerts = festymas_concerts_env.sudo().search_read(
            fields=search_fields
        )
        count = len(festymas_concerts)
        return festymas_concerts

    @staticmethod
    def get_festymas_festivals(fields=[]):
        festymas_festival_env = request.env["festymas.festival"]
        search_fields = fields
        _logger.info("Checking festymas festivals...")
        festymas_festivals = festymas_festival_env.sudo().search_read(
            fields=search_fields
        )
        return festymas_festivals

    @staticmethod
    def get_festymas_locations(fields=[]):
        festymas_location_env = request.env["festymas.location"]
        search_fields = fields
        _logger.info("Checking festymas locations...")
        festymas_locations = festymas_location_env.sudo().search_read(
            fields=search_fields
        )
        return festymas_locations

    @staticmethod
    def get_festymas_participants(fields=[]):
        festymas_participant_env = request.env["festymas.participant"]
        search_fields = fields
        _logger.info("Checking festymas participants...")
        festymas_participants = festymas_participant_env.sudo().search_read(
            fields=search_fields
        )
        return festymas_participants

    @staticmethod
    def get_festymas_artists(fields=[]):
        festymas_artist_env = request.env["festymas.artist"]
        search_fields = fields
        _logger.info("Checking festymas artists...")
        festymas_artists = festymas_artist_env.sudo().search_read(
            fields=search_fields
        )
        return festymas_artists
