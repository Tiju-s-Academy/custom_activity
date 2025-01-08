from odoo import fields,models,api

class MailMessageInherit(models.Model):
    _inherit = 'mail.message'

    department_id = fields.Many2one(
        'hr.department',
        string="Department",
        compute="_compute_department_id",
        store=True
    )

    @api.depends('author_id')
    def _compute_department_id(self):
        for activity in self:
            employee = self.env['hr.employee'].search([('user_id', '=', activity.author_id.id)], limit=1)
            activity.department_id = employee.department_id if employee else False

    manifest_name = fields.Char(string='App Name', compute='_compute_manifest_name')

    def _compute_manifest_name(self):
        for message in self:
            if message.model:
                # Fetch the model details
                ir_model = self.env['ir.model'].search([('model', '=', message.model)], limit=1)
                if ir_model and ir_model.modules:
                    # Fetch the module details
                    ir_module = self.env['ir.module.module'].search([('name', '=', ir_model.modules)], limit=1)
                    if ir_module:
                        message.manifest_name = ir_module.shortdesc  # Short description from the manifest
                        continue
            message.manifest_name = 'Unknown'

    def action_view_activity_message_record(self):
        self.ensure_one()
        return {
            'name': 'Activity Message Record',
            'type': 'ir.actions.act_window',
            'res_model': 'mail.activity.message',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.activity_message_id.id,
        }