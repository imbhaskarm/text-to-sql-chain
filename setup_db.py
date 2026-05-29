"""
Creates comic_store.db with 8 tables and seed data.
Run this once before running main.py.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "comic_store.db")


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
        DROP TABLE IF EXISTS sale_transaction;
        DROP TABLE IF EXISTS sale;
        DROP TABLE IF EXISTS inventory;
        DROP TABLE IF EXISTS employee;
        DROP TABLE IF EXISTS customer;
        DROP TABLE IF EXISTS comic;
        DROP TABLE IF EXISTS publisher;
        DROP TABLE IF EXISTS branch;

        CREATE TABLE branch (
            branch_id   INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            location    TEXT NOT NULL
        );

        CREATE TABLE publisher (
            publisher_id INTEGER PRIMARY KEY,
            name         TEXT NOT NULL
        );

        CREATE TABLE comic (
            comic_id     INTEGER PRIMARY KEY,
            title        TEXT NOT NULL,
            genre        TEXT,
            price        REAL NOT NULL,
            publisher_id INTEGER REFERENCES publisher(publisher_id)
        );

        CREATE TABLE customer (
            customer_id INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            email       TEXT,
            phone       TEXT
        );

        CREATE TABLE employee (
            employee_id INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            role        TEXT,
            branch_id   INTEGER REFERENCES branch(branch_id)
        );

        CREATE TABLE inventory (
            inventory_id INTEGER PRIMARY KEY,
            branch_id    INTEGER REFERENCES branch(branch_id),
            comic_id     INTEGER REFERENCES comic(comic_id),
            stock_count  INTEGER NOT NULL
        );

        CREATE TABLE sale (
            sale_id      INTEGER PRIMARY KEY,
            customer_id  INTEGER REFERENCES customer(customer_id),
            employee_id  INTEGER REFERENCES employee(employee_id),
            sale_date    TEXT NOT NULL,
            total_amount REAL NOT NULL
        );

        CREATE TABLE sale_transaction (
            transaction_id INTEGER PRIMARY KEY,
            sale_id        INTEGER REFERENCES sale(sale_id),
            comic_id       INTEGER REFERENCES comic(comic_id),
            quantity       INTEGER NOT NULL,
            unit_price     REAL NOT NULL
        );

        INSERT INTO branch VALUES (1,'Manhattan Branch','New York, NY'),(2,'Brooklyn Branch','Brooklyn, NY');

        INSERT INTO publisher VALUES (1,'Marvel Comics'),(2,'DC Comics'),(3,'IDW Publishing'),(4,'Dark Horse');

        INSERT INTO comic VALUES
        (1,'Wolverine','Action',9.99,1),(2,'Spider-Man','Action',8.99,1),
        (3,'Batman: The Killing Joke','Drama',12.99,2),(4,'V for Vendetta','Drama',14.99,2),
        (5,'Transformers #1','Sci-Fi',7.99,3),(6,'Hellboy Vol.1','Horror',11.99,4),
        (7,'X-Men: Days of Future Past','Action',10.99,1),(8,'Superman: Red Son','Alternate',13.99,2),
        (9,'Iron Man #128','Action',9.49,1),(10,'Wonder Woman: Year One','Action',11.49,2);

        INSERT INTO customer VALUES
        (1,'Tony Stark','tony@stark.com','555-0101'),(2,'Bruce Wayne','bruce@wayne.com','555-0102'),
        (3,'Peter Parker','peter@daily.com','555-0103'),(4,'Diana Prince','diana@themyscira.com','555-0104'),
        (5,'Clark Kent','clark@daily.com','555-0105'),(6,'Natasha Romanoff','nat@shield.com','555-0106'),
        (7,'Steve Rogers','steve@shield.com','555-0107'),(8,'Thor Odinson','thor@asgard.com','555-0108'),
        (9,'Barry Allen','barry@ccpd.com','555-0109'),(10,'Hal Jordan','hal@oa.com','555-0110'),
        (11,'Oliver Queen','ollie@qc.com','555-0111'),(12,'Arthur Curry','arthur@atlantis.com','555-0112'),
        (13,'Dick Grayson','dick@gotham.com','555-0113'),(14,'Wanda Maximoff','wanda@avengers.com','555-0114'),
        (15,'Scott Summers','scott@xmen.com','555-0115'),(16,'Jean Grey','jean@xmen.com','555-0116'),
        (17,'Logan Howlett','logan@xmen.com','555-0117'),(18,'Rogue Marie','rogue@xmen.com','555-0118'),
        (19,'Kurt Wagner','kurt@xmen.com','555-0119'),(20,'Ororo Monroe','storm@xmen.com','555-0120');

        INSERT INTO employee VALUES
        (1,'Alice Johnson','Sales Associate',1),(2,'Bob Smith','Manager',1),
        (3,'Carol White','Sales Associate',2),(4,'Dave Brown','Manager',2);

        INSERT INTO inventory VALUES
        (1,1,1,15),(2,1,2,10),(3,1,3,8),(4,1,4,12),(5,1,5,20),
        (6,2,6,5),(7,2,7,18),(8,2,8,7),(9,2,9,14),(10,2,10,9);

        INSERT INTO sale VALUES
        (1,1,1,'2024-01-10',45.97),(2,2,1,'2024-01-11',27.98),(3,1,2,'2024-01-12',19.99),
        (4,3,3,'2024-01-13',31.97),(5,4,3,'2024-01-14',14.99),(6,5,4,'2024-01-15',22.98),
        (7,1,1,'2024-01-16',24.98),(8,2,2,'2024-01-17',35.97),(9,6,3,'2024-01-18',18.99),
        (10,7,4,'2024-01-19',29.99),(11,1,1,'2024-01-20',41.97),(12,8,2,'2024-01-21',15.99),
        (13,3,3,'2024-01-22',28.98),(14,9,4,'2024-01-23',19.99),(15,10,1,'2024-01-24',33.97);

        INSERT INTO sale_transaction VALUES
        (1,1,1,1,9.99),(2,1,4,1,14.99),(3,1,7,2,10.99),
        (4,2,3,1,12.99),(5,2,2,1,14.99),(6,3,7,1,19.99),
        (7,4,1,1,9.99),(8,4,5,1,7.99),(9,4,9,1,9.49),
        (10,5,4,1,14.99),(11,6,2,1,8.99),(12,6,5,1,7.99),
        (13,7,1,1,9.99),(14,7,10,1,11.49),(15,8,1,2,9.99),
        (16,8,6,1,11.99),(17,8,8,1,13.99),(18,9,9,1,18.99),
        (19,10,1,1,9.99),(20,10,3,1,12.99),(21,10,7,1,10.99);
    """)

    conn.commit()
    conn.close()
    print(f"✅ comic_store.db created at: {DB_PATH}")


if __name__ == "__main__":
    create_database()
