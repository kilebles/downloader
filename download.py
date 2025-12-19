import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def get_video_id_from_url(url):
    """Извлекает ID видео из URL для именования файла."""
    parsed = urlparse(url)

    if "youtube.com" in parsed.netloc or "youtu.be" in parsed.netloc:
        if "youtube.com" in parsed.netloc:
            query_params = parse_qs(parsed.query)
            video_id = query_params.get("v", [None])[0]
        else:
            video_id = parsed.path.strip("/")
        return f"youtube_{video_id}" if video_id else None

    elif "rutube.ru" in parsed.netloc:
        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "video":
            return f"rutube_{parts[1]}"

    return None


def video_already_exists(output_dir, video_id):
    """Проверяет, существует ли видео в папке."""
    if not video_id:
        return False

    output_path = Path(output_dir)
    existing_files = list(output_path.glob(f"*{video_id}*.mp4"))
    return len(existing_files) > 0


def download_video(url, output_dir):
    """Скачивает видео с помощью yt-dlp."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    video_id = get_video_id_from_url(url)
    if video_id and video_already_exists(output_dir, video_id):
        print(f"⏭️  Видео {video_id} уже существует, пропускаем: {url}")
        return True

    # Оптимизированные параметры yt-dlp:
    # -f: Простой выбор формата - лучшее видео+аудио до 720p
    # --remux-video mp4: Ремукс в MP4 через ffmpeg (быстрее и надежнее чем fixup)
    # --no-keep-video: Удалять промежуточные файлы
    # --concurrent-fragments: Параллельная загрузка
    # --format-sort: Приоритет не-фрагментированным форматам
    command = [
        'yt-dlp',
        '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '--remux-video', 'mp4',
        '--no-keep-video',
        '--format-sort', 'hasaud,res:720,fps,br,codec:h264:m4a',
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
        print(f"{'=' * 60}")
        result = subprocess.run(command, check=True, text=True)
        print(f"{'=' * 60}")
        print(f"✅ Успешно скачано: {url}")
        print(f"{'=' * 60}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{'=' * 60}")
        print(f"❌ Ошибка при скачивании {url}")
        print(f"{'=' * 60}\n")
        return False


def main():
    videos_file = "videos.txt"  # Список видео
    output_dir = r"E:\vk"  # Директория для установки видео

    if not os.path.exists(videos_file):
        print(f"❌ Файл {videos_file} не найден!")
        return

    with open(videos_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"📋 Найдено {len(urls)} видео для скачивания")
    print(f"📁 Папка назначения: {output_dir}\n")

    success = 0
    skipped = 0
    failed = 0

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Обработка: {url}")

        video_id = get_video_id_from_url(url)
        if video_id and video_already_exists(output_dir, video_id):
            skipped += 1
            print(f"⏭️  Пропущено (уже существует)")
            continue

        if download_video(url, output_dir):
            success += 1
        else:
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"📊 Статистика:")
    print(f"  ✅ Успешно скачано: {success}")
    print(f"  ⏭️  Пропущено: {skipped}")
    print(f"  ❌ Ошибок: {failed}")
    print(f"  📋 Всего: {len(urls)}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
