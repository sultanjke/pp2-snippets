# Music Player with Keyboard Controller

## Objective

Build a simple music player with keyboard controls and playlist support.

## Requirements

Install dependencies from repo root:

```bash
python -m pip install -r "Practice 09/requirements.txt"
```

Also install VLC Media Player on your system (desktop app), because this player uses the VLC backend. [Download](https://mirror.hyd.albony.in/videolan-ftp/vlc/3.0.23/win64/vlc-3.0.23-win64.exe)
If VLC is not installed, you may see an error about missing `libvlc.dll`.

## Run

```bash
python "Practice 09/music_player/main.py"
```

## Controls

- `P` - Play current track
- `S` - Stop
- `N` - Next track
- `B` - Previous track
- `Q` - Quit

## Folder Files

- `main.py`: creates window, fonts, and game loop.
- `player.py`: playlist + playback logic + keyboard actions + UI text.
- `music/track1.wav`, `music/track2.wav`: sample tracks for testing.
- You can add your own songs to `music/`.

## How This Mini-Game Works (Step by Step)

1. `main.py` initializes `pygame`.
2. It creates `MusicPlayer()` from `player.py`.
3. `MusicPlayer` loads audio files from the `music/` folder.
   - It scans common formats (`.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a`, `.aac`, `.opus`, `.it`, `.xm`, `.mod`).
   - It keeps playable files in the playlist.
4. Key press events call actions:
   - `P` -> play current track
   - `S` -> stop
   - `N` -> next (wrap to first after last)
   - `B` -> previous (wrap to last before first)
   - `Q` -> quit
5. The UI is redrawn each frame with:
   - current track name
   - current status (Playing/Stopped/etc.)
   - progress time (`current / total`)
6. On every frame, `player.update()` checks VLC playback state.
7. When a track ends, player automatically starts the next one.

## Brief Code Explanation

- `load_playlist()`:
  - scans `music/` folder
  - checks many common audio extensions
  - sorts files for stable track order
- `play_current_track()`:
  - creates VLC media from selected file
  - starts playback with `media_player.play()`
- `next_track()` and `previous_track()`:
  - change index using wrap-around math
  - call `play_current_track()`
- `handle_event(event)`:
  - maps keyboard keys to player actions
- `update()`:
  - polls VLC state (`Ended`, `Error`)
  - auto-advances to next track when needed
- `get_progress_text()`:
  - gets current playback position from VLC (`get_time()`)
  - formats both current and total duration as `MM:SS`
  - uses `mutagen` metadata first for better duration support
- `draw_ui(...)`:
  - renders labels/instructions on screen
  - shows backend + format notes

## Key Notes

- Playlist management is done by `current_index`.
- Player does not crash when playlist is empty; it shows a clear message.
- VLC backend gives much better support for `.m4a` and other compressed formats.
- On Windows, install VLC from VideoLAN so `libvlc.dll` is available. [Download](https://mirror.hyd.albony.in/videolan-ftp/vlc/3.0.23/win64/vlc-3.0.23-win64.exe)
