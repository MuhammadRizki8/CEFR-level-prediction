-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Waktu pembuatan: 15 Des 2024 pada 15.47
-- Versi server: 8.0.30
-- Versi PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `english_app`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `cefr_results`
--

CREATE TABLE `cefr_results` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `text` text NOT NULL,
  `predicted_level` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `cefr_results`
--

INSERT INTO `cefr_results` (`id`, `user_id`, `text`, `predicted_level`) VALUES
(1, 2, 'string', 'b2'),
(2, 2, 'Then I awake and look around me', 'a2'),
(3, 3, 'Learning a new language can be challenging, but it is also a rewarding experience. It allows you to connect with people from different cultures, understand their perspectives, and expand your personal and professional opportunities. Consistent practice and exposure to the language are key to making progress.', 'a1'),
(4, 3, 'Traveling to new places can be both exciting and educational. It gives people the chance to explore different cultures, try new foods, and meet interesting people. While it can sometimes be challenging to communicate in a foreign language, many travelers find that these experiences help them improve their skills and gain confidence. Moreover, traveling can teach valuable lessons about planning, problem-solving, and adapting to new situations.', 'a1'),
(5, 3, 'While technological advancements have undoubtedly improved communication and efficiency, they have also raised concerns about privacy and the over-reliance on digital tools. Striking a balance between embracing innovation and preserving human connection remains a significant challenge in today\'s fast-paced world.', 'a2'),
(6, 3, 'Despite the undeniable benefits of globalization, such as economic growth and cultural exchange, it has also exacerbated income inequality and eroded local traditions. This paradox highlights the need for policies that balance global integration with the preservation of regional identity.', 'c1');

-- --------------------------------------------------------

--
-- Struktur dari tabel `choices`
--

