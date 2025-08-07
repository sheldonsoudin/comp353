-- Disable foreign key checks to safely truncate tables
SET FOREIGN_KEY_CHECKS = 0;

-- Truncate all tables to reset data and auto-increment IDs
TRUNCATE TABLE EmailLog;
TRUNCATE TABLE team_session;
TRUNCATE TABLE team_player;
TRUNCATE TABLE Sessions;
TRUNCATE TABLE Team;
TRUNCATE TABLE cm_hobby;
TRUNCATE TABLE Hobby;
TRUNCATE TABLE cm_payment;
TRUNCATE TABLE Payment;
TRUNCATE TABLE cm_location;
TRUNCATE TABLE family_association;
TRUNCATE TABLE secondary_fm;
TRUNCATE TABLE FamilyMember;
TRUNCATE TABLE ClubMember;
TRUNCATE TABLE personnel_location;
TRUNCATE TABLE Personnel;
TRUNCATE TABLE Location;
TRUNCATE TABLE Person;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Person (50 people: club members, family members, personnel)
INSERT INTO Person (person_id, first_name, last_name, ssn, dob, mcn, telephone, address, city, province, postal_code, email) VALUES
(1, 'John', 'Doe', '123-45-6789', '1985-03-15', 'MCN001', '514-555-0101', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'john.doe@club.com'),
(2, 'Jane', 'Smith', '234-56-7890', '1990-07-20', 'MCN002', '514-555-0102', '456 Pine Rd', 'Montreal', 'QC', 'H2B3C4', 'jane.smith@club.com'),
(3, 'Alice', 'Brown', '345-67-8901', '2010-01-10', 'MCN003', '514-555-0103', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'alice.brown@club.com'),
(4, 'Bob', 'Wilson', '456-78-9012', '1975-11-05', 'MCN004', '514-555-0104', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 'bob.wilson@club.com'),
(5, 'Emma', 'Davis', '567-89-0123', '2012-06-12', 'MCN005', '514-555-0105', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'emma.davis@club.com'),
(6, 'Michael', 'Lee', '678-90-1234', '1988-09-01', 'MCN006', '514-555-0106', '321 Maple Dr', 'Brossard', 'QC', 'H6F7G8', 'michael.lee@club.com'),
(7, 'Sarah', 'Adams', '789-01-2345', '1995-04-25', 'MCN007', '514-555-0107', '147 Elm Rd', 'Longueuil', 'QC', 'H7G8H9', 'sarah.adams@club.com'),
(8, 'David', 'Clark', '890-12-3456', '2009-02-15', 'MCN008', '514-555-0108', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 'david.clark@club.com'),
(9, 'Laura', 'Evans', '901-23-4567', '1982-12-20', 'MCN009', '514-555-0109', '741 Ash St', 'Verdun', 'QC', 'H0J1K2', 'laura.evans@club.com'),
(10, 'James', 'White', '012-34-5678', '2011-08-30', 'MCN010', '514-555-0110', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'james.white@club.com'),
(11, 'Sophie', 'Taylor', '123-45-6790', '1992-05-10', 'MCN011', '514-555-0111', '456 Pine Rd', 'Montreal', 'QC', 'H2B3C4', 'sophie.taylor@club.com'),
(12, 'Thomas', 'Green', '234-56-7891', '2008-03-25', 'MCN012', '514-555-0112', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'thomas.green@club.com'),
(13, 'Olivia', 'Martin', '345-67-8902', '1980-09-15', 'MCN013', '514-555-0113', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'olivia.martin@club.com'),
(14, 'William', 'Harris', '456-78-9013', '2013-11-20', 'MCN014', '514-555-0114', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 'william.harris@club.com'),
(15, 'Emily', 'Lewis', '567-89-0124', '1998-02-28', 'MCN015', '514-555-0115', '321 Maple Dr', 'Brossard', 'QC', 'H6F7G8', 'emily.lewis@club.com'),
(16, 'Daniel', 'Walker', '678-90-1235', '2007-07-12', 'MCN016', '514-555-0116', '147 Elm Rd', 'Longueuil', 'QC', 'H7G8H9', 'daniel.walker@club.com'),
(17, 'Chloe', 'Hall', '789-01-2346', '1987-04-10', 'MCN017', '514-555-0117', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 'chloe.hall@club.com'),
(18, 'Matthew', 'Allen', '890-12-3457', '2010-10-05', 'MCN018', '514-555-0118', '741 Ash St', 'Verdun', 'QC', 'H0J1K2', 'matthew.allen@club.com'),
(19, 'Ava', 'Young', '901-23-4568', '1993-06-22', 'MCN019', '514-555-0119', '321 Maple Dr', 'Brossard', 'QC', 'H6F7G8', 'ava.young@club.com'),
(20, 'Ethan', 'King', '012-34-5679', '2012-12-15', 'MCN020', '514-555-0120', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'ethan.king@club.com'),
(21, 'Mia', 'Scott', '123-45-6791', '1984-08-30', 'MCN021', '514-555-0121', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 'mia.scott@club.com'),
(22, 'Lucas', 'Wright', '234-56-7892', '2009-05-17', 'MCN022', '514-555-0122', '321 Maple Dr', 'Brossard', 'QC', 'H6F7G8', 'lucas.wright@club.com'),
(23, 'Isabella', 'Lopez', '345-67-8903', '1991-01-25', 'MCN023', '514-555-0123', '147 Elm Rd', 'Longueuil', 'QC', 'H7G8H9', 'isabella.lopez@club.com'),
(24, 'Mason', 'Hill', '456-78-9014', '2011-03-10', 'MCN024', '514-555-0124', '741 Ash St', 'Verdun', 'QC', 'H0J1K2', 'mason.hill@club.com'),
(25, 'Sophia', 'Green', '567-89-0125', '1986-11-12', 'MCN025', '514-555-0125', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'sophia.green@club.com'),
(26, 'Logan', 'Adams', '678-90-1236', '2008-09-05', 'MCN026', '514-555-0126', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'logan.adams@club.com'),
(27, 'Amelia', 'Nelson', '789-01-2347', '1994-07-18', 'MCN027', '514-555-0127', '456 Pine Rd', 'Montreal', 'QC', 'H2B3C4', 'amelia.nelson@club.com'),
(28, 'Oliver', 'Carter', '890-12-3458', '2010-04-22', 'MCN028', '514-555-0128', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 'oliver.carter@club.com'),
(29, 'Charlotte', 'Mitchell', '901-23-4569', '1983-02-15', 'MCN029', '514-555-0129', '321 Maple Dr', 'Brossard', 'QC', 'H6F7G8', 'charlotte.mitchell@club.com'),
(30, 'Elijah', 'Perez', '012-34-5680', '2012-01-30', 'MCN030', '514-555-0130', '147 Elm Rd', 'Longueuil', 'QC', 'H7G8H9', 'elijah.perez@club.com'),
(31, 'Harper', 'Roberts', '123-45-6792', '1990-10-10', 'MCN031', '514-555-0131', '258 Spruce Ave', 'Montreal', 'QC', 'H8H9I0', 'harper.roberts@club.com'),
(32, 'Benjamin', 'Turner', '234-56-7893', '2009-06-25', 'MCN032', '514-555-0132', '741 Ash St', 'Verdun', 'QC', 'H0J1K2', 'benjamin.turner@club.com'),
(33, 'Evelyn', 'Phillips', '345-67-8904', '1988-12-05', 'MCN033', '514-555-0133', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'evelyn.phillips@club.com'),
(34, 'Liam', 'Campbell', '456-78-9015', '2011-08-15', 'MCN034', '514-555-0134', '456 Pine Rd', 'Montreal', 'QC', 'H2B3C4', 'liam.campbell@club.com'),
(35, 'Aria', 'Parker', '567-89-0126', '1992-03-20', 'MCN035', '514-555-0135', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 'aria.parker@club.com'),
(36, 'Noah', 'Evans', '678-90-1237', '2010-11-10', 'MCN036', '514-555-0136', '321 Maple Dr', 'Brossard', 'QC', 'H6F7G8', 'noah.evans@club.com'),
(37, 'Zoe', 'Edwards', '789-01-2348', '1985-05-30', 'MCN037', '514-555-0137', '147 Elm Rd', 'Longueuil', 'QC', 'H7G8H9', 'zoe.edwards@club.com'),
(38, 'James', 'Collins', '890-12-3459', '2008-02-28', 'MCN038', '514-555-0138', '258 Spruce Ave', 'Montreal', 'QC', 'H8H9I0', 'james.collins@club.com'),
(39, 'Lily', 'Stewart', '901-23-4570', '1993-09-12', 'MCN039', '514-555-0139', '741 Ash St', 'Verdun', 'QC', 'H0J1K2', 'lily.stewart@club.com'),
(40, 'Henry', 'Sanchez', '012-34-5681', '2012-07-05', 'MCN040', '514-555-0140', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'henry.sanchez@club.com'),
(41, 'Ella', 'Morris', '123-45-6793', '1987-01-25', 'MCN041', '514-555-0141', '456 Pine Rd', 'Montreal', 'QC', 'H2B3C4', 'ella.morris@club.com'),
(42, 'Alexander', 'Rogers', '234-56-7894', '2009-04-15', 'MCN042', '514-555-0142', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 'alexander.rogers@club.com'),
(43, 'Grace', 'Reed', '345-67-8905', '1990-06-20', 'MCN043', '514-555-0143', '321 Maple Dr', 'Brossard', 'QC', 'H6F7G8', 'grace.reed@club.com'),
(44, 'Daniel', 'Cook', '456-78-9016', '2011-10-30', 'MCN044', '514-555-0144', '147 Elm Rd', 'Longueuil', 'QC', 'H7G8H9', 'daniel.cook@club.com'),
(45, 'Victoria', 'Morgan', '567-89-0127', '1984-08-15', 'MCN045', '514-555-0145', '258 Spruce Ave', 'Montreal', 'QC', 'H8H9I0', 'victoria.morgan@club.com'),
(46, 'Joseph', 'Murphy', '678-90-1238', '2010-03-10', 'MCN046', '514-555-0146', '741 Ash St', 'Verdun', 'QC', 'H0J1K2', 'joseph.murphy@club.com'),
(47, 'Samantha', 'Bailey', '789-01-2349', '1992-11-25', 'MCN047', '514-555-0147', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 'samantha.bailey@club.com'),
(48, 'David', 'Rivera', '890-12-3460', '2008-07-20', 'MCN048', '514-555-0148', '456 Pine Rd', 'Montreal', 'QC', 'H2B3C4', 'david.rivera@club.com'),
(49, 'Hannah', 'Cooper', '901-23-4571', '1986-02-28', 'MCN049', '514-555-0149', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 'hannah.cooper@club.com'),
(50, 'Andrew', 'Richardson', '012-34-5682', '2011-05-15', 'MCN050', '514-555-0150', '321 Maple Dr', 'Brossard', 'QC', 'H6F7G8', 'andrew.richardson@club.com');

