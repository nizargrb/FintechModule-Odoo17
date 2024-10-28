# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
from tokenize import String
#from openerp.exceptions import AccessError
##############################################################################
#
#    NEW API
#
##############################################################################
from odoo import models, fields, api, _


class Employee(models.Model):
	_name = 'guerrabi.employee'
	name = fields.Many2one('res.partner', 'Client')
	cin  = fields.Char(string='CIN', required=True)
	state = fields.Selection([('dossier','Dossier'), ('crm','CRM'),('agence','Agence'), ('directeur','Directeur'), ('financier','Financement')], default='dossier')
	duree = fields.Integer(string='durée du crédit: mois', default=12)
	date_demande = fields.Date(string='date de la demande', default=fields.Date.today())
	revenu = fields.Float(string='revenu mensuel')
	credit = fields.Float(string='credit')
	taux_interet = fields.Float(string='taux intérêt annuel', default=0.1)
	taux_tva = fields.Float(string='taux tva annuel', default=0.1)
	taux_interetmttc = fields.Float(string='Taux intérêt mensuel TTC', compute='_compute_taux_interetmttc', store=True)
	mensualite=fields.Float(string='mensualité',compute='_compute_mensualite', store=True)
	nationality = fields.Many2one(string='Nationalité', comodel_name='guerrabi.nationality')
	specializations = fields.Many2one(string='Métier', comodel_name='guerrabi.specialization')
	#plafond = fields.Float(string='Plafond', compute='_compute_plafond', store=True)
	decision = fields.Integer(string='Décision', compute='_compute_decision', store=True)

	@api.depends('taux_interet', 'taux_tva')
	def _compute_taux_interetmttc(self):
		for rec in self:
			rec.taux_interetmttc = (((1 + rec.taux_interet) ** (1 / 12)) - 1) * (1 + rec.taux_tva)

	@api.depends('credit', 'taux_interetmttc', 'duree')
	def _compute_mensualite(self):
		for rec in self:
			rec.mensualite = (rec.credit * rec.taux_interetmttc) / (1 - ((1 + rec.taux_interetmttc) ** (-rec.duree)))

	@api.depends('revenu', 'mensualite')
	def _compute_decision(self):
		for rec in self:
			if rec.mensualite > rec.revenu * 0.4:
				rec.decision = 0
			else:
				rec.decision = 1
    




	def financier_button(self):
		self.write({'state': 'financier'})

	def directeur_button(self):
		self.write({'state': 'directeur'})

	def crm_button(self):
		self.write({'state': 'crm'})

	def agence_button(self):
		self.write({'state': 'agence'})	
		
	def dossier_button(self):
		self.write({'state': 'dossier'})
		
class Nationality(models.Model):
    _name = 'guerrabi.nationality'

    name = fields.Char(string='Title', required=True,
        help="This is your Nationality not the where you are living!")

class Specialization(models.Model):
    _name = 'guerrabi.specialization'

    name = fields.Char(string='Nom de la spécialisation', required=True)
	
