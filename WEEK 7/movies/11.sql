SELECT title from movies, stars, people, ratings
WHERE movies.id = stars.movie_id
AND stars.person_id = people.id
AND people.name = "Chadwick Boseman"
AND stars.movie_id = ratings.movie_id
ORDER BY ratings.rating DESC
LIMIT 5;