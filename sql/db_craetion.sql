DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS federal_laws;
DROP TABLE IF EXISTS state_laws;
DROP TABLE IF EXISTS discussions;
DROP TABLE IF EXISTS thread;
DROP TABLE IF EXISTS forum_post;

CREATE TABLE user (
  id SERIAL PRIMARY KEY,
  first_name text NOT NULL,
  last_name text NOT NULL,
  password text NULL, -- Can be null if social login is used
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE role (
  id SERIAL PRIMARY KEY
);

CREATE TABLE role_permission (
  id SERIAL PRIMARY KEY
);

CREATE TABLE address (
  id SERIAL PRIMARY KEY,
  street_1 text,
  street_2 text,
  city text NOT NULL,
  state text NOT NULL,
  postal_code text,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE federal_laws (
  id SERIAL PRIMARY KEY,
  title text NOT NULL,
  url text NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE forum_comment (
  id SERIAL PRIMARY KEY,
  author int REFERENCES user(id),
  content text NOT NULL
);

CREATE TABLE thread (
  id SERIAL PRIMARY KEY,
  name text NOT NULL,
  starter_text text,
  comments INT REFERENCES forum_comment(id)
);

CREATE TABLE discussions (
  id SERIAL PRIMARY KEY,
  threads INT REFERENCES thread(id)
);
