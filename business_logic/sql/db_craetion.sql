CREATE TABLE role_permission (
  id SERIAL PRIMARY KEY,
  comment_permission int NOT NULL,
  view_permission int NOT NULL
);

CREATE TABLE role (
  id SERIAL PRIMARY KEY,
  level int REFERENCES role_permission(id)
);


CREATE TABLE "user" (
  id uuid PRIMARY KEY,
  username VARCHAR(20) UNIQUE NOT NULL,
  first_name VARCHAR(20),
  last_name VARCHAR(20),
  password VARCHAR(100) NOT NULL, -- Can be null if social login is used
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE address (
  id SERIAL PRIMARY KEY,
  street_1 VARCHAR(80),
  street_2 VARCHAR(80),
  city TEXT,
  state TEXT,
  belongs_to uuid REFERENCES "user"(id),
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE interests (
    interest VARCHAR(20) PRIMARY KEY
);

-- one to many table linking users to their interests
-- a user can have more than one interest
-- but to avoid duplication of interests 
-- we made them a seperate table
-- A user can have any number of interests
-- and an interest can belong to any number
-- of users.
CREATE TABLE users_and_interests (
    id SERIAL PRIMARY KEY,
    "user" uuid REFERENCES "user"(id),
    interest VARCHAR(20) REFERENCES interests(interest)
);

CREATE TABLE federal_law (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

-- table linking interests to what laws affect them
-- multiple laws can affect the same interest
-- many to many since one interest can be affected by
-- multiple laws and one law can be associated with 
-- any number of interests
CREATE TABLE interests_and_laws (
    id SERIAL PRIMARY KEY,
    interest VARCHAR(20) REFERENCES interests(interest),
    law INT REFERENCES federal_law(id)
);

CREATE TABLE discussion (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  thread_permission_req INT NOT NULL DEFAULT 0, -- permission level needed to create a thread
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE thread (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  discussion_id INT NOT NULL REFERENCES discussion(id),
  comment_permission_req INT NOT NULL DEFAULT 0,
  view_permission_req INT NOT NULL DEFAULT 0,
  starter_text TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);


CREATE TABLE forum_comment (
  id SERIAL PRIMARY KEY,
  author uuid REFERENCES "user"(id),
  content TEXT NOT NULL,
  thread_id INT NOT NULL REFERENCES thread(id),
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);
