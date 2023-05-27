# AudioFrog
A Music Bot using Lavalink allowing users to create playlists of songs from youtube and spotify, and play them via voice chat in a discord server.

## Setup
- Requires the use of a lavalink server. Lavalink can be downloaded [here](https://github.com/lavalink-devs/Lavalink/releases).
- Create a .env file in the cloned directory. Paste the following tokens if you have them: (only the discord token is required, but spotify functionality will not work without an API key.)
  - DISCORD_TOKEN=your token
  - SPOTIFY_ID=your spotify api id
  - SPOTIFY_SECRET=your spotify secret
- Once the lavalink server is running (java -jar Lavalink.jar) with a supported java version), start the bot using python 3.8 or later.
- Enjoy!
