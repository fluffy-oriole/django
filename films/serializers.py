from rest_framework import serializers
from films.models import Actor, Collection, Director, Film, FilmImages, Genre, Review, Profile


class GenreSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
            if 'request' in self.context:
                validated_data['user'] = self.context['request'].user
                
            return super().create(validated_data)

    class Meta:
        model = Genre
        fields = "__all__"


class DirectorSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
            if 'request' in self.context:
                validated_data['user'] = self.context['request'].user
                
            return super().create(validated_data)

    class Meta:
        model = Director
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
            if 'request' in self.context:
                validated_data['user'] = self.context['request'].user
                
            return super().create(validated_data)

    class Meta:
        model = Actor
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
            if 'request' in self.context:
                validated_data['user'] = self.context['request'].user
                
            return super().create(validated_data)

    class Meta:
        model = Review
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
            if 'request' in self.context:
                validated_data['user'] = self.context['request'].user
                
            return super().create(validated_data)

    class Meta:
        model = Collection
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class FilmImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmImages
        fields = "__all__"


class FilmSerializer(serializers.ModelSerializer):
    images = FilmImagesSerializer(many=True, read_only=True)

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
    
    class Meta:
        model = Film
        fields =  "__all__"
