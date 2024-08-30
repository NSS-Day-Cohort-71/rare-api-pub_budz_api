CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
  FOREIGN KEY(`category_id`) REFERENCES `Categories`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Categories ('label') VALUES ('Technology');
INSERT INTO Categories ('label') VALUES ('Entertainment');

INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'content', 'approved') VALUES (1, 5, 'AI - Friend, or Foe?', '2023-04-15', 'AI is super helpful, but it is also super scary.', 1);
INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'content', 'approved') VALUES (1, 5, 'AI - Friend, or Foe?', '2023-04-15', 'AI is super helpful, but it is also super scary.', 1);
INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'content', 'approved') VALUES (2, 1, 'Global Warming: What You Need to Know', '2024-08-15', 'Global warming is a critical issue that affects everyone. Learn what you can do to help.', 1);
INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'content', 'approved') VALUES (3, 5, 'The Rise of Quantum Computing', '2024-08-20', 'Quantum computing is poised to revolutionize technology. Discover its potential impacts.', 1);
INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'content', 'approved') VALUES (3, 5, 'The Rise of Quantum Computing', '2024-08-20', 'Quantum computing is poised to revolutionize technology. Discover its potential impacts.', 1);
INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'content', 'approved') VALUES (2, 3, 'Top 10 Movies to Watch in 2024', '2024-08-25', 'Here''s a list of the top 10 movies to watch in 2024. Don''t miss out on these hits!', 1);

ALTER TABLE Posts ADD COLUMN is_deleted INTEGER DEFAULT 0;

INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Tags ('label') VALUES ('HTML');
INSERT INTO Tags ('label') VALUES ('CSS');

INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');

INSERT INTO Users ( 'first_name', 'last_name', 'email', 'username', 'password') VALUES ( 'john', 'doe', 'j.doe@gmail.com', 'j.doe45', '121x390');
INSERT INTO Users ( 'first_name', 'last_name', 'email', 'username', 'password') VALUES ( 'Jane', 'Doe', 'jane@email.com', 'janeDoe', 'passwordX1');
INSERT INTO Users ( 'first_name', 'last_name', 'email', 'username', 'password') VALUES ( 'Johnny', 'Dough', 'johnsdough@email.com', 'doughboi', 'passwordx2');

INSERT INTO Comments ('post_id', 'author_id', 'content') VALUES (1, 2, 'Great post!');
INSERT INTO Comments ('post_id', 'author_id', 'content') VALUES (3, 1, 'I totally agree with your point.');
INSERT INTO Comments ('post_id', 'author_id', 'content') VALUES (2, 3, 'Can you provide more details?');
DELETE from Posts WHERE id = 12;