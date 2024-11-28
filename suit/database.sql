CREATE DATABASE servindtec;
USE servindtec;

create table TiposEmpresas
(
    Numero   INT(5),
    Nombre   VARCHAR(40),
    Opciones VARCHAR(1000)
);

ALTER TABLE TiposEmpresas
    ADD CONSTRAINT
        PRIMARY KEY (Numero);

ALTER TABLE TiposEmpresas
    MODIFY Numero INT(10) NOT NULL AUTO_INCREMENT;

-- EMPRESAS

CREATE TABLE empresas
(
    id              INT AUTO_INCREMENT PRIMARY KEY,
    nombreComercial VARCHAR(80),
    rfc             VARCHAR(13) UNIQUE NOT NULL,
    codigoPostal    VARCHAR(5),
    calle           VARCHAR(80),
    numero          VARCHAR(10),
    estado          VARCHAR(80),
    pais            VARCHAR(80),
    fechaRegistro   TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipoEmpresa     INT REFERENCES TiposEmpresas (Numero)
);

CREATE TABLE trabajadores
(
    codigo              INT AUTO_INCREMENT PRIMARY KEY,
    nombre              VARCHAR(50),
    apellidopat         VARCHAR(50),
    apellidomat         VARCHAR(50),
    /* ubicacion geografica */
    codigopostal        VARCHAR(5),
    calle               VARCHAR(80),
    numero              VARCHAR(10),
    estado              VARCHAR(80),
    pais                VARCHAR(80),

    nombrepc            VARCHAR(50),
    servicetag          VARCHAR(40),
    modelo              VARCHAR(40),
    fechainiciogarantia TIMESTAMP,
    nombreusuario       VARCHAR(40),
    pin                 VARCHAR(40),
    passwordpc          VARCHAR(40),
    usuariodominio      VARCHAR(40),
    passworddominio     VARCHAR(40),
    departamento        VARCHAR(40),
    numerotelefonico    VARCHAR(20),
    anydesk             VARCHAR(40),
    correo              VARCHAR(50),
    passwordcorreo      VARCHAR(40),
    forwardcorreo       VARCHAR(50),
    listasdistribucion  VARCHAR(50),
    usuariosage         VARCHAR(40),
    passwordsage        VARCHAR(40),
    usuarioproseries    VARCHAR(40),
    passwordproseries   VARCHAR(40),
    pcvirtual           VARCHAR(40),
    usuariovpn          VARCHAR(40),
    passwordvpn         VARCHAR(40),
    usuariocotizador    VARCHAR(40),
    ams360              VARCHAR(40),
    passwordams360      VARCHAR(40),
    horariocomida       VARCHAR(40),

    empresa             INT REFERENCES empresas (id)
);


-- ACTIVITY LOGS

CREATE TABLE `activity_logs`
(
    `log_id`    int(11)      NOT NULL,
    `user_id`   int(11)      NOT NULL,
    `action`    varchar(255) NOT NULL,
    `timestamp` datetime DEFAULT current_timestamp(),
    `details`   text     DEFAULT NULL
);

CREATE TABLE `users`
(
    `id`              int(11)      NOT NULL,
    `username`        varchar(255) NOT NULL,
    `name`            varchar(40)  NOT NULL,
    `paternal`        varchar(40)  NOT NULL,
    `maternal`        varchar(40)  NOT NULL,
    `ciudad`          varchar(40)  NOT NULL,
    `pais`            varchar(40)  NOT NULL,
    `company`         varchar(40)  NOT NULL,
    `role`            varchar(40)  NOT NULL,
    `hashed_password` varchar(255) NOT NULL,
    `email`           varchar(255) NOT NULL,
    `date`            datetime     NOT NULL DEFAULT current_timestamp(),
    `disabled`        tinyint(1)            DEFAULT 0
);

ALTER TABLE `activity_logs`
    ADD PRIMARY KEY (`log_id`),
    ADD KEY `user_id` (`user_id`);

ALTER TABLE `users`
    ADD PRIMARY KEY (`id`),
    ADD UNIQUE KEY `username` (`username`),
    ADD UNIQUE KEY `email` (`email`);

ALTER TABLE `activity_logs`
    MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `users`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 4;

ALTER TABLE `activity_logs`
    ADD CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);



CREATE TABLE usuarios_empresas
(
    usuario INT REFERENCES users(id),
    empresa INT REFERENCES empresas(id),
    PRIMARY KEY (usuario, empresa)
);


/**********************

    DATOS DE PRUEBA    

**********************/

INSERT INTO TiposEmpresas (Numero, Nombre, Opciones)
VALUES (1, "primerTipo", "nombrePC, modelo, correo, passwordCorreo"),
       (2, "segundoTipo", "passwordCorreo, correo, usuarioproseries, passwordproseries"),
       (3, "tercerTipo", "servicetag, anydesk ");

 
