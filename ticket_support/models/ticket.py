from odoo import fields, models, api  # type: ignore
from datetime import datetime, timedelta

class Ticket(models.Model):
    _name = 'support.ticket'
    _description = 'Support Ticket'
    _rec_name = 'ticket_code'

    is_customer = fields.Boolean(string="Is Customer", default = True)
    # partner issue the ticket
        #both user and partner can issue the ticket (and both can be shown as res.partner)
    partner_issue_ticket = fields.Many2one('res.partner', string="Partner")

    ################################
    #                              #
    #      Basic information       #                
    #                              #
    ################################
    ticket_code = fields.Char(string="Ticket Code",
                              readonly=True,
                              compute="_compute_ticket_code",
                              store = True,
                              help="Ticket Code"

                              )
    name = fields.Char(string="Ticker Title",
                       required=True,
                       help="Ticket Title"
                       )
    custom_create_date = fields.Datetime(string="Create Day", default=fields.Datetime.now)

    stage = fields.Many2one('support.ticket.stage',
                            string="Ticket Stage",
                            readonly=True,
                            group_expand="_read_group_stage"  # for getting all the stage
                            )
    # left side is the value, right side is the string that is shown
    # we can utilizing the left size to store the color code
    status = fields.Selection([
        ("10", "New"),
        ("3", "In Week"),
        ("1", "In Month"),
        ],
        default="10",
        string="Status")

    content = fields.Html(string="Ticket description", help="Description")

    ticket_additional = fields.One2many('support.ticket', 'parent_ticket_id', string="Ticket Response")

    note = fields.Html(string="Note")

    # inhouse user to handle the ticket
    user_handling = fields.Many2many('res.users', string="User")
    user_handling_image = fields.Binary(related='user.image_1920', string='User Image')

    ####################
    #                  #
    #     customer     #
    #                  #
    ####################
    email = fields.Char(string="Email", related="partner_issue_ticket.email")
    phone = fields.Char(string="Phone", related="partner_issue_ticket.phone")
    website = fields.Char(string="Website", related="partner_issue_ticket.website")


    # Added Many2one field to establish the inverse relation
    parent_ticket_id = fields.Many2one('support.ticket', string="Parent Ticket")

    ticket_type = fields.Many2one('support.ticket.type', string="Ticket Type")

    
    @api.model
    def _read_group_stage(self, group, domain, order):
        return self.env['support.ticket.status'].search([])
    
    color = fields.Integer(string="Color", compute="compute_color")

    @api.model
    def update_status(self):
        datetime_now = datetime.now()
        for ticket in self:
            if ticket.custom_create_date:
                create_date = datetime.strptime(ticket.custom_create_date, '%Y-%m-%d %H:%M:%S')
                if (datetime_now - create_date).days < 7:
                    ticket.status = "10"
                elif(datetime_now - create_date).days < 30:
                    ticket.status = "3"
                else:
                    ticket.status = "1"
                ticket.compute_color()

    @api.depends("status")
    def compute_color(self):
        if self.status:
            self.color = int(self.status)

    @api.depends("id")
    def _compute_ticket_code(self):
        for ticket in self:
            ticket.ticket_code = "TK" + str(ticket.id).zfill(10)
    
