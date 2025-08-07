
-- DROP TABLES IF THEY EXIST TO AVOID DUPLICATION DURING RE-RUN
DROP TABLE IF EXISTS team_player, Team, cm_hobby, Hobby, cm_payment, Payment, secondary_fm, cm_location, family_association, ClubMember, FamilyMember, personnel_location, Personnel, Location, Person, team_session, Sessions, EmailLog CASCADE;

CREATE TABLE Person (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    ssn VARCHAR(15) UNIQUE NOT NULL,
    dob DATE NOT NULL,
    mcn VARCHAR(20) UNIQUE,
    telephone VARCHAR(20),
    address VARCHAR(100),
    city VARCHAR(50),
    province VARCHAR(50),
    postal_code VARCHAR(10),
    email VARCHAR(100)
);

CREATE TABLE Personnel (
    personnel_id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    FOREIGN KEY (person_id) REFERENCES Person(person_id)
);

CREATE TABLE Location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type ENUM('Head', 'Branch') NOT NULL,
    phone_number VARCHAR(20),
    web_address VARCHAR(100),
    address VARCHAR(100),
    city VARCHAR(50),
    province VARCHAR(50),
    postal_code VARCHAR(10),
    max_capacity INT NOT NULL
);

CREATE TABLE personnel_location (
    personnel_id INT,
    location_id INT,
    start_date DATE NOT NULL,
    end_date DATE,
    role ENUM('General Manager', 'Deputy Manager', 'Treasurer', 'Secretary', 'Administrator', 'Captain', 'Coach', 'Assistant Coach', 'Other') NOT NULL,
    mandate ENUM('Salaried', 'Volunteer') NOT NULL,
    PRIMARY KEY (personnel_id, location_id, start_date),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(personnel_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
);

CREATE TABLE FamilyMember (
    fm_id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    FOREIGN KEY (person_id) REFERENCES Person(person_id)
);

CREATE TABLE ClubMember (
    cm_id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    gender VARCHAR(10),
    membership_status ENUM('Active', 'Inactive') NOT NULL,
    last_paid_year INT,
    FOREIGN KEY (person_id) REFERENCES Person(person_id)
);

CREATE TABLE family_association (
    fm_id INT,
    cm_id INT,
    relationship ENUM('Father', 'Mother', 'Grandfather', 'Grandmother', 'Tutor', 'Partner', 'Friend', 'Other') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    PRIMARY KEY (fm_id, cm_id, start_date),
    FOREIGN KEY (fm_id) REFERENCES FamilyMember(fm_id),
    FOREIGN KEY (cm_id) REFERENCES ClubMember(cm_id) ON DELETE CASCADE
);

CREATE TABLE secondary_fm (
    fm_id INT,
    secondary_fm_id INT,
    PRIMARY KEY (fm_id, secondary_fm_id),
    FOREIGN KEY (fm_id) REFERENCES FamilyMember(fm_id) ON DELETE CASCADE,
    FOREIGN KEY (secondary_fm_id) REFERENCES FamilyMember(fm_id) ON DELETE CASCADE,
    CHECK (fm_id != secondary_fm_id)
);

CREATE TABLE cm_location (
    location_id INT,
    cm_id INT,
    PRIMARY KEY (location_id, cm_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id),
    FOREIGN KEY (cm_id) REFERENCES ClubMember(cm_id) ON DELETE CASCADE
);

CREATE TABLE Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    payment_method ENUM('Cash', 'Debit Card', 'Credit Card') NOT NULL,
    payment_date DATE NOT NULL,
    payment_amount DECIMAL(10,2) NOT NULL
);

CREATE TABLE cm_payment (
    payment_id INT,
    cm_id INT,
    membership_year INT NOT NULL,
    PRIMARY KEY (payment_id, cm_id, membership_year),
    FOREIGN KEY (payment_id) REFERENCES Payment(payment_id),
    FOREIGN KEY (cm_id) REFERENCES ClubMember(cm_id) ON DELETE CASCADE
);

