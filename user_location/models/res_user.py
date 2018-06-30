# -*- coding: utf-8 -*-
from openerp import api, fields, models
import requests
from geopy.geocoders import Nominatim
from openerp.http import request


class ResUserLog(models.Model):
    _name = 'res.users.logs'

    location = fields.Char()
    login_date = fields.Datetime(
        compute="_get_login_date", string="Login Date")
    user_id = fields.Many2one('res.users')

    @api.multi
    def _get_login_date(self):
        for rec in self:
            rec.login_date = rec.create_date


class Users(models.Model):

    _inherit = 'res.users'

    logs_ids = fields.One2many('res.users.logs', 'user_id')

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
        if location:
            vals.update({
                'location': location.address,
                'user_id': self.env.user.id
            })
        self.env['res.users.logs'].create(vals)
