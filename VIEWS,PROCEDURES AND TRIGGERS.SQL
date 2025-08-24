-- VIEW 1
CREATE VIEW  AllSongs AS
SELECT 
    Song.title AS SongTitle,
    Artist.artist_name AS Artist,
    Album.album_title AS Album
FROM Song
LEFT JOIN Artist ON Song.artist_id=Artist.artist_id
LEFT JOIN Album ON Song.album_id=Album.album_id;
SELECT * FROM AllSongs;
-- VIEW 2
CREATE VIEW UserPlaylists AS
SELECT 
    Playlist.playlist_name AS PlaylistName,
    User.username AS CreatedBy,
    Playlist.creation_date AS CreatedOn
FROM Playlist
JOIN User ON Playlist.user_id=User.user_id;
SELECT * FROM UserPlaylists;
-- PROCEDURE 1
DELIMITER //
DROP PROCEDURE IF EXISTS Adduser;
CREATE PROCEDURE AddUser(IN username VARCHAR(50),IN password VARCHAR(100),IN email VARCHAR(100))
BEGIN
    INSERT INTO User(username,password,email) VALUES(username,password,email);
END //
DELIMITER ;
CALL Adduser("RAM",123,"ram@gmail.com");
-- PROCEDURE 2
DELIMITER //
DROP PROCEDURE IF EXISTS Addsong;
CREATE PROCEDURE AddSong
(
    IN song_title VARCHAR(100),
    IN artist_id INT,
    IN audio_link VARCHAR(255)
)
BEGIN
    INSERT INTO Song(title,artist_id,audio_link)
    VALUES(song_title,artist_id,audio_link);
END //
DELIMITER ;
CALL Addsong("KALANK",1,NULL);
-- TRIGGER 1
DELIMITER //

CREATE TRIGGER set_default_playlist_name
BEFORE INSERT ON Playlist
FOR EACH ROW
BEGIN
    IF NEW.playlist_name IS NULL OR NEW.playlist_name = '' THEN
        SET NEW.playlist_name = 'Untitled Playlist';
    END IF;
END //
DELIMITER ;
INSERT INTO Playlist (playlist_id,playlist_name,user_id,creation_date) VALUES (4,NULL,2,'2024-11-17 18:17:47');

-- TRIGGER 2
CREATE TABLE PlaylistLog (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_name VARCHAR(255),
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER log_playlist_creation
AFTER INSERT ON Playlist
FOR EACH ROW
BEGIN
    INSERT INTO PlaylistLog (playlist_name,user_id)
    VALUES(NEW.playlist_name, NEW.user_id);
END //
DELIMITER ;
-- Insert a new playlist into the Playlist table
INSERT INTO Playlist (playlist_name, user_id)
VALUES ('My Favorite Songs', 1);

-- Verify that the log was created in the PlaylistLog table
SELECT * FROM PlaylistLog;