CREATE TABLE `choices` (
  `id` int NOT NULL,
  `question_id` int NOT NULL,
  `choice_text` text NOT NULL,
  `is_correct` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `choices`
--

INSERT INTO `choices` (`id`, `question_id`, `choice_text`, `is_correct`) VALUES
(1, 1, 'do not have', 1),
(2, 1, 'did not have', 0),
(3, 1, 'have not had', 0),
(4, 1, 'has not had', 0),
(5, 2, 'providing', 0),
(6, 2, 'provided', 1),
(7, 2, 'have provided', 0),
(8, 2, 'has not had', 0),
(9, 4, 'Anything', 0),
(10, 4, 'Something', 0),
(11, 4, 'Nothing', 1),
(12, 4, 'Everything', 0),
(13, 5, 'Nothing', 1),
(14, 5, 'Something', 0),
(15, 5, 'Everything', 0),
(16, 5, 'None of the above', 0),
(17, 6, 'Anything', 0),
(18, 6, 'Something', 0),
(19, 6, 'Nothing', 1),
(20, 6, 'Everything', 0),
(21, 7, 'Nothing', 1),
(22, 7, 'Something', 0),
(23, 7, 'Everything', 0),
(24, 7, 'None of the above', 0),
(25, 8, 'The match was very exciting, with both teams playing well and creating many chances.', 1),
(26, 8, 'The match was very exciting, with both teams played well and created many chances.', 0),
(27, 8, 'The match was very exciting, with both teams play well and create many chances.', 0),
(28, 8, 'The match was very exciting, with both teams playing good and creating many chances.', 0),
(29, 9, 'The striker has just scored a magnificent goal, giving his team the lead.', 1),
(30, 9, 'The striker has just scored a magnificent goal, gave his team the lead.', 0),
(31, 9, 'The striker just scored a magnificent goal, giving his team the lead.', 0),
(32, 9, 'The striker just scored a magnificent goal, gave his team the lead.', 0);

-- --------------------------------------------------------

--
-- Struktur dari tabel `exam_attempts`
--

CREATE TABLE `exam_attempts` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `batch_id` int NOT NULL,
  `score` int NOT NULL,
  `total_questions` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `exam_attempts`
--

INSERT INTO `exam_attempts` (`id`, `user_id`, `batch_id`, `score`, `total_questions`) VALUES
(1, 2, 1, 1, 2),
(2, 3, 1, 1, 2),
(3, 4, 1, 1, 2);

-- --------------------------------------------------------

--
-- Struktur dari tabel `exam_submission_details`
--

CREATE TABLE `exam_submission_details` (
  `id` int NOT NULL,
  `attempt_id` int NOT NULL,
  `question_id` int NOT NULL,
  `choice_id` int NOT NULL,
  `is_correct` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `exam_submission_details`
--

INSERT INTO `exam_submission_details` (`id`, `attempt_id`, `question_id`, `choice_id`, `is_correct`) VALUES
(1, 3, 1, 2, 0),
(2, 3, 2, 6, 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `interests`
--

CREATE TABLE `interests` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `interests`
--

INSERT INTO `interests` (`id`, `name`) VALUES
(3, 'coding'),
(2, 'reading'),
(1, 'traveling');

-- --------------------------------------------------------

--
-- Struktur dari tabel `questions`
--

CREATE TABLE `questions` (
  `id` int NOT NULL,
  `batch_id` int NOT NULL,
  `question_text` text NOT NULL,
  `correct_answer` varchar(255) NOT NULL,
  `explanation` text,
  `tips` text,
  `cefr_level` varchar(255) DEFAULT NULL,
  `interest` varchar(255) DEFAULT NULL,
  `subject` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `questions`
--

INSERT INTO `questions` (`id`, `batch_id`, `question_text`, `correct_answer`, `explanation`, `tips`, `cefr_level`, `interest`, `subject`) VALUES
(1, 1, 'Even though the team members worked diligently to complete the project, they __________ enough time to finalize all the details.', 'do not have', 'Kalimat pertama menunjukkan bahwa tindakan tim bekerja keras terjadi di masa lampau. Karena itu, bagian setelah klausa tersebut harus tetap konsisten menggunakan tense lampau. Berdasarkan konteks, tim tidak memiliki cukup waktu untuk menyelesaikan detail proyek. Jawaban yang paling tepat adalah did not have, yang menggunakan bentuk negatif dalam past tense. Pilihan seperti do not have dan have not had tidak sesuai karena menggunakan tense present atau present perfect. Pilihan has not had juga salah karena subjeknya jamak, yaitu they. Jawaban akhir adalah did not have karena sesuai dengan tense dan makna kalimat.', 'Ketika menghadapi soal seperti ini, identifikasi tense yang digunakan dalam klausa utama dan pastikan pilihan jawaban sesuai dengan konteks waktu. Selalu periksa kesesuaian subjek dan kata kerja serta hubungan logis antar klausa.', NULL, NULL, NULL),
(2, 1, 'The cultural artifacts discovered by archaeologists in the region __________ important information about the trade routes of ancient civilizations.', 'provided', 'Kalimat kedua membutuhkan kata kerja utama yang melengkapi makna. Subjek utama adalah cultural artifacts yang ditemukan di masa lalu. Oleh karena itu, kata kerja yang paling sesuai adalah provided, yang menunjukkan bahwa artefak tersebut memberikan informasi penting tentang jalur perdagangan kuno. Pilihan lain seperti have provided dan has not had tidak sesuai karena konteks kalimat berbicara tentang fakta masa lalu, bukan sesuatu yang sedang berlangsung atau belum terjadi. Dengan demikian, jawaban yang benar adalah provided.', 'Perhatikan apakah kalimat memiliki kata kerja utama yang lengkap dan sesuai dengan waktu atau tense. Untuk kalimat deskriptif atau fakta, pastikan kata kerja mendukung konteks deskripsi dengan tepat.', NULL, NULL, NULL),
(4, 2, 'Which of the following is NOT a type of anything?', 'c', NULL, 'Anything refers to any object, concept, or idea, while nothing refers to the absence of anything. Therefore, nothing is not a type of anything.', 'anything', 'anything', 'anything'),
(5, 2, 'What is the opposite of anything?', 'a', NULL, 'Nothing is the opposite of anything because it represents the absence of anything, while something, everything, and none of the above imply the existence of something.', 'anything', 'anything', 'anything'),
(6, 3, 'Which of the following is NOT a type of anything?', 'c', 'Anything refers to any object, concept, or idea, while nothing refers to the absence of anything. Therefore, nothing is not a type of anything.', NULL, 'anything', 'anything', 'anything'),
(7, 3, 'What is the opposite of anything?', 'a', 'Nothing is the opposite of anything because it represents the absence of anything, while something, everything, and none of the above imply the existence of something.', NULL, 'anything', 'anything', 'anything'),
(8, 4, 'Which of these sentences is grammatically correct and most appropriate for a news article about a soccer match?', 'a', 'a is correct because it uses the correct verb tense (playing) and subject-verb agreement (both teams playing). b is incorrect because it uses the past tense of play (played) instead of the present continuous tense (playing). c is incorrect because it uses the present tense of play (play) instead of the present continuous tense (playing). d is incorrect because it uses the incorrect adjective (good) instead of the correct adverb (well).', NULL, 'B2', 'soccer', 'written expression'),
(9, 4, 'Which of these sentences is most likely to be found in a commentary about a soccer match?', 'a', 'a is correct because it uses the present perfect tense (has just scored) to describe an action that has just happened. b is incorrect because it uses the past tense of give (gave) instead of the present perfect tense (has given). c is incorrect because it does not use the present perfect tense (has just scored). d is incorrect because it uses the past tense of give (gave) instead of the present perfect tense (has given).', NULL, 'B2', 'soccer', 'written expression');

-- --------------------------------------------------------

--
-- Struktur dari tabel `question_batches`
--

CREATE TABLE `question_batches` (
  `id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `cefr_rank` varchar(50) NOT NULL,
  `description` text,
  `category` enum('Structure grammar','Written expression') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `question_batches`
--

INSERT INTO `question_batches` (`id`, `title`, `cefr_rank`, `description`, `category`) VALUES
(1, 'title 1', 'B2', 'A set of practice questions.', 'Structure grammar'),
(2, 'title 2', 'B1', 'A set of practice questions no 2', 'Written expression'),
(3, 'title 3', 'anything', 'null', ''),
(4, 'title 4', 'B2', 'null', 'Written expression');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fullname` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `fullname`) VALUES
(2, 'string', '$2b$12$i8ytcm/9sYgZe1Xhm.Q/juRm7J/YnA0HSqpO2WplSEIPcDKguZQB6', 'string'),
(3, 'john_doe', '$2b$12$tWFHrl6OcG5CQTsKbOGKYOW1bUIklkDri96vMOzCLmaeUg.6B6TRi', 'jon'),
(4, 'johndoe', '$2b$12$erBRY.wAogR1bPazHilSrOxdJxG/RMmCh0qQUe3ljQtsLct36KT42', 'John Doe');

-- --------------------------------------------------------

--
-- Struktur dari tabel `user_interests`
--

CREATE TABLE `user_interests` (
  `user_id` int NOT NULL,
  `interest_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `user_interests`
--

INSERT INTO `user_interests` (`user_id`, `interest_id`) VALUES
(3, 1),
(4, 1),
(3, 2),
(4, 2),
(3, 3),
(4, 3);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `cefr_results`
--
ALTER TABLE `cefr_results`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `ix_cefr_results_id` (`id`);

--
-- Indeks untuk tabel `choices`
--
ALTER TABLE `choices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `question_id` (`question_id`),
  ADD KEY `ix_choices_id` (`id`);

--
-- Indeks untuk tabel `exam_attempts`
--
ALTER TABLE `exam_attempts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `batch_id` (`batch_id`),
  ADD KEY `ix_exam_attempts_id` (`id`);

--
-- Indeks untuk tabel `exam_submission_details`
--
ALTER TABLE `exam_submission_details`
  ADD PRIMARY KEY (`id`),
  ADD KEY `attempt_id` (`attempt_id`),
  ADD KEY `question_id` (`question_id`),
  ADD KEY `choice_id` (`choice_id`),
  ADD KEY `ix_exam_submission_details_id` (`id`);

--
-- Indeks untuk tabel `interests`
--
ALTER TABLE `interests`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `ix_interests_id` (`id`);

--
-- Indeks untuk tabel `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `batch_id` (`batch_id`),
  ADD KEY `ix_questions_id` (`id`);

--
-- Indeks untuk tabel `question_batches`
--
ALTER TABLE `question_batches`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_question_batches_id` (`id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_username` (`username`),
  ADD KEY `ix_users_id` (`id`);

--
-- Indeks untuk tabel `user_interests`
--
ALTER TABLE `user_interests`
  ADD PRIMARY KEY (`user_id`,`interest_id`),
  ADD KEY `interest_id` (`interest_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `cefr_results`
--
ALTER TABLE `cefr_results`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `choices`
--
ALTER TABLE `choices`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT untuk tabel `exam_attempts`
--
ALTER TABLE `exam_attempts`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `exam_submission_details`
--
ALTER TABLE `exam_submission_details`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `interests`
--
ALTER TABLE `interests`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT untuk tabel `question_batches`
--
ALTER TABLE `question_batches`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `cefr_results`
--
ALTER TABLE `cefr_results`
  ADD CONSTRAINT `cefr_results_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ketidakleluasaan untuk tabel `choices`
--
ALTER TABLE `choices`
  ADD CONSTRAINT `choices_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`);

--
-- Ketidakleluasaan untuk tabel `exam_attempts`
--
ALTER TABLE `exam_attempts`
  ADD CONSTRAINT `exam_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `exam_attempts_ibfk_2` FOREIGN KEY (`batch_id`) REFERENCES `question_batches` (`id`);

--
-- Ketidakleluasaan untuk tabel `exam_submission_details`
--
ALTER TABLE `exam_submission_details`
  ADD CONSTRAINT `exam_submission_details_ibfk_1` FOREIGN KEY (`attempt_id`) REFERENCES `exam_attempts` (`id`),
  ADD CONSTRAINT `exam_submission_details_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`),
  ADD CONSTRAINT `exam_submission_details_ibfk_3` FOREIGN KEY (`choice_id`) REFERENCES `choices` (`id`);

--
-- Ketidakleluasaan untuk tabel `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`batch_id`) REFERENCES `question_batches` (`id`);

--
-- Ketidakleluasaan untuk tabel `user_interests`
--
ALTER TABLE `user_interests`
  ADD CONSTRAINT `user_interests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `user_interests_ibfk_2` FOREIGN KEY (`interest_id`) REFERENCES `interests` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