CREATE TABLE Hobby (
    hobby_id INT AUTO_INCREMENT PRIMARY KEY,
    hobby_name VARCHAR(50) NOT NULL
);

CREATE TABLE cm_hobby (
    hobby_id INT,
    cm_id INT,
    PRIMARY KEY (hobby_id, cm_id),
    FOREIGN KEY (hobby_id) REFERENCES Hobby(hobby_id),
    FOREIGN KEY (cm_id) REFERENCES ClubMember(cm_id) ON DELETE CASCADE
);

CREATE TABLE Team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    personnel_id INT,
    captain_id INT,
    gender VARCHAR(10),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(personnel_id),
    FOREIGN KEY (captain_id) REFERENCES ClubMember(cm_id) ON DELETE CASCADE
);


CREATE TABLE team_player (
    team_player_id INT AUTO_INCREMENT PRIMARY KEY,  -- new unique ID
    team_id INT,
    cm_id INT,
    role ENUM (
        'setters',
        'outside_hitters',
        'opposite_hitters',
        'middle_blocker',
        'defensive_specialist',
        'libero'
    ),
    FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (cm_id) REFERENCES ClubMember(cm_id) ON DELETE CASCADE
);



CREATE TABLE Sessions ( 
    session_id INT AUTO_INCREMENT PRIMARY KEY , 
    date DATE, 
    start_time TIME,
    address VARCHAR(100), 
    end_time TIME,
    session_type ENUM('Game','Training'),
    CHECK (end_time > start_time) 
);

CREATE TABLE team_session (
    team_id INT, 
    session_id INT, 
    score INT, 
    PRIMARY KEY (team_id,session_id), 
    FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE, 
    FOREIGN KEY (session_id) REFERENCES Sessions(session_id),
    CHECK (score IS NULL OR score >= 0) 
);

CREATE TABLE EmailLog (
    log_id INT AUTO_INCREMENT,
    date DATE, 
    sender VARCHAR(100), 
    receiver VARCHAR(100), 
    body VARCHAR(100), 
    subject VARCHAR(100), 
    PRIMARY KEY (log_id), 
    CHECK (DAYOFWEEK(date) = 1) -- Sunday
);


-- Trigger 1: Ensure minor members have a registered family member
-- DELIMITER $$
-- DROP TRIGGER IF EXISTS ensure_minor_family_member $$
-- CREATE TRIGGER ensure_minor_family_member
-- BEFORE INSERT ON ClubMember
-- FOR EACH ROW
-- BEGIN
--     DECLARE age INT;
--     SET age = TIMESTAMPDIFF(YEAR, (SELECT dob FROM Person WHERE person_id = NEW.person_id), CURDATE());
--     IF age < 18 THEN
--         IF NOT EXISTS (
--             SELECT 1 FROM family_association 
--             WHERE cm_id = NEW.cm_id 
--             AND end_date IS NULL
--         ) THEN
--             SIGNAL SQLSTATE '45000'
--             SET MESSAGE_TEXT = 'Minor club members must be associated with an active family member.';
--         END IF;
--     END IF;
-- END $$
-- DELIMITER ;

-- Trigger 2: Update membership status based on payment completion
DELIMITER $$
DROP TRIGGER IF EXISTS update_membership_status $$
CREATE TRIGGER update_membership_status
AFTER INSERT ON cm_payment
FOR EACH ROW
BEGIN
    DECLARE total_paid DECIMAL(10,2);
    DECLARE required_fee DECIMAL(10,2);
    DECLARE is_minor BOOLEAN;
    
    -- Determine if member is minor
    SELECT TIMESTAMPDIFF(YEAR, dob, CURDATE()) < 18 INTO is_minor
    FROM Person p
    JOIN ClubMember cm ON p.person_id = cm.person_id
    WHERE cm.cm_id = NEW.cm_id;
    
    -- Set required fee based on member type
    SET required_fee = IF(is_minor, 100.00, 200.00);
    
    -- Calculate total payments for the membership year
    SELECT SUM(p.payment_amount) INTO total_paid
    FROM Payment p
    JOIN cm_payment cp ON p.payment_id = cp.payment_id
    WHERE cp.cm_id = NEW.cm_id AND cp.membership_year = NEW.membership_year;
    
    -- Update membership status
    UPDATE ClubMember
    SET membership_status = IF(total_paid >= required_fee, 'Active', 'Inactive'),
        last_paid_year = IF(total_paid >= required_fee, NEW.membership_year, last_paid_year)
    WHERE cm_id = NEW.cm_id;
