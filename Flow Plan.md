
# Flow Plan

What am I trying to make? 

> A bot that can manage advertising accounts on a discord server.
## Break down

| Word/Phrase          | Meaning                                                |
| -------------------- | ------------------------------------------------------ |
| Bot                  | A discord bot                                          |
| Advertising Accounts | There will need to be some storage of accounts.        |
| Manage               | This bot will be used to interface with this database. |

Bot:
- All normal discord bot functions
	- Announcements
	- Moderation
	- Logging
	- Tickets
- It will need extra functionality
	- The ad account management
Advertising Accounts:
- It will need to store accounts
	- Those accounts user-ids
	- Moderation Status
	- Level
	- Due Payments
	- Codes
Manage:
- The bot will need to do all of this

> There are two major aspects, the database and the interface. 

# The Database

## Payments

| Data                | Data Type             | Inputs                                    |
| ------------------- | --------------------- | ----------------------------------------- |
| Payment Id          | Int (**Primary-Key**) | **Automatic**                             |
| User Id             | Int                   | Grabbed from when a user creates a ticket |
| Amount              | Int                   | Grabbed when payment attempt is made      |
| Product Description | String                | From when the user creates a ticket       |
| Date                | Date                  | Grabbed once payment is verified          |
| Code                | Int                   | From when the user creates a ticket       |
| Ticket ID           | Int                   | From when the user creates a ticket       |
| Valid               | Bool                  | From verification, Default = False                                          |
## Advertising Accounts

| Data           | Data Type             | Inputs                                                                                        |
| -------------- | --------------------- | --------------------------------------------------------------------------------------------- |
| Emails         | String                | On Sign-Up                                                                                    |
| User Id        | Int (**Primary-Key**) | **On Sign-Up**                                                                                |
| Level          | Int                   | default = 1, Max = 15, When user gets a new client, their level goes up until max is reached. |
| Clients Gotten | Int                   | default = 0, when user gets a new client                                                      |
| Code           | Int                   | On Sign-Up (randomly generated and Unique)                                                    |

# User Interface

## Levels

| Level Name | Description                                                 | level Number |
| ---------- | ----------------------------------------------------------- | ------------ |
| Max        | has continuous access to all of the application             | 5             |
| Admin      | has access to all of the application with logs              | 4             |
| Moderation | has access to most of the application with logs             | 3             |
| Advertiser | has access to create and delete their data in Advertiser DB | 2             |
| Client     | does not have access to the database                        | 1             |
| Unsigned   | No access to the entire application                         | 0             |

## User Access

| User       | Level |
| ---------- | ----- |
| Advertiser | 2     |
| User       | 1     |
| Moderator  | 3     |
| Admin      | 4     |
| Owner      | 5     |

# User Interactions

## Advertiser Sign-up

### Checks:

- User Id does not already exist in Advertiser Database

> /ad_profile

This will DM the user an Embed explaining the Email Address and have a view.

Embed.View.Componets = (Powder Blue, "Add PayPal Email")
> Opens a view where View.Email can be set.

Checks if it is email format

[[#Advertising Accounts]] entry;

| Data           | Entry                                   |
| -------------- | --------------------------------------- |
| Email          | **View.Email.Value**                       |
| User_Id        | **interaction.user.id**                 |
| Level          | 1                                       |
| Clients_Gotten | 0                                       |
| Code           | Unique Code - randomint(100000, 999999) |

## Advertiser Delete

### Checks

- User Id exists in Database

> /ad_profile_delete

DM's the user with a embed explaining the permanence of deletion, asks them to click button

### Button Interaction

Search data base for user's id and deletes that instance. 

## Change Advertiser PayPal Email

### Checks

- User Id exists in Database

> /ad_edit [email_address : str]

Grabs the user id and searches the database. It edits the instance, replacing the email.
## Get Code

### Check

- user id exists in db

> /get_code

Returns the code for the user.

## Get Levels

### Check

- user id exists in db

> /level

Displays the current level of the user.
## Client Queues for Consult

### Checks

- None

> Button Press

Modal created with two options, Product Description, and Code.

Check if code exists, if code does exist, continue, if not, Send User DM and ask them to hit a button (sends another modal) for a valid code over and over until valid code is reached. 

| Data                | Data Type             | Inputs              |
| ------------------- | --------------------- | ------------------- |
| Payment Id          | Int (**Primary-Key**) | **Generated**       |
| User Id             | Int                   | Interaction.User.Id |
| Product Description | String                | Modal.Desc.Value    |
| Date                | Date                  | Interaction.Date_at |
| Code                | Int                   | Modal.Code.Value    |
| Ticket_Id           | Int                   | Channel.Id                    |

## Payment Attempt

### Checks

- Valid Code

> /pay

Sends User embed with information on how to pay. Links to PayPal, Ko-Fi with a button. 
Sends Owner an Embed, grabbing the user they need to pay and what percentage (based on Level). Updates Database with Client Gotten for Advertiser and Payment amount and date for Payment Database.

## Owner sent Receipt

Check paypal for user id and amount, once seen, manually verify;

> /verify [payment_id : int]

Grab payment id from database, send message in channel to let dev know the payment is verified. 

# Tickets

## Ticket create

> Button 

Get ticket Category
Create ticket Channel with username of user and two generated ints
==Ticket-[Username]-[random two digits]==
Set Perms
Send User Modal Information

## Ticket Close

Check if this is a ticket (startswith: ticket)
Change perms
Change ticket to:
==Ticket-[Username]-[Random two digits]-[Closed]==

To do:

Payments