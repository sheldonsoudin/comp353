host = "gtc353.encs.concordia.ca"  # e.g., "127.0.0.1" if not local
user = "gtc353_1"  # e.g., "root"
password = "Wahh1234"  # e.g., "your_secure_password"
database = "gtc353_1"  # e.g., "volleyball_club"

# Add your queries here and please label them question wise
queries = [
    "SELECT * FROM ClubMember",  # Question number 1
    "",  # Question number 2
    "",  # Question number 2
    "",  # Question number 2
    "",  # Question number 2
    "",  # Question number 2
    "",  # Question number 2
    # 8
    # used gemini
    """
        
        with 
        table1 as 
        ( 
            SELECT Location.location_id, 
            Location.address, 
            Location.city, 
            Location.province, 
            Location.postal_code, 
            Location.phone_number, 
            Location.web_address, 
            Location.type, 
             Location.max_capacity 
            FROM Location 
        ), 
        table2 as 
        ( 
            SELECT personnel_location.location_id,
            Person.first_name,
            Person.last_name 
            FROM personnel_location , Person , Personnel , Location 
            WHERE personnel_location.location_id = Location.location_id 
            AND Person.person_id = Personnel.person_id 
            AND personnel_location.personnel_id = Personnel.personnel_id 
            AND personnel_location.role = 'General Manager' 
        ), 
        table3 as (
            SELECT cm_location.location_id, COUNT(ClubMember.cm_id) AS Major FROM cm_location , ClubMember , Person 
            WHERE cm_location.cm_id = ClubMember.cm_id 
            AND Person.person_id = ClubMember.person_id 
            AND TIMESTAMPDIFF(YEAR, Person.dob, CURDATE()) >= 18 GROUP BY location_id 
        ),
        table4 as (
            SELECT cm_location.location_id, 
            COUNT(ClubMember.cm_id) AS MINOR FROM cm_location ,
            ClubMember ,
            Person 
            WHERE cm_location.cm_id = ClubMember.cm_id 
            AND Person.person_id = ClubMember.person_id 
            AND TIMESTAMPDIFF(YEAR, Person.dob, CURDATE()) < 18 GROUP BY location_id 
        ), 
        table5 as ( 
                   SELECT Location.location_id, 
                   Team.team_name FROM Team ,
                   Location,team_session,
                   Sessions 
                   WHERE team_session.team_id = Team.team_id 
                   and team_session.session_id = Sessions.session_id 
                   and Sessions.address = Location.address 
        )
        select table1.location_id,
        	table1.address,
        	table1.city,
        	table1.province,
        	table1.postal_code,
        	table1.phone_number,
        	table1.web_address,
        	table1.type,
        	table1.max_capacity,
        	table2.first_name,
        	table2.last_name,
        	table3.Major,
        	table4.Minor,
        	table5.team_name 
        FROM Location 
        	left JOIN table1 ON Location.location_id = table1.location_id 
       		left JOIN table2 ON Location.location_id = table2.location_id 
        	left JOIN table3 ON Location.location_id = table3.location_id 
        	left JOIN table4 ON Location.location_id = table4.location_id 
        	left JOIN table5 ON Location.location_id = table5.location_id 
        order by Province asc, city asc


    """,
    # 9
    """

	with 
	table1 as (  

    	select FamilyMember.fm_id,
    		Person.first_name,
    		Person.last_name,
    		Person.telephone FROM FamilyMember,
    		family_association,
    		secondary_fm,
    		Person 
    	WHERE FamilyMember.fm_id = 1 
    		AND FamilyMember.fm_id = family_association.fm_id 
    		AND FamilyMember.fm_id = secondary_fm.fm_id 
    		AND Person.person_id = FamilyMember.person_id  

	),  

	table2 as (  

    	select FamilyMember.fm_id,
   		ClubMember.cm_id,
    		Person.first_name,
    		Person.last_name,
    		Person.dob,
    		Person.ssn,
    		Person.mcn,
    		Person.telephone ,
    		Person.address,
    		Person.city,
    		Person.province,
    		Person.postal_code,
    		family_association.relationship 
    	from family_association, FamilyMember, Person, ClubMember 
    	where Person.person_id= ClubMember.person_id 
    		and FamilyMember.fm_id = family_association.fm_id 
    		and ClubMember.cm_id = family_association.cm_id 
    		and FamilyMember.fm_id = 1 
    		and family_association.fm_id = 1  

	) 

	select table1.first_name as secondaryfirstname,
		table1.last_name as secondarylasttname,
		table1.telephone as secondarytelephone,
		table2.cm_id as associateid,
		table2.first_name as associatefirsname,
		table2.last_name as associatelastname,
		table2.dob as associatedob,
		table2.ssn as associatessn,
		table2.mcn as associatemcn,
		table2.telephone as associate,
		table2.address,
		table2.city,
		table2.province,
		table2.postal_code,
		table2.relationship 
	FROM table1 ,table2 
	WHERE table1.fm_id = table2.fm_id; 




	""",
    # 10
    """
with table1 as (  

    select Sessions.session_id,
    Person.first_name as Coachfirsname,
    Person.last_name as coachlastname,
    Sessions.start_time,
    Sessions.address,
    Team.team_name,
    team_session.score 
    from Sessions,
    team_session,
    Team,
    ClubMember,
    Person 
    where 
    Sessions.address = '123 Main St, Montreal'
    and Sessions.date between '2025-07-01' and '2025-10-30' 
    and Sessions.session_id = team_session.session_id 
    and Sessions.session_id = Team.team_id 
    and Team.captain_id = ClubMember.cm_id 
    and ClubMember.person_id = Person.person_id 

), table2 as(  

    select Sessions.session_id,
    Person.first_name as playerfirstname,
    Person.last_name as playerlastname,
    team_player.role from Sessions,
    team_session,
    Team,
    team_player,
    Person,
    ClubMember 
    where Sessions.address = '123 Main St, Montreal' 
    and Sessions.date between '2025-07-01' and '2025-10-30' 
    and team_session.team_id = Team.team_id
    and team_session.session_id = Sessions.session_id 
    and team_player.cm_id = ClubMember.cm_id 
    and team_player.team_id = Team.team_id 
    and ClubMember.person_id = Person.person_id 
    )  

select table1.session_id,
	table1.Coachfirsname,
	table1.coachlastname,
	table1.start_time,
	table1.address,
	table1.team_name,
	table1.score,
	table2.playerfirstname,
	table2.playerlastname,
	table2.role from table1,
	table2 
where table1.session_id = table2.session_id 
order by start_time asc 
    """,  
    # 11
    """
        select ClubMember.cm_id,
        	Person.first_name,
       		Person.last_name from ClubMember,
        	cm_location,
        	Location,
        	cm_payment,
        	Person 
        where ClubMember.membership_status = 'Inactive' 
        	and cm_location.cm_id = ClubMember.cm_id 
        	and cm_location.location_id = Location.location_id 
        	and cm_payment.cm_id = ClubMember.cm_id 
        	and ClubMember.person_id = Person.person_id 
        group by ClubMember.cm_id 
        having count(cm_location.cm_id) >= 2 and count(cm_payment.membership_year) >= 2 
        order by ClubMember.cm_id asc
    """,
    # 12
    """
	with 
	table1 as 
	( 

	select Location.name,
		count(distinct(Sessions.session_id)) as numberoftrainingsession,
		count(distinct(team_player.cm_id)) as numberofplayerstrainingsession from Sessions, 
		Location,
		team_session,
		Team,
		team_player 
	where Sessions.date between '2025-06-01' and '2025-09-01' 
		and (Sessions.address = concat(Location.address, ', ', Location.city) or Sessions.address = Location.address) 
		and Team.team_id = team_session.team_id 
		and team_session.session_id = Sessions.session_id 
		and Team.team_id = team_player.team_id 
		and team_player.team_id = Team.team_id 
		and Sessions.session_type = 'Training' 
	group by Location.name

 	), 
	table2 as 

	(

	select Location.name,
		count(distinct(Sessions.session_id)) as numberofgamesession,
		count(distinct(team_player.cm_id)) as numberofplayersgamesession from Sessions,
		Location,
		team_session,
		Team,
		team_player 
	where Sessions.date between '2025-06-01' and '2025-09-01' 
		and (Sessions.address = concat(Location.address, ', ', Location.city) or Sessions.address = Location.address) 
		and Team.team_id = team_session.team_id 
		and team_session.session_id = Sessions.session_id 
		and Team.team_id = team_player.team_id 
		and team_player.team_id = Team.team_id 
		and Sessions.session_type = 'Game' group by Location.name 

	)

	select * from table1,
	table2 
	where table1.name = table2.name 
	order by numberofgamesession desc 

    """,
    # /*13. */
    """
SELECT DISTINCT  
	ClubMember.cm_id,
	Person.first_name, 
	Person.last_name, 
	TIMESTAMPDIFF(YEAR, Person.dob, CURDATE()) AS age,
	Person.telephone, 
	Person.email,
	Location.name
FROM Person 
	JOIN ClubMember ON Person.person_id = ClubMember.person_id
	JOIN cm_location ON ClubMember.cm_id = cm_location.cm_id
	JOIN Location ON cm_location.location_id = Location.location_id
	LEFT JOIN team_player ON ClubMember.cm_id = team_player.cm_id
	LEFT JOIN team_session ON team_player.team_id = team_session.team_id 
WHERE team_session.team_id IS NULL AND ClubMember.membership_status = 'Active'
ORDER BY Location.name ASC, age;
""",
    # /*14. */
    """
SELECT DISTINCT  
	ClubMember.cm_id,
	Person.first_name, 
	Person.last_name, 
	family_association.start_date,
	TIMESTAMPDIFF(YEAR, Person.dob, CURDATE()) AS age,
	Person.telephone, 
	Person.email,
	Location.name
FROM Person 
	JOIN ClubMember ON Person.person_id = ClubMember.person_id
	JOIN cm_location ON ClubMember.cm_id = cm_location.cm_id
        JOIN Location ON cm_location.location_id = Location.location_id
	JOIN family_association on ClubMember.cm_id = family_association.cm_id
WHERE TIMESTAMPDIFF(YEAR, Person.dob, CURDATE())>= 18 AND TIMESTAMPDIFF(YEAR, Person.dob, family_association.start_date) < 18 AND ClubMember.membership_status = 'Active'  
ORDER BY Location.name ASC, age;
""",
    # /*15.  */
    """
SELECT DISTINCT  
	ClubMember.cm_id,
	Person.first_name, 
	Person.last_name, 
	TIMESTAMPDIFF(YEAR, Person.dob, CURDATE()) as age,
	Person.telephone, 
	Person.email,
	Location.name
FROM Person 
	JOIN ClubMember ON Person.person_id = ClubMember.person_id
	JOIN cm_location ON ClubMember.cm_id = cm_location.cm_id
        JOIN Location ON cm_location.location_id = Location.location_id
	JOIN team_player ON ClubMember.cm_id = team_player.cm_id
	JOIN team_session ON team_player.team_id = team_session.team_id 
WHERE ClubMember.membership_status = 'Active'
	AND ClubMember.cm_id IN (SELECT cm_id FROM team_player WHERE role = 'setter')
	AND ClubMember.cm_id NOT IN (SELECT cm_id FROM team_player WHERE role != 'setter')
ORDER BY Location.name ASC, ClubMember.cm_id;
""",
    # /*16. */
    """
SELECT DISTINCT  
	ClubMember.cm_id,
	Person.first_name, 
	Person.last_name, 
	TIMESTAMPDIFF(YEAR, Person.dob, CURDATE()) as age,
	Person.telephone, 
	Person.email,
	Location.name
FROM Person 
	JOIN ClubMember ON Person.person_id = ClubMember.person_id
	JOIN cm_location ON ClubMember.cm_id = cm_location.cm_id
        JOIN Location ON cm_location.location_id = Location.location_id
	JOIN team_player ON ClubMember.cm_id = team_player.cm_id
	JOIN team_session ON team_player.team_id = team_session.team_id 
WHERE ClubMember.membership_status = 'Active'
	AND ClubMember.cm_id IN (SELECT cm_id FROM team_player WHERE role = 'setters')
	AND ClubMember.cm_id IN (SELECT cm_id FROM team_player WHERE role = 'libero')
	AND ClubMember.cm_id IN (SELECT cm_id FROM team_player WHERE role = 'outside_hitters')
	AND ClubMember.cm_id IN (SELECT cm_id FROM team_player WHERE role = 'opposite_hitters')
ORDER BY Location.name ASC, ClubMember.cm_id;
        """,
    # /*17 */
    """
SELECT DISTINCT
	Person.first_name,
	Person.last_name, 
	Person.telephone
FROM Person
	JOIN FamilyMember ON Person.person_id = FamilyMember.person_id
	JOIN Personnel ON Person.person_id = Personnel.person_id 
	JOIN personnel_location ON Personnel.personnel_id = personnel_location.personnel_id 
	JOIN family_association on FamilyMember.fm_id  = family_association.fm_id
	JOIN ClubMember ON family_association.cm_id = ClubMember.cm_id
	JOIN cm_location ON ClubMember.cm_id = cm_location.cm_id
WHERE ClubMember.membership_status = 'Active'
	AND cm_location.location_id = personnel_location.location_id
	AND personnel_location.role = 'Coach'
	AND Personnel.personnel_id IN (
		SELECT Personnel.personnel_id  
		FROM Personnel 
		JOIN Team ON Personnel.personnel_id = Team.personnel_id 
		JOIN team_session ON Team.team_id = team_session.team_id );
""",
    # /* 18. */
    """
SELECT DISTINCT 
	cm.cm_id, 
	Person.first_name,
	Person.last_name, 
	TIMESTAMPDIFF(YEAR, Person.dob, CURDATE()) as age,
	Person.telephone,
	Person.email,
	Location.name
FROM Person 
	JOIN ClubMember AS cm ON Person.person_id = cm.person_id
	JOIN cm_location ON cm.cm_id = cm_location.cm_id
        JOIN Location ON cm_location.location_id = Location.location_id
	JOIN team_player ON cm.cm_id = team_player.cm_id
	JOIN team_session ON team_player.team_id = team_session.team_id 
WHERE cm.membership_status = 'Active'
	AND cm.cm_id NOT IN (
		SELECT cm2.cm_id
		FROM ClubMember AS cm2
			JOIN team_player as tp2 ON cm2.cm_id = tp2.cm_id
			JOIN team_session as tp2Team ON tp2.team_id = tp2Team.team_id 
			JOIN team_session as otherTeam ON tp2Team.session_id = otherTeam.session_id 
				AND tp2Team.team_id != otherTeam.team_id 
		WHERE tp2Team.score < otherTeam.score)
ORDER BY Location.name ASC, cm.cm_id;
""",
    # /*19.*/
    """
SELECT DISTINCT  
	Person.first_name,
	Person.last_name, 
	COUNT(family_association.cm_id),
	Person.telephone, 
	Person.email,
	Location.name, 
	personnel_location.role
FROM Person
	JOIN FamilyMember ON Person.person_id = FamilyMember.person_id
	JOIN Personnel ON Person.person_id = Personnel.person_id 
	JOIN personnel_location ON Personnel.personnel_id = personnel_location.personnel_id 
        JOIN Location ON personnel_location.location_id = Location.location_id
	JOIN family_association on FamilyMember.fm_id  = family_association.fm_id
WHERE mandate = 'Volunteer' AND TIMESTAMPDIFF(YEAR, Person.dob, CURDATE()) < 18
GROUP BY
	Person.first_name,
	Person.last_name, 
	Person.telephone, 
	Person.email,
	Location.name, 
	personnel_location.role
HAVING COUNT(family_association.fm_id) >= 1
ORDER BY Location.name ASC, personnel_location.role, Person.first_name, Person.last_name; 
""",
]
