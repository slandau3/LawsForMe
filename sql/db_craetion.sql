DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS federal_laws;
DROP TABLE IF EXISTS state_laws;
DROP TABLE IF EXISTS discussions;
DROP TABLE IF EXISTS thread;
DROP TABLE IF EXISTS forum_post;


CREATE TABLE role (
  id SERIAL PRIMARY KEY
);

CREATE TABLE role_permission (
  id SERIAL PRIMARY KEY
);

CREATE TABLE address (
  id SERIAL PRIMARY KEY,
  street_1 VARCHAR(80),
  street_2 VARCHAR(80),
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  postal_code VARCHAR(5) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE user (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  password VARCHAR(50) NOT NULL, -- Can be null if social login is used
  address INT REFERENCES address(id)
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE federal_laws (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  url TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE forum_comment (
  id SERIAL PRIMARY KEY,
  author INT REFERENCES user(id),
  content TEXT NOT NULL
);

CREATE TABLE thread (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  starter_text TEXT,
  comments INT REFERENCES forum_comment(id)
);

CREATE TABLE discussions (
  id SERIAL PRIMARY KEY,
  threads INT REFERENCES thread(id)
);
