from linebot.models import (
    CarouselTemplate,
    CarouselColumn,
    FlexSendMessage,
    BubbleContainer,
    ImageComponent,
    BoxComponent,
    TextComponent,
    IconComponent,
    ButtonComponent,
    URIAction,
)

import json, os
from dotenv import load_dotenv

load_dotenv()
liff_url = f"{os.environ.get('LIFF_URL')}"


# 根據語言回傳引導指示文案
def get_instruction_text(langcode):
    if langcode == "zh":
        return "【使用說明】\n\n• 拍照點單\n點擊按鈕，開起相機，拍攝招牌以獲得點餐連結\n\n• 語言設定\n選擇中文、日文或英文\n\n• 探索\n尋找更多夜市美食 "
    elif langcode == "ja":
        return "【使用説明】\n\n• 画像検索\nボタンをタップしてカメラを起動し、看板を撮影して注文リンクをゲットしよう\n\n• 言語\n中国語、日本語、英語から選択\n\n• 探す\nもっと夜市の美味しいものを見つけよう！"
    else:
        return "Instructions:\n\n• Snap-to-Order\nJust tap the button, open your camera, snap a photo of the sign, and get the ordering link.\n\n• Language\nChoose from Chinese, Japanese, or English.\n\n• Explore\nDiscover more night market delights!"


# create shop list as carousel
def create_carousel_template(langcode):
    global liff_url
    carousel_columns = []
    shops = json.load(open(f'static/shoplist_{langcode}.json', 'r'))
    action_label = {'zh': '點餐', 'ja': '注文', 'en': 'Order Link'}

    for shop in shops:
        carousel_column = CarouselColumn(
            thumbnail_image_url=shop['image'],
            title=shop['title'],
            text=shop['description'],
            actions=[
                URIAction(
                    label=action_label[langcode],
                    uri=f'{liff_url}/{"jp" if langcode=="ja" else langcode}/shop/{shop["id"]}',
                )
            ],
        )
        carousel_columns.append(carousel_column)

    carousel_template = CarouselTemplate(columns=carousel_columns)
    return carousel_template


# create shop detail as flex
def create_flex_message(shop_id, langcode):
    global liff_url
    shop_list = json.load(open(f'static/shoplist_en.json', 'r'))
    shop = shop_list[shop_id]
    recommend_text = {'zh': '推薦餐點', 'ja': 'おすすめ', 'en': 'Best Items'}
    hours_text = {'zh': '営業時間', 'ja': '営業時間', 'en': 'Hours'}
    menu_text = {'zh': '菜單', 'ja': 'メニュー', 'en': 'Menu'}

    # Hero Image
    hero_image = ImageComponent(
        url=shop['image'],
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover",
    )

    # Body Text Components
    title_text = TextComponent(text=shop['title'], weight="bold", size="xl")
    star_count = round(shop['ratings'])

    rating_stars = [
        IconComponent(
            url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
            size="sm",
        )
    ] * star_count

    rating_stars.extend(
        [
            IconComponent(
                url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
                size="sm",
            )
        ]
        * (5 - star_count)
    )

    rating_stars.append(
        TextComponent(
            text=str(shop['ratings']), size="sm", color="#999999", margin="md", flex=0
        )
    )

    rating_stars_box = BoxComponent(
        layout="baseline", margin="md", contents=rating_stars
    )

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(
                text=recommend_text[langcode], color="#aaaaaa", size="sm", flex=2
            ),
            TextComponent(
                text=shop['recommend'], wrap=True, color="#666666", size="sm", flex=5
            ),
        ],
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(
                text=hours_text[langcode], color="#aaaaaa", size="sm", flex=2
            ),
            TextComponent(
                text=shop['hours'], wrap=True, color="#666666", size="sm", flex=5
            ),
        ],
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours,
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(
            label=menu_text[langcode],
            uri=f'{liff_url}/{"jp" if langcode=="ja" else langcode}/shop/{shop["id"]}',
        ),
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(body=body_box, hero=hero_image, footer=footer_box)

    # Return the Flex Message
    return FlexSendMessage(
        alt_text=f'{shop["title"]}{menu_text[langcode]}', contents=bubble
    )
