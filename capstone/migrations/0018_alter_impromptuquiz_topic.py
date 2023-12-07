# Generated by Django 4.2.7 on 2023-11-26 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0017_rename_usertopic_surveytopicbyuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impromptuquiz',
            name='topic',
            field=models.CharField(choices=[('가구', '개인주택이나 아파트에 홀로 거주'), ('명절/휴일', '가족과 함께 주택이나 아파트 거주'), ('재활용', '영화보기'), ('지형과 활동', '공연보기'), ('자유시간', '공원가기'), ('모임', '해변가기'), ('호텔', '카페/커피 전문점 가기'), ('기술', '쇼핑하기'), ('휴대폰', 'TV시청하기'), ('인터넷', '스포츠관람'), ('산업', '음악 감상하기'), ('교통수단', '악기 연주하기'), ('음식/음식점', '독서'), ('건강', '혼자 노래 부르거나 합창하기'), ('은행', '요리하기'), ('약속', '조깅'), ('날씨', '걷기'), ('의상/패션', '헬스')], max_length=100),
        ),
    ]