INSERT INTO empresas (nombreComercial, rfc, codigoPostal, calle, numero, estado, pais, tipoEmpresa)
VALUES ('EcoTech Solutions', 'ETC123456789', '12345', 'Avenida Innovación', '101', 'Ciudad de México', 'Mexico', 1),
       ('Green Horizons', 'GHZ987654321', '54321', 'Calle Verde', '202', 'Jalisco', 'Mexico', 2),
       ('Solarize Corp', 'SLC456789123', '67890', 'Ruta Solar', '403', 'Nuevo León', 'Mexico', 1),
       ('Recicladora Express', 'REC321654987', '13579', 'Boulevard Reciclaje', '404', 'Yucatán', 'Mexico', 3),
       ('EcoSostenible', 'ECO123789456', '24680', 'Calle Sustentabilidad', '505', 'Puebla', 'Mexico', 1);


INSERT INTO trabajadores
(codigo, nombre, apellidopat, apellidomat, codigopostal, calle, numero, estado, pais, nombrepc, servicetag, modelo,
 fechainiciogarantia, nombreusuario, pin, passwordpc, usuariodominio, passworddominio, departamento, numerotelefonico,
 anydesk, correo, passwordcorreo, forwardcorreo, listasdistribucion, usuariosage, passwordsage, usuarioproseries,
 passwordproseries, pcvirtual, usuariovpn, passwordvpn, usuariocotizador, ams360, passwordams360, horariocomida,
 empresa)
VALUES (NULL, 'Carlos', 'Perez', 'Lopez', '01234', 'Av. Reforma', '123', 'CDMX', 'Mexico', 'PC-Carlos', 'ST12345',
        'Dell Inspiron', NOW(), 'carlos.p', '1234', 'passpc1', 'domuser1', 'dompass1', 'IT', '5551234567', 'AD-1234',
        'carlos.p@example.com', 'emailpass1', 'fwd@example.com', 'list1', 'sageuser1', 'sagepass1', 'proseriesuser1',
        'proseriespass1', 'PC-Virtual', 'vpnuser1', 'vpnpass1', 'cotizador1', 'ams360user1', 'ams360pass1',
        '12:00-13:00', 1),
       (NULL, 'Maria', 'Gonzalez', 'Martinez', '56789', 'Calle 5', '456', 'Jalisco', 'Mexico', 'PC-Maria', 'ST67890',
        'HP Pavilion', NOW(), 'maria.g', '5678', 'passpc2', 'domuser2', 'dompass2', 'HR', '5559876543', 'AD-5678',
        'maria.g@example.com', 'emailpass2', 'fwd2@example.com', 'list2', 'sageuser2', 'sagepass2', 'proseriesuser2',
        'proseriespass2', 'PC-Virtual2', 'vpnuser2', 'vpnpass2', 'cotizador2', 'ams360user2', 'ams360pass2',
        '13:00-14:00', 1),
       (NULL, 'Luis', 'Fernandez', 'Ramirez', '87654', 'Calle 10', '789', 'Nuevo Leon', 'Mexico', 'PC-Luis', 'ST34567',
        'Lenovo ThinkPad', NOW(), 'luis.f', '9101', 'passpc3', 'domuser3', 'dompass3', 'Finance', '5554567890',
        'AD-9101', 'luis.f@example.com', 'emailpass3', 'fwd3@example.com', 'list3', 'sageuser3', 'sagepass3',
        'proseriesuser3', 'proseriespass3', 'PC-Virtual3', 'vpnuser3', 'vpnpass3', 'cotizador3', 'ams360user3',
        'ams360pass3', '14:00-15:00', 1),
       (NULL, 'Ana', 'Martinez', 'Hernandez', '34567', 'Calle 15', '159', 'Puebla', 'Mexico', 'PC-Ana', 'ST89012',
        'Acer Aspire', NOW(), 'ana.m', '1121', 'passpc4', 'domuser4', 'dompass4', 'Marketing', '5553216548', 'AD-1121',
        'ana.m@example.com', 'emailpass4', 'fwd4@example.com', 'list4', 'sageuser4', 'sagepass4', 'proseriesuser4',
        'proseriespass4', 'PC-Virtual4', 'vpnuser4', 'vpnpass4', 'cotizador4', 'ams360user4', 'ams360pass4',
        '15:00-16:00', 1),
       (NULL, 'Jorge', 'Lopez', 'Cruz', '23456', 'Av. Juarez', '258', 'Veracruz', 'Mexico', 'PC-Jorge', 'ST45678',
        'Asus ZenBook', NOW(), 'jorge.l', '3141', 'passpc5', 'domuser5', 'dompass5', 'Sales', '5556547890', 'AD-3141',
        'jorge.l@example.com', 'emailpass5', 'fwd5@example.com', 'list5', 'sageuser5', 'sagepass5', 'proseriesuser5',
        'proseriespass5', 'PC-Virtual5', 'vpnuser5', 'vpnpass5', 'cotizador5', 'ams360user5', 'ams360pass5',
        '16:00-17:00', 2),
       (NULL, 'Laura', 'Rios', 'Sanchez', '45678', 'Calle 20', '321', 'Guanajuato', 'Mexico', 'PC-Laura', 'ST56789',
        'Microsoft Surface', NOW(), 'laura.r', '1617', 'passpc6', 'domuser6', 'dompass6', 'Support', '5559871234',
        'AD-1617', 'laura.r@example.com', 'emailpass6', 'fwd6@example.com', 'list6', 'sageuser6', 'sagepass6',
        'proseriesuser6', 'proseriespass6', 'PC-Virtual6', 'vpnuser6', 'vpnpass6', 'cotizador6', 'ams360user6',
        'ams360pass6', '17:00-18:00', 2),
       (NULL, 'Felipe', 'Salas', 'Gonzalez', '67890', 'Calle 25', '654', 'Tlaxcala', 'Mexico', 'PC-Felipe', 'ST67890',
        'Razer Blade', NOW(), 'felipe.s', '1819', 'passpc7', 'domuser7', 'dompass7', 'Operations', '5551239876',
        'AD-1819', 'felipe.s@example.com', 'emailpass7', 'fwd7@example.com', 'list7', 'sageuser7', 'sagepass7',
        'proseriesuser7', 'proseriespass7', 'PC-Virtual7', 'vpnuser7', 'vpnpass7', 'cotizador7', 'ams360user7',
        'ams360pass7', '18:00-19:00', 2),
       (NULL, 'Sofia', 'Hernandez', 'Vazquez', '78901', 'Calle 30', '987', 'Chiapas', 'Mexico', 'PC-Sofia', 'ST78901',
        'Dell XPS', NOW(), 'sofia.h', '2021', 'passpc8', 'domuser8', 'dompass8', 'Research', '5554563210', 'AD-2021',
        'sofia.h@example.com', 'emailpass8', 'fwd8@example.com', 'list8', 'sageuser8', 'sagepass8', 'proseriesuser8',
        'proseriespass8', 'PC-Virtual8', 'vpnuser8', 'vpnpass8', 'cotizador8', 'ams360user8', 'ams360pass8',
        '19:00-20:00', 3),
       (NULL, 'Gabriel', 'Mendoza', 'Ponce', '89012', 'Calle 35', '654', 'Yucatan', 'Mexico', 'PC-Gabriel', 'ST89012',
        'Sony Vaio', NOW(), 'gabriel.m', '3031', 'passpc9', 'domuser9', 'dompass9', 'Legal', '5553219876', 'AD-3031',
        'gabriel.m@example.com', 'emailpass9', 'fwd9@example.com', 'list9', 'sageuser9', 'sagepass9', 'proseriesuser9',
        'proseriespass9', 'PC-Virtual9', 'vpnuser9', 'vpnpass9', 'cotizador9', 'ams360user9', 'ams360pass9',
        '20:00-21:00', 3),
       (NULL, 'Paola', 'Serrano', 'Cortez', '90123', 'Av. Hidalgo', '852', 'Hidalgo', 'Mexico', 'PC-Paola', 'ST90123',
        'HP Spectre', NOW(), 'paola.s', '4041', 'passpc10', 'domuser10', 'dompass10', 'Admin', '5556543210', 'AD-4041',
        'paola.s@example.com', 'emailpass10', 'fwd10@example.com', 'list10', 'sageuser10', 'sagepass10',
        'proseriesuser10', 'proseriespass10', 'PC-Virtual10', 'vpnuser10', 'vpnpass10', 'cotizador10', 'ams360user10',
        'ams360pass10', '21:00-22:00', 5);


