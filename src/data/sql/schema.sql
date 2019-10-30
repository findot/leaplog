CREATE TABLE vectors (
    id INTEGER NOT NULL AUTO INCREMENT,

    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    z FLOAT NOT NULL,

    PRIMARY KEY(id)
);

CREATE TABLE subjects (
    id          INTEGER NOT NULL AUTO INCREMENT,
    firstname   VARCHAR(255) NOT NULL,
    lastname    VARCHAR(255) NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE actions (
    id          INTEGER NOT NULL AUTO INCREMENT,
    
    subject     INTEGER NOT NULL,
    reference   INTEGER NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (subject)   REFERENCES subject(id)
);

CREATE TABLE frames (
    id          INTEGER NOT NULL AUTO INCREMENT,
    
    action      INTEGER NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (action)    REFERENCES action(id)
);

CREATE TABLE arms (
    id          INTEGER NOT NULL AUTO INCREMENT,

    basis       INTEGER NOT NULL,
    direction   INTEGER NOT NULL,
    elbow_position INTEGER NOT NULL,
    wrist_position INTEGER NOT NULL,

    width       FLOAT NOT NULL,


    FOREIGN KEY (basis) REFERENCES vectors(id),
    FOREIGN KEY (direction) REFERENCES vectors(id),
    FOREIGN KEY (elbow_position) REFERENCES vectors(id),
    FOREIGN KEY (wrist_position) REFERENCES vectors(id)
);

CREATE TABLE hands (
    id              INTEGER NOT NULL AUTO INCREMENT,

    frame           INTEGER NOT NULL AUTO INCREMENT,

    is_left         INTEGER(1) NOT NULL,
    is_right        INTEGER(1) NOT NULL,

    basis           INTEGER NOT NULL,
    direction       INTEGER NOT NULL,

    palm_normal     INTEGER NOT NULL,
    palm_position   INTEGER NOT NULL,
    palm_velocity   INTEGER NOT NULL,

    wrist_position  INTEGER NOT NULL,

    confidence      FLOAT,
    time_visible    FLOAT,

    PRIMARY KEY (id),
    FOREIGN KEY (frame)     REFERENCES frames(id),
    FOREIGN KEY (basis)     REFERENCES basis(id),
    FOREIGN KEY (direction) REFERENCES vectors(id),
    FOREIGN KEY (palm_normal)  REFERENCES vectors(id),
    FOREIGN KEY (palm_position) REFERENCES vectors(id),
    FOREIGN KEY (palm_velocity) REFERENCES vectors(id),
    FOREIGN KEY (wrist_position) REFERENCES vectors(id)
);

CREATE TABLE sphere (
    id              INTEGER NOT NULL AUTO INCREMENT,

    center          INTEGER NOT NULL,
    radius          FLOAT NOT NULL,

    FOREIGN KEY (center) REFERENCES vector(id)
);

CREATE TABLE fingers (
    id          INTEGER NOT NULL AUTO INCREMENT,

    hand        INTEGER NOT NULL,

    type        TINYINT(4),

    PRIMARY KEY (id),
    FOREIGN KEY (hand) REFERENCES hands(id)
);

CREATE TABLE fingers_bones (
    id          INTEGER NOT NULL AUTO INCREMENT,

    finger      INTEGER NOT NULL,
    bone        INTEGER NOT NULL,

    FOREIGN KEY(finger) REFERENCES fingers(id),
    FOREIGN KEY(bone) REFERENCES bones(id)
);

CREATE TABLE bones(
    ID          INTEGER NOT NULL AUTO INCREMENT,

    basis       INTEGER NOT NULL,
    position    INTEGER NOT NULL,
    center      INTEGER NOT NULL,

    type        INTEGER NOT NULL,
    length      FLOAT NOT NULL,
    width       FLOAT NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (basis) REFERENCES vectors(id),
    FOREIGN KEY (position) REFERENCES vectors(id),
    FOREIGN KEY (center) REFERENCES vectors(id)
);
