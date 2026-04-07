CREATE TABLE IF NOT EXISTS summary AS
SELECT year,
	count(id) AS count,
	ROUND (
		AVG(
			CASE
				WHEN price LIKE '€%'
					THEN CAST(trim(price,'€') AS REAL) * 1.2
				ELSE CAST(trim(price,'$') AS REAL)
			END
		), 2) AS avg_price_usd
FROM books
GROUP BY year;