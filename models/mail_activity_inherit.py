from odoo import models,fields,api
from odoo.exceptions import UserError

class MailActivityInherit(models.Model):
    _inherit = 'mail.activity'

    department_id = fields.Many2one(
        'hr.department',
        string="Department",
        compute="_compute_department_id",
        store=True
    )
    stored_state = fields.Char(string="Stored State", compute="_compute_stored_state", store=True)

    @api.depends('state')
    def _compute_stored_state(self):
        for activity in self:
            activity.stored_state = activity.state

    @api.depends('user_id')
    def _compute_department_id(self):
        for activity in self:
            employee = self.env['hr.employee'].search([('user_id', '=', activity.user_id.id)], limit=1)
            activity.department_id = employee.department_id if employee else False

    def action_view_activity_record(self):
        """
        Redirect to the related activity's record.
        """
        if not self.res_id or not self.res_model:
            raise UserError("This activity is not linked to a specific record.")
        return {
            'type': 'ir.actions.act_window',
            'name': self.res_name,
            'res_model': self.res_model,
            'view_mode': 'form',
            'res_id': self.res_id,
            'target': 'current',
        }
