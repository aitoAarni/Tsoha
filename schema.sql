CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, moderator BOOLEAN);
CREATE TABLE areas (id SERIAL PRIMARY KEY, name TEXT UNIQUE, visible BOOLEAN);
CREATE TABLE message_chains (id SERIAL PRIMARY KEY, header TEXT, user_id INTEGER, area_id INTEGER, visible BOOLEAN, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (area_id) REFERENCES areas(id));
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT DEFAULT TRUE, time TIMESTAMP DEFAULT NOW(), user_id IINTEGER, chain_id INTEGER, visible BOOLEAN, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (chain_id) REFERENCES message_chains(id));
