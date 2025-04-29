from djoser.serializers import UserCreateSerializer,UserSerializer

class UserCreateSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name','address','phone_number']

class CurrentUserSerializers(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email','first_name', 'last_name','address','phone_number', 'is_staff']
        read_only_fields = ['is_staff']
    