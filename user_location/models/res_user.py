# -*- coding: utf-8 -*-
from odoo import api, fields, models
import requests
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
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        vals = {}
        url = 'http://ipinfo.io?' + ip_address + '=$' + ip_address
        r = requests.get(url)
        js = r.json()
        address = False
        country_id = False

        city = js['city']
        region = js['region']
        country_code = js['country']
        if country_code:
            country_id = self.env['res.country'].search(
                [('code', '=', country_code)], limit=1)
        if country_code:
            for country in country_id:
                address = city + ', ' + region + ', ' + country.name
        vals.update({
            'location': address,
            'user_id': self.env.user.id})
        user_log_id = self.env['res.users.log'].create(vals)
        user = self.env.user
        user.write({'log_ids': [(6, 0, [user_log_id.id])]})