-- Location (5 locations: 1 Head, 4 Branches)
INSERT INTO Location (location_id, name, type, phone_number, web_address, address, city, province, postal_code, max_capacity) VALUES
(1, 'Montreal Head', 'Head', '514-555-1001', 'www.mvc-head.com', '123 Main St', 'Montreal', 'QC', 'H1A2B3', 50),
(2, 'Laval Branch', 'Branch', '514-555-1002', 'www.mvc-laval.com', '789 Oak Ave', 'Laval', 'QC', 'H4D5E6', 30),
(3, 'Brossard Branch', 'Branch', '514-555-1003', 'www.mvc-brossard.com', '321 Maple Dr', 'Brossard', 'QC', 'H6F7G8', 20),
(4, 'Longueuil Branch', 'Branch', '514-555-1004', 'www.mvc-longueuil.com', '147 Elm Rd', 'Longueuil', 'QC', 'H7G8H9', 20),
(5, 'Verdun Branch', 'Branch', '514-555-1005', 'www.mvc-verdun.com', '741 Ash St', 'Verdun', 'QC', 'H0J1K2', 20);

-- Personnel (10 personnel, including General Managers)
INSERT INTO Personnel (personnel_id, person_id) VALUES
(1, 1), -- John Doe
(2, 4), -- Bob Wilson
(3, 6), -- Michael Lee
(4, 7), -- Sarah Adams
(5, 9), -- Laura Evans
(6, 13), -- Olivia Martin
(7, 17), -- Chloe Hall
(8, 21), -- Mia Scott
(9, 25), -- Sophia Green
(10, 29); -- Charlotte Mitchell

