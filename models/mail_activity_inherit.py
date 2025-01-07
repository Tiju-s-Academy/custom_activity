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

    app_name = fields.Char('App Name', compute='_compute_app_name', store=True)
    model_name = fields.Char('Model Name', compute='_compute_model_name', store=True)

    @api.depends('res_model')
    def _compute_model_name(self):
        for record in self:
            if record.res_model:
                # Get the model name from res_model field
                model = self.env['ir.model'].search([('model', '=', record.res_model)], limit=1)
                if model:
                    record.model_name = model.name
                else:
                    record.model_name = 'Unknown'

    @api.depends('model_name')
    def _compute_app_name(self):
        for record in self:
            if record.model_name:
                # Get the model object to find associated modules
                model = self.env['ir.model'].search([('model', '=', record.res_model)], limit=1)

                if model:
                    # Find the module(s) associated with this model
                    modules = model.modules
                    if modules:
                        # Prioritize the custom module (if any)
                        custom_modules = [mod for mod in modules if 'custom' in mod]
                        if custom_modules:
                            module_name = custom_modules[0]
                        else:
                            # Default to the first module if no custom ones
                            module_name = modules[0]

                        # Now, retrieve the app name from the manifest
                        try:
                            module = self.env['ir.module.module'].search([('name', '=', module_name)], limit=1)
                            if module:
                                module_path = module.path
                                manifest_file = os.path.join(module_path, '__manifest__.py')
                                with open(manifest_file, 'r', encoding='utf-8') as f:
                                    manifest_data = f.read()
                                    manifest = eval(manifest_data)  # Convert the string into a dictionary
                                    record.app_name = manifest.get('name', 'Unknown')
                        except Exception as e:
                            record.app_name = 'Unknown'
            else:
                record.app_name = 'Unknown'

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
