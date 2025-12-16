# longform/thumbnail_generator.py
import os
from PIL import Image, ImageDraw, ImageFont

DEFAULT_BG_US = "assets/thumb_bg_us.png"
DEFAULT_BG_KR = "assets/thumb_bg_kr.png"


def _load_font(size: int):
    # 윈도우/리눅스 모두 안전하게: 폰트 파일을 프로젝트에 넣는 게 베스트
    # assets/NotoSansKR-Bold.otf 같은 걸 넣어두면 안정적임
    font_path = "assets/NotoSansKR-Bold.otf"
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size=size)
    # 폰트 없으면 기본 폰트(환경 따라 한글 깨질 수 있음)
    return ImageFont.load_default()


def generate_thumbnail(
    cta_text: str,
    market_type: str,
    output_path: str = "output/thumbnail.png",
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    bg_path = DEFAULT_BG_US if market_type == "US" else DEFAULT_BG_KR
    if not os.path.exists(bg_path):
        # 배경이 없으면 단색으로 생성
        img = Image.new("RGB", (1280, 720), (10, 10, 10))
    else:
        img = Image.open(bg_path).convert("RGB").resize((1280, 720))

    draw = ImageDraw.Draw(img)

    # 텍스트 박스
    font = _load_font(72)
    text = cta_text.strip()

    # 텍스트 크기 측정
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # 가운데 배치
    x = (1280 - tw) // 2
    y = int(720 * 0.58)  # 살짝 아래쪽

    # 반투명 박스(흉내): 검은 박스를 깔고 글자
    pad_x, pad_y = 40, 20
    box = (x - pad_x, y - pad_y, x + tw + pad_x, y + th + pad_y)
    draw.rectangle(box, fill=(0, 0, 0))

    # 외곽선(가독성)
    outline_font = _load_font(72)
    for ox in (-2, -1, 1, 2):
        for oy in (-2, -1, 1, 2):
            draw.text((x + ox, y + oy), text, font=outline_font, fill=(0, 0, 0))

    # 본문 텍스트(흰색)
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    img.save(output_path, quality=95)
    print("🖼 썸네일 생성 완료:", output_path)
    return output_path
