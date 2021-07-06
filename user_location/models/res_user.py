# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

from odoo import api, fields, models
import requests


class ResUserLog(models.Model):
    _inherit = 'res.users.log'

    location = fields.Char()
    login_date = fields.Datetime(
        compute="_get_login_date", string="Login Date")

    def _get_login_date(self):
        """ Get login Date """
        for rec in self:
            rec.login_date = rec.create_date


class Users(models.Model):

    _inherit = 'res.users'

    @api.model
    def _update_last_login(self):
        """ TO update login deatils """
        vals = {}
        url = 'http://ipinfo.io/json'
        r = requests.get(url)
        js = r.json()
        city = js['city']
        region = js['region']
        country_code = js['country']
        country_id = self.env['res.country'].search([
            ('code', '=', country_code)], limit=1)
        for country in country_id:
            address = city + ', ' + region + ', ' + country.name
        vals.update({
            'location': address,
        })
        user_log_id = self.env['res.users.log'].create(vals)
        user = self.env.user
        user.write({'log_ids': [(6, 0, [user_log_id.id])]})
