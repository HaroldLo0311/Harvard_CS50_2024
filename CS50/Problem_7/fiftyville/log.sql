-- Keep a log of any SQL queries you execute as you solve the mystery.
-- 1. Look out the crime reports of the crime
SELECT * FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street' AND description LIKE '%Theft%';
-- 2. Find the interview transcript of the three witness
SELECT name, transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';
-- The results show that:
-- 2.1: Look for the car left the bakery parking lot within 10 min. of the theft.
-- 2.2: Eugene saw the thief withdrawing money from the ATM on Leggett Street at 2023/7/28 before 10:15 a.m..
-- 2.3: The theif called someone less than a minute before leaving to order the earliest flight out of Fiftyville tommorow.
-- 3. Find the answer according to the evidance
-- 3.1: Find the car match evidence 2.1
SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND (hour = 10 AND minute >= 15 AND minute <= 25)) ORDER BY name;
-- 3.2: Find the people match evidence 2.2
SELECT * FROM people WHERE id IN (SELECT person_id FROM atm_transactions JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw') ORDER BY name;
-- 3.3: Find the people match evidence 2.3
SELECT name, receiver FROM phone_calls JOIN people ON people.phone_number = phone_calls.caller WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60 ORDER by phone_calls;
SELECT name, receiver FROM phone_calls JOIN people ON people.phone_number = phone_calls.receiver WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60 ORDER by phone_calls;
-- Conclusion: the thief suspectator is lower to Bruce and Diana, and the reletive accomplice to Robin and Philip
SELECT name FROM passengers JOIN people ON passengers.passport_number = people.passport_number WHERE flight_id = 36 ORDER BY name;
-- 4. From the flight passenger list above, we can conclude that the perpetrator is Bruce and the accomplice is Doris.
SELECT flights.id, destination_airport_id, year, month, day, hour, minute, full_name, city, abbreviation FROM flights JOIN airports ON airports.id = flights.destination_airport_id WHERE flights.id = 36;
-- And their flight destination will be: New York City
