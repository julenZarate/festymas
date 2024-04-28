# © 2024 Festymas S.L - Julen Zarate <julen.zarate@festymas.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html)

import json
import logging

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
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_concerts(self, id=None, page=None, **kw):
        domain = []
        if request.dispatcher:
            body = request.dispatcher.jsonrequest
            if body.get("adjustment"):
                domain = self._generate_adjustment_domain(body.get("adjustment"))
        model = "festymas.concert"
        offset = False
        limit = False
        sort = False
        if request.httprequest.args.get("sort_by"):
            sort = (
                request.httprequest.args.get("sort_by")
                + " "
                + request.httprequest.args.get("sort_in")
            )
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
        if id:
            ids = id.split(",")
            domain.append(("id", "in", ids))
        if page:
            offset = ((page - 1) * self._items_per_page,)
            limit = self._items_per_page
        data = self.get_festymas_concerts(fields, domain, limit, offset, sort)
        count = self._get_model_count(model)
        return data, count

    @http.route(
        [
            "/festymas/festivals",
            "/festymas/festivals/<string:id>",
            "/festymas/festivals/page/<int:page>",
            "/festymas/festivals/home",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_festivals(self, id=None, page=None, **kw):
        model = "festymas.festival"
        offset = False
        limit = False
        sort = False
        if request.httprequest.args.get("sort_by"):
            sort = (
                request.httprequest.args.get("sort_by")
                + " "
                + request.httprequest.args.get("sort_in")
            )
        domain = []
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
        if id:
            ids = id.split(",")
            domain = [("id", "in", ids)]
        if page:
            offset = ((page - 1) * self._items_per_page,)
            limit = self._items_per_page
        data = self.get_festymas_festivals(fields, domain, limit, offset, sort)
        count = self._get_model_count(model)
        return data, count

    @http.route(
        [
            "/festymas/locations",
            "/festymas/locations/<string:id>",
            "/festymas/locations/page/<int:page>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_locations(self, id=None, page=None, **kw):
        offset = False
        limit = False
        sort = False
        if request.httprequest.args.get("sort_by"):
            sort = (
                request.httprequest.args.get("sort_by")
                + " "
                + request.httprequest.args.get("sort_in")
            )
        domain = []
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
        if id:
            ids = id.split(",")
            domain = [("id", "in", ids)]
        if page:
            offset = ((page - 1) * self._items_per_page,)
            limit = self._items_per_page
        data = self.get_festymas_locations(fields, domain, limit, offset, sort)
        count = self._get_model_count("festymas.location")
        return data, count

    @http.route(
        [
            "/festymas/participants",
            "/festymas/participants/<string:id>",
            "/festymas/participants/page/<int:page>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_participants(self, id=None, page=None, **kw):
        offset = False
        limit = False
        sort = False
        if request.httprequest.args.get("sort_by"):
            sort = (
                request.httprequest.args.get("sort_by")
                + " "
                + request.httprequest.args.get("sort_in")
            )
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
        login_error = False
        if login_error:
            return login_error
        if id:
            ids = id.split(",")
            domain = [("id", "in", ids)]
        if page:
            offset = ((page - 1) * self._items_per_page,)
            limit = self._items_per_page
        data = self.get_festymas_participants(fields, domain, limit, offset, sort)
        count = self._get_model_count("festymas.participant")
        return data, count

    @http.route(
        [
            "/festymas/artists",
            "/festymas/artists/<string:id>",
            "/festymas/artists/page/<int:page>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_artist(self, id=None, page=None, **kw):
        offset = False
        limit = False
        sort = False
        if request.httprequest.args.get("sort_by"):
            sort = (
                request.httprequest.args.get("sort_by")
                + " "
                + request.httprequest.args.get("sort_in")
            )
        domain = []
        fields = ["name", "description", "festymas_participant_ids"]
        login_error = False
        if login_error:
            return login_error
        if id:
            ids = id.split(",")
            domain = [("id", "in", ids)]
        if page:
            offset = ((page - 1) * self._items_per_page,)
            limit = self._items_per_page
        data = self.get_festymas_artists(fields, domain, limit, offset, sort)
        count = self._get_model_count("festymas.artist")
        return data, count

    @http.route(
        [
            "/festymas/genres",
            "/festymas/genres/<string:id>",
            "/festymas/genres/page/<int:page>",
        ],
        type="json",
        cors="*",
        csrf=False,
        methods=["POST", "GET", "OPTIONS"],
        auth="public",
        no_jsonrpc=True,
    )
    def festymas_genres(self, id=None, page=None, **kw):
        offset = False
        limit = False
        sort = False
        if request.httprequest.args.get("sort_by"):
            sort = (
                request.httprequest.args.get("sort_by")
                + " "
                + request.httprequest.args.get("sort_in")
            )
        domain = []
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
        if id:
            ids = id.split(",")
            domain = [("id", "in", ids)]
        if page:
            offset = ((page - 1) * self._items_per_page,)
            limit = self._items_per_page
        data = self.get_festymas_genres(fields, domain, limit, offset, sort)
        count = self._get_model_count("festymas.genre")
        return data, count

    def _get_festymas_home(self, fields, model):
        data = (
            request.env[model]
            .sudo()
            .search_read(
                [], fields=fields, order="visit_count desc", limit=self._items_per_home
            )
        )
        return data

    def _get_model_count(self, model):
        count = request.env[model].sudo().search_count([])
        return count

    def _generate_adjustment_domain(self, adjustments):
        domain = []
        for adjustment in adjustments:
            domain.append((adjustment, "in", adjustments[adjustment]))
        return domain

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

    @staticmethod
    def get_festymas_concerts(fields, domain, limit, offset, sort):
        festymas_concerts_env = request.env["festymas.concert"]
        search_fields = fields
        _logger.info("Checking festymas concerts...")
        festymas_concerts = festymas_concerts_env.sudo().search_read(
            domain=domain,
            fields=search_fields,
            limit=limit,
            offset=offset,
            order=sort,
        )
        return festymas_concerts

    @staticmethod
    def get_festymas_festivals(fields, domain, limit, offset, sort):
        festymas_festival_env = request.env["festymas.festival"]
        search_fields = fields
        _logger.info("Checking festymas festivals...")
        festymas_festivals = festymas_festival_env.sudo().search_read(
            domain=domain,
            fields=search_fields,
            limit=limit,
            offset=offset,
            order=sort,
        )
        return festymas_festivals

    @staticmethod
    def get_festymas_locations(fields, domain, limit, offset, sort):
        festymas_location_env = request.env["festymas.location"]
        search_fields = fields
        _logger.info("Checking festymas locations...")
        festymas_locations = festymas_location_env.sudo().search_read(
            domain=domain,
            fields=search_fields,
            limit=limit,
            offset=offset,
            order=sort,
        )
        return festymas_locations

    @staticmethod
    def get_festymas_participants(fields, domain, limit, offset, sort):
        festymas_participant_env = request.env["festymas.participant"]
        search_fields = fields
        _logger.info("Checking festymas participants...")
        festymas_participants = festymas_participant_env.sudo().search_read(
            domain=domain,
            fields=search_fields,
            limit=limit,
            offset=offset,
            order=sort,
        )
        return festymas_participants

    @staticmethod
    def get_festymas_artists(fields, domain, limit, offset, sort):
        festymas_artist_env = request.env["festymas.artist"]
        search_fields = fields
        _logger.info("Checking festymas artists...")
        festymas_artists = festymas_artist_env.sudo().search_read(
            domain=domain,
            fields=search_fields,
            limit=limit,
            offset=offset,
            order=sort,
        )
        return festymas_artists

    @staticmethod
    def get_festymas_genres(fields, domain, limit, offset, sort):
        festymas_genre_env = request.env["festymas.genre"]
        search_fields = fields
        _logger.info("Checking festymas genres...")
        festymas_genres = festymas_genre_env.sudo().search_read(
            domain=domain,
            fields=search_fields,
            limit=limit,
            offset=offset,
            order=sort,
        )
        return festymas_genres
