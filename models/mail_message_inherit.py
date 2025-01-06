from odoo import fields,models

class MailMessageInherit(models.Model):
    _inherit = 'mail.message'

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