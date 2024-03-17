from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from Codemonkuser.serializers import UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
from Codemonkuser.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import ParagraphSerializer

from Codemonkuser import models


def get_tokens_for_user(user):
    refresh = RefreshToken. for_user(user)
    return {
        ' refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#i followed django rest framework documentation for user authentication 


class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Sucessful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get ( 'email')
            password = serializer.data.get( 'password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
            else:
                return Response({ 'errors':{'non_field_errors':['Email or Password is not valid']}}, status=status.НТТР_400_BAD_REQUEST)  
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None) :
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#************************************IMPORTANTNOTE*****************************************************#
#most important of the code as i know json can't accept new line in json fromat as funtionality says split the paragraph as next 
#line arises so to implement that function i am running small code for the input of data  to convert into desriable format that i
#can use it adding of data 
# Replace new line characters with "id//"
    
#IMPORTANT
           #IMPORTANT
                        #IMPORTANT
                                            #IMPORTANT
#this part of code is most important for adding of pragraph

# text_with_delimiter = text.replace("\n\n", "id//")
# text_with_delimiter = text_with_delimiter.lower()

# print(text_with_delimiter)
    

# first input data looks like this text = 
#Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
#Magna ac placerat vestibulum lectus. Elit duis tristique sollicitudin nibh sit amet commodo. Senectus et netus et malesuada 
#fames. Fermentum iaculis eu non diam phasellus vestibulum lorem sed. Dictumst quisque sagittis purus sit amet volutpat 
#consequat mauris. Aliquam ut porttitor leo a diam sollicitudin tempor. Consectetur a erat nam atlectus urna duis convallis. 
#Sed viverra ipsum nunc aliquet bibendum enim facilisis gravida neque.
     
#Maecenas volutpat blandit aliquam etiam erat velit scelerisque. Lectus sit amet est placerat in egestas erat imperdiet. 
#Ante in nibh mauris cursus mattis. Tellus rutrum tellus pellentesque eu tincidunt. Euismod quis viverra nibh cras pulvinar 
#mattis. Proin nibh nisl condimentum idvenenatis a. Quam elementum pulvinar etiam non quam. Arcu dictum varius duis at 
#consectetur lorem donec. Aliquet porttitor lacus luctus accumsan tortor. Duis ut diam quam nulla porttitor massa id.
    
#after runing above code becomes like this

#lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
#magna ac placerat vestibulum lectus. elit duis tristique sollicitudin nibh sit amet commodo. senectus et netus et malesuada 
#fames. fermentum iaculis eu non diam phasellus vestibulum lorem sed. dictumst quisque sagittis purus sit amet volutpat 
#consequat mauris. aliquam ut porttitor leo a diam sollicitudin tempor. consectetur a erat nam atlectus urna duis convallis. 
#sed viverra ipsum nunc aliquet bibendum enim facilisis gravida neque. id//maecenas volutpat blandit aliquam etiam erat velit 
#scelerisque. lectus sit amet est placerat in egestas erat imperdiet. ante in nibh mauris cursus mattis. tellus rutrum tellus 
#pellentesque eu tincidunt. euismod quis viverra nibh cras pulvinar mattis. proin nibh nisl condimentum idvenenatis a. 
#quam elementum pulvinar etiam non quam. arcu dictum varius duis at consectetur lorem donec. aliquet porttitor lacus luctus 
#accumsan tortor. duis ut diam quam nulla porttitor massa id.




    

class ParagraphListCreateAPIView(APIView):
    def post(self, request):
        serializer = ParagraphSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data.get('content')
            paragraphs = content.split("id//")
            for i, paragraph in enumerate(paragraphs, start=1):
                paragraph = models.Paragraph.objects.create(Paragraph_no={'paragraph':i},content=paragraph.strip())
            words = content.lower().split()
            for word in words:
                models.WordMap.objects.create(word=word, paragraph=paragraph)

            return Response({'message': 'Paragraph submitted successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParagraphSearchAPIView(APIView):
    def get(self, request):
        search_term = request.GET.get('word', '').lower()  # Get the search term from the request
        matching_paragraphs = models.Paragraph.objects.filter(content__icontains=search_term)[:10]   # Case-insensitive search
        matching_ids = [paragraph.Paragraph_no for paragraph in matching_paragraphs]  # Extract IDs of matching paragraphs
        return JsonResponse({'matching_paragraph': matching_ids})