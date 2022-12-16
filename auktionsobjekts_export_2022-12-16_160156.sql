CREATE TABLE `auktionsobjekts` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `titel` varchar(255) NOT NULL,
  `beskrivning` varchar(255) NOT NULL,
  `starttid` datetime NOT NULL,
  `sluttid` datetime NOT NULL,
  `bild` varchar(255) DEFAULT NULL,
  `saljare` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auktionsobjekts_saljare_foreign` (`saljare`),
  CONSTRAINT `auktionsobjekts_saljare_foreign` FOREIGN KEY (`saljare`) REFERENCES `konto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;insert into `auktionsobjekts` (`beskrivning`, `bild`, `id`, `saljare`, `sluttid`, `starttid`, `titel`) values ('sitter på den', NULL, 1, 1, '2022-12-12 08:00:00', '2022-12-11 08:00:00', 'Stol');
insert into `auktionsobjekts` (`beskrivning`, `bild`, `id`, `saljare`, `sluttid`, `starttid`, `titel`) values ('dem är blåa', '', 3, 1, '2022-12-13 15:05:00', '2022-12-12 15:05:00', 'skor');
insert into `auktionsobjekts` (`beskrivning`, `bild`, `id`, `saljare`, `sluttid`, `starttid`, `titel`) values ('den finns', NULL, 5, 2, '2022-12-13 18:00:00', '2022-12-12 08:00:00', 'bord');
