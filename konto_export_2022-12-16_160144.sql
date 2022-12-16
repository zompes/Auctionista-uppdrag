CREATE TABLE `konto` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `fornamn` varchar(255) NOT NULL,
  `efternamn` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `lossenord` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;insert into `konto` (`efternamn`, `email`, `fornamn`, `id`, `lossenord`) values ('Svensson', 'sven@gmail.com', 'Erik', 1, 'abc123');
insert into `konto` (`efternamn`, `email`, `fornamn`, `id`, `lossenord`) values ('Larsson', 'larsson@hotmail.com', 'Sven', 2, 'abc124');
insert into `konto` (`efternamn`, `email`, `fornamn`, `id`, `lossenord`) values ('Stor', 'svenerik@gmail.com', 'jonathan', 3, 'epic');
