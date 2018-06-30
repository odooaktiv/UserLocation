# -*- coding: utf-8 -*-
from odoo import api, fields, models
import requests
from geopy.geocoders import Nominatim
from odoo.http import request


class ResUserLog(models.Model):
    _inherit = 'res.users.log'

    location = fields.Char()
    login_date = fields.Datetime(
        compute="_get_login_date", string="Login Date")

    @api.multi
    def _get_login_date(self):
        for rec in self:
            rec.login_date = rec.create_date


class Users(models.Model):

    _inherit = 'res.users'

    @api.model
    def _update_last_login(self):
        vals = {}
        ip = request.httprequest.environ.get('REMOTE_ADDR')
        url = 'http://freegeoip.net/json/' + ip
        r = requests.get(url)
        js = r.json()
        geolocator = Nominatim(timeout=None)
        a = js['latitude'], js['longitude']
        location = geolocator.reverse(a)
        user = self.search([('id', '=', self.id)])
        if user and location:
            vals.update({
                'location': location.address
            })
        self.env['res.users.log'].create(vals)