-- personnel_location (assign personnel to locations)
INSERT INTO personnel_location (personnel_id, location_id, start_date, role, mandate) VALUES
(1, 1, '2024-01-01', 'General Manager', 'Salaried'),
(2, 2, '2024-01-01', 'General Manager', 'Salaried'),
(3, 3, '2024-01-01', 'General Manager', 'Salaried'),
(4, 4, '2024-01-01', 'General Manager', 'Salaried'),
(5, 5, '2024-01-01', 'General Manager', 'Salaried'),
(6, 1, '2024-01-01', 'Coach', 'Salaried'),
(7, 2, '2024-01-01', 'Coach', 'Volunteer'),
(8, 1, '2024-01-01', 'Administrator', 'Salaried'),
(9, 1, '2024-01-01', 'Secretary', 'Salaried'),
(10, 1, '2024-01-01', 'Treasurer', 'Salaried');

-- ClubMember (30 members: 15 minors, 15 majors)
INSERT INTO ClubMember (cm_id, person_id, height, weight, gender, membership_status, last_paid_year) VALUES
(1, 3, 150.25, 45.30, 'Female', 'Active', 2025),
(2, 5, 145.50, 40.80, 'Female', 'Active', 2025),
(3, 8, 155.00, 50.20, 'Male', 'Active', 2025),
(4, 10, 148.75, 42.60, 'Male', 'Active', 2025),
(5, 12, 152.00, 47.50, 'Male', 'Active', 2025),
(6, 14, 147.25, 43.80, 'Male', 'Active', 2025),
(7, 16, 149.50, 46.20, 'Male', 'Active', 2025),
(8, 18, 151.75, 48.90, 'Male', 'Active', 2025),
(9, 20, 146.00, 44.30, 'Male', 'Active', 2025),
(10, 22, 153.25, 49.60, 'Male', 'Active', 2025),
(11, 24, 148.50, 45.70, 'Male', 'Active', 2025),
(12, 26, 150.75, 47.10, 'Male', 'Active', 2025),
(13, 28, 152.50, 48.40, 'Male', 'Active', 2025),
(14, 30, 147.75, 44.90, 'Male', 'Active', 2025),
(15, 32, 149.00, 46.60, 'Male', 'Active', 2025),
(16, 2, 165.00, 60.50, 'Female', 'Active', 2025),
(17, 11, 168.25, 62.70, 'Female', 'Active', 2025),
(18, 15, 170.50, 65.90, 'Female', 'Active', 2025),
(19, 19, 172.75, 68.20, 'Female', 'Active', 2025),
(20, 23, 167.00, 61.40, 'Female', 'Active', 2025),
(21, 27, 169.25, 63.80, 'Female', 'Active', 2025),
(22, 29, 171.50, 66.10, 'Female', 'Active', 2025),
(23, 31, 166.75, 60.90, 'Female', 'Inactive', 2024),
(24, 33, 168.50, 62.20, 'Female', 'Inactive', 2024),
(25, 35, 170.00, 64.50, 'Female', 'Inactive', 2024),
(26, 37, 172.25, 67.80, 'Female', 'Inactive', 2024),
(27, 39, 167.50, 61.10, 'Female', 'Inactive', 2024),
(28, 41, 169.75, 63.40, 'Female', 'Inactive', 2024),
(29, 43, 171.00, 65.70, 'Female', 'Inactive', 2024),
(30, 45, 166.25, 60.00, 'Female', 'Inactive', 2024);

-- FamilyMember (10 family members for minors)
INSERT INTO FamilyMember (fm_id, person_id) VALUES
(1, 1), -- John Doe
(2, 2), -- Jane Smith
(3, 4), -- Bob Wilson
(4, 6), -- Michael Lee
(5, 7), -- Sarah Adams
(6, 9), -- Laura Evans
(7, 13), -- Olivia Martin
(8, 17), -- Chloe Hall
(9, 21), -- Mia Scott
(10, 25); -- Sophia Green

-- family_association (minors linked to fm_id = 1 for Query 9, others for triggers)
INSERT INTO family_association (fm_id, cm_id, relationship, start_date) VALUES
(1, 1, 'Father', '2024-01-10'), -- John Doe -> Alice Brown
(1, 2, 'Father', '2024-06-12'), -- John Doe -> Emma Davis
(1, 3, 'Father', '2024-02-15'), -- John Doe -> David Clark
(1, 4, 'Father', '2024-08-30'), -- John Doe -> James White
(1, 5, 'Father', '2024-03-25'), -- John Doe -> Thomas Green
(1, 6, 'Father', '2024-11-20'), -- John Doe -> William Harris
(1, 7, 'Father', '2024-07-12'), -- John Doe -> Daniel Walker
(1, 8, 'Father', '2024-10-05'), -- John Doe -> Matthew Allen
(1, 9, 'Father', '2024-12-15'), -- John Doe -> Ethan King
(1, 10, 'Father', '2024-05-17'), -- John Doe -> Lucas Wright
(2, 11, 'Mother', '2024-03-10'), -- Jane Smith -> Mason Hill
(3, 12, 'Father', '2024-09-05'), -- Bob Wilson -> Logan Adams
(4, 13, 'Father', '2024-04-22'), -- Michael Lee -> Oliver Carter
(5, 14, 'Mother', '2024-01-30'), -- Sarah Adams -> Elijah Perez
(6, 15, 'Mother', '2024-06-25'); -- Laura Evans -> Benjamin Turner

