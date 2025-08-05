host="localhost"  # e.g., "127.0.0.1" if not local
user="root"  # e.g., "root"
password=""  # e.g., "your_secure_password"
database=""  # e.g., "volleyball_club"

queries = [
#/*13. */
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
#/*14. */
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

#/*15.  */
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
#/*16. */
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

#/*17 */
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
#/* 18. */
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
#/*19.*/
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
"""


]
