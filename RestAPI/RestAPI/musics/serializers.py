from rest_framework import serializers
from musics.models import Music


class MusicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Music
        # fields = '__all__'
        fields = ('id', 'song', 'singer', 'last_modify_date', 'created','url')