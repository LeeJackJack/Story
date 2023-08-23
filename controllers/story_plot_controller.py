from database.models import StoryPlot, Image, db
from typing import Optional
from sqlalchemy.sql.expression import func
from generate.text_to_image import generate_and_stream_plot_image


def add_story_plot():

    return ""


def get_story_plot():
    return ''


def edit_story_plot():
    return ''


def del_story_plot():
    return ''


def get_random_story_plot(chapter, theme_id):
    story_plots = StoryPlot.query.filter_by(chapter=chapter, theme_id=theme_id).order_by(func.random()).limit(
        4).all()

    results = []
    for plot in story_plots:
        descriptions = plot.gpt_description
        for description in descriptions:
            image_url = description.image.image_url if description.image else None

            generated_image_url = ''
            # 如果image_url为空，调用generate方法
            if not image_url:
                generator = generate_and_stream_plot_image(description.content)
                next(generator)
                generated_image_url = next(generator)

                # 如果Description没有关联的Image，创建一个新的Image实例
                if not description.image:
                    new_image = Image(image_url=generated_image_url, user_id=1, image_description=description.content)  # 这里需要提供其他必要的字段
                    db.session.add(new_image)
                    description.image = new_image
                else:
                    description.image.image_url = generated_image_url

                db.session.commit()

            results.append({
                "id": plot.id,
                "theme_id": plot.theme_id,
                "chapter": plot.chapter,
                "description": {
                    "id": description.id,
                    "content": description.content,
                    "image_id": description.image_id,
                },
                "plot": plot.description,
                "created_at": plot.created_at,
                "updated_at": plot.updated_at,
                "image_url": image_url if image_url else generated_image_url
            })

    return results

