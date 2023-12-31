import peewee as pw
from dotenv import load_dotenv
from os import getenv

load_dotenv('keys.env')

db = pw.SqliteDatabase("database/zenith.db")
db.connect()

class BaseModel(pw.Model):
    class Meta:
        database = db

class Ticket(BaseModel):
    '''
    ## Zenith Collective
    
    `ticket_id (::Primary Key::) = Auto-incrementing ID of the ticket

    `guild_id = ID of the guild where the ticket was created

    `channel_id` = ID of the channel created

    `type` = 
    - 0 for support ticket, 
    - 1 for moderation ticket, 
    - 2 for custom bot ticket, 
    - 3 for custom server ticket,
    - 4 for other tickets

    `status` = 
    - 0 for open
    - 1 for closed
    - 2 for frozen, no activity allowed
    '''
    ticket_id = pw.AutoField(primary_key=True)
    guild_id = pw.IntegerField()
    channel_id = pw.IntegerField()
    channel_type = pw.IntegerField()
    status = pw.IntegerField()

    class Meta:
        table_name = "tickets"

class Payments(BaseModel):
    '''
    
    ## Zenith Collective

    ### Payments

    `payment_id` (::Primary Key::) = Auto-incrementing ID of the payment

    `user_id` = ID of the user who made the payment

    `amount` = Amount of money paid

    `product_description` = Description of the product paid for

    `date` = Date of the payment

    `code` = Code of the payment

    `ticket_id` = ID of the ticket the payment is for

    `valid` = Whether the payment is valid or not
    
    '''
    payment_id = pw.AutoField(primary_key=True)
    user_id = pw.IntegerField()
    amount = pw.IntegerField()
    product_description = pw.TextField()
    date = pw.DateTimeField()
    code = pw.IntegerField()
    ticket_id = pw.IntegerField()
    valid = pw.BooleanField(default=False)

class Advertisers(BaseModel):
    '''
    ## Zenith Collective

    ### Advertisers

    `emails` = Emails of the advertisers

    `user_id` (::Primary Key::) = ID of the advertiser

    `level` = Level of the advertiser

    `client_count` = Number of clients the advertiser has

    `code` = Code of the advertiser
    '''
    code = pw.AutoField(primary_key=True)
    email = pw.TextField()
    user_id = pw.IntegerField()
    level = pw.IntegerField(default=1)
    client_count = pw.IntegerField(default=0)

    def get_rowid(self):
        rowid_query = 'SELECT ROWID FROM Advertisers WHERE user_id = ?'
        cursor = self._meta.database.execute_sql(rowid_query, (self.user_id,))
        return cursor.fetchone()[0]

class CustomBot(BaseModel):
    '''
     
    ## Zenith

    ### Custom Bots

    bot_id (::primary key::) = ID of the Bot

    ticket_id = ID of the ticket this is founded in

    code = the code of the advertiser that this client is from

    user_id = Id of the person wanting the bot

    cost = default 0 

    bot_name = default "nameless bot"

    bot_logo = https://cdn4.iconfinder.com/data/icons/scripting-and-programming-languages/512/Python_logo-512.png

    bot_description = description of the bot
     
     '''

    bot_id = pw.AutoField(primary_key = True)
    ticket_id = pw.IntegerField()
    code = pw.IntegerField()
    user_id = pw.IntegerField()
    cost = pw.IntegerField(default=0)
    bot_name = pw.TextField(default = "nameless bot")
    bot_logo = pw.TextField(default= "https://cdn4.iconfinder.com/data/icons/scripting-and-programming-languages/512/Python_logo-512.png")
    bot_description = pw.TextField()

db.create_tables([Ticket, Payments, Advertisers, Payments, CustomBot])

def reset_tables(Pass):
        db.drop_tables([Ticket, Payments, Advertisers])
        db.create_tables([Ticket, Payments, Advertisers])
