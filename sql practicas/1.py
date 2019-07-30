CREATE TABLE customer (
	id serial PRIMARY KEY,  /*CustomerID*/
	CustomerName  VARCHAR (50) NOT NULL,
	City VARCHAR (20) NOT NULL
	); 

INSERT INTO customer(CustomerName, City) VALUES ('C1','Arequipa');
ALTER TABLE customer RENAME COLUMN CustomerID TO id;

/* Fx for add ramdom values */
CREATE OR REPLACE FUNCTION addCustomer(j INTEGER, i INTEGER)
RETURNS INTEGER AS $total$
DECLARE
	total INTEGER;
	counter INTEGER := j ; 
BEGIN
	LOOP
		EXIT when counter = i;
		counter := counter+1;
		INSERT INTO customer(CustomerName, City) VALUES ( CONCAT('Customer', counter) , CONCAT('City', counter));
	END LOOP;
	SELECT count(*) into total FROM customer;
	RETURN total;
END;
$total$ LANGUAGE plpgsql;

/*****************************************************************************************************************/
/* Table order */
CREATE TABLE theorder (
	id serial PRIMARY KEY,  /*CustomerID*/
	CustomerID  INTEGER, 
	amoumt INTEGER,
	date timestamp NOT NULL DEFAULT NOW(),
	FOREIGN KEY (CustomerID) REFERENCES customer(id) ON DELETE CASCADE
); 

CREATE OR REPLACE FUNCTION addOrder(i INTEGER)
RETURNS INTEGER AS $total$
DECLARE
	total INTEGER;
	rd INTEGER;
	rd2 INTEGER;
	counter INTEGER := 0 ; 

BEGIN
	LOOP
		EXIT when counter = i;
		counter := counter+1;
		rd := random() * 10 + 5;
		rd2 := random() * 40 + 15;
		INSERT INTO theorder(CustomerID,amoumt) VALUES (rd, rd2);
	END LOOP;
	SELECT count(*) into total FROM theorder;
	RETURN total;
END;
$total$ LANGUAGE plpgsql;

select addOrder(11);

/**Left joim */
SELECT Customer.id, Customer.CustomerName, theorder.id
FROM theorder
LEFT JOIN Customer ON Customer.id = theorder.CustomerID
ORDER BY Customer.id;

/*Cross joim*/
SELECT Customer.id, Customer.CustomerName, theorder.id
FROM Customer
cross JOIN theorder WHERE Customer.id <> theorder.CustomerID;

/* Amount paid by each customer*/
SELECT customer.id, customer.CustomerName, 
	sum(theorder.amoumt) as total
from theorder inner JOIn customer on theorder.customerid = customer.id
GROUP BY customer.id;

/* or: */
SELECT 
	customerid ,
	sum(amoumt) as total
from theorder 
GROUP BY customerid; 

/* count(*) */
select count(*) as total
	from customer;

/* count(col) */
select count(amoumt) as total
from theorder where amoumt > 40;

/* sum() EJER 3 Image(8).jpg */
select  theorder.id as ID, 
	extract(year from date) as amho, 
	EXTRACT(MONTH FROM date) as mes,
	sum(amoumt) as momto_veNdido
from theorder
group BY theorder.id 
ORDER BY ID ASC;

/************************************************/
CREATE TABLE persom (
	id serial PRIMARY KEY,
	pname varchar(50) not null,
	Sexo Boolean,
	salario Integer);


/*Fx addpersom */
CREATE OR REPLACE FUNCTION addPersom(i INTEGER)
RETURNS INTEGER AS $total$
DECLARE 
	total iNteger;
	counter InTEGER := 0;
	rd InTEGER;
	sr BOOLEAN;
BEGIN
	LOOP 
		EXIT when counter = i;
		counter := counter + 1;
		rd := random()*2000+1000;
		sr := random()>0.5;
		INSERT INTO persom (pname, sexo, salario) VALUES ( CONCAT('persom', counter), sr, rd);
	END LOOP;
	SELECT couNt(*) into total from persom;
	RETURN total;
END;
$total$ LANGUAGE plpgsql;

select addPersom(5);

/*UPDATE + CASE*/
UPDATE persom
SET sexo = CASE WHEN 
	sexo = FALSE THEN TRUE 
	ELSE FALSE
END;

/* order by 2md col */
select id, pname from persom order by 2;

/* Duplicate values at pname */
INSERT INTO persom (pname, sexo, salario) VALUES ('persom3', FALSE,1091);
/*nombres repetidos */
 SELECT count(pname) as cou, pname FROM persom GROUP BY(pname) HAVING count(pname) > 1;
/*salarios repetidos */
 SELECT count(salario) as co, salario from persom GROUP BY salario HAVING count(salario) > 1;

 /* TABLA GUSTAR */
 create table gustar(
	id serial PRIMARY KEY,
	id1 integer,
	id2 integer,
	FOREIGn KEY (id1) references persom(id) on delete cascade,
	FOREIGn KEY (id2) references persom(id) on delete cascade);

INSERT INTO gustar(id1, id2) VALUES(1,2);
INSERT INTO gustar(id1, id2) VALUES(2,1);
INSERT INTO gustar(id1, id2) VALUES(2,3);

/* gusto mutuamemte */
create view gustados as 
SELECT HS1.pName as N1, HS2.pName as N2 from (persom as hs1 
	INNER JOIN gustar as L1
	ON L1.id1 = hs1.id 
	INNER JOIN gustar as L2 
	ON L2.id1 = L1.id2 AND L2.id2 = L1.id1 
	INNER JOIN persom as HS2
	ON L1.id2 = hs2.id );
	
SELECT T1.N1, T2.N1 FROM gustados  AS T1
	INNER JOIN gustados AS T2 
	ON T1.N1 = T2.N2  

SELECT l1.id1, l1.id2, persom.pName FROM gustar as l1
INNER JOIN gustar as l2
ON l1.id1 = l2.id2 aNd l2.id1 = l1.id2 
INNER JOIN persom 
oN persom.id = l2.id1

/* Les gusto, pero ellos mo me gustam*/
SELECT l1.id1, l1.id2, p1.pName , p2.pName FROM gustar as l1
INNER JOIN gustar as l2
ON l1.id1 = l2.id2 aNd l2.id1 <> l1.id2
INNER JOIN persom  as p1
oN p1.id = l2.id1
iNNER JOIN persom as p2
oN p2.id = l1.id2