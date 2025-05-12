-- Escriba una sentencia SQL que devuelva el listado de Category de la table Sales Data.
-- Forma sencilla
SELECT DISTINCT Category
FROM sales_data;

-- Con algo más de informacion
SELECT Category, 
	   SUM([Units Sold]) AS "Units Sold By Category"
FROM sales_data
GROUP BY Category
ORDER BY [Units Sold By Category] DESC;


-- Escriba una sentencia SQL que devuelva el total de Revenue del año.
-- Total por categoria
SELECT Category, 
	   SUM([Units Sold]) AS "Units Sold By Category",	
	   SUM([Unit Revenue]*[Units Sold]) AS "Total Revenue by Category"
FROM sales_data
GROUP BY Category
ORDER BY [Total Revenue by Category] DESC;

-- Total Revenue general
SELECT SUM([Unit Revenue]*[Units Sold]) AS "Total Revenue"
FROM sales_data;

-- Escriba una sentencia SQL que devuelva el total de Revenue por mes de cada categoría.

SELECT strftime('%Y-%m', Date) AS Month, 	
	   Category, SUM([Unit Revenue]*[Units Sold]) AS "Total Revenue by Month and Category"
FROM sales_data
GROUP BY Month, Category
ORDER BY Month, Category;

-- Escriba una sentencia SQL que devuelva las categorías cuyas ventas totales de un promedio de Revenue mayor a $500.000

WITH revenue_by_month AS (
    SELECT Category, strftime('%Y-%m', Date) AS Month, SUM([Unit Revenue]*[Units Sold]) AS "Total Revenue by Month and Category"
    FROM sales_data
    GROUP BY Category, Month
)

-- Opcion que veo mas logica
SELECT *
FROM revenue_by_month
WHERE [Total Revenue by Month and Category] > 500000; 

--Pense que habia algo mal aqui pero esta bien, todas superar el promedio de 500000
-- No tiene sentido que haga el promedio porque aqui las 5 categorias estarian entrando 
SELECT Category, AVG([Total Revenue by Month and Category]) AS "Average Monthly Revenue by Category"
FROM revenue_by_month
GROUP BY Category
HAVING "Average Monthly Revenue by Category" > 500000
ORDER BY "Average Monthly Revenue by Category" DESC;


-- Escriba una sentencia SQL que devuelva las localidades que no cuentan con clientes.

SELECT l.Location
FROM location l
LEFT JOIN customer_data c ON l.ID = c.id_Location
WHERE c.ID IS NULL;

-- Escriba una sentencia SQL que devuelva las provincias que no cuentan con clientes.

SELECT DISTINCT p.provincia
FROM provincia p
LEFT JOIN location l ON p.ID = l.id_provincia
LEFT JOIN customer_data c ON l.ID = c.id_Location
WHERE c.ID IS NULL;


-- Escriba una sentencia SQL las provincias con mayores clientes y cuantos por localidad.

SELECT 
    p.provincia,
    l.Location,
    COUNT(c.ID) AS "Numbers of Clients"
FROM customer_data c
JOIN location l ON c.id_Location = l.ID
JOIN provincia p ON l.id_provincia = p.ID
GROUP BY p.provincia, l.Location
ORDER BY [Numbers of Clients] DESC;


-- Escriba una sentencia SQL que muestre los clientes femeninos que su edad se encuentre entre 25 a 45 años y masculinos menores a 35. Se debe buscar el género mediante uso de subconsulta.

SELECT 
    c.ID,
    c.Age,
    g.Gender,
    c.id_Location,
    c.Segment
FROM customer_data c
JOIN gender g ON g.ID = c.id_Gender
WHERE (
    ((SELECT Gender FROM gender WHERE ID = c.id_Gender) = 'Female' AND c.Age BETWEEN 25 AND 45 )
    OR
    ((SELECT Gender FROM gender WHERE ID = c.id_Gender) = 'Male' AND c.Age < 35 )
);


-- Escriba una sentencia SQL que muestre los clientes que compraron en los últimos 3 meses y cuyo genero sea “otros” mediante subconsulta.
-- Ultimo cliente que hizo una compra para tener un punto de partida 
SELECT 
    ID,
    MAX([Last Purchase Date]) AS Ultima_Fecha_Compra
FROM 
    customer_data
ORDER BY 
    Ultima_Fecha_Compra DESC;


SELECT 
    c.ID,
    c.Age,
    g.Gender,
    c.[Last Purchase Date],
    c.Segment
FROM customer_data c
JOIN gender g ON g.ID = c.id_Gender
WHERE 
    c.[Last Purchase Date] >= DATE('2024-07-01', '-3 months')
    AND g.Gender = 'Other';
	
	
-- 	Escriba una sentencia SQL que muestre los clientes que compraron en los últimos 3 meses en las 3 provincias con mayores clientes.
SELECT 
    c.ID,
    c.Age,
    c.[Last Purchase Date],
    l.Location,
    p.provincia
FROM customer_data c
JOIN location l ON c.id_Location = l.ID
JOIN provincia p ON l.id_provincia = p.ID
WHERE 
    c.[Last Purchase Date] >= DATE('2024-07-01', '-3 months')
    AND p.provincia IN (
        SELECT p2.provincia
        FROM customer_data c2
        JOIN location l2 ON c2.id_Location = l2.ID
        JOIN provincia p2 ON l2.id_provincia = p2.ID
        GROUP BY p2.provincia
        ORDER BY COUNT(c2.ID) DESC
        LIMIT 3
    );

	
-- Escriba una sentencia SQL que muestre la información de cliente ID, edad, genero, localidad, provincia.
SELECT 
	c.ID,
	c.Age,
	g.gender,
	l.Location,
	p.provincia
FROM customer_data c
JOIN gender g ON c.id_gender = g.ID
JOIN location l ON c.id_location = l.ID
JOIN provincia p ON l.id_provincia = p.ID
ORDER BY c.ID;

-- Escriba una sentencia SQL que muestre la provincia, localidad y media de edad de manera ascendente

SELECT 
	l.Location,
	p.provincia,
	ROUND(AVG(c.Age),2) AS "Average Age by Location and Provincia"
FROM customer_data c
JOIN location l ON c.id_location = l.ID
JOIN provincia p ON l.id_provincia = p.ID
GROUP BY p.Provincia, l.Location
ORDER BY [Average Age by Location and Provincia];