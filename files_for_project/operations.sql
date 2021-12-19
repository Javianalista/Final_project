USE final_project;

SELECT *
FROM final_project.ratings;


SELECT ROUND(AVG(rating), 2) AS people_rating, COUNT(movieId) AS number_of_votes
FROM final_project.movies m 
LEFT JOIN final_project.ratings r USING (movieID)
GROUP BY movieId
ORDER BY movieId ASC;