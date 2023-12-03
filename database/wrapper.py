import peewee as pw

db = pw.SqliteDatabase("database/zenith.db")
db.connect()

class BaseModel(pw.Model):
    class Meta:
        database = db

class Ticket(BaseModel):
    '''
    ## Zenith Collective
    
    ticket_id (::Primary Key::) = Auto-incrementing ID of the ticket

    guild_id = ID of the guild where the ticket was created

    channel_id = ID of the channel created

    type = 
    - 0 for support ticket, 
    - 1 for moderation ticket, 
    - 2 for custom bot ticket, 
    - 3 for custom server ticket,
    - 4 for other tickets

    status = 
    - 0 for open
    - 1 for closed
    - 2 for frozen, no activity allowed
    '''
    ticket_id = pw.AutoField(primary_key=True)
    guild_id = pw.IntegerField()
    channel_id = pw.IntegerField()
    type = pw.IntegerField()
    status = pw.IntegerField()

    class Meta:
        table_name = "tickets"

db.create_tables([Ticket])