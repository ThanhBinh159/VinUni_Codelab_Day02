"""Render the Xanh SM current-state workflow as a reproducible PNG."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1600
HEIGHT = 900

COLORS = {
    "background": "#F7F8FA",
    "ink": "#17212B",
    "muted": "#52606D",
    "line": "#9AA5B1",
    "card": "#FFFFFF",
    "blue": "#1665D8",
    "blue_soft": "#E8F1FC",
    "green": "#13795B",
    "green_soft": "#E7F6F1",
    "red": "#C83E4D",
    "red_soft": "#FDECEE",
    "amber": "#A65D03",
    "amber_soft": "#FFF3D6",
}


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    windows_fonts = Path("C:/Windows/Fonts")
    names = ["arialbd.ttf", "segoeuib.ttf"] if bold else ["arial.ttf", "segoeui.ttf"]
    for name in names:
        candidate = windows_fonts / name
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default(size=size)


def _wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        left, _, right, _ = draw.textbbox((0, 0), candidate, font=font)
        if right - left <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _centered_wrapped_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: str,
    line_spacing: int = 8,
) -> None:
    x1, y1, x2, y2 = box
    lines = _wrap_text(draw, text, font, x2 - x1)
    heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total_height = sum(heights) + line_spacing * max(0, len(lines) - 1)
    y = y1 + (y2 - y1 - total_height) / 2
    for line, height in zip(lines, heights):
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        draw.text((x1 + (x2 - x1 - width) / 2, y), line, font=font, fill=fill)
        y += height + line_spacing


def _draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    label: str,
    label_font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> None:
    draw.line((start, end), fill=COLORS["line"], width=5)
    end_x, end_y = end
    draw.polygon(
        [(end_x, end_y), (end_x - 14, end_y - 9), (end_x - 14, end_y + 9)],
        fill=COLORS["line"],
    )
    if label:
        bbox = draw.textbbox((0, 0), label, font=label_font)
        width = bbox[2] - bbox[0]
        x = (start[0] + end[0] - width) / 2
        draw.text((x, start[1] - 54), label, font=label_font, fill=COLORS["blue"])


def render(output_path: Path) -> Path:
    """Render the current-state workflow and return the output path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (WIDTH, HEIGHT), COLORS["background"])
    draw = ImageDraw.Draw(image)

    title_font = _font(44, bold=True)
    subtitle_font = _font(22)
    step_font = _font(17, bold=True)
    card_title_font = _font(24, bold=True)
    body_font = _font(18)
    label_font = _font(12, bold=True)
    time_font = _font(17, bold=True)
    footer_font = _font(20, bold=True)
    note_font = _font(16)

    draw.text((70, 54), "Current-State Workflow", font=title_font, fill=COLORS["ink"])
    draw.text(
        (70, 112),
        "Xanh SM - xử lý sự cố pin thấp ngoài hiện trường",
        font=subtitle_font,
        fill=COLORS["muted"],
    )

    card_width = 230
    card_height = 300
    gap = 80
    start_x = 65
    card_y = 300
    cards = [
        {
            "step": "BƯỚC 1",
            "title": "Tài xế báo sự cố",
            "body": "Gửi mức pin, vị trí và tình trạng xe qua app hoặc điện thoại.",
            "time": "1 phút",
            "accent": "blue",
        },
        {
            "step": "BƯỚC 2",
            "title": "Xác minh dữ liệu",
            "body": "Điều phối viên kiểm tra xe, mức pin và tọa độ trên dashboard.",
            "time": "2 phút",
            "accent": "blue",
        },
        {
            "step": "BƯỚC 3",
            "title": "Tra trạm phù hợp",
            "body": "Đối chiếu bản đồ, khoảng cách, cổng sạc và trạng thái trạm.",
            "time": "6 phút",
            "accent": "red",
        },
        {
            "step": "BƯỚC 4",
            "title": "Chọn phương án",
            "body": "Soạn hướng dẫn hoặc gọi đội hỗ trợ sạc pin lưu động.",
            "time": "4 phút",
            "accent": "red",
        },
        {
            "step": "BƯỚC 5",
            "title": "Xác nhận và gửi",
            "body": "Kiểm tra lại, gửi hướng dẫn cho tài xế và ghi nhận ticket.",
            "time": "2 phút",
            "accent": "green",
        },
    ]

    third_x = start_x + 2 * (card_width + gap)
    fourth_x = start_x + 3 * (card_width + gap)
    band_box = (third_x - 20, card_y - 58, fourth_x + card_width + 20, card_y + card_height + 32)
    draw.rounded_rectangle(
        band_box,
        radius=18,
        fill=COLORS["red_soft"],
        outline=COLORS["red"],
        width=3,
    )
    draw.text(
        (third_x, card_y - 44),
        "BOTTLENECK - 10 phút",
        font=label_font,
        fill=COLORS["red"],
    )

    handoff_labels = ["HANDOFF 1", "HANDOFF 2", "ĐỐI CHIẾU", "XÁC NHẬN"]
    for index, card in enumerate(cards):
        x = start_x + index * (card_width + gap)
        accent = COLORS[card["accent"]]
        soft = COLORS[f"{card['accent']}_soft"]
        draw.rounded_rectangle(
            (x, card_y, x + card_width, card_y + card_height),
            radius=12,
            fill=COLORS["card"],
            outline=accent,
            width=3,
        )
        draw.rounded_rectangle(
            (x + 18, card_y + 18, x + 102, card_y + 52),
            radius=8,
            fill=soft,
        )
        draw.text((x + 30, card_y + 26), card["step"], font=step_font, fill=accent)
        _centered_wrapped_text(
            draw,
            (x + 20, card_y + 72, x + card_width - 20, card_y + 142),
            card["title"],
            card_title_font,
            COLORS["ink"],
            line_spacing=4,
        )
        _centered_wrapped_text(
            draw,
            (x + 22, card_y + 150, x + card_width - 22, card_y + 244),
            card["body"],
            body_font,
            COLORS["muted"],
            line_spacing=5,
        )
        pill = (x + 73, card_y + 256, x + card_width - 73, card_y + 290)
        draw.rounded_rectangle(pill, radius=8, fill=soft)
        _centered_wrapped_text(draw, pill, card["time"], time_font, accent, 0)

        if index < len(cards) - 1:
            start = (x + card_width + 6, card_y + card_height // 2)
            end = (x + card_width + gap - 8, card_y + card_height // 2)
            _draw_arrow(draw, start, end, handoff_labels[index], label_font)

    summary_box = (65, 685, 1535, 808)
    draw.rounded_rectangle(
        summary_box,
        radius=12,
        fill=COLORS["amber_soft"],
        outline=COLORS["amber"],
        width=2,
    )
    draw.text(
        (95, 714),
        "Tổng thời gian hiện tại: 15 phút/lượt",
        font=footer_font,
        fill=COLORS["ink"],
    )
    draw.text(
        (95, 756),
        "Điểm nghẽn chính: tra trạm + chọn phương án = 10 phút (bước 3-4)",
        font=body_font,
        fill=COLORS["muted"],
    )
    note = "Số liệu là giả định bài lab; cần xác minh bằng log vận hành Xanh SM."
    note_bbox = draw.textbbox((0, 0), note, font=note_font)
    draw.text(
        (1535 - (note_bbox[2] - note_bbox[0]), 842),
        note,
        font=note_font,
        fill=COLORS["muted"],
    )

    image.save(output_path, format="PNG", optimize=True)
    return output_path


if __name__ == "__main__":
    destination = Path(__file__).parents[1] / "04-workflow-diagram.png"
    print(render(destination))
