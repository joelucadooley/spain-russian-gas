-- Spain's gas suppliers in 2025, largest first

SELECT country, SUM(gwh) AS total_gwh
FROM imports
WHERE date LIKE '2025%'
GROUP BY country
ORDER BY total_gwh DESC;
