# Generated by Django 4.2.7 on 2023-12-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("capstone", "0022_alter_responsemodel_current_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="responsemodel",
            name="topic",
            field=models.CharField(
                choices=[
                    ("가구", "가구"),
                    ("명절/휴일", "명절/휴일"),
                    ("재활용", "재활용"),
                    ("지형과 활동", "지형과 활동"),
                    ("자유시간", "자유시간"),
                    ("모임", "모임"),
                    ("호텔", "호텔"),
                    ("기술", "기술"),
                    ("휴대폰", "휴대폰"),
                    ("인터넷", "인터넷"),
                    ("산업", "산업"),
                    ("교통수단", "교통수단"),
                    ("음식/음식점", "음식/음식점"),
                    ("건강", "건강"),
                    ("은행", "은행"),
                    ("약속", "약속"),
                    ("날씨", "날씨"),
                    ("의상/패션", "의상/패션"),
                ],
                default=1,
                max_length=100,
            ),
            preserve_default=False,
        ),
    ]