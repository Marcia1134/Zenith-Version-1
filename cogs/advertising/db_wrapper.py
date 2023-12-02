import peewee as pw
import datetime

db = pw.SqliteDatabase('advertising.db')
db.connect()

class BaseModel(pw.Model):
    class Meta:
        database = db

class Payments(BaseModel):
    payment_id = pw.AutoField(primary_key=True)
    user_id = pw.IntegerField()
    amount = pw.IntegerField(null= True)
    product_description = pw.TextField(null= True)
    date = pw.DateTimeField(null= True)
    code = pw.IntegerField(null= True)
    ticket_id = pw.IntegerField()
    valid = pw.BooleanField(default=False)

class Advertisers(BaseModel):
    emails = pw.TextField(null=True)
    user_id = pw.IntegerField(primary_key=True, unique=True)
    level = pw.IntegerField(default=1)
    client_count = pw.IntegerField(default=0)
    code = pw.IntegerField(null=True)

db.create_tables([Payments, Advertisers])