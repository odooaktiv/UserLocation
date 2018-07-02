# -*- coding: utf-8 -*-
from odoo import api, fields, models
import requests


class ResUserLog(models.Model):
    _inherit = 'res.users.log'

    location = fields.Char()
    login_date = fields.Datetime(compute="_get_login_date",
                                 string="Login Date")

    @api.multi
    def _get_login_date(self):
        for rec in self:
            rec.login_date = rec.create_date


class Users(models.Model):

    _inherit = 'res.users'

    @api.model
    def _update_last_login(self):
        vals = {}
        url = 'http://ip-api.com/json/'
        r = requests.get(url)
        js = r.json()
        city = js['city']
        regionname = js['regionName']
        country = js['country']
        address = city + ', ' + regionname + ', ' + country
        vals.update({
            'location': address,
            'user_id': self.env.user.id})
        user_log_id = self.env['res.users.log'].create(vals)
        user = self.env.user
        user.write({'log_ids': [(6, 0, [user_log_id.id])]})
