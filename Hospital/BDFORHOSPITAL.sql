use hospital

CREATE TABLE `pacientes` (
    `id_paciente` int PRIMARY KEY AUTO_INCREMENT,
    `nombre` varchar(100) NOT NULL,
    `apellido` varchar(100) NOT NULL,
    `dni` varchar(20) UNIQUE NOT NULL,
    `fecha_nacimiento` date,
    `sexo` varchar(20),
    `direccion` varchar(255),
    `telefono` varchar(30),
    `email` varchar(100),
    `grupo_sanguineo` varchar(5),
    `contacto_emergencia` varchar(100),
    `telefono_emergencia` varchar(30),
    `obra_social` varchar(100),
    `numero_afiliado` varchar(50),
    `fecha_alta` date,
    `estado` varchar(20)
);

CREATE TABLE `alergias` (
    `id_alergia` int PRIMARY KEY AUTO_INCREMENT,
    `id_paciente` int NOT NULL,
    `nombre` varchar(100) NOT NULL,
    `gravedad` varchar(20)
);

CREATE TABLE `especialidades` (
    `id_especialidad` int PRIMARY KEY AUTO_INCREMENT,
    `nombre` varchar(100) UNIQUE NOT NULL
);

CREATE TABLE `medicos` (
    `id_medico` int PRIMARY KEY AUTO_INCREMENT,
    `nombre` varchar(100) NOT NULL,
    `apellido` varchar(100) NOT NULL,
    `matricula` varchar(50) UNIQUE NOT NULL,
    `telefono` varchar(30),
    `email` varchar(100),
    `consultorio` varchar(50),
    `horario_atencion` varchar(255),
    `fecha_ingreso` date,
    `estado` varchar(20),
    `id_especialidad` int NOT NULL
);

CREATE TABLE `citas` (
    `id_cita` int PRIMARY KEY AUTO_INCREMENT,
    `fecha_hora` datetime NOT NULL,
    `estado` varchar(20),
    `tipo_cita` varchar(50),
    `motivo_consulta` text,
    `observaciones` text,
    `id_paciente` int NOT NULL,
    `id_medico` int NOT NULL
);

CREATE TABLE `historiales` (
    `id_historial` int PRIMARY KEY AUTO_INCREMENT,
    `fecha_creacion` date,
    `id_paciente` int UNIQUE NOT NULL
);

CREATE TABLE `registros_medicos` (
    `id_registro` int PRIMARY KEY AUTO_INCREMENT,
    `fecha_registro` datetime NOT NULL,
    `diagnostico` text,
    `observaciones` text,
    `estudios_realizados` text,
    `id_historial` int NOT NULL,
    `id_medico` int NOT NULL
);

CREATE TABLE `tratamientos` (
    `id_tratamiento` int PRIMARY KEY AUTO_INCREMENT,
    `descripcion` text,
    `fecha_prescripcion` date,
    `fecha_inicio` date,
    `fecha_fin` date,
    `estado` varchar(20),
    `observaciones` text,
    `id_paciente` int NOT NULL,
    `id_medico` int NOT NULL
);

CREATE TABLE `medicamentos` (
    `id_medicamento` int PRIMARY KEY AUTO_INCREMENT,
    `nombre` varchar(100) NOT NULL,
    `descripcion` text
);

CREATE TABLE `tratamiento_medicamento` (
    `id_tratamiento` int NOT NULL,
    `id_medicamento` int NOT NULL,
    `dosis` varchar(50),
    `frecuencia` varchar(50),
    `indicaciones` text, PRIMARY KEY (`id_tratamiento`, `id_medicamento`)
);

ALTER TABLE `alergias` ADD FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`);

ALTER TABLE `medicos` ADD FOREIGN KEY (`id_especialidad`) REFERENCES `especialidades` (`id_especialidad`);

ALTER TABLE `citas` ADD FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`);

ALTER TABLE `citas` ADD FOREIGN KEY (`id_medico`) REFERENCES `medicos` (`id_medico`);

ALTER TABLE `historiales` ADD FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`);

ALTER TABLE `registros_medicos` ADD FOREIGN KEY (`id_historial`) REFERENCES `historiales` (`id_historial`);

ALTER TABLE `registros_medicos` ADD FOREIGN KEY (`id_medico`) REFERENCES `medicos` (`id_medico`);

ALTER TABLE `tratamientos` ADD FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`);

ALTER TABLE `tratamientos` ADD FOREIGN KEY (`id_medico`) REFERENCES `medicos` (`id_medico`);

ALTER TABLE `tratamiento_medicamento` ADD FOREIGN KEY (`id_tratamiento`) REFERENCES `tratamientos` (`id_tratamiento`);

ALTER TABLE `tratamiento_medicamento` ADD FOREIGN KEY (`id_medicamento`) REFERENCES `medicamentos` (`id_medicamento`);


INSERT INTO pacientes (nombre, apellido, dni, fecha_nacimiento, sexo, estado)
VALUES ('Juan', 'Perez', '12345678', '1985-03-20', 'Masculino', 'Activo');

INSERT INTO pacientes (nombre, apellido, dni, fecha_nacimiento, sexo, estado)
VALUES ('Maria', 'Gomez', '87654321', '1992-07-14', 'Femenino', 'Activo');

INSERT INTO especialidades (nombre) VALUES ('Cardiologia');

INSERT INTO medicos (nombre, apellido, matricula, telefono, id_especialidad, estado)
VALUES ('Carlos', 'Lopez', '4521', '351-1234567', 1, 'Activo');