-- secondary_fm (secondary family members for fm_id = 1)
INSERT INTO secondary_fm (fm_id, secondary_fm_id) VALUES
(1, 2), -- Jane Smith
(1, 3), -- Bob Wilson
(1, 4), -- Michael Lee
(1, 5), -- Sarah Adams
(1, 6), -- Laura Evans
(1, 7), -- Olivia Martin
(1, 8), -- Chloe Hall
(1, 9), -- Mia Scott
(1, 10), -- Sophia Green
(2, 1); -- John Doe (for 10+ tuples)

-- cm_location (club members to locations, respecting max_capacity)
INSERT INTO cm_location (location_id, cm_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), -- Montreal (10 Active)
(2, 11), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), -- Laval (6 Active)
(3, 17), (3, 18), (3, 19), (3, 20), -- Brossard (4 Active)
(4, 21), (4, 22), (4, 23), (4, 24), -- Longueuil (4 Active)
(5, 25), (5, 26), (5, 27), (5, 28), -- Verdun (4 Active)
(1, 29), (1, 30); -- Inactive members for Query 11

-- Payment (30 payments, including installments)
INSERT INTO Payment (payment_id, payment_method, payment_date, payment_amount) VALUES
(1, 'Credit Card', '2025-01-10', 100.00), -- Alice Brown (Minor)
(2, 'Debit Card', '2025-01-15', 100.00), -- Emma Davis (Minor)
(3, 'Cash', '2025-01-20', 100.00), -- David Clark (Minor)
(4, 'Credit Card', '2025-01-25', 100.00), -- James White (Minor)
(5, 'Debit Card', '2025-01-30', 100.00), -- Thomas Green (Minor)
(6, 'Credit Card', '2025-02-05', 100.00), -- William Harris (Minor)
(7, 'Cash', '2025-02-10', 100.00), -- Daniel Walker (Minor)
(8, 'Debit Card', '2025-02-15', 100.00), -- Matthew Allen (Minor)
(9, 'Credit Card', '2025-02-20', 100.00), -- Ethan King (Minor)
(10, 'Cash', '2025-02-25', 100.00), -- Lucas Wright (Minor)
(11, 'Credit Card', '2025-03-01', 100.00), -- Mason Hill (Minor)
(12, 'Debit Card', '2025-03-05', 100.00), -- Logan Adams (Minor)
(13, 'Cash', '2025-03-10', 100.00), -- Oliver Carter (Minor)
(14, 'Credit Card', '2025-03-15', 100.00), -- Elijah Perez (Minor)
(15, 'Debit Card', '2025-03-20', 100.00), -- Benjamin Turner (Minor)
(16, 'Credit Card', '2025-01-10', 100.00), -- Jane Smith (Major, installment 1)
(17, 'Credit Card', '2025-02-10', 100.00), -- Jane Smith (Major, installment 2)
(18, 'Debit Card', '2025-01-15', 100.00), -- Sophie Taylor (Major, installment 1)
(19, 'Debit Card', '2025-02-15', 100.00), -- Sophie Taylor (Major, installment 2)
(20, 'Cash', '2025-01-20', 200.00), -- Emily Lewis (Major)
(21, 'Credit Card', '2025-01-25', 200.00), -- Ava Young (Major)
(22, 'Debit Card', '2025-01-30', 200.00), -- Isabella Lopez (Major)
(23, 'Credit Card', '2025-02-05', 200.00), -- Amelia Nelson (Major)
(24, 'Cash', '2025-02-10', 200.00), -- Charlotte Mitchell (Major)
(25, 'Debit Card', '2024-02-15', 50.00), -- Harper Roberts (Inactive)
(26, 'Credit Card', '2024-02-20', 50.00), -- Evelyn Phillips (Inactive)
(27, 'Cash', '2024-02-25', 50.00), -- Aria Parker (Inactive)
(28, 'Debit Card', '2024-03-01', 50.00), -- Zoe Edwards (Inactive)
(29, 'Credit Card', '2024-03-05', 50.00), -- Lily Stewart (Inactive)
(30, 'Cash', '2024-03-10', 50.00); -- Victoria Morgan (Inactive)

-- cm_payment (link payments to members)
INSERT INTO cm_payment (payment_id, cm_id, membership_year) VALUES
(1, 1, 2025), (2, 2, 2025), (3, 3, 2025), (4, 4, 2025), (5, 5, 2025),
(6, 6, 2025), (7, 7, 2025), (8, 8, 2025), (9, 9, 2025), (10, 10, 2025),
(11, 11, 2025), (12, 12, 2025), (13, 13, 2025), (14, 14, 2025), (15, 15, 2025),
(16, 16, 2025), (17, 16, 2025), (18, 17, 2025), (19, 17, 2025), (20, 18, 2025),
(21, 19, 2025), (22, 20, 2025), (23, 21, 2025), (24, 22, 2025), (25, 23, 2024),
(26, 24, 2024), (27, 25, 2024), (28, 26, 2024), (29, 27, 2024), (30, 28, 2024);

-- Hobby (10 hobbies)
INSERT INTO Hobby (hobby_id, hobby_name) VALUES
(1, 'Volleyball'), (2, 'Soccer'), (3, 'Tennis'), (4, 'Ping Pong'), (5, 'Swimming'),
(6, 'Hockey'), (7, 'Golf'), (8, 'Basketball'), (9, 'Running'), (10, 'Yoga');

