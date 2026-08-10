"""
Разовый тестовый скрипт — проверяет, как выглядит пост "картинка + длинный
текст" через механизм превью по ссылке (вместо sendPhoto с подписью).

Не часть регулярной автоматизации, только для проверки формата.
"""

import os
import sys

import requests

# Публичная ссылка на тестовую картинку.
IMAGE_URL = "https://raw.githubusercontent.com/boyarinya/tergar-post-images/main/test.jpg"

TEST_CAPTION = (
    '<a href="{image_url}">&#8203;</a>'
    "🏠 Приглашаем на регулярные медитации в группах офлайн!\n\n"
    "<blockquote>"
    "• Понедельник, 17 августа, 19:30-21:00\n"
    "<u>Санкт-Петербург</u>, м. «Горьковская», Кронверкский проспект, 59, «Зелёная Тара»\n"
    "Еженедельные вечерние практики.\n"
    "По предварительной оплате, количество мест ограничено. На месте необходимо показать билет.\n"
    "➡️ На страницу события\n"
    "💬 Телеграм-канал группы\n\n"
    "• Вторник, 18 августа, 19:30-21:00\n"
    "<u>Москва</u>, м. Красные ворота, Мясницкий пр-д, 2/1, «Шанти».\n"
    "Еженедельные вечерние практики."
    "</blockquote>\n\n"
    "<i>Это тестовое сообщение — проверяем формат превью.</i>"
)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_ids_raw = os.environ.get("TELEGRAM_CHAT_IDS")
    if not token or not chat_ids_raw:
        print("Нужны TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_IDS", file=sys.stderr)
        sys.exit(1)

    chat_ids = [c.strip() for c in chat_ids_raw.split(",") if c.strip()]
    caption = TEST_CAPTION.format(image_url=IMAGE_URL)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for chat_id in chat_ids:
        resp = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": caption,
                "parse_mode": "HTML",
            },
            timeout=30,
        )
        if not resp.ok:
            print(f"Telegram ответил: {resp.status_code} {resp.text}", file=sys.stderr)
        resp.raise_for_status()
        print(f"Тестовое сообщение отправлено в чат {chat_id}")


if __name__ == "__main__":
    main()
