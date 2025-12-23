import os
from pathlib import Path
from settings import settings
from download import get_ai_filename

def bulk_rename_videos():
    """
    Проходит по всем видео в output_dir и переименовывает их с помощью AI.
    """
    output_path = Path(settings.output_dir)
    
    if not output_path.exists():
        print(f"❌ Директория не найдена: {output_path}")
        return

    # Расширения файлов, которые считаем видео
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.webm'}
    
    # Получаем список всех файлов в папке
    files = [f for f in output_path.iterdir() if f.is_file() and f.suffix.lower() in video_extensions]
    
    if not files:
        print(f"📂 В папке {output_path} видеофайлы не найдены.")
        return

    print(f"🔍 Найдено файлов для обработки: {len(files)}")
    print(f"📁 Папка: {output_path}\n")

    success_count = 0
    error_count = 0

    for i, file_path in enumerate(files, 1):
        try:
            print(f"[{i}/{len(files)}] Обработка: {file_path.name}")
            
            # Извлекаем "чистое" имя для нейронки (без расширения)
            # Если в имени есть _id (как после yt-dlp), отсекаем его
            original_stem = file_path.stem
            if "_" in original_stem:
                name_parts = original_stem.rsplit("_", 1)
                original_title = name_parts[0]
            else:
                original_title = original_stem

            # Получаем новое имя от AI
            print(f"  🤖 Запрос к AI...")
            new_name = get_ai_filename(original_title)
            
            # Формируем новый путь
            new_path = output_path / f"{new_name}{file_path.suffix}"

            # Проверка на конфликт имен
            if new_path.exists() and new_path != file_path:
                counter = 1
                while new_path.exists():
                    new_path = output_path / f"{new_name}_{counter}{file_path.suffix}"
                    counter += 1

            # Переименование
            if file_path != new_path:
                file_path.rename(new_path)
                print(f"  ✅ Переименовано в: {new_path.name}")
                success_count += 1
            else:
                print(f"  ℹ️ Имя файла не изменилось.")

        except Exception as e:
            print(f"  ❌ Ошибка при обработке {file_path.name}: {e}")
            error_count += 1

    print(f"\n{'=' * 50}")
    print(f"📊 Итоги переименования:")
    print(f"  ✅ Успешно: {success_count}")
    print(f"  ❌ Ошибок: {error_count}")
    print(f"  📋 Всего обработано: {len(files)}")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    bulk_rename_videos()