-- cm_hobby (assign hobbies to club members)
INSERT INTO cm_hobby (hobby_id, cm_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
(2, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
(1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20);

-- Team (10 teams, split by gender and location)
INSERT INTO Team (team_id, team_name, personnel_id, captain_id, gender) VALUES
(1, 'Montreal Mens', 6, 3, 'Male'),
(2, 'Laval Mens', 7, 11, 'Male'),
(3, 'Brossard Mens', 3, 8, 'Male'),
(4, 'Longueuil Mens', 4, 13, 'Male'),
(5, 'Verdun Mens', 5, 11, 'Male'),
(6, 'Montreal Womens', 6, 1, 'Female'),
(7, 'Laval Womens', 7, 2, 'Female'),
(8, 'Brossard Womens', 3, 18, 'Female'),
(9, 'Longueuil Womens', 4, 19, 'Female'),
(10, 'Verdun Womens', 5, 20, 'Female');

-- team_player (assign players to teams, respecting gender and cm_id <= 30)
INSERT INTO team_player (team_id, cm_id, role) VALUES
(1, 3, 'setters'), (1, 5, 'outside_hitters'), (1, 8, 'libero'), (1, 10, 'middle_blocker'),
(2, 11, 'setters'), (2, 12, 'outside_hitters'), (2, 14, 'libero'), (2, 16, 'middle_blocker'),
(3, 8, 'setters'), (3, 9, 'outside_hitters'), (3, 10, 'libero'), (3, 11, 'middle_blocker'),
(4, 13, 'setters'), (4, 14, 'outside_hitters'), (4, 15, 'libero'), (4, 12, 'middle_blocker'),
(5, 11, 'setters'), (5, 13, 'outside_hitters'), (5, 14, 'libero'), (5, 15, 'middle_blocker'),
(6, 1, 'setters'), (6, 2, 'outside_hitters'), (6, 16, 'libero'), (6, 17, 'middle_blocker'),
(7, 2, 'setters'), (7, 17, 'outside_hitters'), (7, 18, 'libero'), (7, 19, 'middle_blocker'),
(8, 18, 'setters'), (8, 19, 'outside_hitters'), (8, 20, 'libero'), (8, 21, 'middle_blocker'),
(9, 19, 'setters'), (9, 20, 'outside_hitters'), (9, 21, 'libero'), (9, 22, 'middle_blocker'),
(10, 20, 'setters'), (10, 21, 'outside_hitters'), (10, 22, 'libero'), (10, 16, 'middle_blocker');

-- Sessions (20 sessions, mix of Game and Training)
INSERT INTO Sessions (session_id, date, start_time, address, end_time, session_type) VALUES
(1, '2025-08-03', '09:00:00', '123 Main St, Montreal', '11:00:00', 'Game'),
(2, '2025-08-03', '13:00:00', '123 Main St, Montreal', NULL, 'Training'),
(3, '2025-08-04', '10:00:00', '789 Oak Ave, Laval', '12:00:00', 'Game'),
(4, '2025-08-04', '15:00:00', '789 Oak Ave, Laval', NULL, 'Training'),
(5, '2025-08-05', '11:00:00', '321 Maple Dr, Brossard', '13:00:00', 'Game'),
(6, '2025-08-05', '16:00:00', '321 Maple Dr, Brossard', NULL, 'Training'),
(7, '2025-08-06', '09:00:00', '147 Elm Rd, Longueuil', '11:00:00', 'Game'),
(8, '2025-08-06', '14:00:00', '147 Elm Rd, Longueuil', NULL, 'Training'),
(9, '2025-08-07', '10:00:00', '741 Ash St, Verdun', '12:00:00', 'Game'),
(10, '2025-08-07', '15:00:00', '741 Ash St, Verdun', NULL, 'Training'),
(11, '2025-08-08', '09:00:00', '123 Main St, Montreal', '11:00:00', 'Game'),
(12, '2025-08-08', '13:00:00', '123 Main St, Montreal', NULL, 'Training'),
(13, '2025-08-09', '10:00:00', '789 Oak Ave, Laval', '12:00:00', 'Game'),
(14, '2025-08-09', '15:00:00', '789 Oak Ave, Laval', NULL, 'Training'),
(15, '2025-07-01', '11:00:00', '123 Main St, Montreal', '13:00:00', 'Game'),
(16, '2025-07-02', '09:00:00', '123 Main St, Montreal', NULL, 'Training'),
(17, '2025-07-15', '10:00:00', '123 Main St, Montreal', '12:00:00', 'Game'),
(18, '2025-07-16', '14:00:00', '123 Main St, Montreal', NULL, 'Training'),
(19, '2025-09-01', '11:00:00', '123 Main St, Montreal', '13:00:00', 'Game'),
(20, '2025-09-02', '09:00:00', '123 Main St, Montreal', NULL, 'Training');

-- team_session (assign sessions to teams, no overlaps)
INSERT INTO team_session (team_id, session_id) VALUES
(1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (3, 6), (4, 7), (4, 8), (5, 9), (5, 10),
(6, 11), (6, 12), (7, 13), (7, 14), (8, 15), (8, 16), (9, 17), (9, 18), (10, 19), (10, 20);

-- Query 11: Club members whose membership_status = 'Inactive' and associated with location_id = 1
-- Add more inactive members to location_id = 1
INSERT INTO cm_location (location_id, cm_id) VALUES
(1, 27), -- Mia Scott (Inactive)
(1, 28), -- Sophia Green (Inactive)
(1, 26), -- Chloe Hall (Inactive)
(1, 25), -- Olivia Martin (Inactive)
(1, 24); -- Laura Evans (Inactive)

/* ─────────  LOCATIONS  ───────── */
INSERT INTO Location
        (location_id, name,type,  phone_number, web_address,
         address,      city,    province, postal_code, max_capacity)
VALUES  (101,'Main Gym', 'Head',  '555-0001','https://maingym.example.com',
         '123 Main St','Toronto','ON','M1A 1A1',200),
        (102,'North Br.', 'Branch','555-0002','https://north.example.com',
         '456 North Rd','Toronto','ON','M1A 1A2',150),
        (103,'South Br.', 'Branch','555-0003','https://south.example.com',
         '789 South Av','Toronto','ON','M1A 1A3',150);

/* ─────────  PEOPLE  ──────────── */
INSERT INTO Person
        (person_id, first_name, last_name, ssn, dob,  mcn,
         telephone, address, city, province, postal_code, email)
VALUES
 /* 5 ACTIVE MEMBERS WITHOUT TEAMS  → query 13 */
 (1101,'Alice','Adams','SSN0001','1999-04-15',NULL,'555-1001',
    '11 A St','Toronto','ON','M1B 1B1','alice.adams@example.com'),
 (1102,'Ben','Brown','SSN0002','1998-07-12',NULL,'555-1002',
    '12 B St','Toronto','ON','M1B 1B2','ben.brown@example.com'),
 (1103,'Cara','Clark','SSN0003','2001-09-20',NULL,'555-1003',
    '13 C St','Toronto','ON','M1B 1B3','cara.clark@example.com'),
 (1104,'Dave','Davis','SSN0004','1997-01-05',NULL,'555-1004',
    '14 D St','Toronto','ON','M1B 1B4','dave.davis@example.com'),
 (1105,'Eva','Evans','SSN0005','2002-11-11',NULL,'555-1005',
    '15 E St','Toronto','ON','M1B 1B5','eva.evans@example.com'),

 /* ADULT-NOW / MINOR-AT-LINK MEMBERS → query 14 */
 (1106,'Finn','Fisher','SSN0006','2005-08-03',NULL,'555-1006',
    '16 F St','Toronto','ON','M1B 1B6','finn.fisher@example.com'),
 (1107,'Grace','Green','SSN0007','2005-02-28',NULL,'555-1007',
    '17 G St','Toronto','ON','M1B 1B7','grace.green@example.com'),
 (1108,'Hank','Hall','SSN0008','2006-07-15',NULL,'555-1008',
    '18 H St','Toronto','ON','M1B 1B8','hank.hall@example.com'),
 (1109,'Ivy','Irwin','SSN0009','2004-12-22',NULL,'555-1009',
    '19 I St','Toronto','ON','M1B 1B9','ivy.irwin@example.com'),
 (1110,'Jack','Jones','SSN0010','2005-05-30',NULL,'555-1010',
    '20 J St','Toronto','ON','M1B 1C0','jack.jones@example.com'),

 /* “SETTERS-ONLY” PLAYERS           → query 15 */
 (1111,'Kelly','King','SSN0011','1999-03-03',NULL,'555-1011',
    '21 K St','Toronto','ON','M1B 1C1','kelly.king@example.com'),
 (1112,'Liam','Lee','SSN0012','1998-12-14',NULL,'555-1012',
    '22 L St','Toronto','ON','M1B 1C2','liam.lee@example.com'),
 (1113,'Mia','Moore','SSN0013','1997-06-08',NULL,'555-1013',
    '23 M St','Toronto','ON','M1B 1C3','mia.moore@example.com'),
 (1114,'Noah','Novak','SSN0014','2000-10-25',NULL,'555-1014',
    '24 N St','Toronto','ON','M1B 1C4','noah.novak@example.com'),
 (1115,'Olivia','Olsen','SSN0015','1996-01-19',NULL,'555-1015',
    '25 O St','Toronto','ON','M1B 1C5','olivia.olsen@example.com'),

 /* MULTI-ROLE PLAYERS               → query 16 */
 (1116,'Paul','Perez','SSN0016','1999-09-09',NULL,'555-1016',
    '26 P St','Toronto','ON','M1B 1C6','paul.perez@example.com'),
 (1117,'Quinn','Quill','SSN0017','2000-04-24',NULL,'555-1017',
    '27 Q St','Toronto','ON','M1B 1C7','quinn.quill@example.com'),
 (1118,'Ruby','Reed','SSN0018','1998-11-30',NULL,'555-1018',
    '28 R St','Toronto','ON','M1B 1C8','ruby.reed@example.com'),
 (1119,'Sam','Smith','SSN0019','1997-08-18',NULL,'555-1019',
    '29 S St','Toronto','ON','M1B 1C9','sam.smith@example.com'),
 (1120,'Tina','Turner','SSN0020','1999-02-13',NULL,'555-1020',
    '30 T St','Toronto','ON','M1B 1D0','tina.turner@example.com'),

 /* UNDEFEATED PLAYERS               → query 18 */
 (1121,'Uri','Underwood','SSN0021','1995-11-11',NULL,'555-1021',
    '31 U St','Toronto','ON','M1B 1D1','uri.underwood@example.com'),
 (1122,'Vera','Vega','SSN0022','1998-02-02',NULL,'555-1022',
    '32 V St','Toronto','ON','M1B 1D2','vera.vega@example.com'),
 (1123,'Will','White','SSN0023','1996-07-07',NULL,'555-1023',
    '33 W St','Toronto','ON','M1B 1D3','will.white@example.com'),
 (1124,'Xena','Xu','SSN0024','1997-12-12',NULL,'555-1024',
    '34 X St','Toronto','ON','M1B 1D4','xena.xu@example.com'),
 (1125,'Yara','Young','SSN0025','1998-06-06',NULL,'555-1025',
    '35 Y St','Toronto','ON','M1B 1D5','yara.young@example.com'),

 /* PARENTS / COACHES (Adults)       → query 17 */
 (1126,'Greg','Guardian','SSN0026','1975-03-14',NULL,'555-1026',
    '36 Z St','Toronto','ON','M1B 1D6','greg.guardian@example.com'),
 (1127,'Harriet','Guardian','SSN0027','1976-09-09',NULL,'555-1027',
    '37 AA St','Toronto','ON','M1B 1D7','harriet.guardian@example.com'),
 (1128,'Ian','Guardian','SSN0028','1974-01-21',NULL,'555-1028',
    '38 AB St','Toronto','ON','M1B 1D8','ian.guardian@example.com'),
 (1129,'Julia','Guardian','SSN0029','1973-05-05',NULL,'555-1029',
    '39 AC St','Toronto','ON','M1B 1D9','julia.guardian@example.com'),
 (1130,'Karl','Guardian','SSN0030','1972-11-11',NULL,'555-1030',
    '40 AD St','Toronto','ON','M1B 1E0','karl.guardian@example.com'),

 /* EXTRA OPPONENT PLAYERS           (for losing team) */
 (1141,'Quentin','Opponent','SSN0041','1995-06-06',NULL,'555-1041',
    '51 AO St','Toronto','ON','M1B 1F1','quentin.opponent@example.com'),
 (1142,'Rachel','Opponent','SSN0042','1996-07-07',NULL,'555-1042',
    '52 AP St','Toronto','ON','M1B 1F2','rachel.opponent@example.com'),
 (1143,'Steve','Opponent','SSN0043','1997-08-08',NULL,'555-1043',
    '53 AQ St','Toronto','ON','M1B 1F3','steve.opponent@example.com'),
 (1144,'Tracy','Opponent','SSN0044','1998-09-09',NULL,'555-1044',
    '54 AR St','Toronto','ON','M1B 1F4','tracy.opponent@example.com'),
 (1145,'Uma','Opponent','SSN0045','1999-10-10',NULL,'555-1045',
    '55 AS St','Toronto','ON','M1B 1F5','uma.opponent@example.com'),

 /* MINOR VOLUNTEERS (<18)           → query 19 */
 (1136,'Lily','Volunteer','SSN0036','2010-03-03',NULL,'555-1036',
    '46 AJ St','Toronto','ON','M1B 1E6','lily.volunteer@example.com'),
 (1137,'Max','Volunteer','SSN0037','2011-06-06',NULL,'555-1037',
    '47 AK St','Toronto','ON','M1B 1E7','max.volunteer@example.com'),
 (1138,'Nora','Volunteer','SSN0038','2009-12-12',NULL,'555-1038',
    '48 AL St','Toronto','ON','M1B 1E8','nora.volunteer@example.com'),
 (1139,'Oscar','Volunteer','SSN0039','2010-08-08',NULL,'555-1039',
    '49 AM St','Toronto','ON','M1B 1E9','oscar.volunteer@example.com'),
 (1140,'Penny','Volunteer','SSN0040','2011-07-07',NULL,'555-1040',
    '50 AN St','Toronto','ON','M1B 1F0','penny.volunteer@example.com');

/* ─────────  CLUB MEMBERS  ─────── */
INSERT INTO ClubMember
        (cm_id, person_id, height, weight, gender,
         membership_status, last_paid_year)
VALUES  -- 5 non-team actives
        (2001,1101,NULL,NULL,'F','Active',2025),
        (2002,1102,NULL,NULL,'M','Active',2025),
        (2003,1103,NULL,NULL,'F','Active',2025),
        (2004,1104,NULL,NULL,'M','Active',2025),
        (2005,1105,NULL,NULL,'F','Active',2025),

        -- adult-now/minor-then group
        (2006,1106,NULL,NULL,'M','Active',2025),
        (2007,1107,NULL,NULL,'F','Active',2025),
        (2008,1108,NULL,NULL,'M','Active',2025),
        (2009,1109,NULL,NULL,'F','Active',2025),
        (2010,1110,NULL,NULL,'M','Active',2025),

        -- setters-only
        (2011,1111,NULL,NULL,'F','Active',2025),
        (2012,1112,NULL,NULL,'M','Active',2025),
        (2013,1113,NULL,NULL,'F','Active',2025),
        (2014,1114,NULL,NULL,'M','Active',2025),
        (2015,1115,NULL,NULL,'F','Active',2025),

        -- multi-role players
        (2016,1116,NULL,NULL,'M','Active',2025),
        (2017,1117,NULL,NULL,'F','Active',2025),
        (2018,1118,NULL,NULL,'F','Active',2025),
        (2019,1119,NULL,NULL,'M','Active',2025),
        (2020,1120,NULL,NULL,'F','Active',2025),

        -- undefeated players
        (2021,1121,NULL,NULL,'M','Active',2025),
        (2022,1122,NULL,NULL,'F','Active',2025),
        (2023,1123,NULL,NULL,'M','Active',2025),
        (2024,1124,NULL,NULL,'F','Active',2025),
        (2025,1125,NULL,NULL,'F','Active',2025),

        -- losing-team opponents
        (2026,1141,NULL,NULL,'M','Active',2025),
        (2027,1142,NULL,NULL,'F','Active',2025),
        (2028,1143,NULL,NULL,'M','Active',2025),
        (2029,1144,NULL,NULL,'F','Active',2025),
        (2030,1145,NULL,NULL,'F','Active',2025);

/* ─────────  FAMILY MEMBERS  ───── */
INSERT INTO FamilyMember (fm_id, person_id) VALUES
 (3001,1126),(3002,1127),(3003,1128),(3004,1129),(3005,1130),  -- adult coaches
 (3006,1136),(3007,1137),(3008,1138),(3009,1139),(3010,1140); -- minor volunteers

/* ────────  PERSONNEL  ─────────── */
INSERT INTO Personnel (personnel_id, person_id) VALUES
 (4001,1126),(4002,1127),(4003,1128),(4004,1129),(4005,1130),  -- coaches
 (4006,1136),(4007,1137),(4008,1138),(4009,1139),(4010,1140);  -- volunteers

/* ────────  CM ↔ LOCATION  ─────── */
INSERT INTO cm_location (location_id, cm_id) VALUES
 -- everyone trains at Main Gym (location_id 101)
 (101,2001),(101,2002),(101,2003),(101,2004),(101,2005),
 (101,2006),(101,2007),(101,2008),(101,2009),(101,2010),
 (101,2011),(101,2012),(101,2013),(101,2014),(101,2015),
 (101,2016),(101,2017),(101,2018),(101,2019),(101,2020),
 (101,2021),(101,2022),(101,2023),(101,2024),(101,2025),
 (101,2026),(101,2027),(101,2028),(101,2029),(101,2030);

/* ────────  PERSONNEL ↔ LOCATION  ─ */
INSERT INTO personnel_location
        (personnel_id, location_id, start_date, end_date, `role`, mandate)
VALUES  -- salaried coaches (query 17)
 (4001,101,'2023-01-01',NULL,'Coach','Salaried'),
 (4002,101,'2023-01-01',NULL,'Coach','Salaried'),
 (4003,101,'2023-01-01',NULL,'Coach','Salaried'),
 (4004,101,'2023-01-01',NULL,'Coach','Salaried'),
 (4005,101,'2023-01-01',NULL,'Coach','Salaried'),

 -- minor volunteers (query 19)
 (4006,102,'2024-01-01',NULL,'Assistant Coach','Volunteer'),
 (4007,102,'2024-01-01',NULL,'Assistant Coach','Volunteer'),
 (4008,102,'2024-01-01',NULL,'Assistant Coach','Volunteer'),
 (4009,102,'2024-01-01',NULL,'Assistant Coach','Volunteer'),
 (4010,102,'2024-01-01',NULL,'Assistant Coach','Volunteer');

/* ─────────  TEAMS  ────────────── */
INSERT INTO Team
        (team_id, team_name, personnel_id, captain_id, gender)
VALUES  (501,'Setters Squad',     4001,2011,'Mixed'),
        (502,'Libero Squad',      4002,2016,'Mixed'),
        (503,'OH Squad',          4003,2016,'Mixed'),
        (504,'Opposite Squad',    4004,2016,'Mixed'),
        (505,'Winners United',    4005,2021,'Mixed'),
        (506,'Challengers',       NULL,2026,'Mixed');     -- losing opponents

/* ───────  TEAM PLAYERS  ───────── */
INSERT INTO team_player (team_id, cm_id, `role`) VALUES
 -- setters-only group
 (501,2011,'setters'),(501,2012,'setters'),(501,2013,'setters'),
 (501,2014,'setters'),(501,2015,'setters'),

 -- multi-role players (each across 4 teams)
 (501,2016,'setters'),   (502,2016,'libero'), (503,2016,'outside_hitters'), (504,2016,'opposite_hitters'),
 (501,2017,'setters'),   (502,2017,'libero'), (503,2017,'outside_hitters'), (504,2017,'opposite_hitters'),
 (501,2018,'setters'),   (502,2018,'libero'), (503,2018,'outside_hitters'), (504,2018,'opposite_hitters'),
 (501,2019,'setters'),   (502,2019,'libero'), (503,2019,'outside_hitters'), (504,2019,'opposite_hitters'),
 (501,2020,'setters'),   (502,2020,'libero'), (503,2020,'outside_hitters'), (504,2020,'opposite_hitters'),

 -- undefeated players
 (505,2021,'middle_blocker'),(505,2022,'middle_blocker'),
 (505,2023,'middle_blocker'),(505,2024,'middle_blocker'),(505,2025,'middle_blocker'),

 -- losing-team opponents
 (506,2026,'middle_blocker'),(506,2027,'middle_blocker'),
 (506,2028,'middle_blocker'),(506,2029,'middle_blocker'),(506,2030,'middle_blocker');

/* ─────────  SESSIONS  ─────────── */
INSERT INTO Sessions
        (session_id, date, start_time, end_time, address)
VALUES  (601,'2025-07-01','18:00:00','20:00:00','123 Main St'),
        (602,'2025-07-05','18:00:00','20:00:00','123 Main St'),
        (603,'2025-07-10','18:00:00','20:00:00','123 Main St'),
        (604,'2025-07-15','18:00:00','20:00:00','123 Main St'),
        (605,'2025-07-20','18:00:00','20:00:00','123 Main St');

/* ───────  TEAM ↔ SESSION  ─────── */
INSERT INTO team_session (team_id, session_id, score) VALUES
 (501,601,25),
 (502,602,25),
 (503,603,25),
 (504,604,25),
 -- head-to-head match: winners vs challengers
 (505,605,30),   -- Winners United
 (506,605,20);   -- Challengers  (lost)

/* ───────  FAMILY ASSOCIATIONS  ── */
INSERT INTO family_association
        (fm_id, cm_id, relationship, start_date, end_date) VALUES
 /* parents of adult-now/minor-then members */
 (3001,2006,'Father','2020-01-01',NULL),(3002,2007,'Mother','2020-01-01',NULL),
 (3003,2008,'Father','2020-01-01',NULL),(3004,2009,'Mother','2020-01-01',NULL),
 (3005,2010,'Father','2020-01-01',NULL),

 /* same parents also linked to multi-role players → query 17 */
 (3001,2016,'Father','2015-01-01',NULL),(3002,2017,'Mother','2015-01-01',NULL),
 (3003,2018,'Father','2015-01-01',NULL),(3004,2019,'Mother','2015-01-01',NULL),
 (3005,2020,'Father','2015-01-01',NULL),

 /* minor volunteers linked to undefeated players → query 19 */
 (3006,2021,'Other','2024-06-01',NULL),(3007,2022,'Other','2024-06-01',NULL),
 (3008,2023,'Other','2024-06-01',NULL),(3009,2024,'Other','2024-06-01',NULL),
 (3010,2025,'Other','2024-06-01',NULL);
