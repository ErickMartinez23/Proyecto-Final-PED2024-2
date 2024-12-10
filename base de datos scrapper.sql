drop database if exists ProyectoPED;
create database ProyectoPED;
use ProyectoPED;
SET SQL_SAFE_UPDATES = 0;
CREATE TABLE Clima_Tijuana (
    Fecha DATE NOT NULL,
    Temperatura_Maxima FLOAT,
    Temperatura_Minima FLOAT,
    Condicion_Climatica VARCHAR(50),
    PRIMARY KEY (Fecha)
);
select * from Clima_Tijuana;