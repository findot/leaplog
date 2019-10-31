CREATE TABLE vectors (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,

    x           FLOAT NOT NULL,
    y           FLOAT NOT NULL,
    z           FLOAT NOT NULL,
    pitch       FLOAT NOT NULL,
    yaw         FLOAT NOT NULL,
    roll        FLOAT NOT NULL
);

CREATE TABLE basis (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,

    x           INTEGER NOT NULL,
    y           INTEGER NOT NULL,
    Z           INTEGER NOT NULL,
    origin      INTEGER NOT NULL,

    FOREIGN KEY (x) REFERENCES vectors(id),
    FOREIGN KEY (y) REFERENCES vectors(id),
    FOREIGN KEY (z) REFERENCES vectors(id),
    FOREIGN KEY (origin) REFERENCES vectors(id)
);

CREATE TABLE subjects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    
    firstname   VARCHAR(255) NOT NULL,
    lastname    VARCHAR(255) NOT NULL
);

CREATE TABLE actions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    
    subject     INTEGER NOT NULL,
    reference   INTEGER NOT NULL,
    record_time TIMESTAMP NOT NULL,

    FOREIGN KEY (subject)   REFERENCES subject(id)
);

CREATE TABLE frames (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    
    action      INTEGER NOT NULL,
    whence      INT,

    FOREIGN KEY (action)    REFERENCES action(id)
);

CREATE TABLE arms (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,

    basis       INTEGER NOT NULL,
    direction   INTEGER NOT NULL,
    elbow_position INTEGER NOT NULL,
    wrist_position INTEGER NOT NULL,

    width       FLOAT NOT NULL,

    FOREIGN KEY (basis) REFERENCES basis(id),
    FOREIGN KEY (direction) REFERENCES vectors(id),
    FOREIGN KEY (elbow_position) REFERENCES vectors(id),
    FOREIGN KEY (wrist_position) REFERENCES vectors(id)
);

CREATE TABLE hands (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,

    frame           INTEGER NOT NULL,
    arm             INTEGER NOT NULL,

    is_left         TINYINT(1) NOT NULL,
    is_right        TINYINT(1) NOT NULL,

    basis           INTEGER NOT NULL,
    direction       INTEGER NOT NULL,

    palm_normal     INTEGER NOT NULL,
    palm_position   INTEGER NOT NULL,
    palm_velocity   INTEGER NOT NULL,

    sphere_center   INTEGER NOT NULL,
    sphere_radius   FLOAT NOT NULL,

    wrist_position  INTEGER NOT NULL,

    confidence      FLOAT,
    time_visible    FLOAT,

    FOREIGN KEY (frame)     REFERENCES frames(id),
    FOREIGN KEY (basis)     REFERENCES basis(id),
    FOREIGN KEY (direction) REFERENCES vectors(id),
    FOREIGN KEY (palm_normal)  REFERENCES vectors(id),
    FOREIGN KEY (palm_position) REFERENCES vectors(id),
    FOREIGN KEY (palm_velocity) REFERENCES vectors(id),
    FOREIGN KEY (wrist_position) REFERENCES vectors(id),
    FOREIGN KEY (sphere_center) REFERENCES vectors(id)
);

CREATE TABLE fingers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,

    hand        INTEGER NOT NULL,

    type        TINYINT(4),

    FOREIGN KEY (hand) REFERENCES hands(id)
);

CREATE TABLE bones (
    ID          INTEGER PRIMARY KEY AUTOINCREMENT,

    finger      INTEGER NOT NULL,

    basis       INTEGER NOT NULL,
    position    INTEGER NOT NULL,
    direction   INTEGER NOT NULL,
    center      INTEGER NOT NULL,

    type        INTEGER NOT NULL,
    length      FLOAT NOT NULL,
    width       FLOAT NOT NULL,


    FOREIGN KEY (finger) REFERENCES finger(id),
    FOREIGN KEY (basis) REFERENCES basis(id),
    FOREIGN KEY (position) REFERENCES vectors(id),
    FOREIGN KEY (direction) REFERENCES vectors(id),
    FOREIGN KEY (center) REFERENCES vectors(id)
);
