DROP TABLE IF EXISTS `registrationform`;

CREATE TABLE `registrationform` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `age` int NOT NULL,
  `gender` varchar(45) NOT NULL,
  `interests` varchar(255) DEFAULT NULL,
  `role` varchar(45) NOT NULL DEFAULT 'user',
  `profile_pic` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `game_tips_threads`;

CREATE TABLE `game_tips_threads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `author` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `opened` tinyint DEFAULT '1',
  `author_key` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_author_game_tips_threads` (`author_key`),
  CONSTRAINT `fk_author_game_tips_threads` FOREIGN KEY (`author_key`) REFERENCES `registrationform` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



LOCK TABLES `game_tips_threads` WRITE;
INSERT INTO `game_tips_threads` VALUES (2,'aaaaaaaaaaa','aaaaaaaa','stoianul','2023-11-04 21:10:29',1,1),(3,'aaaaaaaaaaa','aaaaaaaaaaa2','stoianul','2023-11-04 21:16:13',1,1),(4,'aaaaaaaaaaa','aaaaaaaaaaaaaaa555353','stoianul','2023-11-04 21:17:24',1,1),(5,'aaaaaaaaaaaaaaa61361631','1561613613613','stoianul','2023-11-04 21:17:39',1,1),(6,'MyNewGameTipsThread','Es is noch andere gut thread','stoianul','2023-11-04 21:56:01',1,1),(7,'agaegaeggggg','gggggggg','Stoianul','2023-11-05 17:11:23',1,1),(8,'gggggggg','gggggggggggggggggggg','Stoianul','2023-11-05 17:11:27',1,1);
UNLOCK TABLES;


DROP TABLE IF EXISTS `game_tips_threads_comments`;

CREATE TABLE `game_tips_threads_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `thread_id` int NOT NULL,
  `author` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `encryption_key` varchar(255) NOT NULL,
  `author_key` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `game_tips_threads_comments_ibfk_1` (`thread_id`),
  KEY `fk_author_game_tips_threads_comments` (`author_key`),
  CONSTRAINT `fk_author_game_tips_threads_comments` FOREIGN KEY (`author_key`) REFERENCES `registrationform` (`id`),
  CONSTRAINT `game_tips_threads_comments_ibfk_1` FOREIGN KEY (`thread_id`) REFERENCES `game_tips_threads` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




LOCK TABLES `game_tips_threads_comments` WRITE;
INSERT INTO `game_tips_threads_comments` VALUES (1,8,'stoianul','gAAAAABlTBWXeoQ0UOV2UxPZdYTM3Ik23awL60i64lnKoV2hEF2ipw1FvqdrwKQ42lCnxQPkB3_SYiYLQytRnbhHOWfhmWWc-lY_LyEgXmN3U9F1_Dibj6U=','2023-11-08 23:11:19','y8vgnhyaaGfp0DH6uF23ghLGp6A4ViT4T4cAkPb-RSs=',1),(2,8,'stoianul','gAAAAABlTBW4qIigOeFl30ow9RiLAKWj-A_wpd48LsHHegUQ2t_McKcRYzDglXu5qcJiaZ-o8v8PhV5u1J-mm6pBy9SaEdOJkg==','2023-11-08 23:11:52','fCOVB7Sy2uDlxYRYex67xTOy5VUcAgWUWzu8wkSLr2k=',1);
UNLOCK TABLES;



LOCK TABLES `registrationform` WRITE;
INSERT INTO `registrationform` VALUES (1,'stoianul','mailulll@mailul.com','$2b$12$QJMJ/FpbjMr2CmcEH6dbtuz7j3viEsO94beY/MdbWCLLRq5C2jqDO',12,'Adventurer','','admin','/static/profile_pictures/pic.jpg');
UNLOCK TABLES;



DROP TABLE IF EXISTS `threads`;

CREATE TABLE `threads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `author` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `opened` tinyint DEFAULT '1',
  `author_key` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_author_threads` (`author_key`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



LOCK TABLES `threads` WRITE;
INSERT INTO `threads` VALUES (5,'aaaaaaaaaa','aaaaaaaaaa','stoianul','2023-11-04 21:02:34',1,1),(6,'111111111','1111111','stoianul','2023-11-04 21:10:42',1,1),(7,'222222222','22222222222','stoianul','2023-11-04 21:10:51',1,1),(8,'333333333','333333333','stoianul','2023-11-04 21:11:01',1,1),(9,'MyNewGenereal Discussion Threa','Es ist eine gut thread','stoianul','2023-11-04 21:55:35',1,1),(10,'a15151aaaaaaaa','aaaaaaaaaaaaaa53a5a35a3','stoianul','2023-11-05 00:00:51',1,1),(11,'Thread Nr 1','Thread n1\r\n','Stoianul','2023-11-05 17:10:58',1,1),(12,'ThreadNr2 ','Thread NR2\r\n','Stoianul','2023-11-05 17:11:07',1,1),(13,'Thread Nr3','gageagaegaeg','Stoianul','2023-11-05 17:11:18',0,1),(14,'15125','15215215','stoianul','2023-11-07 19:33:34',1,1),(15,'haheahae','heahaehaeh','stoianul','2023-11-07 21:42:34',1,1),(16,'Thread Created As User','I am a basic user:(((','stoianuser','2023-11-08 18:00:07',0,NULL),(17,'aguieag','geagagaeg','stoianuser','2023-11-08 23:04:52',0,NULL),(19,'I created a thread as a user to see how it works','AEahaehaehaeh','stoianuser','2023-11-09 15:26:39',0,NULL),(20,'agaegaegaegaeg','gaegaegagea','stoianul','2023-11-09 15:27:13',1,1);
UNLOCK TABLES;



DROP TABLE IF EXISTS `threads_comments`;

CREATE TABLE `threads_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `thread_id` int NOT NULL,
  `author` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `encryption_key` varchar(255) NOT NULL,
  `author_key` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `threads_comments_ibfk_1` (`thread_id`),
  KEY `fk_author_threads_comments` (`author_key`),
  CONSTRAINT `fk_author_threads_comments` FOREIGN KEY (`author_key`) REFERENCES `registrationform` (`id`),
  CONSTRAINT `threads_comments_ibfk_1` FOREIGN KEY (`thread_id`) REFERENCES `threads` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `threads_comments` WRITE;
