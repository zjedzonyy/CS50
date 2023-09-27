SELECT DISTINCT name FROM people, stars
WHERE people.id = stars.person_id
AND stars.movie_id in
(SELECT movie_id FROM stars, people
WHERE stars.person_id = people.id
AND people.name = "Kevin Bacon"
AND people.birth = 1958)
AND people.name != "Kevin Bacon";
