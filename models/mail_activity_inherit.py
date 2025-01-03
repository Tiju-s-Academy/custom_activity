from odoo import models,fields
from odoo.exceptions import UserError

class MailActivityInherit(models.Model):
    _inherit = 'mail.activity'

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
