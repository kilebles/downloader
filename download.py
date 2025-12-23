import os
import subprocess
import json
from pathlib import Path

from settings import settings


def download_video(url, output_dir):
    """Скачивает видео с помощью yt-dlp."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Оптимизированные параметры yt-dlp:
    # -f: Простой выбор формата - лучшее видео+аудио до 1080p
    # --remux-video mp4: Ремукс в MP4 через ffmpeg (быстрее и надежнее чем fixup)
    # --no-keep-video: Удалять промежуточные файлы
    # --concurrent-fragments: Параллельная загрузка
    # --format-sort: Приоритет не-фрагментированным форматам
    command = [
        'yt-dlp',
        '-f', 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '--remux-video', 'mp4',
        '--no-keep-video',
        '--format-sort', 'hasaud,res:1080,fps,br,codec:h264:m4a',
        '--cookies', 'cookies.txt',
        '--concurrent-fragments', '8',
        '--retries', '10',
        '--fragment-retries', '10',
        '--throttled-rate', '100K',
        '-o', os.path.join(output_dir, '%(title)s_%(id)s.%(ext)s'),
        url
    ]

    try:
        print(f"\n{'=' * 60}")
        print(f"📥 Скачиваю: {url}")
        print(f"{'=' * 60}\n")

        # Запускаем скачивание с отображением прогресса
        subprocess.run(command, check=True, text=True)

        print(f"\n{'=' * 60}")
        print(f"✅ Успешно скачано: {url}")
        print(f"{'=' * 60}\n")

        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{'=' * 60}")
        print(f"❌ Ошибка при скачивании {url}")
        print(f"{'=' * 60}\n")
        return False


def main():
    # Используем настройки из settings.py
    videos_file = settings.videos_file
    output_dir = settings.output_dir

    if not os.path.exists(videos_file):
        print(f"❌ Файл {videos_file} не найден!")
        return

    with open(videos_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"📋 Найдено {len(urls)} видео для скачивания")
    print(f"📁 Папка назначения: {output_dir}\n")

    success = 0
    failed = 0

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Обработка: {url}")

        if download_video(url, output_dir):
            success += 1
        else:
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"📊 Статистика:")
    print(f"  ✅ Успешно скачано: {success}")
    print(f"  ❌ Ошибок: {failed}")
    print(f"  📋 Всего: {len(urls)}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
