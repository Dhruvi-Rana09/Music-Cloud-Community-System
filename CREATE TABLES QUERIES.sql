USE music_db;

CREATE TABLE if not exists user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE if not exists Artist (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(100) NOT NULL,
    country VARCHAR(50)
);
CREATE TABLE if not exists Song (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    artist_id INT NOT NULL,
    album_id INT,
    audio_link VARCHAR(255),
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id),
    FOREIGN KEY (album_id) REFERENCES Album(album_id)
);
CREATE TABLE if not exists Album (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    album_title VARCHAR(100) NOT NULL,
    release_year YEAR,
    artist_id INT NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
);
CREATE TABLE if not exists Playlist (
    playlist_id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_name VARCHAR(100),
    user_id INT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);
CREATE TABLE PlaylistSongs (
    playlist_id INTEGER,
    song_id INTEGER,
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);
