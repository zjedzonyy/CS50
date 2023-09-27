SELECT title FROM movies, stars, people
WHERE movies.id = stars.movie_id
AND stars.person_id = people.id
AND people.name = "Bradley Cooper"
AND title IN
(SELECT title FROM movies, stars, people
WHERE movies.id = stars.movie_id
AND stars.person_id = people.id
AND people.name = "Jennifer Lawrence");

