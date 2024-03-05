from app import mysql, PORT # import variables from app.py
from blockchain import Block, Blockchain # import blockchain classes

class InvalidTransactionException(Exception): # custom exception
    pass


class InsufficientFundsException(Exception): # custom exception
    pass


class Table():
    """
    Represents a table in the database.

    Attributes:
    - table: The name of the table.
    - columns: The columns of the table.
    - columnsList: A list of column names.

    Methods:
    - __init__(self, table_name, *args): Initializes the table.
    - getall(self): Retrieves all values from the table.
    - getone(self, search, value): Retrieves a single value from the table based on a column's data.
    - deleteone(self, search, value): Deletes a value from the table based on a column's data.
    - deleteall(self): Deletes all values from the table.
    - drop(self): Removes the table from the database.
    - insert(self, *args): Inserts values into the table.
    """

    def __init__(self, table_name, *args):
        """
        Initializes the table.

        Parameters:
        - table_name: The name of the table.
        - *args: The column names of the table.
        """
        self.table = table_name
        self.columns = "(%s)" % ",".join(args)
        self.columnsList = args

        if isnewtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(100)," % column

            cur = mysql.connection.cursor()
            cur.execute("CREATE TABLE %s(%s)" %
                        (self.table, create_data[:len(create_data)-1]))
            cur.close()

    def getall(self):
        """
        Retrieves all values from the table.

        Returns:
        - data: A list of dictionaries representing the rows in the table.
        """
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" % self.table)
        data = cur.fetchall()
        return data

    def getone(self, search, value):
        """
        Retrieves a single value from the table based on a column's data.

        Parameters:
        - search: The column to search in.
        - value: The value to search for.

        Returns:
        - data: A dictionary representing the row in the table.
        """
        data = {}
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" %
                             (self.table, search, value))
        if result > 0:
            data = cur.fetchone()
        cur.close()
        return data

    def deleteone(self, search, value):
        """
        Deletes a value from the table based on a column's data.

        Parameters:
        - search: The column to search in.
        - value: The value to search for.
        """
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" %
                    (self.table, search, value))
        mysql.connection.commit()
        cur.close()

    def deleteall(self):
        """
        Deletes all values from the table.
        """
        self.drop()
        self.__init__(self.table, *self.columnsList)

    def drop(self):
        """
        Removes the table from the database.
        """
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" % self.table)
        cur.close()

    def insert(self, *args):
        """
        Inserts values into the table.

        Parameters:
        - *args: The values to insert into the table.
        """
        data = ""
        for arg in args:
            data += "\"%s\"," % (arg)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" %
                    (self.table, self.columns, data[:len(data)-1]))
        mysql.connection.commit()
        cur.close()
    

def sql_raw(execution):
    """
    Executes raw SQL code.

    Parameters:
    - execution: The SQL code to execute.
    """
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()


def isnewtable(tableName):
    """
    Checks if a table already exists in the database.

    Parameters:
    - tableName: The name of the table to check.

    Returns:
    - True if the table does not exist, False otherwise.
    """
    cur = mysql.connection.cursor()

    try:
        result = cur.execute("SELECT * from %s" % tableName)
        cur.close()
    except:
        return True
    else:
        return False


def isnewuser(username):
    """
    Checks if a user already exists in the database.

    Parameters:
    - username: The username to check.

    Returns:
    - True if the user does not exist, False otherwise.
    """
    users = Table("users", "name", "email", "username", "password")
    data = users.getall()
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True

def get_user_username(username):
    """
    Retrieves a user from the database based on their username.

    Parameters:
    - username: The username to search for.

    Returns:
    - data: A dictionary representing the user.
    """
    users = Table("users", "name", "email", "username", "password")
    data = users.getone("username", username)
    return data.get('email')


def send_money(sender, recipient, amount):
    """
    Sends money from one user to another.

    Parameters:
    - sender: The sender's username.
    - recipient: The recipient's username.
    - amount: The amount of money to send.

    Raises:
    - InvalidTransactionException: If the transaction is invalid.
    - InsufficientFundsException: If the sender has insufficient funds.
    """
    try:
        amount = float(amount)
    except ValueError:
        raise InvalidTransactionException("Invalid Transaction.")

    if amount > get_balance(sender) and sender != "BANK":
        raise InsufficientFundsException("Insufficient Funds.")

    elif sender == recipient or amount <= 0.00:
        raise InvalidTransactionException("Invalid Transaction.")

    elif isnewuser(recipient):
        raise InvalidTransactionException("User Does Not Exist.")

    blockchain = get_blockchain()
    number = len(blockchain.chain) + 1
    data1 = "From: %s" % (sender)
    data2 = "To: %s" % (recipient)
    data3 = "Amount: %s" % (amount)
    blockchain.mine(Block(number, sender=data1, recipient=data2, amount=data3))
    blockchain.isValid()
    sync_blockchain(blockchain)
    

def get_balance(username):
    """
    Retrieves the balance of a user.

    Parameters:
    - username: The username of the user.

    Returns:
    - balance: The balance of the user.
    """
    balance = 0.00
    blockchain = get_blockchain()

    for block in blockchain.chain:
        data1 = block.sender.split(" ")
        data2 = block.recipient.split(" ")
        data3 = block.amount.split(" ")
        if username == data1[1]:
            balance -= float(data3[1])
        elif username == data2[1]:
            balance += float(data3[1])
    return balance


def get_blockchain():
    """
    Retrieves the blockchain from the database and converts it to a Blockchain object.

    Returns:
    - blockchain: The Blockchain object representing the blockchain.
    """
    blockchain = Blockchain()
    blockchain_sql = Table("PORT" + PORT , "number", "hash",
                           "previous", "sender", "recipient", "amount", "nonce")
    for b in blockchain_sql.getall():
        blockchain.add(Block(int(b.get('number')), b.get('previous'), b.get(
            'sender'), b.get('recipient'), b.get('amount'), int(b.get('nonce'))))

    blockchain.isValid()

    return blockchain


def dict_blockchain():
    """
    Retrieves the blockchain from the database as a list of dictionaries.

    Returns:
    - blockchain: A list of dictionaries representing the blockchain.
    """
    blockchain_sql = Table("PORT" + PORT , "number", "hash",
                           "previous", "sender", "recipient", "amount", "nonce")
    return blockchain_sql.getall()


def function(dictionary):
    """
    Inserts a dictionary into the blockchain table.

    Parameters:
    - dictionary: The dictionary to insert into the table.

    Returns:
    - res: The list of values from the dictionary.
    """
    res = list(dictionary.values())
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO PORT{PORT} (number, hash, previous, sender, recipient, amount, nonce) VALUES ('{res[0]}', '{res[1]}', '{res[2]}', '{res[3]}', '{res[4]}', '{res[5]}', '{res[6]}')")
    mysql.connection.commit()
    cur.close()
    return res


def sync_blockchain(blockchain):
    """
    Updates the blockchain table in the database with the given blockchain.

    Parameters:
    - blockchain: The Blockchain object representing the blockchain.
    """
    blockchain_sql = Table("PORT" + PORT , "number", "hash",
                           "previous", "sender", "recipient", "amount", "nonce")
    blockchain_sql.deleteall()

    for block in blockchain.chain:
        blockchain_sql.insert(str(block.number), block.hash(
        ), block.previous_hash, block.sender, block.recipient, block.amount, block.nonce)