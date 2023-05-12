CREATE TABLE paises (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

CREATE TABLE departamentos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  pais_id INT NOT NULL,
  FOREIGN KEY (pais_id) REFERENCES paises(id)
);

CREATE TABLE ciudades (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  departamento_id INT NOT NULL,
  FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

CREATE TABLE datos_de_contacto (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sexo VARCHAR(10) NOT NULL,
  fecha_nacimiento DATE NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  direccion VARCHAR(100) NOT NULL,
  casa_apartamento VARCHAR(20) NOT NULL,
  ciudad_id INT NOT NULL,
  departamento_trabajo VARCHAR(50) NOT NULL,
  FOREIGN KEY (ciudad_id) REFERENCES ciudades(id)
);

INSERT INTO paises (nombre) VALUES
('Colombia');

INSERT INTO departamentos (nombre, pais_id) VALUES
('Antioquia', 1),
('Cundinamarca', 1),
('Valle del Cauca', 1),
('Atlántico', 1),
('Santander', 1);

INSERT INTO ciudades (nombre, departamento_id) VALUES
('Medellín', 1),
('Bogotá', 2),
('Cali', 3),
('Barranquilla', 4),
('Bucaramanga', 5);


#create create schema and tables