INSERT INTO `threads_comments` VALUES (1,16,'stoianuser','gAAAAABlS_ZYMpTLlyxoZlzvikPePLS-w1vi9PvrwFsHd7izbY_gc5107z3Ex4ip32rl_l4Ej8x3ykp-9iIyZVVVJcR4WROdVQ==','2023-11-08 20:58:00','L51Ixb0kOYzJCL2d4WdP9G1uq_-8EOlf_vJ5A3peYcA=',NULL),(2,16,'stoianuser','gAAAAABlS_bAqoJpvWNwvWDDWb06WJ3g1bbbVrFtSgOHynruShmGc4NVqHoBC2S-j_lNNttEm3y277lThptwKyth0ZylHcRgBw==','2023-11-08 20:59:44','jvc371fGzjHJdHfxN_eiPkvpiBwzNU-SnBqtMdt3w68=',NULL),(3,16,'stoianuser','gAAAAABlS_lA1BbKSBgrZ3YBq_8Yc7TB8zk9W38EubRxg7EmbT0ct7sSNh1dVm8RpIB5bQx26LIS5JOPIapTCnihubMrWGjEMA==','2023-11-08 21:10:24','cds-IoNqf8Q-dcq1XPFvuApmXN0DXghRKAbHJcoi6Sc=',NULL),(4,16,'stoianuser','gAAAAABlTAiBTywuECrw8rMcHVhhEnCZ8XpYJOnUlH8gP8XpRJQwBI-Osl0Cyf7fxjsCkutEhw4yEb6n8swn1M-D2x3kDEfHHQ==','2023-11-08 22:15:29','TvbeVrjthkT8_hnFWvYmFLAy3wbXsBWGuQ3DgPFBXJw=',NULL),(5,16,'stoianuser','gAAAAABlTAiI6C5abz6N54hwGBoF88rps2oXWuH4m1flSk2naosotKvINbvQbI1os0jilsSC54l7qS2RhtGajib3YjeeapH_3A==','2023-11-08 22:15:36','9QkOso6X31f5HPGIxyFjE79UgMrt5ufiBjaQ1FyToEA=',NULL),(6,16,'stoianuser','gAAAAABlTAihkFVVsw5A6cDiqSDnHf-IAETyYKlisIEtJa167fUicH4rZKyWt3yHxowA6U5wWv7d7uQixFtHWV_RSs3R1ytH5x73jDVFpCAZ7Tjzsu3C2aGK56zI0X9vqwxX_qDOSD-N53x6C8C9cdOJpn7JxTwFq869bBmX5-Rgx-tSVIOwx8T6m55DWWLDWedPVUMarDLzaLfuO0ta6_OoBdd3K2Peiwk55CHhRS_sL5UNcNtBtRRi2c61dFlNOUOO7Xca6Q_P1FnK0sgqrFeK9xZVw4-jkTxcCdXfmOls7HxahzW6M94vevyieyST9fpcosozpYoeLmhZed7EKIIBDQ9uUF5uQks5Aeka1aiH8LO5gnevjDT8QbDsHIi7MEkGIEIs7xajCqiIDwZuOSaiYy15V5IriEA_TJbVbDxyL5CXsN7aA8dt3IhtpYixCMVynoUHA_urUoOWKQhNgYLL2zV89dZv509T7ZBe5Bh6Y_E5Gr5h98wV25H3eiXSz0Yld9iMFhJjmfEeewjxyHS6wLbouUGJijo5vfhCWAeGqy_oWDLsrIuYtDrvPjTjTVmV46vy7hwwTHcV78yFvSu1IeeKHRi7_Yv0plqSNZR8vs646o7hw7jwL2xQ2foCyBgiQFmCpErKeLfnRPwEDGOPo7-SpAefsMazrc4V8ICYRaW8XNkLOldj1rGsBpFSQyL-UI6oPhPW','2023-11-08 22:16:01','zJ1ZxZvNSF2HHoev9QdUpQMY99tLDxPBmRPsZN9WQ-s=',NULL),(7,13,'stoianuser','gAAAAABlTAr2s__Xvyh7Se9gjoadG5Ik2QqU9xFdY5AN0eVc4MXvlatc9xUf2hKlog5VqkfZi9BXADleEE1oyKcqrnbDoBS0hRkJH7DF9LU1FS3FPVJvUB8=','2023-11-08 22:25:58','eFwK5StPL4D_RYlOFMofLBoPeX0hpKL_RJai6ZEwnVI=',NULL),(8,17,'stoianuser','gAAAAABlTBQyPpw0gCz9LmHytxGPDYL073C_qnT5sh9Q4eUnhT1NvldvMbtIO7B3eDMfTf02irLK_K9Te_UI_4hqE3RUAEwPPg==','2023-11-08 23:05:22','QcLmss57YduGu8n3IwNmvzT9K5RRed9RrFdCIIyrlNw=',NULL),(10,15,'stoianul','gAAAAABlTM8B__s5Y3hjpPhR0NvoHMuBwencpRpBHeRybOptrvSZhilCIdayQIpkoURMDIgRLVtsliX4SdEpJp1Y-yncMQK7sg==','2023-11-09 12:22:25','sCX55K_vmvDuCjy8ox5AM--KE14PXN1vpoW5tpVJb-M=',1),(11,15,'stoianul','gAAAAABlTNH1ckBPhwdVmPA75cUVLBLBbrtC05rCSBssGK07WSRLMQBdarEkz_LXErlyR8UINaqQjGcbJ4TwZaXeTNqNHCKlRA==','2023-11-09 12:35:01','nw2DU3vuY-Woyqo0ozMhA6rtMXHDAs3_RctyWML4-BA=',1),(12,15,'stoianul','gAAAAABlTNIdCGPQUZnjk9TrpCKNkOgZqojiLF8iL6MmlvF5jB2WL37yROkykQokoj4JNW5imQjTvaXLB1Q23e9loEw1LmERqA==','2023-11-09 12:35:41','s3wSTSupmyNqi4Sdk6Cv0Gdr_KwntfDsy4DA4aO5ztk=',1),(13,15,'stoianul','gAAAAABlTNKzUy6lhnnIzR7gf1r0vohexMcMy22rl8Oaq5DLLjrGdIjS85YbFsHG7Q1jz7H6dsYUfUktMzodROmrXs75PsWZCA==','2023-11-09 12:38:11','8ZWagLaCMZwbmJi51ktxPlrbHDc5m_ooO6sikhSf2Lc=',1),(14,15,'stoianul','gAAAAABlTNNBO-2pigw0nwCqJzVkvfYfmPfFVyW5O0N4OiFM2ZqB8GFH3_Zkque6izKxCa9VHy3tuNoAE4TwR821VfTxZ7hdmQ==','2023-11-09 12:40:33','kyTIE0dnujFH7fmsvF-RKUxwMvD8SJPbV_eNx5mL-rE=',1),(15,15,'stoianul','gAAAAABlTNNofgXW_8IqPFu8a-gHHEItXe_AmdzQqasVhTQ0fqPaSGRF5T71KN5mhVgSPTgyNynPZU5Aci1s5K_E4gZvlMfjDg==','2023-11-09 12:41:12','RtMvGFktG3gjKBuev1NIqA-jg6YbDe_sSxfPfoVz9gE=',1),(16,15,'stoianul','gAAAAABlTNNwqd418o4qqtREbz18Y_C2A3FGAhamKpS3lwD5xVsTPTwwXyF912Bp-4MvkiFs_WWRVpJ6OATaQUkbiJ2ac9x4RTiEi-vfuePHCjZ5zcNUwhs=','2023-11-09 12:41:20','F4caEmLYvIaJtyk9YZlg2042Y3OZaoguOzLnhF_zDIM=',1),(17,15,'stoianuser','gAAAAABlTNOgHzTe7vnrEHI9pga7XM7fapzujsu25r-ERMB9E5ND_8WxYE4U4InhTFJ-LQe-1xcjMQ-ZT7R5AWqU2EGAdizLGw==','2023-11-09 12:42:08','MfHjJWz_djepmj6Q-ouzRanHmfL-58xTJMfdmkwCFyE=',NULL),(18,15,'stoianuser','gAAAAABlTNO0hqQIXfH3OSnaxBR6ZPN1d1NAhFFXGoHmbvVF0U6szrMBgy69LIn0Clpy8xqsgcononsZ07h5XRAScx4JdZR1iGmeQ9qnLhsERTvs5HFxetY=','2023-11-09 12:42:28','dUhc_pqNP40v-GjWuXxxEjKXubxA6uxzsb80FI56DDA=',NULL),(19,15,'stoianuser','gAAAAABlTPLiDRFIKOBexdqN6VKS6-ws76pken_Nl1oaDskJlFqWsHGvWPPJJ8DZDpjrGqUcj3YUFyB5FV2ksJx5V-_1__bSkg==','2023-11-09 14:55:30','JTh1HBVXzNvJ8LlazK9TqkR_Dm9V70SuZngZaMkve3o=',NULL),(20,20,'stoianul','gAAAAABlTPpiMSqieymE_PFGl6vCMThPCKSYHi-QX5BzKutnll2wQMF-5qf-4dC0jy9WZEwwTxTWcWJPzgWTZ3ACwtZgpbm9j92rgrbCFaeaCjJ_ivOgTw4=','2023-11-09 15:27:31','bdkjCSrugP-4ZHaYSgpFGBYw-1qxpoIqSQ8u1vpuLEo=',1),(21,20,'stoianuser','gAAAAABlTPpzNS-sHiMkUi6_FuFTRopiM-ajGIT4sUM1g8Br2iSFqsdbkhw1LdEIPwtWTMTDmBXknRFO46XnIuDvIyqQD_rnk_8mBks93ocUy1MPi2ycc94=','2023-11-09 15:27:47','OjPYF82q22oBDWQkNz3ImhhNLo2enfavlcPuYw3GMkQ=',NULL);
UNLOCK TABLES;