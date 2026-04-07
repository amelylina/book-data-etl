DROP TABLE IF EXISTS summary;
CREATE TABLE summary AS
SELECT year,
	count(id) AS book_count,
	ROUND (
		AVG(
			CASE
				WHEN price LIKE '€%'
					THEN CAST(trim(price,'€') AS REAL) * 1.2
				ELSE CAST(trim(price,'$') AS REAL)
			END
		), 2) AS average_price
FROM books
GROUP BY year;