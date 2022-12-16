CREATE TABLE `bud` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `bud` int NOT NULL,
  `konto` int unsigned NOT NULL,
  `auktionobjekt` int unsigned NOT NULL,
  `tidpunkt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `bud_konto_foreign` (`konto`),
  KEY `bud_auktionobjekt_foreign` (`auktionobjekt`),
  CONSTRAINT `bud_auktionobjekt_foreign` FOREIGN KEY (`auktionobjekt`) REFERENCES `auktionsobjekts` (`id`),
  CONSTRAINT `bud_konto_foreign` FOREIGN KEY (`konto`) REFERENCES `konto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;insert into `bud` (`auktionobjekt`, `bud`, `id`, `konto`, `tidpunkt`) values (1, 1000, 1, 1, '2022-12-11 10:30:05');
insert into `bud` (`auktionobjekt`, `bud`, `id`, `konto`, `tidpunkt`) values (1, 1100, 2, 1, '2022-12-11 10:30:06');
insert into `bud` (`auktionobjekt`, `bud`, `id`, `konto`, `tidpunkt`) values (1, 1200, 3, 1, '2022-12-11 10:30:07');
insert into `bud` (`auktionobjekt`, `bud`, `id`, `konto`, `tidpunkt`) values (1, 1300, 4, 1, '2022-12-11 10:30:08');
insert into `bud` (`auktionobjekt`, `bud`, `id`, `konto`, `tidpunkt`) values (1, 1400, 5, 1, '2022-12-11 10:30:09');
insert into `bud` (`auktionobjekt`, `bud`, `id`, `konto`, `tidpunkt`) values (1, 1500, 6, 1, '2022-12-11 10:30:10');
insert into `bud` (`auktionobjekt`, `bud`, `id`, `konto`, `tidpunkt`) values (5, 1600, 7, 1, '2022-12-12 19:30:05');
