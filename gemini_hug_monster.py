"""
감정 몬스터 껴안기 이미지 생성기
Google Gemini Imagen API 사용
"""

import os
import base64
import webbrowser
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("google-genai 패키지가 없어요! 먼저 설치해 주세요:")
    print("  pip install google-genai python-dotenv")
    exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv(".env.local")
except ImportError:
    print("python-dotenv 패키지가 없어요! 먼저 설치해 주세요:")
    print("  pip install python-dotenv")
    exit(1)

# .env 파일에서 API 키 읽기
API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not API_KEY or API_KEY == "여기에_API_키_입력":
    print(".env 파일에 GEMINI_API_KEY를 입력해 주세요!")
    print("  파일 위치: .env")
    print("  내용 예시: GEMINI_API_KEY=AIzaSy...")
    exit(1)

# ── 이미지 생성 프롬프트 ───────────────────────────────────
PROMPT = """
A heartwarming and adorable illustration of a child gently hugging a cute, chubby emotional monster.
The monster is round and fluffy, mint green color, with tiny horns, big sparkling eyes closed in happiness,
rosy cheeks, and a big smile. The child has purple hair and wears a pastel pink hoodie,
eyes closed with a warm smile, arms wrapped lovingly around the monster.
Soft pink hearts and sparkles float around them.
Background: soft pastel gradient (pink to lavender).
Style: cute chibi anime illustration, warm and cozy, kawaii, children's book style.
High quality, vibrant but soft colors.
"""

def generate_hug_image():
    print("제미나이 API로 포근한 몬스터 이미지 생성 중... 💚")

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=PROMPT,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
            safety_filter_level="BLOCK_LOW_AND_ABOVE",
        ),
    )

    if not response.generated_images:
        print("이미지 생성에 실패했어요.")
        return

    # 이미지 저장
    image_data = response.generated_images[0].image.image_bytes
    output_path = Path("hug_monster_generated.png")
    output_path.write_bytes(image_data)
    print(f"이미지 저장 완료: {output_path.resolve()}")

    # HTML로 결과 보기
    b64 = base64.b64encode(image_data).decode()
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>포근한 감정 몬스터</title>
  <style>
    body {{
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: linear-gradient(160deg, #ffe8f5, #e8d5f5);
      font-family: 'Segoe UI', sans-serif;
    }}
    img {{
      max-width: 512px;
      width: 90vw;
      border-radius: 24px;
      box-shadow: 0 8px 40px rgba(200,100,160,0.3);
    }}
    h1 {{ color: #c2607e; margin-bottom: 16px; font-size: 22px; }}
    p  {{ color: #e896b8; margin-top: 12px; font-size: 14px; }}
  </style>
</head>
<body>
  <h1>포근하게 꼭 껴안아 줄게 🤗</h1>
  <img src="data:image/png;base64,{b64}" alt="감정 몬스터 껴안기"/>
  <p>감정 몬스터도 사랑받으면 기뻐해요 💚 · Gemini Imagen 3으로 생성</p>
</body>
</html>"""

    result_html = Path("hug_monster_result.html")
    result_html.write_text(html, encoding="utf-8")
    webbrowser.open(result_html.resolve().as_uri())
    print("브라우저에서 결과를 열었어요!")


if __name__ == "__main__":
    generate_hug_image()
