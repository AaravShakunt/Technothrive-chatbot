import psycopg2

class TransactionFetcher:
    def __init__(self, db_params):
        self.db_params = db_params
        self.conn = None
        self.connect()  # Establish the database connection in the constructor

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_params)
            print("Connected to the database.")
        except psycopg2.Error as e:
            print("Error:", e)

    def fetch_transactions_by_user(self, customer_id, name):
        query = "SELECT transactions FROM transactions WHERE patient_id = %s AND doctor_name = %s;"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (customer_id, name))
            result = cursor.fetchone()
            if result:
                transactions = result[0]
                return transactions
            else:
                return None
    
    def getAppointments(self, doctor_name):
        try:

            
            cursor = self.conn.cursor()
            
            query = "SELECT * FROM Appointments"
            cursor.execute(query, (doctor_name))
            appointments = cursor.fetchall()
            
            # cursor.close()
            # self.conn.close()
            
            if len(appointments) == 0:
                return None
            else:
                return appointments
            
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)
    
    def authenticate_doctor(self, id, doctor_name):
        try:

            
            cursor = self.conn.cursor()
            
            query = "SELECT * FROM Appointments WHERE patient_id = %s AND doctor_name = %s"
            cursor.execute(query, (id, doctor_name))
            appointments = cursor.fetchall()

            
            
            
            if len(appointments) == 0:
                return None
            else:
                appointments = self.getAppointments(doctor_name)
                cursor.close()
                self.conn.close()
                return appointments
            
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)



    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def process_request(self, customer_id, name):
        

        transactions = self.fetch_transactions_by_user(customer_id, name)

        if transactions:
            print(f"Transactions for {name} :")
            for transaction in transactions:
                print(transaction)
            return 1
        else:
            print("User does not exist.")
            return 0

    def __del__(self):
        self.close_connection()  # Close the database connection when the instance is deleted

if __name__ == "__main__":
    db_params = {
        'dbname': 'Converge',
        'user': 'postgres',
        'password': 'password',
        'host': 'localhost'
    }
    customer_id = int(input("Enter customer_id: "))
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    transaction_fetcher = TransactionFetcher(db_params)
    transaction_fetcher.process_request(customer_id, first_name, last_name)
