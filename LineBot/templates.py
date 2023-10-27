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
def instruction_text(langcode):
    return open(f'static/instruction_{langcode}.txt', 'r').read()


# create shop list as carousel
def shoplist_carousel_template(langcode):
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
def shop_detail_flex_message(shop_id, langcode):
    global liff_url
    shop_list = json.load(open(f'static/shoplist_{langcode}.json', 'r'))
    shop = shop_list[shop_id]
    recommend_ = {'zh': '推薦餐點', 'ja': 'おすすめ', 'en': 'Best Items'}
    hours_ = {'zh': '営業時間', 'ja': '営業時間', 'en': 'Hours'}
    menu_ = {'zh': '菜單', 'ja': 'メニュー', 'en': 'Menu'}

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
                text=recommend_[langcode], color="#aaaaaa", size="sm", flex=2
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
            TextComponent(text=hours_[langcode], color="#aaaaaa", size="sm", flex=2),
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
            label=menu_[langcode],
            uri=f'{liff_url}/{"jp" if langcode=="ja" else langcode}/shop/{shop["id"]}',
        ),
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(body=body_box, hero=hero_image, footer=footer_box)

    # Return the Flex Message
    return FlexSendMessage(
        alt_text=f'{shop["title"]}{menu_[langcode]}', contents=bubble
    )


def order_detail_flex_message(
    order_id, shop_id, total_price, payment, created_at, items, paid, langcode
):
    order_number_ = {'zh': '訂單編號', 'ja': '注文番号', 'en': 'Order Number'}
    total_ = {'zh': '總金額', 'ja': '総額', 'en': 'Total'}
    payment_ = {'zh': '支付方式', 'ja': '支払い', 'en': 'Payment'}
    paid_ = {'zh': '已支付', 'ja': '支払済', 'en': 'Paid'}
    not_paid_ = {'zh': '未支付', 'ja': '未払い', 'en': 'Not Paid'}
    order_time_ = {'zh': '建立時間', 'ja': '注文時間', 'en': 'Order Time'}

    order_url = f'{liff_url}/{"jp" if langcode == "ja" else langcode}/user/order'

    flex_content = json.load(open('static/order_flex.json', 'r'))
    shoplist = json.load(open(f'static/shoplist_{langcode}.json', 'r'))
    shop = shoplist[shop_id]

    flex_content['header']['contents'][0]['text'] = order_number_[langcode]
    flex_content['header']['contents'][1]['text'] = str(order_id)
    flex_content['header']['contents'][1]['action']['uri'] = order_url
    flex_content['hero']['url'] = shop['image']
    flex_content['body']['contents'][0]['text'] = shop['title']
    flex_content['body']['contents'][1]['contents'] = [
        {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": str(item['qty']),
                    "weight": "bold",
                    "size": "lg",
                    "color": "#ffc648",
                },
                {
                    "type": "text",
                    "text": str(item['name']),
                    "wrap": True,
                    "size": "md",
                    "color": "#666666",
                    "flex": 6,
                    "weight": "bold",
                },
                {
                    "type": "text",
                    "text": str(item['price']),
                    "align": "end",
                    "weight": "bold",
                    "size": "md",
                },
            ],
        }
        for item in items
    ]
    flex_content['body']['contents'][3]['contents'][0]['text'] = total_[langcode]
    flex_content['body']['contents'][3]['contents'][1]['text'] = str(total_price)
    flex_content['body']['contents'][5]['contents'][0]['text'] = payment_[langcode]
    flex_content['body']['contents'][5]['contents'][1]['text'] = str(payment)
    flex_content['body']['contents'][5]['contents'][2]['text'] = (
        paid_[langcode] if paid else not_paid_[langcode]
    )
    flex_content['body']['contents'][5]['contents'][2]['color'] = (
        '#93c878' if paid else '#e06666'
    )
    flex_content['body']['contents'][6]['contents'][0]['text'] = order_time_[langcode]
    flex_content['body']['contents'][6]['contents'][1]['text'] = str(created_at)
    return flex_content
