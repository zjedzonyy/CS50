-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Crime_scene_reports from that day
 SELECT * from crime_scene_reports
 WHERE day = 28
 AND month = 7
 AND street = "Humphrey Street";

 | 295 | 2021 | 7     | 28  | Humphrey Street | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
 Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions
 the bakery.

 -- Interviews of the theft
 SELECT * from interviews
 WHERE day = 28
 AND month = 7;

| 161 | Ruth    | 2021 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
 If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| 162 | Eugene  | 2021 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's'
bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| 163 | Raymond | 2021 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on
the other end of the phone to purchase the flight ticket.

-- Find security footage, 10:15 - 10:25
SELECT * from bakery_security_logs
WHERE day = 28
AND month = 7
AND hour >= 10
AND hour <= 11;
 260 | 2021 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 262 | 2021 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 263 | 2021 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 265 | 2021 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 266 | 2021 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55

-- Find who whaws withdrawing money from ATM on Legget Street before 10:15AM
SELECT account_number, transaction_type, amount from atm_transactions
WHERE year = 2021
AND month = 7
AND day = 28
AND atm_location = "Leggett Street";

-- Find who has this bank account:
SELECT * from bank_accounts, atm_transactions
WHERE bank_accounts.account_number = atm_transactions.account_number
AND month = 7
AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";

| account_number | person_id | creation_year | id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
+----------------+-----------+---------------+-----+----------------+------+-------+-----+----------------+------------------+--------+
| 28500762       | 467400    | 2014          | 246 | 28500762       | 2021 | 7     | 28  | Leggett Street | withdraw         | 48     |
| 28296815       | 395717    | 2014          | 264 | 28296815       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 76054385       | 449774    | 2015          | 266 | 76054385       | 2021 | 7     | 28  | Leggett Street | withdraw         | 60     |
| 49610011       | 686048    | 2010          | 267 | 49610011       | 2021 | 7     | 28  | Leggett Street | withdraw         | 50     |
| 16153065       | 458378    | 2012          | 269 | 16153065       | 2021 | 7     | 28  | Leggett Street | withdraw         | 80     |
| 25506511       | 396669    | 2014          | 288 | 25506511       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 81061156       | 438727    | 2018          | 313 | 81061156       | 2021 | 7     | 28  | Leggett Street | withdraw         | 30     |
| 26013199       | 514354    | 2012          | 336 | 26013199       | 2021 | 7     | 28  | Leggett Street | withdraw         | 35

SELECT DISTINCT name, phone_number, passport_number, license_plate from people, bank_accounts, atm_transactions
WHERE people.id in
(SELECT person_id from bank_accounts, atm_transactions
WHERE bank_accounts.account_number = atm_transactions.account_number
AND month = 7
AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw");

|  name   |  phone_number  | passport_number | license_plate |
+---------+----------------+-----------------+---------------+
| Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       ||
| Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
| Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
+---------+----------------+-----------------+---------------+

--Check billings those people from 10:15AM ish, he called
SELECT * from phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration <= 60
AND caller = "(829) 555-5269"
or caller = "(389) 555-5198"
or caller = "(367) 555-5533";

+-----+----------------+----------------+------+-------+-----+----------+
| id  |     caller     |    receiver    | year | month | day | duration |
+-----+----------------+----------------+------+-------+-----+----------+
| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |

Bruce is a thief
Accomplice is: (375) 555-8161, Rboin

--Find accomplice
SELECT * from people
WHERE phone_number = "(375) 555-8161";

|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |
+--------+-------+----------------+-----------------+---------------+

--Find Luca's ID etc.
SELECT * from people
WHERE phone_number = "(367) 555-5533";

-- Robin purchuased flight tickets
SELECT * from flights, passengers
where flights.id = passengers.flight_id
and passport_number = "5773159633";

SELECT * from airports
WHERE id = 4;

+----+--------------+-------------------+---------------+
| id | abbreviation |     full_name     |     city      |
+----+--------------+-------------------+---------------+
| 4  | LGA          | LaGuardia Airport | New York City |
+----+--------------+-------------------+---------------+