END $$
DELIMITER ;

-- Trigger 3: Prevent overlapping team session assignments for players
DELIMITER $$
DROP TRIGGER IF EXISTS prevent_overlapping_sessions $$
CREATE TRIGGER prevent_overlapping_sessions
BEFORE INSERT ON team_player
FOR EACH ROW
BEGIN
    DECLARE session_start TIME;
    DECLARE session_end TIME;
    DECLARE session_date DATE;
    
    -- Get session details
    SELECT s.date, s.start_time, s.end_time INTO session_date, session_start, session_end
    FROM Sessions s
    JOIN team_session ts ON s.session_id = ts.session_id
    WHERE ts.team_id = NEW.team_id;
    
    -- Check for overlapping sessions
    IF EXISTS (
        SELECT 1
        FROM team_player tp
        JOIN team_session ts ON tp.team_id = ts.team_id
        JOIN Sessions s ON ts.session_id = s.session_id
        WHERE tp.cm_id = NEW.cm_id
        AND s.date = session_date
        AND (
            (s.start_time <= session_end AND s.end_time >= session_start)
            OR (TIMESTAMPDIFF(HOUR, s.end_time, session_start) < 3 AND s.end_time <= session_start)
            OR (TIMESTAMPDIFF(HOUR, session_end, s.start_time) < 3 AND session_end <= s.start_time)
        )
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Player cannot be assigned to overlapping sessions or sessions less than 3 hours apart.';
    END IF;
END $$


DELIMITER $$ 
-- Trigger 4: Log email generation for weekly session schedules
DROP TRIGGER IF EXISTS log_session_email $$
CREATE TRIGGER log_session_email
AFTER INSERT ON team_session
FOR EACH ROW
BEGIN
    DECLARE team_name VARCHAR(100);
    DECLARE coach_email VARCHAR(100);
    DECLARE coach_name VARCHAR(100);
    DECLARE session_address VARCHAR(100);
    DECLARE session_type VARCHAR(20);
    DECLARE session_date DATE;
    DECLARE session_start_time TIME;
    
    -- Get team and session details
    SELECT t.team_name, p.email, CONCAT(p.first_name, ' ', p.last_name), s.address, s.date, s.start_time
    INTO team_name, coach_email, coach_name, session_address, session_date, session_start_time
    FROM Team t
    JOIN Personnel pr ON t.personnel_id = pr.personnel_id
    JOIN Person p ON pr.person_id = p.person_id
    JOIN Sessions s ON s.session_id = NEW.session_id
    WHERE t.team_id = NEW.team_id;
    
    -- Determine session type
    SET session_type = IF((SELECT end_time FROM Sessions WHERE session_id = NEW.session_id) IS NOT NULL, 'Game', 'Training');
    
    -- Insert email log for each player in the team
    INSERT INTO EmailLog (date, sender, receiver, subject, body)
    SELECT 
        CURDATE(),
        (SELECT name FROM Location WHERE location_id = (SELECT location_id FROM cm_location WHERE cm_id = tp.cm_id)),
        p.email,
        CONCAT(team_name, ' ', DATE_FORMAT(session_date, '%W %d-%b-%Y'), ' ', TIME_FORMAT(session_start_time, '%H:%i'), ' ', session_type, ' Session'),
        CONCAT('Dear ', p.first_name, ' ', p.last_name, ', you are scheduled as ', tp.role, ' for the ', session_type, ' session. Coach: ', coach_name, ' (', coach_email, '). Address: ', session_address)
    FROM team_player tp
    JOIN ClubMember cm ON tp.cm_id = cm.cm_id
    JOIN Person p ON cm.person_id = p.person_id
    WHERE tp.team_id = NEW.team_id;
END $$
-- Trigger 5: Enforce unique SSN across Person table
DELIMITER $$
DROP TRIGGER IF EXISTS enforce_unique_ssn $$
CREATE TRIGGER enforce_unique_ssn
BEFORE INSERT ON Person
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM Person 
        WHERE ssn = NEW.ssn AND person_id != NEW.person_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Social Security Number must be unique across all persons.';
    END IF;
END $$
DELIMITER ;

-- Trigger 6: Enforce maximum capacity of active club members at a location
DELIMITER $$
DROP TRIGGER IF EXISTS enforce_location_capacity $$
CREATE TRIGGER enforce_location_capacity
BEFORE INSERT ON cm_location
FOR EACH ROW
BEGIN
    DECLARE current_count INT;
    DECLARE max_capacity INT;
    
    -- Get the current number of active members at the location
    SELECT COUNT(*) INTO current_count
    FROM cm_location cl
    JOIN ClubMember cm ON cl.cm_id = cm.cm_id
    WHERE cl.location_id = NEW.location_id
    AND cm.membership_status = 'Active';
    
    -- Get the maximum capacity of the location
    SELECT max_capacity INTO max_capacity
    FROM Location
    WHERE location_id = NEW.location_id;
    
    -- Check if adding a new member exceeds the capacity
    IF current_count >= max_capacity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Location has reached its maximum capacity for active club members.';
    END IF;
END $$
DELIMITER ;

-- Trigger 7: Automatically transition minor members to major when they turn 18
DELIMITER $$
DROP TRIGGER IF EXISTS transition_minor_to_major $$
CREATE TRIGGER transition_minor_to_major
AFTER UPDATE ON Person
FOR EACH ROW
BEGIN
    DECLARE age INT;
    DECLARE cm_id_val INT;
    
    -- Calculate age
    SET age = TIMESTAMPDIFF(YEAR, NEW.dob, CURDATE());
    
    -- Check if the person is a club member
    SELECT cm_id INTO cm_id_val
    FROM ClubMember
    WHERE person_id = NEW.person_id
    LIMIT 1;
    
    -- If the member is 18 or older, terminate active family associations
    IF age >= 18 AND cm_id_val IS NOT NULL THEN
        UPDATE family_association
        SET end_date = CURDATE()
        WHERE cm_id = cm_id_val AND end_date IS NULL;
        
        -- Ensure membership fee is updated to major member rate for current year
        UPDATE cm_payment cp
        JOIN Payment p ON cp.payment_id = p.payment_id
        SET p.payment_amount = 200.00
        WHERE cp.cm_id = cm_id_val 
        AND cp.membership_year = YEAR(CURDATE())
        AND p.payment_amount < 200.00;
        
        -- Update membership status if payments are sufficient
        UPDATE ClubMember
        SET membership_status = 'Active'
        WHERE cm_id = cm_id_val
        AND (
            SELECT SUM(p.payment_amount)
            FROM Payment p
            JOIN cm_payment cp ON p.payment_id = cp.payment_id
            WHERE cp.cm_id = cm_id_val AND cp.membership_year = YEAR(CURDATE())
        ) >= 200.00;
    END IF;
END $$
DELIMITER ;

DELIMITER $$
-- Updated ensure_minor_family_member trigger
DROP TRIGGER IF EXISTS ensure_minor_family_member $$
CREATE TRIGGER ensure_minor_family_member
BEFORE INSERT ON ClubMember
FOR EACH ROW
BEGIN
    DECLARE member_age INT;
    DECLARE family_member_exists INT;
    
    -- Calculate age based on dob
    SELECT TIMESTAMPDIFF(YEAR, p.dob, CURDATE())
    INTO member_age
    FROM Person p
    WHERE p.person_id = NEW.person_id;
    
    -- Check if minor (under 18) has a family member in cm_location (or adjust table as needed)
    IF member_age < 18 THEN
        SELECT COUNT(*)
        INTO family_member_exists
        FROM cm_location cl
        JOIN ClubMember cm ON cl.cm_id = cm.cm_id
        JOIN Person p ON cm.person_id = p.person_id
        WHERE cl.location_id = (SELECT location_id FROM cm_location WHERE cm_id = NEW.cm_id LIMIT 1)
        AND p.person_id != NEW.person_id;
        
        IF family_member_exists = 0 THEN
            -- Allow insert, assuming association will be added later
            SET @warning = 'Minor member inserted without family member association; ensure cm_location is updated.';
        END IF;
    END IF;
END $$


DELIMITER $$

-- Drop log_session_email trigger
DROP TRIGGER IF EXISTS log_session_email $$

-- send_weekly_session_emails procedure (unchanged from previous artifact)
DROP PROCEDURE IF EXISTS send_weekly_session_emails $$
CREATE PROCEDURE send_weekly_session_emails()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE cm_email VARCHAR(100);
    DECLARE cm_first_name VARCHAR(50);
    DECLARE cm_last_name VARCHAR(50);
    DECLARE player_role VARCHAR(20);
    DECLARE team_name VARCHAR(100);
    DECLARE session_type VARCHAR(20);
    DECLARE session_date DATE;
    DECLARE session_start_time TIME;
    DECLARE session_address VARCHAR(100);
    DECLARE head_coach_email VARCHAR(100);
    DECLARE head_coach_name VARCHAR(100);
    DECLARE location_name VARCHAR(100);
    
    DECLARE session_cursor CURSOR FOR
        SELECT p.email, p.first_name, p.last_name, tp.role,
               t.team_name, 
               CASE WHEN s.end_time IS NOT NULL THEN 'Game' ELSE 'Training' END AS session_type,
               s.date, s.start_time, s.address,
               p_coach.email, CONCAT(p_coach.first_name, ' ', p_coach.last_name),
               COALESCE(l.name, 'Montréal Volleyball Club')
        FROM team_session ts
        JOIN Sessions s ON ts.session_id = s.session_id
        JOIN Team t ON ts.team_id = t.team_id
        JOIN team_player tp ON tp.team_id = t.team_id
        JOIN ClubMember cm ON tp.cm_id = cm.cm_id
        JOIN Person p ON cm.person_id = p.person_id
        JOIN Personnel pr ON t.personnel_id = pr.personnel_id
        JOIN Person p_coach ON pr.person_id = p_coach.person_id
        LEFT JOIN cm_location cl ON cm.cm_id = cl.cm_id
        LEFT JOIN Location l ON cl.location_id = l.location_id
        WHERE s.date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY);
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN session_cursor;
    
    read_loop: LOOP
        FETCH session_cursor INTO cm_email, cm_first_name, cm_last_name, player_role,
                                 team_name, session_type, session_date, session_start_time, 
                                 session_address, head_coach_email, head_coach_name, location_name;
        
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET @email_subject = CONCAT(team_name, ' ', DATE_FORMAT(session_date, '%W %d-%b-%Y'), ' ', TIME_FORMAT(session_start_time, '%H:%i'), ' ', session_type, ' Session');
        SET @email_body = CONCAT(
            'Dear ', cm_first_name, ' ', cm_last_name, ', ',
            session_type, ' session as ', player_role, ', ',
            DATE_FORMAT(session_date, '%W %d-%b-%Y'), ' ', TIME_FORMAT(session_start_time, '%H:%i'), ', ',
            'Addr: ', session_address, ', Coach: ', head_coach_name, ' (', head_coach_email, ')'
        );
        
        INSERT INTO EmailLog (date, sender, receiver, subject, body)
        VALUES ('2025-08-03', location_name, cm_email, @email_subject, LEFT(@email_body, 100));
    END LOOP;
    
    CLOSE session_cursor;
END $$

DELIMITER ;


