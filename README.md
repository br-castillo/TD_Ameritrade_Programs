# TD_Ameritrade_Programs
Python Programs involving TD Ameritrade

This is a program developed using TD Ameritrade's python API. The main purpose of the program is to constantly read the orders for options trades, 
pulling a request every second and notifying for any new options orders coming in via a discord channel. Any old orders will be added to a dictionary for the 
duration fo the program being run and will not be sent out more than once. 
