from apps.topic_record.models import TopicRecord, Topic2Student, Topic2Teacher
from django.forms import ModelForm


class TopicRecordForm(ModelForm):
    class Meta:
        model = TopicRecord
        fields = [
            'title',
            'detail',
            'limit_num',
        ]


# class Topic2UserForm(ModelForm):
#     class Meta:
#         model = Topic2User
#         fields = [
#             'topic',
#             'user',
#         ]