INSERT INTO `users` (`id`, `username`, `name`, `paternal`, `maternal`, `ciudad`, `pais`, `company`, `role`,
                     `hashed_password`, `email`, `date`, `disabled`)
VALUES (1, 'arath', 'ramses', 'porcayo', 'mercado', 'Tijuana', 'Mexico', 'Tile Market', 'admin',
        '$2b$12$BSuaupCtzwgD/Ldcliri9uWu0ZQ37tg4OY2o2eyqnfKKWwu5SUm.m', 'arathmercado2417@gmail.com',
        '2024-10-25 15:25:52', 0),
       (2, 'Enrique', 'Alberto', 'Manrique', 'Martinez', 'Tijuana', 'Mexico', 'EnriquezSoftware', 'support',
        '$2b$12$GL2okGUeO3ADx2QztVeTDuWLXHWCoeTsoxLzcbPPXtVp3bbcBy4ba', 'soporte1@gmail.com', '2024-10-25 15:30:05', 0),
       (3, 'Danna', 'Danna', 'Torres', 'Martinez', 'Acapulco', 'Mexico', 'Fuerza armada de mexico', 'client',
        '$2b$12$0atPP8274MPDvk.4zEYK9O0j/K2SCg6.mZWPz8HEmHW3jpjtaKFeO', 'Danna@gmail.com', '2024-10-25 15:30:05', 0),
    (4, 'Jonathan17', 'Jonathan', 'Barajas', 'Arellano', 'Tijuana', 'Mexico', 'ITSoft', 'admin', '$2b$12$BSuaupCtzwgD/Ldcliri9uWu0ZQ37tg4OY2o2eyqnfKKWwu5SUm.', 'jobaan17@gmail.com', '2024-10-25 15:30:05', 0);
        


INSERT INTO usuarios_empresas VALUES
                                  (4, 1),
                                  (4, 2),
                                  (4, 3),
                                  (1, 1);

