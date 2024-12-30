import pygame


def smooth_play(file_path):
    pygame.mixer.init(buffer=2048)  # Increase buffer size
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1, fade_ms=400)  # Add slight crossfade

    try:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
    finally:
        pygame.mixer.quit()


# Usage
filename = "brownnoise.mp3"
smooth_play(filename)
